"""Thin orchestration: validated settings in, one report out, safe diagnostics."""

import argparse
import json
import os
import sys
from contextlib import ExitStack
from dataclasses import fields
from datetime import UTC, datetime
from pathlib import Path

from authlens import __version__
from authlens.config import Settings, read_config
from authlens.engine import detect
from authlens.errors import AuthLensError
from authlens.i18n import Translator, choose_language
from authlens.ingest import ingest
from authlens.models import SEVERITIES
from authlens.reporting import make_report, render
from authlens.safeio import new_output


class Parser(argparse.ArgumentParser):
    def __init__(self, *args, translator=None, **kwargs):
        self.tr = translator or Translator("en")
        kwargs.update(add_help=False, allow_abbrev=False)
        super().__init__(*args, **kwargs)
        self._positionals.title = self.tr("positional")
        self._optionals.title = self.tr("options")

    def error(self, message):
        # argparse interpolates rejected values into errors. Do not expose those values.
        raise AuthLensError("usage")

    def exit(self, status=0, message=None):
        try:
            sys.stdout.flush()
        except OSError:
            _discard_stdout_buffer()
            raise SystemExit(3) from None
        super().exit(status, message)

    def format_help(self):
        return super().format_help().replace("usage: ", self.tr("usage"), 1)

    def format_usage(self):
        return super().format_usage().replace("usage: ", self.tr("usage"), 1)


def _parser(tr):
    parser = Parser(prog="authlens", description=tr("description"), translator=tr)
    parser.add_argument("-h", "--help", action="help", help=tr("help"))
    parser.add_argument(
        "--version", action="version", version=f"AuthLens {__version__}", help=tr("version")
    )
    for name in ("lang", "config"):
        parser.add_argument("--" + name, default=argparse.SUPPRESS, metavar="VALUE", help=tr(name))
    sub = parser.add_subparsers(dest="command", required=True, title=tr("positional"))
    analyze = sub.add_parser(
        "analyze", translator=tr, description=tr("analyze"), help=tr("analyze")
    )
    analyze.add_argument("-h", "--help", action="help", help=tr("help"))
    analyze.add_argument("input", type=Path, help=tr("input"))
    for name in ("lang", "config"):
        analyze.add_argument("--" + name, default=argparse.SUPPRESS, metavar="VALUE", help=tr(name))
    analyze.add_argument(
        "--format",
        choices=("text", "json", "csv", "markdown", "html"),
        default="text",
        help=tr("format"),
    )
    analyze.add_argument(
        "--input-format",
        choices=("jsonl", "ssh"),
        default=argparse.SUPPRESS,
        help=tr("input_format"),
    )
    for name in ("output", "log_file"):
        analyze.add_argument("--" + name.replace("_", "-"), type=Path, help=tr(name))
    for name in (
        "window_seconds",
        "burst_threshold",
        "spray_threshold",
        "success_threshold",
        "max_bytes",
        "max_line_bytes",
        "max_events",
        "year",
    ):
        analyze.add_argument(
            "--" + name.replace("_", "-"),
            type=int,
            default=argparse.SUPPRESS,
            metavar="N",
            help=tr(name),
        )
    analyze.add_argument(
        "--timezone", default=argparse.SUPPRESS, metavar="OFFSET", help=tr("timezone")
    )
    for name in ("exclude_cidr", "exclude_user"):
        analyze.add_argument(
            "--" + name.replace("_", "-"),
            action="append",
            default=argparse.SUPPRESS,
            metavar="VALUE",
            help=tr(name),
        )
    for name in ("keep_duplicates", "strict"):
        analyze.add_argument(
            "--" + name.replace("_", "-"),
            action="store_true",
            default=argparse.SUPPRESS,
            help=tr(name),
        )
    analyze.add_argument("--fail-on", choices=SEVERITIES, help=tr("fail_on"))
    mode = analyze.add_mutually_exclusive_group()
    mode.add_argument("-v", "--verbose", action="store_true", help=tr("verbose"))
    mode.add_argument("-q", "--quiet", action="store_true", help=tr("quiet"))
    analyze.add_argument("--no-color", action="store_true", help=tr("no_color"))
    return parser


def _log(stream, level, event, **values):
    if stream:
        stream.write(
            json.dumps(
                {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "level": level,
                    "event": event,
                    **values,
                },
                ensure_ascii=True,
            )
            + "\n"
        )
        stream.flush()


def _execute(args, settings, tr):
    paths = [args.input] + [
        p
        for p in (
            args.output,
            args.log_file,
            Path(args.config) if hasattr(args, "config") else None,
        )
        if p
    ]
    try:
        resolved = [path.resolve() for path in paths]
    except (OSError, RuntimeError):
        raise AuthLensError("io", 3) from None
    if len(resolved) != len(set(resolved)):
        raise AuthLensError("output", 3)
    with ExitStack() as stack:
        log = (
            stack.enter_context(new_output(args.log_file, keep_on_error=True))
            if args.log_file
            else None
        )
        _log(log, "INFO", "started")
        try:
            with ExitStack() as report_stack:
                # Finalize durable output before logging completion.
                output = (
                    report_stack.enter_context(new_output(args.output))
                    if args.output
                    else sys.stdout
                )
                dataset = ingest(args.input, settings)
                findings = detect(dataset.events, settings)
                report = make_report(dataset, findings, settings, tr.language)
                try:
                    output.write(render(report, args.format, tr))
                    output.flush()
                except OSError:
                    if output is sys.stdout:
                        _discard_stdout_buffer()
                    raise AuthLensError("output", 3) from None
            _log(
                log,
                "INFO",
                "completed",
                events=len(dataset.events),
                findings=len(findings),
                complete=dataset.summary["complete"],
            )
            if not dataset.summary["complete"]:
                print(tr("partial"), file=sys.stderr)
                return 4
            if args.verbose:
                print(
                    tr("completed", events=len(dataset.events), findings=len(findings)),
                    file=sys.stderr,
                )
            if args.fail_on and any(
                SEVERITIES.index(f.severity) >= SEVERITIES.index(args.fail_on) for f in findings
            ):
                return 1
            return 0
        except AuthLensError as error:
            _log(log, "ERROR", "failed", code=error.code)
            raise


def _discard_stdout_buffer():
    """Prevent a second flush of a failed pipe from replacing our exit code at shutdown."""
    descriptor = os.open(os.devnull, os.O_WRONLY)
    try:
        os.dup2(descriptor, sys.stdout.fileno())
    finally:
        os.close(descriptor)


def main(argv=None):
    # Avoid platform code-page failures for all four catalogs, including redirected output.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    tr = Translator(choose_language(None))
    try:
        bootstrap = Parser(prog="authlens", translator=tr)
        bootstrap.add_argument("--lang")
        bootstrap.add_argument("--config", type=Path)
        early, _ = bootstrap.parse_known_args(argv)
        if early.lang:
            tr = Translator(choose_language(early.lang))
        config = read_config(early.config) if early.config else {}
        tr = Translator(choose_language(early.lang or config.get("language")))
        args = _parser(tr).parse_args(argv)
        overrides = {
            field.name: getattr(args, field.name)
            for field in fields(Settings)
            if hasattr(args, field.name)
        }
        if hasattr(args, "lang"):
            overrides["language"] = args.lang
        settings = Settings.from_mapping(config | overrides)
        return _execute(args, settings, tr)
    except AuthLensError as error:
        print(f"{error.code}: {tr('err_' + error.code)}", file=sys.stderr)
        return error.exit_code
    except KeyboardInterrupt:
        print(tr("err_cancelled"), file=sys.stderr)
        return 130
    except BrokenPipeError:
        _discard_stdout_buffer()
        return 3
    except OSError:
        print(tr("err_io"), file=sys.stderr)
        return 3

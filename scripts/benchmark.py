"""Deterministic local performance measurement; emits metrics, not an SLA."""

import json
import platform
import tempfile
import time
import tracemalloc
from datetime import UTC, datetime, timedelta
from pathlib import Path

from authlens.config import Settings
from authlens.engine import detect
from authlens.i18n import Translator
from authlens.ingest import ingest
from authlens.reporting import make_report, render


def benchmark():
    count = 10000
    with tempfile.TemporaryDirectory(prefix="authlens-benchmark-") as directory:
        path = Path(directory) / "synthetic.jsonl"
        base = datetime(2026, 1, 1, tzinfo=UTC)
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            for i in range(count):
                stream.write(
                    json.dumps(
                        dict(
                            timestamp=(base + timedelta(seconds=i)).isoformat(),
                            host="lab",
                            service="ssh",
                            username=f"user-{i % 10}",
                            source_ip="192.0.2.10",
                            outcome="failure",
                        )
                    )
                    + "\n"
                )
        tracemalloc.start()
        start = time.perf_counter()
        settings = Settings()
        dataset = ingest(path, settings)
        findings = detect(dataset.events, settings)
        output = render(make_report(dataset, findings, settings, "en"), "json", Translator("en"))
        seconds = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(
            json.dumps(
                dict(
                    events=count,
                    findings=len(findings),
                    input_bytes=path.stat().st_size,
                    report_bytes=len(output.encode("utf-8")),
                    elapsed_seconds=round(seconds, 4),
                    peak_traced_bytes=peak,
                    python=platform.python_version(),
                    platform=platform.platform(),
                )
            )
        )


if __name__ == "__main__":
    benchmark()

# Configuration reference

Pass one explicit `--config path.toml`. Files are UTF-8 TOML, <=64 KiB. CLI values replace config values, including entire repeatable exclusion lists. No environment secrets or automatic discovery. All keys are top-level and closed; booleans are not integers. Negative offsets use `--timezone=-03:00` to avoid CLI option ambiguity.

| Key / CLI flag | Default | Accepted values |
|---|---|---|
| language / --lang | OS → en | en, es, ru, zh-CN |
| input_format / --input-format | jsonl | jsonl, ssh |
| window_seconds | 300 | 1–86400 |
| burst_threshold | 5 | 2–10000 |
| spray_threshold | 5 | 2–10000 distinct accounts |
| success_threshold | 5 | 2–10000 prior failures |
| max_bytes | 16777216 | 1–268435456 |
| max_line_bytes | 16384 | 1–1048576, including newline |
| max_events | 50000 | 1–500000 valid records before exclusions/deduplication |
| year | unset | 1–9999; required for traditional SSH |
| timezone | unset | fixed ±HH:MM, hours 00–23; required for traditional SSH |
| exclude_cidr | [] | <=256 strict network CIDRs, no host bits |
| exclude_user | [] | <=256 exact usernames |
| keep_duplicates | false | true/false |
| strict | false | true/false |

Underscores become hyphens in CLI flags except language → `--lang`. Output format/path, fail-on threshold, logging and verbosity are CLI-only. Runtime flags unsupported in TOML are errors, not silently ignored. Booleans in TOML are lowercase. No implicit local timezone conversion or daylight-saving inference.

Identity strings are 1–256 characters, have no leading/trailing whitespace and no Unicode control/format/surrogate/private-use/unassigned categories. Exact Unicode equality is intentional; names differing in normalization/case remain separate. IPs normalize through `ipaddress`; IPv4-mapped IPv6 becomes IPv4 (use matching IPv4 exclusions). Scoped IPv6 zone IDs are rejected.

Language precedence: explicit CLI, config, LC_ALL, LC_MESSAGES, LANG, system locale, English fallback. Regional OS locale prefixes are mapped to supported languages. Explicit unsupported language fails. Config is parsed before full help; remove/fix a malformed explicitly supplied config to show help.

Input quality identities:

`lines = accepted + malformed + ignored`

`accepted = analyzed + excluded + duplicates`

Blank lines count as ignored. Malformed counts all rejected lines, but only first 20 diagnostics are retained. `complete` means no malformed records and at least one analyzed event; it is not a claim of complete real-world collection. Hard limits/source mutation produce no final report. Strict mode stops on first malformed record. Neither mode silently produces a clean assessment after truncation.

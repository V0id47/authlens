# Troubleshooting

| Symptom / code | Action |
|---|---|
| `usage` / 2 | Run `authlens analyze --help`; provide flag values, use `--timezone=-03:00`, avoid abbreviations |
| `config` / 2 | Use only documented top-level TOML keys, correct types/ranges; CLI-only output flags do not belong in config |
| `language` / 2 | Use en, es, ru or zh-CN for explicit selection; regional strings apply only to OS detection |
| `io` / 3 | Supply readable regular input/config files; inspect permissions, links and directories |
| `output` / 3 | Choose a new filename in a writable controlled directory; a closed consumer pipe is also an output failure |
| `limit` / 3 | Split the export or deliberately raise bounded settings; no truncated clean report is produced |
| `input_changed` / 3 | Copy the source to an immutable export and rerun |
| Partial / 4 | Inspect counts and first 20 line diagnostics; empty/wholly excluded input is not a clean assessment |
| `record` / 4 in strict mode | Check exact JSONL fields/SSH grammar; ignored lines differ from malformed auth-like lines |
| `encoding` / 4 | Convert the export to UTF-8; a BOM is allowed only at the beginning |
| `legacy_time` | Supply explicit year/fixed offset or use ISO dates |
| `legacy_order` / 4 | Traditional timestamps decreased; convert to explicit ISO years/offsets rather than guessing rollover |
| Missing AL-003 | Verify exact host/service/source/account and timing; another source or a success before failures cannot match |
| Missing later episode | 0.1.0 emits only first threshold crossing per rule/group; use a separately scoped export |

Do not paste real logs or sensitive identities into public issues. Reproduce with synthetic records, version, OS, exact flags with safe paths and expected/actual exit codes.

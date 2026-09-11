# Security engineering notes

Reviewed surfaces: command injection, traversal, SSRF, deserialization, file races, temporary files, credential leakage, permission handling, log/HTML/CSV injection, malformed input, dependencies and resource exhaustion. Runtime neither executes commands nor opens network connections; no network scope/rate/thread flags are fabricated.

Regular input exports are checked at lstat/open/fstat and after reading; platform flags prevent following links/non-regular blocking where available. There is no decompression, arbitrary globbing or recursive directory traversal. The operator chooses local paths intentionally; directory manipulation by a hostile local actor remains outside scope.

The report file is reserved with exclusive creation and removed on processing/write/finalization failure. Existing files remain intact. Lifecycle logs are retained on analysis failure with machine codes; they contain no paths, user names or input records. A storage failure may leave an incomplete log, and an abrupt process kill can leave incomplete artifacts. Do not treat file existence as success.

No raw line is included in reports; SSH suffixes are discarded. That is minimization, not a secret detector: supplied usernames/hosts may themselves be sensitive. HTML escapes all variable content with a restrictive CSP and no scripts or remote assets. Markdown uses escaped text and preformatted evidence. CSV protects standalone cells from common formula prefixes; JSON within cells remains JSON. JSON consumers must perform their own escaping if embedding the result elsewhere.

The CLI replaces unsafe parser error interpolation with translated actionable categories. It never prints the rejected value. The tradeoff is less detailed syntax diagnostics; `--help` and schema docs provide accepted values. The CLI handles broken stdout pipes, including help/version, with defined exit 3.

Build/CI tools are separate from runtime. Pinned action revisions and development dependencies need periodic review; automated vulnerability databases and static tools have coverage limits. [Threat model](../THREAT_MODEL.md) and [verification record](release-readiness.md) are authoritative for residual risks.

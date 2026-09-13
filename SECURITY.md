# Security policy

0.1.x is the current published line. This project does not promise a support SLA or claim an external security audit.

Report vulnerabilities privately through [GitHub private vulnerability reporting](https://github.com/V0id47/authlens/security/advisories/new). Do not open a public issue containing sensitive details, credentials or real logs.

Include version, OS/Python, a minimal synthetic reproduction, expected/actual behavior and impact. Do not attach credentials, personal data or operational log exports. The maintainer should reproduce, coordinate a fix and record the advisory/release; timing depends on availability.

Run the tool without elevated privileges on an immutable export, in an operator-controlled directory. It makes no network requests. Reports contain usernames/IPs even though raw lines are omitted. Treat hashes and event references as sensitive identifiers. Source authenticity, local administrators, hostile destination-directory manipulation and safe downstream distribution are outside this tool's trust boundary.

See [threat model](THREAT_MODEL.md), [hardening details](docs/security-model.md), and [release status](docs/release-readiness.md).

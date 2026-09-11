# Security policy

0.1.x is the current local development line. No published support SLA or external security audit is claimed.

For vulnerabilities, contact the repository owner privately through the hosting platform's private vulnerability reporting once enabled. Before that channel exists, do not open an issue containing sensitive details or real logs; ask the owner to establish a private channel. No email address is invented here.

Include version, OS/Python, a minimal synthetic reproduction, expected/actual behavior and impact. Do not attach credentials, personal data or operational log exports. The maintainer should reproduce, coordinate a fix and record the advisory/release; timing depends on availability.

Run the tool without elevated privileges on an immutable export, in an operator-controlled directory. It makes no network requests. Reports contain usernames/IPs even though raw lines are omitted. Treat hashes and event references as sensitive identifiers. Source authenticity, local administrators, hostile destination-directory manipulation and safe downstream distribution are outside this tool's trust boundary.

See [threat model](THREAT_MODEL.md), [hardening details](docs/security-model.md), and [release status](docs/release-readiness.md).

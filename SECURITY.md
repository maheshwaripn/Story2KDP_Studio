# Security policy

## Supported state
Story2KDP Studio is a **development MVP**, not a hardened internet-facing application. Only private localhost/SSH-tunnel use is recommended. There is no public-production security support guarantee or formal SLA.

## Reporting a vulnerability
Please **do not put security exploit details, credentials or private manuscripts in a public GitHub issue**. Use the repository's GitHub **Security → Report a vulnerability** private reporting feature if enabled. Otherwise contact the maintainer privately through GitHub before sharing details. If private reporting is unavailable, open a non-sensitive issue requesting a private contact channel without including an exploit.

Include the branch/commit, affected component, reproducing conditions using synthetic test content, and the security impact. Never share active API keys.

## Current limitations
- No application login or public HTTPS reverse-proxy setup. Streamlit must bind 127.0.0.1.
- Provider text calls are opt-in but hard per-project spending limits are not implemented.
- Upload size/content checks and project-path rules are evolving. Do not expose this service to untrusted users.
- Optional third-party AI model files and provider responses must be treated as untrusted inputs.
- Recovery snapshots are local to the project, and are not encrypted off-host backups.

See [docs/SECURITY_AND_PRIVACY.md](docs/SECURITY_AND_PRIVACY.md) for the full threat model and mitigation backlog.

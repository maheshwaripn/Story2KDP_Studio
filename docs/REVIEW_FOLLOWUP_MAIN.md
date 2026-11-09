# Third review: follow-up decisions for publishing the MVP to main

Date: 2026-11-09.

## Correct observations
The reviewer found that `main` displayed only a one-line README while the actual code lived on an unmerged branch. Publishing the tested source to the default branch resolves this discoverability problem without claiming production maturity. The repo is public according to GitHub metadata.

The current application is a local-first **proofing** tool. Missing capabilities include KDP full-wrap cover, guaranteed high-quality consistent AI illustrations, hard paid API budgets, stable character cards/reference conditioning, robust schema validation, and a pinned VPS dependency lock. These should be implemented through backlog tasks, not misrepresented as finished.

## Corrections and nuance
The reviewer only inspected layout and metadata, not line-by-line code. `story2kdp/illustration.py` actually does contain an optional `openvino_sd15` implementation, and `story2kdp/providers.py` exists. This does not establish that OpenVINO runs on the user's VPS. Tests and smoke runner were also added to GitHub Actions before this review. Their existence is not a CPU benchmark or print certification.

## Actions delivered with this change
- Align README and CI badge with the default `main` branch; remove obsolete feature-branch clone directions.
- Add PR template.
- Ignore Streamlit secrets, key files, model weights, generated databases and build logs.
- Clarify experimental OpenVINO and proof status in README/status matrix.
- Add reviewer recommendations to the backlog for verified lockfiles, offline mock-provider, image approval and character metadata, KDP profile + metadata, and children/IP privacy safeguards.

## Actions deliberately deferred
- Dependency lock generation: only after verified Linux resolver/install, not via guessed versions.
- Production KDP print export: needs official verified specs, current Kindle/paperback distinction and physical signoff.
- Stable git version tag: defer until VPS smoke and user acceptance; `v0.1.0` in packaging is development version.
- Image API and character-consistent art generation: not ready for CPU-only production.
- Public deployment/authentication: private localhost + SSH tunnel only.

## Developer rule
Documentation is not proof of implementation. The canonical current status remains `docs/STATUS_MATRIX.md`. Every Claude Code PR must link a task ID, show observed test results, and explain any change in product readiness.

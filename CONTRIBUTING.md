# Contributing to Story2KDP Studio

We welcome focused fixes and carefully tested implementations. This is an early-stage, local-first picture-book studio. Read [CLAUDE.md](CLAUDE.md), [requirements](docs/PRODUCT_REQUIREMENTS.md), [backlog](docs/IMPLEMENTATION_BACKLOG.md), [acceptance tests](docs/ACCEPTANCE_TESTS.md), and [status matrix](docs/STATUS_MATRIX.md) before opening a PR.

## Priorities and workflow
1. Pick one backlog task ID (e.g. P0-01), or open an issue for a verified bug. Link to that issue.
2. Branch from the current development integration branch. Never commit customer manuscripts, API keys, model files or generated private books.
3. Keep changes small and update docs whenever the status or contract changes.
4. Run `python -m pip install -e '.[dev]'`, `python -m pytest -q` and `python -m compileall story2kdp app.py`.
5. Test edge cases: corrupted inputs, resource exhaustion, path traversal, provider errors and high-cost operations.
6. In the PR describe implementation, tests actually run, OS/Python/CPU constraints, manual verification needed, security/rights impacts, and known limitations.
7. Do not merge without maintainer approval. GitHub CI passing is necessary but not equivalent to safe production publishing.

## AI-assisted contributions
When using Claude Code or another coding assistant, start in the repository root and follow CLAUDE.md. AI outputs and library suggestions must be reviewed. Do not permit unattended network installation, model downloads or paid API calls. Never claim unrun tests passed.

## Product guardrails
The current cover file is a design proof, not a KDP print cover. Neural CPU inference is experimental on 8 GB. Do not claim an image's 300-DPI metadata makes it sharp at print size. Distinguish deterministic findings, creative reviews and human decisions.

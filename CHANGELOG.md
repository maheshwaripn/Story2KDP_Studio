# Changelog

Entries distinguish actual implementation from future plans.

## Unreleased — 2026-11-09 development branch

### Added
- Claude Code instructions, product requirements, ordered implementation backlog, release gates and VPS runbook.
- GitHub issue templates and tracked implementation workstreams.
- Project save revision snapshots under `projects/<name>/revisions/` (previous `project.json` is saved when overwriting). **Not a full autosave/restore UX.**
- Regression tests for snapshots, symlinked project targets, duplicate scene/page identifiers and unfinished placeholders.
- Contributor and security policies and this changelog.

### Changed
- Expanded README describing implemented capabilities, Ubuntu deployment, privacy and planned KDP features.
- Artwork uploads in Streamlit now use generated filenames and decode/re-encode PNG/JPEG with size/dimension limits.
- Mechanical review flags duplicate scene IDs, duplicate page assignments and unfinished placeholder text; checks image effective DPI against its current layout box, approximately.

### Not yet implemented
- Automatic persistent character similarity checks, real cloud image API support, budget enforcement, robust Unicode PDF, final KDP full-wrap cover, app authentication, full recovery UI and completed VPS benchmark.

## v0.1 MVP — initial development branch
- Python/Streamlit manuscript and editable storyboard, procedural illustration proof, optional experimental OpenVINO backend and text AI adapters, draft PDF/proof cover, basic preflight, tests and documentation.

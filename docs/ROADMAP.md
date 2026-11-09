# Development status, priorities and field-test feedback

## Working in v0.1

- TXT, Markdown and DOCX manuscript parsing; editable scene list, prompts and JSON character notes.
- Basic local per-scene procedural concept generation without tokens.
- Experimental optional OpenVINO-based CPU text-to-image path (not tested on the user's machine).
- Manual upload of approved PNG/JPEG illustrations.
- Deterministic review for missing art, approval, resolution, unsafe paths, pages and dense copy.
- OpenAI/Claude/Gemini selectable **text** task calls with explicit permission and local cache.
- 8.5 x 8.5 draft interior PDF, watermarked proof cover, limited preflight JSON.
- Ubuntu bootstrap, Streamlit UI, CLI and automated tests.

## Highest priority after VPS feedback

**P1:** Fix actual VPS installation, dependency compatibility, memory usage and book render failures. Improve manuscript pagination/typography and support Unicode fonts.

**P2:** Implement real character Bible workflows, page approvals, actual art reference conditioning and selective scene re-generation.

**P3:** Add properly isolated CPU inference workers and verified OpenVINO presets by CPU generation, plus benchmark report.

**P4:** Add separate OpenAI/Gemini/other image-generation providers with real model support and calibrated price estimation, task-granular spending reservations, usage accounting and hard budget guardrails.

**P5:** Implement a full-wrap KDP production cover, correct interior bleed/gutter, embedded fonts, high-resolution/effective-DPI checks and KDP compliance regression suite.

**P6:** Provide full review reports with severity, fixing workflow, story/age/visual consistency checkpoints, versioning, backups, and authenticated remote user access.

## Suggested feedback issue template

```text
Environment: Ubuntu version / Python version / lscpu model / RAM / swap
Branch and commit:
Command or UI action:
Expected result:
Actual result and traceback (remove any keys/secrets):
Elapsed seconds and peak RAM:
Art quality observations (image size, consistency, color, positive tone):
PDF issues and KDP Previewer messages:
Proposed improvements:
```

Report separate issues for install defects, model failures, visual quality, and publishing issues so fixes can be tested independently.

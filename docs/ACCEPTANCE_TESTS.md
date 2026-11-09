# Acceptance and verification strategy
**Rule:** Do not mark a milestone done without reproducing its acceptance criteria. No test suite replaces final KDP acceptance or human visual review.

## Test layers
T0 Static: formatting/lint, typing for core data and providers, secret checks, dependency/license audit where feasible.
T1 Unit: parser, schema migration, state changes, scene/asset IDs, budgeting, prompt cache, provider capabilities, geometry and file paths; no network.
T2 Integration: local sample project, procedural preview, editing, PDF interior/proof output and preflight JSON using temporary folders.
T3 Provider contract: mock API responses, failures, rate limits, timeout, malformed output, budget exhaustion; all calls intercepted.
T4 CPU-model field benchmark: optional, explicit, on VPS only. Report CPU, OpenVINO version, model provenance/license/checksum, RAM peak, swap, seconds and output image size. Never run during default CI.
T5 Publishing: automated checks for trim/bleed/gutter, pagination, fonts, overflow, actual effective DPI, wrap cover geometry and barcode safety; report unknowns as not verified.
T6 Human signoff: book-specific characters, emotional tone and cohesive look, copyediting, rights/disclosures, physical proof and KDP Previewer.

## Mandatory cases
- Missing/empty manuscript and disallowed extensions; DOCX with headings; long text; non-Latin text; page directives.
- More scenes than pages; image-only and text-only pages; 24/32/40/48 count; invalid trim profile; zero page assignment.
- Corrupt images, unsafe relative paths, symlinks, huge or decompression-bomb images, unsupported formats, wrong MIME.
- Two books with identical character names have different project-scoped IDs/assets.
- Edit a single character design invalidates only dependent images/reviews, never approved unrelated scenes.
- Generation provider disabled/offline -> absolutely no outbound HTTP; unsupported model capability -> clear error.
- API cost: estimate above cap, unknown price, expired quote, concurrent reservation, retry, mid-call failure; no silent overspend.
- 512px image printed full-page yields LOW_EFFECTIVE_DPI regardless of metadata claiming 300 DPI.
- Cover PDF must include back/spine/front and satisfy correct geometry; proof cover must not be labeled publishable.
- Run image worker with memory insufficient / forced timeout / cancellation; recover gracefully without partial corrupt asset.
- Draft book with unanswered severe review finding cannot receive ready-to-upload status.
- PDF font embedding test, Unicode, mirrored margins, bleed, image positioning, KDP Previewer manual check.

## Sample test commands
```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m compileall story2kdp app.py
story2kdp init examples/story.txt --title 'Test Book' --author 'Demo' --pages 32 --out projects/acceptance
story2kdp concept projects/acceptance scene-001
story2kdp review projects/acceptance
story2kdp export projects/acceptance
```
Use `PYTHONPATH=.` where package cannot be installed. Run against an isolated temp project, not real manuscripts. Capture stdout, Python/OS versions, exit codes and output file listing.

## Evidence template
| Test ID | Requirement | Command/Scenario | Expected | Observed | Result | Evidence link |
|---|---|---|---|---|---|---|
| T2-001 | sample export | CLI smoke | PDF readable | (fill) | NOT RUN | |
| T4-001 | CPU feasibility | explicit model benchmark | finishes under resource cap | (fill) | NOT RUN | |
| T5-001 | KDP wrap cover | 32-page premium cover | correct trim/spine | (fill) | NOT IMPLEMENTED | |

## Release gates
- DEV: unit and mocked integration green, developer docs updated.
- BETA: clean VPS acceptance, no blocking data/security defects, backup/restore test.
- PRINT CANDIDATE: full interior and cover validations pass, rights/AI disclosures reviewed, human approved design.
- PUBLISH: author validates files in the current KDP Print Previewer and inspects physical proof when appropriate.

# Code-specific external review — assessment and implementation disposition

Date: 2026-11-09. Basis: user-supplied Copilot code-specific assessment of extracted repository snapshot, compared to branch `feat/local-first-mvp` as of commit `3122fe60c44e4047d6d60e7cc803e079941eef59`. **This document records decisions; it is not evidence that all findings are fixed.**

## Review applicability
The assessment correctly identifies the discrepancy between ambitious docs and the proof-oriented v0.1 implementation. It reports no public production readiness, no proper cover, no hard cost cap, and no true character consistency. It also confirms present protections such as JSON snapshots, image re-encoding and simple path checks. The review describes the repository as a private/offline proofing MVP, which remains the correct public description.

## Disposition matrix

| Finding | Action | Track | Release gate |
|---|---|---|---|
| Unauthenticated Streamlit exposure | Provide loopback-only default config and private startup commands; design authenticated HTTPS deployment separately | P0-SEC | Baseline private bind + deployment penetration tests before public use |
| Project JSON is unchecked dictionary | Introduce Pydantic v1-to-v2 data migration, strict input validation, canonical path validation and corrupt-file recovery | P0-DATA | Schema unit tests, old JSON roundtrip, hostile input tests |
| AI consent without a monetary cap | Disable default paid requests; implement atomic cost ledger, conservative quotes, per-task/project caps and unknown-price fail-closed | P0-COST / P3 | Concurrent spending and failure tests |
| Documentation says SQLite while code uses JSON | Mark JSON as CURRENT and SQLite as DECIDED NOT IMPLEMENTED; use status matrix as canonical current-capability source | DOC | Docs consistent with code |
| Naive sentence-based page segmentation | Preserve paragraphs/headings/dialogue/page breaks; stable page/scene/spread IDs; split/merge/reorder UI | P1-PAGE | No unexpected content loss or renumbered identities |
| Character Bible free-form JSON | Strict character schema, approved visual references, per-scene dependencies and invalidation | P1-CHAR | Modify one character invalidates only dependent scenes |
| OpenVINO runs in caller process | Isolate optional model into cancellable subprocess and resource gate; disable UI invocation until ready | P2-CPU | Forced timeout/cancel/OOM tests |
| Helvetica/unicode limitations | Add licensed font registry; shaping/RTL decisions, embedding verification and non-Latin tests | P4-FONT | Font validation and visual sample proofs |
| Letterboxed PDF; inadequate preflight | Accurate gutter/bleed/geometry, effective DPI by placement, full wrap-cover and structured blocking report | P4-PRINT | Automated geometry and manual KDP Previewer signoff |
| Generic catch in export UI | Structured sanitized logging, known exception categories and correlation IDs | P0-LOG | No secrets/manuscript content in logs |
| Tests and CI too basic | Add offline CLI smoke, doctor, scenario fixtures, provider contract tests; later targeted lint, audits and coverage thresholds | P0-TEST | CI and real VPS evidence |
| Broad dependencies and root-requiring installer | Reproducible constraints, split doctor/system/python setup and smoke scripts | P0-DEP | Clean target Ubuntu install |
| Documentation duplicates implementation claims | README=entrypoint, STATUS_MATRIX=current, PRODUCT_REQUIREMENTS=target, BACKLOG=plan, DECISIONS=choices, ACCEPTANCE_TESTS=evidence | DOC | Consistency review |

## Scope adaptations for children's *picture books*
The reviewer suggests chapter outlines, headings, ToC and DOCX/EPUB renderer hierarchies appropriate for longer books. Keep a **page/scene-based canonical model** primary for illustrated short books. Add chapter abstractions and Kindle EPUB/DOCX as optional modules only when print foundations and scene continuity work. A chapter-oriented pipeline must not replace the picture-book storyboard.

## Sequenced actionable slices
1. **P0-01**: run `scripts/doctor.py`, `scripts/smoke_test.sh`, baseline tests and clean install on real VPS. Record observed measurements. No paid calls or model weights.
2. **P0-02**: validate JSON/schema, centralize paths and atomic persistence with project locks/restore. No silent migrations.
3. **P0-03**: deterministic test/CI plus reproducible dependency constraints and scan triage; secure localhost defaults.
4. **P0-04**: paid API default-off until an enforceable ledger exists; provider mocks and cache error handling.
5. **P1**: stable creative structures and human approval.
6. **P2**: resource-safe CPU and image providers with provenance.
7. **P3**: mature provider routing, budgets, reviews.
8. **P4**: publishing correctness and signoff.

## Current-branch implementation status
- Loopback Streamlit configuration: **added in this follow-up** (configuration default, not a security boundary; CLI/config overrides remain possible).
- Hardware diagnostic: **added in this follow-up**, must be executed on VPS for real hardware data.
- Offline CLI smoke script: **added in this follow-up**, must be executed and evaluated in CI/VPS.
- All other above improvements: **outstanding, explicitly tracked**.

## Reviewer-facing evidence format
For each task include exact commit/PR, file path, issue/requirement ID, test command, observed status, Ubuntu/CPU/RAM/swap, timing, and manual verification. Do not post private manuscripts, secrets or identifying machine information. Green CI does not certify print output.

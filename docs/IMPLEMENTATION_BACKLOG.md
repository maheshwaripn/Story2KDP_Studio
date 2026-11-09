# Implementation backlog for Claude Code
**Run tasks sequentially, one focused PR per slice.** Status as of 2026-11-09: only v0.1 foundation committed. This backlog is a plan, not completed work.

## Priority and dependency map
P0 -> P1 -> P2 -> P3 -> P4. Every task must include tests, docs, observed results and a rollback plan.

### P0 — VPS reproducibility and safety
**P0-01 Clean Ubuntu acceptance + hardware report** (scripts/doctor.py + scripts/smoke_test.sh now provided; actual VPS measurements and remediation still outstanding)
- Fresh venv test on supported Ubuntu, Python 3.10/3.11; fix incompatible dependencies or scripts.
- Add `scripts/doctor.py` to report OS, CPU model, memory (available and total), swap, disk, Python and installed dependency versions; redact account details.
- CLI smoke test: import sample, generate procedural art, review, export PDF, inspect PDF geometry. Add automated subprocess-based smoke test.
- Acceptance: reproducible commands and saved PASS/FAIL report, no need for API or model download.
**P0-02 Secure installation and project storage** (promoted: strict Pydantic schema, v1 migration, corrupt JSON recovery and project lock required)
- Validate project names and uploads, enforce allowed extensions/magic/size, prevent path escape/symlink abuse, file writes atomic, robust JSON input handling.
- Explicit per-project storage namespace, snapshot/backup and recovery, no exposure of secrets/manuscripts in logs.
- Acceptance: hostile-input tests; no traversal, oversize upload, or accidental overwrite; no public network listener by default.
**P0-03 Baseline quality toolchain** (include localhost bind verification, sanitized logs, dependency lock and CI smoke)
- Pin dependencies via lock strategy appropriate to environment; add ruff, mypy targeted checks, pytest coverage, GitHub Actions caching, license and secret scans as practical.
- Add fixtures for non-English text, very long paragraphs, missing illustration, unexpected PDF, and asset paths.
- Acceptance: documented clean install + deterministic pipeline passing across supported Python versions.

**P0-04 Paid API safety before wider testing:** Existing approval checkbox is not a budget. Default deny for untrusted usage, provider capability restrictions, conservative cost quotes, atomic spend ledger and mocked failure/concurrency tests. No claim of hard caps before they pass.

See [code-specific review disposition](REVIEW_RESPONSE_2026-11-09.md) for exact order and design decisions.

### P1 — Data model and creative editing
**P1-01 Canonical schema + migration:** Pydantic versioned project/scene/character/asset/review/job models; SQLite metadata, filesystem artwork; import v0.1 JSON without data loss. Test backward compatibility.
**P1-02 Manuscript and pagination:** DOCX headings, explicit page breaks, dialogue and Unicode, editable split/merge/reorder and stable scene IDs; test overflow/underflow and sparse picture books.
**P1-03 Approval system:** states DRAFT -> REVIEW -> APPROVED -> INVALIDATED; edits only invalidate dependent artifacts; history, compare, restore, approver and timestamp; test selective invalidation.
**P1-04 UX:** page thumbnails, character-sheet editor, per-scene visual prompt editor, issue list with fix/ignore/approval, export-ready blocker dashboard.

### P2 — Illustration engines and character continuity
**P2-01 Capability-based image adapter:** protocol supporting text-to-image, reference/image-to-image, inpainting, edit, dimensions, quality, provider/model/seed, metadata. Fail explicitly when unsupported; never route image requests into text-only Claude.
**P2-02 CPU worker and benchmark:** OpenVINO optional extra; model directory must be supplied, license/checksum recorded; resource gate, subprocess, cancellation, timeouts, memory/time logs; benchmark 384px and optionally 512px. No download on default installation/CI. Document that 8 GB may fail.
**P2-03 Character references:** per-book original concept variants; approved turnaround sheet and canonical palette; scene conditioning only where backend supports; reference reuse and consistency checks; human sign-off.
**P2-04 External image adapters:** start with one verified, supported image API and stub others with capability errors; require opt-in, provider key, budget reservation, rights metadata and selective scene regeneration. Mock everything in CI.
**P2-05 Quality and asset exports:** safe crop/bleed, effective-DPI calculation from printed placement, compositing at target dimensions, artifact origin tracking. Never claim interpolated upscale equals true new detail.

### P3 — API/task scheduler, review and cost controls
**P3-01 Robust provider abstraction:** text/vision adapters, versioned request schema, explicit permission, caching by input/model/settings, read-only offline mode, retry controls, timeout/cancellation, unit tests using mocks.
**P3-02 Actual spend enforcement:** pricing tables with snapshot timestamp and provider/model coverage; quote before execution, conservative max-cost reservation, per-project/per-task hard budgets, atomic ledger, reconciliation, manual override logging; unknown price blocks. Test concurrent requests and failures.
**P3-03 Review schemas:** severity, evidence, affected revision, actionable fix, waiver rationale, one-click rerun; deterministic reviews vs subjective AI opinion clearly labeled.
**P3-04 Story/child/art continuity review:** benchmarks and human test rubric, readability/visual emotion metrics as heuristics, no unsupported psychological claims.

### P4 — Production publishing
**P4-01 KDP interior geometry:** print configurations driven by validated current official KDP information, 8.5in square initially, odd/even gutter, interior/outside bleed, controlled typography, licensed embedded Unicode font; tests assert trim/bleed/raster effective DPI/overflow.
**P4-02 Cover builder:** official KDP calculator/template import or independently validated page/paper formula; single combined back/spine/front PDF, barcode exclusion, no spine text where prohibited, automated dimensions checks. Existing cover-design-proof must remain clearly non-uploadable.
**P4-03 Preflight and export gate:** detailed structured pass/fail checks; differentiate definite rule error vs recommendation vs external/manual validation; failed gate prohibits "production-ready" mark; KDP Previewer/physical proof human checkpoint.
**P4-04 Regression suite:** representative 24/32/40/48 page books, bleed/no-bleed, image proportions, Unicode, page/cover geometry, reproducibility; CI-generated PDF preview artifacts (without real/private content).
**P4-05 Release/operations:** versioned release notes, upgrade/migration guide, backup/restore, repeatable secure VPS startup, performance/cost observability.

## End-to-end test scenario for release
Using a copyright-safe example story: import -> editable page plan -> new book-specific character definition -> concept illustration -> assign/upload approved final images -> review -> create interior + wrap cover -> pass *automated* preflight -> human KDP Previewer approval. A fully offline run must not contact provider APIs, and all outputs must remain marked PROOF until production gates pass.

## Implementation issue/PR template
- Task ID and context
- Current behavior vs target
- Precise changed modules/data schema
- Security, IP/licensing and resource impact
- Tests (unit/integration/CI) and actual observed output
- Manual Ubuntu VPS commands and evidence
- Known blockers and next dependency

## Copilot review triage (2026-11-09)
Copilot could not retrieve the repository, so its advice was general rather than a file-specific code audit. The development branch is public but unmerged; point reviewers to `feat/local-first-mvp` or PR #1.

**Adopted in the current development branch:** project save revision snapshots and atomic replacement; stricter uploaded art handling; duplicate page/scene IDs and placeholder text in deterministic review. These are safeguards, **not** full autosave, migration, provenance or recovery UI.

**Add to P1:** Design one canonical book document schema with ordered front matter, story pages/scenes and back matter; keep scene/page ID identity and selective invalidation; establish a format-independent renderer interface and revision compare/restore. Do not add chapter structures to a picture-book-only project unless the user asks.

**Add to P3:** Prompt/model/version/temperature/seed metadata when supported, model-output JSON Schema validation, no unbounded retries, cancellation progress and reviewer categories (objective rule / AI heuristic / user choice). Add sensitive content detection with user-editable rules, not a single opaque score.

**Add to P4:** Offer optional DOCX / Kindle EPUB export only after the canonical book model and print PDF pipeline stabilize. Differentiate KDP paperback PDF requirements from Kindle EPUB; implement format-specific re-open/validate tests, and document accessible reading order. Reserve trim, cover and print-specific rules for PDF. Protect against widow/orphan and text overflow in long-form layouts where relevant.

**Repository operations:** Add CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, Dependabot and minimal static-security CI, with false-positive handling; add tests for interrupted processing, no content loss, low-cost retries and non-Latin text. Release notes must clearly distinguish code vs roadmap.

## Follow-up reviewer findings on repository discoverability
- **Repository default branch:** publish the tested development MVP and documentation to `main`, so external review sees actual files. Preserve explicit v0.1 / PROOF status. Merge through PR with checked head SHA.
- **Dependency reproducibility:** design and generate a verified lock/constraints strategy *after* clean Ubuntu acceptance; avoid guessing versions without resolver verification. Split system-level apt prerequisites from non-root repeatable Python installation.
- **Provider interface:** capability protocol, never-network offline mock, mocked failures, no implicit API calls, key material only from environment; protect `.streamlit/secrets.toml`.
- **Art workflow:** consistent character card IDs, prompts, seed/provider/provenance, per-image approval and rejection; no silent auto-approval.
- **Publishing profiles:** add 8×10 as a *target* preset only after current official KDP specs are validated; include metadata and AI disclosure user review. Do not turn proof PDF into a supposedly compliant upload before validation.
- **Repo hygiene:** pull request template, optional future version tag after VPS verification, check status matrix against code at every PR. Do not tag as stable or production-ready at this time.
- **Content safety:** apply rights review for known commercial characters and explicit opt-in for sending images/text or identifiable minors to external APIs; avoid brittle claims that a keyword ban guarantees IP safety.

## Free-for-all-features owner requirement (2026-11-09)
**No paywalls, Pro/Studio levels, payment gateways, subscriptions, quotas, mandatory commercial APIs, or trial locks.** This is an acceptance condition for every P0–P4 task. See [free-first policy](FREE_FIRST_POLICY.md) and [per-feature no-charge paths](FREE_FEATURE_MATRIX.md).

**Immediate:** Keep third-party commercial calls OFF by default, require explicit `STORY2KDP_ENABLE_PAID_APIS=1` plus manual approval, add an offline-no-network test. Do not enable cloud calls just because credentials happen to be present.

**Free baseline P1/P2:** Build proper character cards, visual storyboard, revision history, provenance and consistent prompt templates; offer reference uploads and manual artwork assignment at every stage. A neural generator must not be mandatory; if 8 GB CPU cannot support a model, degrade gracefully.

**Free P3:** Provide deterministic writing/continuity checks and optional locally hosted text model when performance supports it. Offline and manual review workflows must remain available without commercial services. Optional commercial adapters require separate billing protection.

**Free P4:** Use no-fee typography, layout and print-validation libraries; package legal font usage and produce professional PDF artifacts with external KDP Previewer verification. No paid template or print-preflight API dependency.

**Quality acceptance:** Free feature parity means equivalent workflow capability and export availability without payment, **not** guaranteed equivalence of automated illustration quality or runtime across hardware.

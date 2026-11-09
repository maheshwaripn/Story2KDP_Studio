# Story2KDP Studio — Product requirements (target state, not implemented status)
Version: 1.0 planning baseline, 2026-11-09. Owner: repository maintainer.

## 1. Personas and primary workflow
A book creator supplies original TXT/Markdown/DOCX text (later PDF optional), sets audience age/language, trim, print type, page count, author, rights and stylistic preferences. The application parses a book, suggests editable page spreads/individual pages, identifies original book-specific characters, creates a character Bible and storyboard, generates one or more candidate illustrations per scene, supports revision/approval, runs editorial/visual/print reviews, and produces an interior and **single-piece full-wrap cover** for KDP print plus a preflight report. Everything except optional image/text inference must function without an API.

## 2. Modes
- OFFLINE: deterministic parsing, character/scene templates and procedural placeholders; optional CPU diffusion only when model is installed and benchmarked. No network calls, no paid usage.
- HYBRID: user explicitly enables provider and selects exact tasks (character brief, storyboard, editorial review, scene illustration, visual review). Other stages stay local.
- MANUAL-ASSET: upload/assign owned or appropriately licensed art, bypass generation.
- PRODUCTION: not available until every print gate passes and the user approves final outputs; otherwise exports must visibly say PROOF.

## 3. Detailed capabilities and identifiers
PR-01 Manuscript ingestion: reject empty/oversized input, preserve sections/dialogue/page directives, Unicode, page ordering, and character/scene references; reproducible story manifest with revision history.
PR-02 Storyboard: editable scene text, image prompt/negative prompt, featured character IDs, pose/action, continuity markers, camera, foreground/background, emotional beat, page number; separate page count and scene count; allow illustration-only and text-only pages.
PR-03 Character Bible: per-book unique IDs; names, traits, appearance, age presentation, costume, palette, accessories, poses/expressions, visual reference sheet with approved revision; users can override every attribute. Maintain continuity across pages using reference conditioning when supported.
PR-04 Aesthetic control: default original hand-painted, warm, soft-edged animation-book profile; natural daylight, soft textures, positive emotions, balanced contrast, smooth silhouettes. Configurable palette; do not clone protected characters or trademarks.
PR-05 Illustration execution: pluggable backends, capability matrix, reproducible job specs, seed/model reference where possible; at least local procedural previews, manual assets, optional OpenVINO CPU SD1.5; later verified real image API provider(s). The program must never imply local previews are final neural art.
PR-06 Asset operations: upload, image-to-image/references when supported, version/compare, regenerate **one scene** independently, preserve previous files, generate contact sheet, check effective resolution and provenance. No destructive overwrite without explicit confirmation.
PR-07 Multi-layer review: grammar/age-appropriateness/story arc, page/character continuity, emotional tone, composition/color, low-resolution/bleed, page sequence, model/content rights; findings have reviewer type, severity, page/asset ID, evidence, suggestion, status, timestamp. Heuristic checks identified as heuristics; no medical or psychological certification claims.
PR-08 AI orchestration: providers OpenAI, Anthropic, Gemini for supported text/vision tasks, compatible image providers as separately defined. Provider/model task mapping, explicit approval UI, prompt/result cache hashing, rate limiting, timeouts, retries with idempotency where supported, selectable per-task budget.
PR-09 Cost safety: no API execution until enabled + preflight estimated cost + budget reservation approved. Account for currency, text tokens and image-unit pricing separately; conservative unknown-cost behavior = block; billable failures treated conservatively. Store approved/estimated/actual spend. Users may run entirely offline.
PR-10 Publishing: KDP print profiles (trim, bleed, color/paper, binding page thresholds, odd/even gutters), embedded licensed fonts, pagination, overflow check, cover dimensions/spine/barcode safe area, single-page interiors, image effective DPI, deterministic preflight, Previewer signoff. Support draft exports while incomplete; do not label as KDP-ready without all gates.
PR-11 Operations: Ubuntu VPS headless install, non-public SSH tunnel access, backup/restore, migrations, health logs and subprocess isolation, safe deletion, disk quotas, local test fixtures.
PR-12 Rights and transparency: record source of artwork and model license, commercial rights, publication permissions, prompts/references, required AI disclosure check. No unlicensed model bundled.

## 4. Nonfunctional requirements
- 8 GB RAM on Intel Linux, no GPU; graceful refusal to start expensive inference when resources are insufficient.
- Offline workflow install can use internet for packages but runtime must not contact third parties without permission. Separate optional model download with checksums.
- Dependency/version pinning; CI for supported Python/Ubuntu combinations; deterministic unit tests, no real API charges in CI.
- Secure-by-default: path traversal checks, file size limits, MIME validation, redact secrets, prevent URL fetch/SSRF where unsupported, local-only binding, proper project isolation.
- Accessible basic UI, useful error messages, graceful restart after failures; no hidden automation requiring internet.

## 5. Release boundaries
R0 (existing v0.1): proof-oriented manuscript/scene editing, procedural preview, basic checks and PDFs, optional text API, experimental CPU backend.
R1: reliable operational offline pipeline (clean VPS setup, migrations, safe editing, robust test coverage).
R2: production-grade creative reviews, approved asset workflow, optional real image APIs with hard budgets.
R3: print-preflight-complete KDP interior/full-wrap cover and user preview acceptance. No "KDP certified" claim; KDP makes final acceptance decisions.

## 6. Explicit exclusions until separately scoped
No autonomous KDP account upload, no guarantee of copyright ownership or Amazon acceptance, no guaranteed Ghibli likeness or reproduction of existing IP, no claim of high-quality CPU-only offline diffusion under every hardware configuration.

## 7. Permanent free-access and complete-feature requirement
**Owner decision: free and open-source product, with all functional capabilities available without subscription or license payments.** This supersedes any three-tier/free-versus-Pro/Studio monetization recommendations. The no-charge path for every feature can be local/offline or manual-assisted; no commercial AI credentials may be required to create, review or export a book. Future polished AI generation may be limited by available hardware and licensed model capabilities; do not claim an 8 GB CPU can achieve every result autonomously.

- All application features are in one community edition, no feature flags tied to money.
- Offline/manual-only workflow is the baseline acceptance suite. Optional third-party commercial APIs are a convenience rather than a requirement, default disabled, with explicit opt-in and safe budget checks before any use.
- Advanced local models can be optional downloads after license and memory checks. Unsupported low-memory generation must give an actionable fallback (manual art upload or provider-free reference/template workflow).
- KDP-ready export/publishing-validation code should use freely available libraries, scripts, lawful fonts and official KDP specifications; no paid template service dependency.
- User authorship, generated media rights, third-party licensing and printing costs are distinct from the software's free access.
- Details and acceptance: [FREE_FIRST_POLICY.md](FREE_FIRST_POLICY.md), [FREE_FEATURE_MATRIX.md](FREE_FEATURE_MATRIX.md).

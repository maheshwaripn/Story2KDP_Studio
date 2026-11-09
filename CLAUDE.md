# Claude Code: project instructions (read first)

This file is the authoritative instruction entry point for agents working in this repository. Follow instructions in this order: user request, this file, docs/PRODUCT_REQUIREMENTS.md, docs/IMPLEMENTATION_BACKLOG.md, docs/ACCEPTANCE_TESTS.md, then existing implementation. Treat documentation as *requirements*, not proof of implementation.

## Mission and non-negotiables
Build Story2KDP Studio: a Linux-first, CPU/8 GB RAM-friendly, local-first children's pictorial-book creation tool. Import manuscripts; generate unique per-book character concepts and illustrated scenes with warm, soft-edged, hand-painted Japanese-animation-inspired visual direction; review and approve editorial/art decisions; export rigorously checked Amazon KDP print interiors and full-wrap covers. Support selective, user-approved OpenAI, Anthropic/Claude, and Google/Gemini use. No mandatory tokens, no required discrete GPU, no silent external uploads.

Do not claim generative AI quality is possible offline on all 8 GB CPUs. Procedural previews != generated professional art. Explicitly label proofs vs production exports. A successful CI run is not evidence of KDP compliance.

## Working agreement
1. First read README.md, docs/ROADMAP.md, docs/PRODUCT_REQUIREMENTS.md, docs/IMPLEMENTATION_BACKLOG.md, docs/ACCEPTANCE_TESTS.md, docs/SECURITY_AND_PRIVACY.md, docs/UBUNTU_VPS.md.
2. Inspect current implementation and tests; run `python -m pytest -q` before changing anything. Report failures without inventing results.
3. Make only one coherent backlog slice per PR. Begin with P0 blockers; do not attempt every milestone in one prompt.
4. Before coding, write the smallest implementation plan and acceptance checks for the selected task. Prefer Python 3.10/3.11 compatible code and pinned, reproducible dependencies.
5. Add tests with every functional change, including failures, resource/budget limits, bad inputs, and paths. Update corresponding docs and README status.
6. Execute lint/type/tests when installed; run a clean install in a fresh venv where feasible. Record CPU, RAM and observed runtime for model benchmarks. No fabricated timing or hardware claims.
7. Never commit secrets, manuscript content uploaded by users, generated commercial artwork, model weights, project directories or unapproved API calls.
8. Use Git branches and PRs; avoid destructive git commands. Do not merge without user approval. Keep GitHub Actions minimal and cost-free.
9. If blocked by memory, model licensing, external provider access or KDP ambiguity, implement a safe stub and document the exact blocker and manual path.
10. Finish with: files changed, tests actually run, residual risks, and reproduction commands. File a clear issue if work remains.

## Hardware operating constraints
- Target Ubuntu VPS x86_64 Intel CPU, 8 GB total RAM, no dedicated GPU. App, PDF and reviews must function without downloading models.
- Default to a single heavy job at a time. Isolate CPU inference in a subprocess with timeouts, cancellation, progress/health reporting and memory-aware refusal. Do not run diffusion inside a Streamlit request handler.
- Never enable memory-heavy inference by default. No mandatory Swap requirement (swap may prevent OOM but is very slow). Disk quota and model provenance must be recorded.
- No exposed unauthenticated Streamlit service. Use 127.0.0.1 and SSH tunnel; production deployment requires authentication and TLS.

## Essential product constraints
- Human approval gates for character Bible, storyboard, each selected image and final print assets.
- Local SQLite/filesystem as source of truth; reproducible metadata for each asset (prompt, provider, model ID/version, seed if applicable, source, rights, timestamps, revision, cost).
- Task routing: `offline`, `openai`, `anthropic`, `gemini`, `external_image`; capability discovery must reject unsupported requests (Claude text/vision review is not native image generation).
- Default API access OFF; never send a manuscript or character reference without specific user consent. Redact keys and content from logs.
- Use conservative cost reservation, enforce task and project budgets, account for image/unit billing, show actual vs estimated spending; no calls once reservations exceed cap.
- No undisclosed image model/license restrictions. User owns publishing decisions; require review of current KDP print specs and AI disclosure policies.
- Aesthetic: original book-specific characters, luminous backgrounds, gentle emotional tone, rounded silhouette and cohesive color palettes. Do not copy characters/scenes from existing films.

## Definition of Done
See docs/ACCEPTANCE_TESTS.md. No feature is "done" merely because source files exist. CI success, integration tests, field checks, human visual approval, and KDP Previewer are different gates.

## First task to execute on VPS
Work on P0-01 from docs/IMPLEMENTATION_BACKLOG.md. Install in a clean venv, inspect failures, add hardware benchmark without downloading a model, fix packaging and create a test report. Then proceed through P0-02, P0-03 ... one slice per PR.

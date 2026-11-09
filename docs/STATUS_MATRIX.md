# Capability status — checked against v0.1 repository on 2026-11-09

Legend: WORKING BASIC = code in repository and covered by limited tests; EXPERIMENTAL = conditional backend with no user VPS benchmark; PLANNED = spec only; MANUAL = creator supplies/reviews output. Recheck this file after every implementation PR.

| Area | Status | Notes |
|---|---|---|
| TXT/MD/DOCX import | WORKING BASIC | Basic parser, no robust dialogue/complex pagination |
| Editable storyboard | WORKING BASIC | Simple scene edits and JSON character notes |
| Unique original polished characters per book | PLANNED | A character specification is not a generated reference sheet |
| Procedural offline scene art | WORKING BASIC | Low-detail concept preview only |
| OpenVINO CPU SD1.5 | EXPERIMENTAL | Preconverted model separately required; 8 GB may OOM |
| Image API providers | PLANNED | Do not conflate with text API support |
| Text APIs OpenAI/Claude/Gemini | WORKING BASIC | Opt-in; no hard spending ceiling |
| Character continuity reference conditioning | PLANNED | User manual review currently required |
| Deterministic reviews | WORKING BASIC | Limited resolution/path/approval checks |
| Vision and age suitability review | PLANNED | Not a professional certification |
| Interior PDF | WORKING BASIC | Draft/proof, not full production KDP compliance |
| Full-wrap cover | PLANNED | Current front cover is watermarked design proof |
| Comprehensive print compliance | PLANNED | Limited page-count/media-size preflight now |
| CI | WORKING BASIC | GitHub Actions Python tests; no CPU inference |
| Ubuntu VPS acceptance | NOT YET VERIFIED | User to run and share measured results |
| Authentication, secure public deployment | PLANNED | SSH tunnel localhost only |

Release readiness: **development MVP / private trusted testing only**.

## Post-review incremental safeguards (2026-11-09)
The branch now retains a previous project.json snapshot in `revisions/` on each save (not a full autosave/restore system). The Streamlit image upload handler limits raw size and pixel count, decodes PNG/JPEG data and generates its own safe filename. The local reviewer flags duplicate scene IDs, duplicate page assignments and placeholder text, and approximates effective DPI from the *existing* layout box. These do not make KDP production export ready. Additional security, revision UX, schema migrations and CI acceptance remain planned.

## External code-specific review integration (2026-11-09)
The user-provided review confirmed v0.1 is a private proofing MVP. Loopback Streamlit default configuration, a standard-library VPS diagnostics tool, and a synthetic offline CLI smoke script have now been added to the development branch; VPS results and full data-validation hardening remain **NOT VERIFIED/PLANNED** respectively. Details: [review response](REVIEW_RESPONSE_2026-11-09.md).

## Main-branch publication policy
All status flags here reflect actual repository functionality, not promises. GitHub's default branch may include in-progress architecture and documentation; **production KDP support, CPU model reliability and AI spending caps remain unverified or planned** until explicitly promoted by acceptance tests. Optional OpenVINO is a real experimental code path in `illustration.py`, but requires a separately acquired compatible model and has no demonstrated reliable loading on an 8 GB CPU-only VPS.

## Free edition commitment versus implemented features
One official free application edition; no subscriptions or Pro/Studio feature gates. The currently functional offline manuscript/storyboard/proof functions are no-fee, and paid provider calls are disabled by default (`STORY2KDP_ENABLE_PAID_APIS=0`). The future full workflow must provide free local/manual paths as tracked in [FREE_FEATURE_MATRIX.md](FREE_FEATURE_MATRIX.md). **This does not imply all rows are implemented today or that local professional generation is feasible on 8 GB RAM.**

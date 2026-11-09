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

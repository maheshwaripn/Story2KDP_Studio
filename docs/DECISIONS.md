# Architecture decisions record

ADR-001 (2026-11-09): local-first modular Python application, Streamlit/SQLite/filesystem over microservices. Reason: 8 GB headless CPU VPS and solo maintenance. Revisit only with measured scaling need.
ADR-002: procedural offline illustrations are *concept previews*, distinct from professional generative artwork. Optional OpenVINO SD1.5 CPU only as benchmarked plugin. No guarantee of performance or commercial quality.
ADR-003: per-book character Bible + human signoff required before scene generation; each scene references stable character IDs and approved asset revisions.
ADR-004: paid API is task-scoped and explicitly opt-in. OpenAI/Anthropic/Gemini capability adapters must fail closed when a requested model cannot perform image generation. Cost controls must treat images differently from text tokens.
ADR-005: proof exports remain PROOF until print preflight gates, rights review and human Previewer pass. No one-click automatic KDP publishing.
ADR-006: one subprocess heavy job at a time; UI must remain responsive, workers cancellable, and low memory should stop initiation rather than crash VPS.
ADR-007: GitHub `feat/local-first-mvp` is initial integration branch; Claude Code makes small PRs; main changes require user approval. Never assume branch names after merges without checking repository state.
ADR-008: default appearance is original soft hand-painted animation aesthetic, positive emotions and smooth edges; reference to established studio is inspiration only, not replica character design.

ADR-009 (2026-11-09): **All features remain free in the official application**. No tiers, license-key locks or mandatory provider subscriptions. The no-fee implementation path can be offline/manual-assisted where local neural inference is infeasible. Paid cloud APIs are optional, disabled by default, and may charge the operator if separately enabled; they cannot be the only access path to a core operation. This owner decision overrides external monetization suggestions.

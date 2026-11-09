# No-cost implementation matrix for all current and target features

Every row describes a **free user workflow**, not an assertion of already delivered code. The authoritative implemented-versus-planned register remains [STATUS_MATRIX.md](STATUS_MATRIX.md).

| Feature | Free route with no commercial APIs | Current implementation |
|---|---|---|
| Manuscript import, writing and revisions | TXT/MD/DOCX + local editing, snapshots | Basic import, editing, JSON snapshots |
| Storyboard/page/spread planning | Deterministic segmentation, manual reorder/split, page grid | Basic scene editor; visual planning planned |
| Original per-book characters | User-entered character cards, palette/pose/reference sheets, owned uploads | JSON notes only; structured cards planned |
| Character continuity | Approved fixed references and repeatable per-scene context; user compares/rejects | Planned |
| Illustration concepts | Procedural art, manual artwork upload, optional legally permitted local CPU model | Procedural and upload available; OpenVINO experimental |
| High-resolution final artwork | Locally supplied original/licensed art, crop/resize and manual enhancement; optional hardware-feasible local generation | Upload available; print-grade quality not guaranteed |
| Illustration edits and candidate comparison | Local image manipulation, selected variation and asset history | Planned |
| Story/editorial review | Free deterministic checks + manual review, optional on-device LLM after hardware benchmark | Basic deterministic checks; advanced checks planned |
| Age/readability/visual review | Transparent rules, visual checklist, human judgment; local models optional | Planned / basic warning only |
| Approval/version history | Offline saved decisions, revisions, restore | JSON snapshot basic; structured approvals planned |
| Cost and privacy controls | All commercial providers OFF by default; no charge in free mode | Paid calls now default-disabled, hard budget gate pending |
| KDP print profile, margins, bleed, DPI | Local licensed fonts and libraries + official specifications | Draft only; full geometry planned |
| Interior PDF and full-wrap KDP cover | Free Python generators and preflight tools; KDP Previewer manually | Proof-only interior/front cover; production planned |
| DOCX/EPUB accessibility and metadata | Free locally installed renderers and validators | Optional later phase |
| Backup/restore and local deployment | Local filesystem/SQLite, standard SSH, archives | Basic JSON snapshots; migration/restore planned |
| Professional automatic AI illustration on 8 GB CPU | No guaranteed equivalent: use manual approved art; optional model if hardware permits | **NOT GUARANTEED** |

## Do not confuse these
- **Free feature access**: users pay no software subscription or fee for any current/future feature.
- **Fully automated AI quality**: constrained by model technology, RAM, CPU performance, licenses and human skill.
- **KDP eligibility**: validated print specifications, rights, external Previewer and possible paid proof/print costs remain separate.
- **Optional third-party API**: if a user deliberately enables a provider that charges money, that provider can bill them; no official feature should depend on it.

## Acceptance requirement for Claude Code
Before marking a task complete, document its no-fee path; run at least one no-key/offline scenario for it, assert zero outbound provider calls, and keep the UI clear about any quality/performance limitations.

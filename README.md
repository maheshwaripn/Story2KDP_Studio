# Story2KDP Studio

**A local-first Python studio for turning children's story manuscripts into illustrated picture-book proofs, with a roadmap toward validated Amazon KDP print production.**

[![Python tests](https://github.com/maheshwaripn/Story2KDP_Studio/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/maheshwaripn/Story2KDP_Studio/actions/workflows/test.yml)
[![Development roadmap](https://img.shields.io/badge/roadmap-open%20issues-blue)](https://github.com/maheshwaripn/Story2KDP_Studio/issues)](https://github.com/maheshwaripn/Story2KDP_Studio/pull/1)
![Status](https://img.shields.io/badge/status-v0.1%20MVP-orange)
![Hardware](https://img.shields.io/badge/target-Linux%20CPU%20%7C%208GB%20RAM-informational)

> **Project status:** v0.1 development MVP. Its current PDF exports are **proofs, not KDP-ready publishing files**. This application does **not yet** deliver commercially polished, fully consistent new AI characters and illustrations, a KDP full-wrap cover, comprehensive print validation, or enforced API spending ceilings. See the [capability status matrix](docs/STATUS_MATRIX.md) before using any feature.

## Vision

Story2KDP Studio is being developed for creators who want to take a manuscript through **storyboard → original per-book character design → scene illustrations → editorial and visual review → KDP-ready book files**, while retaining control over the creative process and cloud AI usage.

The target look is **original, hand-painted, soft-edged, colorful, warm, uplifting animation-inspired storybook art**. Each book should have its own approved characters and visual identity. Inspiration from Japanese animated storytelling is not permission to copy existing film characters or copyrighted scenes.

### Design principles

- **Linux-first and CPU-friendly:** Intel x86_64, 8 GB RAM, no dedicated GPU; core manuscript, editing, reviews and PDF proofing must function without running a neural model.
- **Offline by default:** no API keys or paid tokens are needed for basic workflow. Procedural concepts are placeholders, not professional text-to-image synthesis.
- **Selective AI:** creators choose which text, review or image tasks may use an external provider, with explicit consent. OpenAI, Claude and Gemini **text** integrations exist in basic form; image API adapters and hard budget gates are planned.
- **Human creative approval:** review characters, page plans, final artwork and print proofs; regenerate only affected work.
- **Honest print readiness:** distinguish draft/proof output from actual KDP upload-ready interior and cover; KDP's own Previewer and publisher approval are mandatory final gates.
- **Reproducible engineering:** documented tasks, measurable acceptance tests, GitHub CI, and small Claude Code pull requests.

## What works now vs what is planned

| Capability | v0.1 state |
|---|---|
| Import TXT, Markdown and DOCX | Basic implementation |
| Split manuscript into editable scenes; storyboard prompts | Basic implementation |
| Character descriptions / JSON Bible | Basic manual editing |
| Offline procedural illustration concepts | Implemented; **not** generative finished art |
| Local OpenVINO Stable Diffusion 1.5 CPU backend | Experimental; separately sourced model, not verified on target VPS |
| OpenAI / Anthropic Claude / Google Gemini **text** tasks | Basic opt-in integrations; no hard cost cap |
| Direct production image APIs | Planned |
| New unique polished character sheets, reference-conditioned continuity | Planned |
| Editorial, missing-image, basic resolution and path checks | Basic checks |
| Draft interior PDF and design-proof front cover | Implemented; **not KDP print production** |
| Full-wrap KDP cover, embedded fonts, bleed/gutter preflight | Planned |
| Automated tests (GitHub Actions on supported Python versions) | Implemented |
| Ubuntu VPS field acceptance and CPU model benchmarking | Awaiting on-device tests |

More precise claims and limitations: [docs/STATUS_MATRIX.md](docs/STATUS_MATRIX.md).

## Quick start — Ubuntu VPS / Linux

Requirements: Python 3.10+ (3.10/3.11 tested in GitHub CI), Git, Python venv support and sufficient disk. The standard setup does **not** require a GPU, model download, or cloud API key.

**The current v0.1 proofing MVP and development documentation are available on `main`.**

```bash
git clone https://github.com/maheshwaripn/Story2KDP_Studio.git
cd Story2KDP_Studio
bash scripts/bootstrap_ubuntu.sh
source .venv/bin/activate
python -m pytest -q
```

Start the app **privately** on the VPS:

```bash
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

On your laptop/computer, create an SSH tunnel:

```bash
ssh -L 8501:127.0.0.1:8501 ubuntu@YOUR_VPS_IP
```

Open **http://localhost:8501** locally. Substitute your actual VPS username/address. **Do not expose port 8501 publicly**: authentication and hardened reverse-proxy deployment are not in the MVP.

Full installation, troubleshooting and operating procedure: [Ubuntu VPS guide](docs/UBUNTU_VPS.md).

## Create your first offline book proof

1. In Streamlit, upload a TXT, Markdown or DOCX manuscript and set the book metadata.
2. Open the **Storyboard** editor to revise page text, prompts and character notes.
3. Generate **offline procedural concept previews**, or upload images you own or are authorized to use.
4. Review missing/low-resolution images and approval issues.
5. Export `interior.pdf`, `cover-design-proof.pdf` and `preflight.json`.
6. Inspect each page. **Do not submit the front-cover design proof as a KDP full-wrap cover or treat the draft interior as validated for upload.**

Command-line equivalent:

```bash
story2kdp init examples/story.txt --title "The Kind Sparrow" --author "Your Name" --pages 32 --out projects/demo
story2kdp concept projects/demo scene-001
story2kdp review projects/demo
story2kdp export projects/demo
```

### Offline image generation: realistic expectations

The standard concept engine draws simple original procedural illustrations. To experiment with **neural** text-to-image on Intel CPU, see [docs/ILLUSTRATION.md](docs/ILLUSTRATION.md). The optional OpenVINO pipeline requires an independently downloaded, compatible, commercially permitted preconverted model. **An 8 GB RAM, no-GPU machine may fail to load the model**, and local diffusion can be slow; do not make it a prerequisite for installing or testing the publishing app.

### Optional AI integrations

The current basic API implementation is documented in [docs/API_PROVIDERS.md](docs/API_PROVIDERS.md). API operations require explicit approval; they may incur provider charges. **Hard project-level budget enforcement and real production image API support are future tasks**, so do not assume a selected provider has every capability. Never commit API keys, model weights or private manuscripts.

## Claude Code implementation handoff

If you will develop this project with Claude Code on your Ubuntu VPS, use these as the **source of truth**, in this order:

1. [CLAUDE.md](CLAUDE.md) — permanent agent instructions and boundaries.
2. [docs/VPS_CLAUDE_CODE_RUNBOOK.md](docs/VPS_CLAUDE_CODE_RUNBOOK.md) — setup, exact starting prompt, safe PR workflow.
3. [docs/PRODUCT_REQUIREMENTS.md](docs/PRODUCT_REQUIREMENTS.md) — end-state feature specifications.
4. [docs/IMPLEMENTATION_BACKLOG.md](docs/IMPLEMENTATION_BACKLOG.md) — ordered P0–P4 tasks and dependencies.
5. [docs/ACCEPTANCE_TESTS.md](docs/ACCEPTANCE_TESTS.md) — unit, integration, hardware and publishing release gates.
6. [docs/SECURITY_AND_PRIVACY.md](docs/SECURITY_AND_PRIVACY.md) — privacy, usage budgets, IP rights and VPS safety.
7. [docs/STATUS_MATRIX.md](docs/STATUS_MATRIX.md) — current implementation versus future capabilities.

**First Claude Code task: P0-01 only.** Run the included hardware diagnostics and synthetic offline smoke test on your VPS; fix actual installation issues and produce a small, tested PR. Claude Code itself is **not** needed to install or operate the existing MVP. Do not download large models, trigger paid APIs or attempt all milestones at once.

Tracked workstreams: [P0 setup](https://github.com/maheshwaripn/Story2KDP_Studio/issues/2), [P0 security](https://github.com/maheshwaripn/Story2KDP_Studio/issues/3), [P1 creative workflow](https://github.com/maheshwaripn/Story2KDP_Studio/issues/4), [P2 illustrations](https://github.com/maheshwaripn/Story2KDP_Studio/issues/5), [P3 API/reviews/budgets](https://github.com/maheshwaripn/Story2KDP_Studio/issues/6), [P4 print production](https://github.com/maheshwaripn/Story2KDP_Studio/issues/7).

## Architecture

```text
Manuscript (TXT / MD / DOCX)
       |
Streamlit UI + Python CLI
       |
Story / Character / Storyboard data (local projects)
       |
+-----------------------------+------------------------------+
| Offline: planning, review,  | Opt-in: text providers,      |
| procedural concepts, PDF    | experimental CPU diffusion,  |
| generation and checks       | future image APIs           |
+-----------------------------+------------------------------+
       |
Human artwork / editorial approvals
       |
Draft interior PDF + proof cover + preflight JSON
       |
Future: production KDP interior + full-wrap cover + validated gates
```

Technical details: [architecture](docs/ARCHITECTURE.md), [architecture decisions](docs/DECISIONS.md), [review & publishing checklist](docs/KDP_CHECKLIST.md).

## Testing and feedback

```bash
python -m pytest -q
python -m compileall story2kdp app.py
```

GitHub Actions runs basic Python tests; it does **not** benchmark an actual 8 GB VPS, run image models, prove visual consistency or certify KDP acceptance. For production, enforce full automated preflight plus human visual review, rights/disclosure verification and current KDP Print Previewer checks.

Please report reproducible issues via [GitHub Issues](https://github.com/maheshwaripn/Story2KDP_Studio/issues) with environment, commit, steps, observed/expected results, safe logs, and timing/RAM if relevant. Do not post secrets, unlicensed images or private manuscript text.

## Additional documentation

- [Development roadmap](docs/ROADMAP.md)
- [Illustrations and style consistency](docs/ILLUSTRATION.md)
- [KDP checklist and outstanding production work](docs/KDP_CHECKLIST.md)
- [Agent architecture decisions](docs/DECISIONS.md)

## Important: MVP scope and release policy

This is a **private/trusted-use proofing MVP**, not a KDP-ready production tool. The optional OpenVINO adapter in `story2kdp/illustration.py` is an **experimental local function**, not a tested, preloaded CPU illustration engine. It is not enabled in the Streamlit UI and requires a separate compatible model and explicit CLI invocation. No professional offline visual-quality guarantee is made. GitHub tests verify proof workflows, not model loading or print acceptance. See [current capability register](docs/STATUS_MATRIX.md).

## License and publishing responsibility

See [LICENSE](LICENSE) for repository software license terms. Third-party models, artwork, fonts, API output and manuscripts can carry separate terms. Authors must confirm rights and current Amazon KDP AI-content disclosures and print specifications. No association with, endorsement by, or certification from Amazon KDP, Studio Ghibli or any AI model vendor is claimed.

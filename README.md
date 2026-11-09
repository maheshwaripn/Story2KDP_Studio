# Story2KDP Studio

Local-first children's illustrated book studio for Linux CPU-only systems. **Current release: v0.1 MVP, not an unattended, KDP-certified commercial publishing pipeline.**

The project creates editable storyboards from manuscripts, supports original offline *procedural previews*, offers an optional experimental OpenVINO Stable Diffusion 1.5 backend for neural images, has opt-in OpenAI/Anthropic/Gemini **text** tasks, offers review rules and generates a single-page interior PDF. Its cover is **design proof only**. It does not yet provide reliable commercial-quality offline illustrations, hard API budget enforcement, direct image API integrations, or production wrap-cover generation.

## 1. Ubuntu VPS setup (Python 3.10+)

```bash
git clone https://github.com/maheshwaripn/Story2KDP_Studio.git
cd Story2KDP_Studio
bash scripts/bootstrap_ubuntu.sh
source .venv/bin/activate
python -m pytest -q
```

If testing an unmerged feature branch, run `git checkout feat/local-first-mvp` after cloning and before bootstrap.

### Launch privately through SSH (recommended)

On VPS:

```bash
source .venv/bin/activate
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

On your computer:

```bash
ssh -L 8501:127.0.0.1:8501 ubuntu@YOUR_VPS_IP
```

Open `http://localhost:8501` in your **local** browser. Streamlit has **no login** in this MVP: never expose port 8501 directly to the public internet. Replace `ubuntu` with your actual VPS account. Use HTTPS and authentication before any production deployment.

## 2. First book — no API cost

1. Open the local forwarded Streamlit URL.
2. Upload a TXT, Markdown or DOCX manuscript; enter title, author and project folder.
3. Create the project. Scenes are segmented deterministically and stored in `projects/<folder>/project.json`.
4. In **Storyboard**, edit page text and illustration prompts, and enter a character Bible as a JSON array; save changes.
5. Under **Illustrations**, generate procedural offline concept previews (these are **not** neural art). Or upload PNG/JPEG illustrations you made or licensed.
6. In **Review**, inspect missing artwork, low resolution, unapproved scenes and more. Fix findings.
7. Under **Export**, create `interior.pdf`, `cover-design-proof.pdf`, and `preflight.json`.
8. Open the interior PDF in a PDF viewer and inspect every page, then validate with KDP's own Previewer before publishing. **Do not upload the proof cover.**

## 3. Terminal alternative

```bash
story2kdp init examples/story.txt --title 'The Kind Sparrow' --author 'Your Name' --pages 32 --out projects/demo
story2kdp concept projects/demo scene-001
story2kdp review projects/demo
story2kdp export projects/demo
```

## 4. Optional image generation on Intel CPU

See [docs/ILLUSTRATION.md](docs/ILLUSTRATION.md). Requires a separately downloaded, commercially permitted, *already OpenVINO-converted* model and significant CPU/RAM. On 8 GB RAM, model loading may fail. Not part of the basic installation.

## 5. Optional text AI (paid)

See [docs/API_PROVIDERS.md](docs/API_PROVIDERS.md). The UI requires explicit approval for each task. The MVP offers no hard monetary spending limit. The exact amount charged by a provider is controlled by its pricing and usage; there is **no automatic retry** for failed calls. API keys stay in environment variables and must never be added to Git.

## 6. Documentation

- [Technical architecture](docs/ARCHITECTURE.md)
- [Ubuntu VPS deployment](docs/UBUNTU_VPS.md)
- [Illustrations and visual consistency](docs/ILLUSTRATION.md)
- [API providers and costs](docs/API_PROVIDERS.md)
- [KDP requirements and limitations](docs/KDP_CHECKLIST.md)
- [Development roadmap and feedback](docs/ROADMAP.md)

## Status / safety

- Current PDF layout fits single pages with **letterboxed** illustration boxes, not edge-to-edge full-bleed illustrations. Media dimensions use KDP's bleed-sized page, but actual imagery does not bleed. Current export is a **draft/proof**, not automatically KDP-compliant.
- No automated font licensing/embedding audit or cover-spine template; non-Latin text may fail with standard Helvetica and must be tested.
- Default output is a 32-page square paperback draft. Short manuscripts can leave blank pages.
- Art and editorial review require human approval. Never assume a machine score guarantees artistic quality, age suitability, or KDP acceptance.
- Model and API licenses, copyright disclosures and KDP's latest AI-content policies remain the publisher's responsibility.

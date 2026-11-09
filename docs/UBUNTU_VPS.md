# Step-by-step: Ubuntu VPS without GPU

## 1. Minimum server preparation

Recommended: Ubuntu 22.04/24.04 with Python >= 3.10, 8 GB RAM, several GB of free disk for Python; considerably more if downloading image models. Use a regular sudo-capable Linux user, not root. Validate hardware:

```bash
lscpu | grep 'Model name'
free -h
df -h
python3 --version
```

## 2. Clone and install

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip
mkdir -p ~/apps && cd ~/apps
git clone https://github.com/maheshwaripn/Story2KDP_Studio.git
cd Story2KDP_Studio
# For unmerged MVP branch, use: git checkout feat/local-first-mvp
bash scripts/bootstrap_ubuntu.sh
source .venv/bin/activate
pytest -q
```

## 3. Launch and access securely

```bash
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

On a separate laptop/desktop, open an SSH tunnel: `ssh -L 8501:127.0.0.1:8501 YOUR_USER@YOUR_VPS_IP`, then browse `http://localhost:8501`. Keep the session active. No new inbound firewall port is required other than SSH. **Do not expose port 8501 on the public IP**. HTTPS/authentication is not built in.

## 4. Sanity test without cloud costs

```bash
story2kdp init examples/story.txt --title 'The Kind Sparrow' --pages 32 --out projects/demo
story2kdp concept projects/demo scene-001
story2kdp review projects/demo
story2kdp export projects/demo
ls -lh projects/demo/output/
```

The interior PDF is **draft only**; the cover is watermarked design proof. Review all output pages. For commercial KDP publishing, follow `KDP_CHECKLIST.md` and create a proper KDP full-wrap cover elsewhere until the cover module is implemented.

## 5. API opt-in

Set optional keys only for the provider you want to use:

```bash
export OPENAI_API_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'
export GEMINI_API_KEY='your-key'
```

Never paste keys into GitHub issues, feedback reports or terminal logs. Prefer a shell environment configuration protected by filesystem permissions. No key = no API calls. Cloud actions are behind the approval checkbox.

## 6. Upgrade and troubleshooting

```bash
cd ~/apps/Story2KDP_Studio
git pull --ff-only
source .venv/bin/activate
python -m pip install -e '.[web,dev]'
pytest -q
```

- `ModuleNotFoundError`: ensure the venv is activated and installation succeeded.
- Browser inaccessible: verify the Streamlit process and SSH tunnel, and address/port values.
- Out of memory: terminate optional diffusion worker, check `free -h`, avoid other heavy processes.
- Overlong manuscript: split scenes or increase book page count; the planner raises an explicit error.
- PDF rendering error: shorten page copy; standard Helvetica has limited non-Latin coverage.
- `400`/`401` API response: check the provider model identifier and key, as models and endpoints can change.

## 7. Feedback to collect

Record OS version, CPU model, RAM/swap, Python version, command run, screenshot or output snippet (without keys), elapsed time, peak RSS memory, generated-art quality, and detailed reproduction steps. Open a GitHub issue with the observations. Do not upload private manuscripts without permission.

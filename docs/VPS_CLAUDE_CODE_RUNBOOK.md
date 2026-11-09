# Ubuntu VPS + Claude Code: implementation runbook

## 0. Assumptions
Intel x86_64 Ubuntu VPS, 8 GB RAM, no NVIDIA GPU. SSH access and GitHub authorization are configured on the VPS. Choose Claude Code plan/approval workflow according to its current official documentation. Do **not** give Claude unrestricted permissions; require review of shell/network changes. Do not paste API tokens into the repository or chat.

## 1. SSH and system inventory
```bash
ssh ubuntu@YOUR_VPS_IP
cat /etc/os-release
lscpu | grep -E 'Model name|Architecture|CPU\(s\)'
free -h
df -h
python3 --version
```
Record results in a private environment log, not issues if they include account-identifying details. Ensure sufficient free disk for dependencies and possible models; do not install a diffusion model yet.

## 2. Clone the development branch
```bash
git clone -b feat/local-first-mvp https://github.com/maheshwaripn/Story2KDP_Studio.git
cd Story2KDP_Studio
git status --short
git rev-parse HEAD
```
Your working tree must be clean. If PR #1 has been merged, use the default branch instead.

## 3. Initial test and baseline
```bash
bash scripts/bootstrap_ubuntu.sh
source .venv/bin/activate
python -m pytest -q
python -m compileall story2kdp app.py
```
Follow README for the first sample CLI export. Record every actual error and exact version; do not assume a passing CI means the VPS works. App listens privately:
```bash
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```
From your own computer: `ssh -L 8501:127.0.0.1:8501 ubuntu@YOUR_VPS_IP` and visit http://localhost:8501.

## 4. Start Claude Code from the repository root
Install/authenticate Claude Code using **official current Anthropic documentation**, not an unverified third-party installer. Start it from the repository directory so `CLAUDE.md` is discovered. Ask it to read docs first.

### Suggested first prompt (copy into Claude Code)
```text
You are implementing Story2KDP Studio in this repository. Read CLAUDE.md,
README.md, docs/PRODUCT_REQUIREMENTS.md, docs/IMPLEMENTATION_BACKLOG.md,
docs/ACCEPTANCE_TESTS.md, docs/SECURITY_AND_PRIVACY.md and
docs/VPS_CLAUDE_CODE_RUNBOOK.md. Do not treat the roadmap as completed work.
Start ONLY with P0-01. Inspect code and run baseline tests; capture Ubuntu,
CPU, RAM and dependency facts; implement missing doctor/acceptance smoke tests,
fix verified setup defects, update docs, and run tests. Do not download AI
model weights, spend API credits, expose Streamlit publicly, or modify main.
Work in a feature branch, create a PR, and report exact results/blockers.
```

### Subsequent sessions
Use one task ID at a time, e.g. `Implement P0-02 from docs/IMPLEMENTATION_BACKLOG.md, with tests and docs. Do not expand scope.`

## 5. Git workflow
```bash
git checkout feat/local-first-mvp
git pull --ff-only
git switch -c feat/p0-01-vps-validation
# work/test/inspect
git diff --check
git status
git add <specific files>
git commit -m "test: verify Ubuntu acceptance and hardware diagnosis"
git push -u origin feat/p0-01-vps-validation
```
Open a PR targeting the current development branch; examine diff, secrets, dependency changes, CI checks and exact tests before merging. Do not merge anything based only on an agent summary.

## 6. Agent guardrails
- Allow reads, tests and local edits in repo; ask approval for installs, networking, model downloads, spending, deleting files, migrations or deploy changes.
- No `curl | bash` from unknown sources, no broad sudo or unreviewed rm commands, no secret printing.
- Distinguish prompts for OpenAI/Claude/Gemini APIs inside the *product* from Claude Code as a developer. Running Claude Code itself can incur its own usage costs, independent of the book app.
- Prefer a separate 8 GB RAM model benchmark only after baseline is stable. Stop if memory safety is uncertain.
- Store real manuscript projects in non-tracked paths; validate that `.gitignore` prevents accidental publishing.

## 7. Report format after each PR
Branch/commit, task ID, files changed, exact shell commands, test count/exit codes, screenshots or sample PDF, measured RAM/time if applicable, failures, risks, manual check needed, and next task ID. Include links to GitHub PR/issues, never API secrets.

## Permanent free-all-features direction
The product owner explicitly requires one free edition with every feature accessible and no subscriptions, paid feature locks or mandatory paid provider. Claude Code must read [FREE_FIRST_POLICY.md](FREE_FIRST_POLICY.md) and [FREE_FEATURE_MATRIX.md](FREE_FEATURE_MATRIX.md), and include the no-charge implementation path in every task. Running Claude Code itself may cost money independently of Story2KDP Studio, and the existing 8 GB CPU VPS may not run a powerful image model. Never install paid-only fonts, model licenses or external dependencies.

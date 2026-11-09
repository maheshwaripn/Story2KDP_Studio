#!/usr/bin/env bash
# Offline CLI acceptance test. Creates synthetic content in a temporary directory.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
printf 'A kind child saw a small sparrow.\n\nThe child offered a bowl of clean water.\n' > "$tmp/story.txt"
python -m story2kdp.cli init "$tmp/story.txt" --title "Offline Acceptance Book" --author "Synthetic Test" --pages 32 --out "$tmp/book"
python -m story2kdp.cli concept "$tmp/book" scene-001
python -m story2kdp.cli review "$tmp/book" > "$tmp/review.json"
python -m story2kdp.cli export "$tmp/book"
python - "$tmp/book" <<'PY'
import json
import sys
from pathlib import Path
import fitz

folder = Path(sys.argv[1])
with fitz.open(folder / "output" / "interior.pdf") as doc:
    assert len(doc) == 32, f"Expected 32 pages, got {len(doc)}"
    assert all(abs(p.rect.width - 621) < 1 and abs(p.rect.height - 630) < 1 for p in doc)
assert (folder / "output" / "cover-design-proof.pdf").is_file()
assert (folder / "output" / "preflight.json").is_file()
issues = json.loads((folder / "output" / "preflight.json").read_text(encoding="utf-8"))
assert any(i["code"] == "KDP_FINAL" for i in issues), "Proof output must retain KDP_FINAL warning"
print("PASS: offline sample import, concept, review, 32-page PDF and proof-only preflight")
PY

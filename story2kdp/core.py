"""Deterministic manuscript planning and durable, editable JSON project files."""
from __future__ import annotations
import json
import re
import uuid
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from docx import Document

STYLE = ("Original hand-painted family-friendly animated picture-book aesthetic; "
         "smooth organic contours, gentle warm light, expressive kind faces, "
         "harmonious soft greens, sky blues, warm peaches; no text in illustration. "
         "New character designs unique to this book; maintain approved references.")

def read_manuscript(path: str | Path) -> str:
    file = Path(path)
    if file.suffix.lower() in (".txt", ".md"):
        return file.read_text(encoding="utf-8-sig").strip()
    if file.suffix.lower() == ".docx":
        doc = Document(str(file))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()
    raise ValueError("Supported manuscript formats: .txt, .md, .docx")

def segment(text: str, max_chars: int = 370) -> list[str]:
    """Preserve paragraphs, split long paragraphs into sentence-sized page chunks."""
    if not text.strip():
        raise ValueError("Manuscript is empty")
    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    output: list[str] = []
    for part in parts:
        sentences = re.split(r"(?<=[.!?])\s+", part)
        block = ""
        for sentence in sentences:
            if len(block) + len(sentence) + 1 > max_chars and block:
                output.append(block.strip()); block = ""
            if len(sentence) > max_chars:
                if block: output.append(block.strip()); block = ""
                for start in range(0, len(sentence), max_chars):
                    output.append(sentence[start:start + max_chars].strip())
            else:
                block = (block + " " + sentence).strip()
        if block: output.append(block)
    return output

def build_project(text: str, title: str, author: str = "", pages: int = 32) -> dict[str, Any]:
    if pages < 24 or pages % 2:
        raise ValueError("For this paperback preset, pages must be an even number >= 24")
    scenes = segment(text)
    if len(scenes) > pages - 4:
        raise ValueError(f"{len(scenes)} scene chunks exceed {pages - 4} interior story slots. Choose more pages or edit text.")
    return {
        "schema_version": 1, "id": str(uuid.uuid4()), "title": title.strip() or "Untitled Story",
        "author": author, "style": STYLE, "trim_inches": [8.5, 8.5], "bleed": True,
        "page_count": pages, "print_mode": "premium_color", "characters": [],
        "status": "draft", "scenes": [
            {"id": f"scene-{i:03d}", "page": i + 3, "text": scene,
             "visual_prompt": f"Illustrate this story moment: {scene}. {STYLE}",
             "image": None, "approved": False, "review": []}
            for i, scene in enumerate(scenes, 1)],
        "approval_gates": {"manuscript": False, "characters": False,
                           "storyboard": False, "artwork": False, "print": False}
    }

def save_project(project: dict[str, Any], directory: str | Path) -> Path:
    folder = Path(directory)
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "project.json"
    # Preserve the last saved state before every modification. Historical
    # snapshots are private local project data and remain out of Git.
    if target.is_symlink():
        raise ValueError("Refusing to overwrite a symlinked project.json")
    if target.exists():
        revisions = folder / "revisions"
        revisions.mkdir(exist_ok=True)
        if revisions.is_symlink():
            raise ValueError("Refusing to write to a symlinked revision directory")
        snapshot = revisions / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid.uuid4().hex[:8] + ".json")
        snapshot.write_bytes(target.read_bytes())
    temp = folder / ("project-" + uuid.uuid4().hex + ".tmp")
    try:
        with temp.open("x", encoding="utf-8") as handle:
            json.dump(project, handle, indent=2, ensure_ascii=False)
            handle.flush()
            os.fsync(handle.fileno())
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)
    (folder / "images").mkdir(exist_ok=True)
    (folder / "output").mkdir(exist_ok=True)
    return target

def load_project(directory: str | Path) -> dict[str, Any]:
    return json.loads((Path(directory) / "project.json").read_text(encoding="utf-8"))

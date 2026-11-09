"""Deterministic review. Rules cannot certify artistic or developmental quality."""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageStat


def review_project(project: dict, directory: str | Path) -> list[dict]:
    base = Path(directory).resolve()
    issues: list[dict] = []
    def add(level, code, message, scene=None):
        issues.append({"severity": level, "code": code, "message": message, "scene": scene})
    if not project.get("title", "").strip(): add("error", "TITLE", "Missing book title")
    scenes = project.get("scenes", [])
    if not scenes: add("error", "EMPTY", "No story scenes")
    if len(scenes) > project.get("page_count", 0) - 4:
        add("error", "PAGES", "Not enough page slots for scenes")
    if not project.get("characters"):
        add("warning", "CHARACTERS", "No approved character reference records")
    for scene in scenes:
        sid = scene.get("id", "unknown")
        if len(scene.get("text", "")) > 500:
            add("warning", "DENSE_TEXT", "Long scene may be hard to typeset", sid)
        if not scene.get("approved"):
            add("warning", "UNAPPROVED", "Scene has not been approved", sid)
        name = scene.get("image")
        if not name:
            add("warning", "MISSING_ART", "Scene has no assigned illustration", sid)
            continue
        path = (base / name).resolve()
        if not path.is_relative_to(base):
            add("error", "UNSAFE_IMAGE_PATH", "Illustration path escapes project folder", sid)
            continue
        if not path.is_file():
            add("error", "IMAGE_NOT_FOUND", f"Missing image: {name}", sid)
            continue
        try:
            with Image.open(path) as im:
                w, h = im.size
                if min(w, h) < 1800:
                    add("warning", "LOW_RES", f"Illustration only {w}x{h}; full-page print target approx 2600px", sid)
                if im.mode in ("RGB", "RGBA"):
                    means = ImageStat.Stat(im.convert("RGB")).mean
                    if max(means) < 45:
                        add("info", "DARK", "Very dark image; inspect emotional tone and print", sid)
        except Exception as exc:
            add("error", "BAD_IMAGE", str(exc), sid)
    return issues

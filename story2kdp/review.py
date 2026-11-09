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
    seen_ids, seen_pages = set(), set()
    for scene in scenes:
        sid, page = scene.get("id"), scene.get("page")
        if sid in seen_ids:
            add("error", "DUPLICATE_SCENE_ID", f"Duplicate scene identifier: {sid}", sid)
        seen_ids.add(sid)
        if page in seen_pages:
            add("error", "DUPLICATE_PAGE", f"Multiple scenes assigned to page {page}", sid)
        seen_pages.add(page)
        if not isinstance(page, int) or isinstance(page, bool) or page < 1 or page > project.get("page_count", 0):
            add("error", "INVALID_PAGE", f"Scene page is outside the book: {page}", sid)
        copy = scene.get("text", "")
        if "TODO" in copy.upper() or "[INSERT" in copy.upper():
            add("warning", "PLACEHOLDER_TEXT", "Scene text contains an unfinished placeholder", sid)
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
                # MVP art box is 80% of a 8.625 x 8.75-in page,
                # preserving aspect ratio via letterboxing (not cropping).
                target_w, target_h = 8.625 * .80, 8.75 * .62
                scale = min(target_w / w, target_h / h)
                effective_dpi = 1 / scale
                if effective_dpi < 300:
                    add("warning", "LOW_RES", f"Illustration {w}x{h} is approx {effective_dpi:.0f} effective DPI at current layout; target 300 DPI", sid)
                if im.mode in ("RGB", "RGBA"):
                    means = ImageStat.Stat(im.convert("RGB")).mean
                    if max(means) < 45:
                        add("info", "DARK", "Very dark image; inspect emotional tone and print", sid)
        except Exception as exc:
            add("error", "BAD_IMAGE", str(exc), sid)
    return issues

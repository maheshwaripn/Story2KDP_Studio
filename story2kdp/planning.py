"""Lossless (at the parsed-chunk level), deterministic scene grouping."""
from __future__ import annotations


def group_scene_chunks(chunks: list[str], target_scenes: int) -> list[str]:
    """Distribute consecutive parsed chunks among the requested story scenes.

    Keeps the exact content and order of each input chunk. Joining with blank
    lines is a layout grouping, not rewriting, shortening, or summarizing.
    """
    if not chunks or any(not isinstance(chunk, str) or not chunk.strip() for chunk in chunks):
        raise ValueError("Supply non-empty manuscript chunks")
    if not isinstance(target_scenes, int) or not 1 <= target_scenes <= len(chunks):
        raise ValueError("Target scene count must be between 1 and chunk count")
    quotient, remainder = divmod(len(chunks), target_scenes)
    result: list[str] = []
    offset = 0
    for index in range(target_scenes):
        size = quotient + (1 if index < remainder else 0)
        result.append("\n\n".join(chunks[offset:offset + size]))
        offset += size
    return result

import json
import pytest
from story2kdp.core import build_project,save_project,load_project,segment
from story2kdp.planning import group_scene_chunks
from story2kdp.illustration import concept_art
from story2kdp.review import review_project
from story2kdp.publishing import interior_pdf,proof_cover,preflight_pdf
import fitz

def test_segment_and_roundtrip(tmp_path):
    project=build_project("The morning was bright.\n\nA bird asked for water.","A New Bird",pages=24)
    assert len(project["scenes"])==2
    save_project(project,tmp_path)
    assert load_project(tmp_path)["title"]=="A New Bird"

def test_empty_and_excess():
    with pytest.raises(ValueError):segment("")
    with pytest.raises(ValueError):build_project("Text","x",pages=23)
    with pytest.raises(ValueError):build_project("\n\n".join("Sentence." for _ in range(40)),"x",pages=24)

def test_concept_and_pdf(tmp_path):
    p=build_project("A kind child saw a bird.","Kind Child",author="A Writer",pages=24)
    save_project(p,tmp_path)
    concept_art(p["scenes"][0]["visual_prompt"],tmp_path/"images/scene-001.png",256)
    p["scenes"][0]["image"]="images/scene-001.png"
    save_project(p,tmp_path)
    warnings=review_project(p,tmp_path)
    assert any(i["code"]=="LOW_RES" for i in warnings)
    target=interior_pdf(p,tmp_path,tmp_path/"output/interior.pdf")
    proof_cover(p,tmp_path/"output/proof.pdf")
    with fitz.open(target) as doc:
        assert len(doc)==24
        assert abs(doc[0].rect.width-621)<1
        assert abs(doc[0].rect.height-630)<1
    assert not any(i["severity"]=="error" for i in preflight_pdf(target,p))

def test_reject_escape(tmp_path):
    p=build_project("Hello bird.","Title")
    p["scenes"][0]["image"]="../../secrets.png"
    assert any(i["code"]=="UNSAFE_IMAGE_PATH" for i in review_project(p,tmp_path))


def test_save_preserves_previous_versions(tmp_path):
    p = build_project("A bird sat on a fence.", "First Version")
    save_project(p, tmp_path)
    p["title"] = "Second Version"
    save_project(p, tmp_path)
    snapshots = list((tmp_path / "revisions").glob("*.json"))
    assert len(snapshots) == 1
    assert json.loads(snapshots[0].read_text(encoding="utf-8"))["title"] == "First Version"
    assert load_project(tmp_path)["title"] == "Second Version"

def test_save_rejects_symlinked_target(tmp_path):
    outside = tmp_path / "outside.json"
    outside.write_text('{"title":"Protected"}')
    project_dir = tmp_path / "book"
    project_dir.mkdir()
    (project_dir / "project.json").symlink_to(outside)
    with pytest.raises(ValueError, match="symlink"):
        save_project(build_project("Hello.", "Book"), project_dir)
    assert outside.read_text() == '{"title":"Protected"}'

def test_review_identifies_duplicate_page_scene_and_placeholders(tmp_path):
    p = build_project("A bird sang." + chr(10) + chr(10) + "A girl replied.", "Continuity", pages=24)
    p["scenes"][1]["page"] = p["scenes"][0]["page"]
    p["scenes"][1]["id"] = p["scenes"][0]["id"]
    p["scenes"][1]["text"] = "TODO: finish the ending"
    codes = {issue["code"] for issue in review_project(p, tmp_path)}
    assert {"DUPLICATE_SCENE_ID", "DUPLICATE_PAGE", "PLACEHOLDER_TEXT"} <= codes


def test_paid_provider_disabled_even_with_approval_and_key(monkeypatch, tmp_path):
    from story2kdp.providers import ProviderError, text_task, paid_api_enabled
    import requests
    monkeypatch.delenv("STORY2KDP_ENABLE_PAID_APIS", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "DO_NOT_USE")
    def forbidden_request(*args, **kwargs):
        raise AssertionError("No external request may occur in free-default mode")
    monkeypatch.setattr(requests, "post", forbidden_request)
    assert paid_api_enabled() is False
    with pytest.raises(ProviderError, match="disabled by default"):
        text_task("openai", "Synthetic story", tmp_path / "cache", approve_paid_request=True)
    assert not (tmp_path / "cache").exists()

def test_auto_group_long_manuscript_preserves_all_chunks():
    text="\n\n".join(f"Scene paragraph {i}. The story continues." for i in range(179))
    chunks=segment(text)
    assert len(chunks)==179
    grouped=group_scene_chunks(chunks,28)
    assert len(grouped)==28
    assert [part for scene in grouped for part in scene.split("\n\n")]==chunks
    project=build_project(text,"Long manuscript",pages=32,scene_chunks=grouped)
    assert len(project["scenes"])==28
    assert project["scenes"][0]["page"]==4
    assert project["scenes"][-1]["page"]==31

def test_group_input_validation():
    with pytest.raises(ValueError):
        group_scene_chunks([],28)
    with pytest.raises(ValueError):
        group_scene_chunks(["Hello"],0)
    with pytest.raises(ValueError):
        group_scene_chunks(["Hello"],2)
    with pytest.raises(ValueError):
        build_project("Hello","Book",scene_chunks=[""])

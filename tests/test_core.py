import json
import pytest
from story2kdp.core import build_project,save_project,load_project,segment
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

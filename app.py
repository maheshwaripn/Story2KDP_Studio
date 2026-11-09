"""Streamlit frontend. Run with: streamlit run app.py"""
from pathlib import Path
import json
import uuid
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import streamlit as st
from story2kdp.core import read_manuscript,build_project,save_project,load_project
from story2kdp.illustration import concept_art
from story2kdp.review import review_project
from story2kdp.publishing import interior_pdf,proof_cover,preflight_pdf
from story2kdp.providers import text_task,ProviderError

ROOT=Path("projects");ROOT.mkdir(exist_ok=True)
st.set_page_config(page_title="Story2KDP Studio",page_icon="📖",layout="wide")
st.title("📖 Story2KDP Studio")
st.caption("Local-first picture-book builder · offline core · paid AI calls are explicitly optional")
with st.sidebar:
    st.header("Projects")
    choices=sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p/"project.json").exists())
    selected=st.selectbox("Open project",["— Create new —"]+choices)
    st.info("Illustration concept mode is procedural draft artwork; commercial illustrations need an approved generation workflow.")
if selected=="— Create new —":
    st.subheader("Create a book")
    uploaded=st.file_uploader("Manuscript (.txt, .md or .docx)",type=["txt","md","docx"])
    title=st.text_input("Book title")
    author=st.text_input("Author")
    pages=st.selectbox("Pages",[24,32,40,48,64],index=1)
    slug=st.text_input("Project folder name","my-book")
    if st.button("Create project",type="primary"):
        if not uploaded or not title.strip():st.error("Supply a manuscript and title")
        elif not slug or not all(c.isalnum() or c in "-_" for c in slug):st.error("Use letters, digits, - or _ for the project folder")
        elif (ROOT/slug).exists():st.error("Folder already exists; select a new name")
        else:
            import tempfile
            with tempfile.TemporaryDirectory() as tmp:
                if uploaded.size > 4 * 1024 * 1024:
                    st.error("Manuscript exceeds 4 MiB upload limit")
                    st.stop()
                temp=Path(tmp)/("manuscript" + Path(uploaded.name).suffix.lower())
                temp.write_bytes(uploaded.getvalue())
                try:
                    project=build_project(read_manuscript(temp),title,author,pages)
                    save_project(project,ROOT/slug)
                    st.success(f"Created projects/{slug}; select it in the sidebar")
                except (ValueError,RuntimeError) as exc:st.error(str(exc))
    st.stop()
base=ROOT/selected
project=load_project(base)
tabs=st.tabs(["Storyboard","Illustrations","Review","AI Assistant","Export"])
with tabs[0]:
    st.subheader(project["title"])
    st.write(f"{len(project['scenes'])} scenes · {project['page_count']} pages")
    st.caption("Edit the story and prompts. Do not insert copyrighted prompts or unlicensed assets.")
    for i,scene in enumerate(project["scenes"]):
        with st.expander(f"Page {scene['page']} · {scene['id']}",expanded=i==0):
            scene["text"]=st.text_area("Page text",scene["text"],key=f"text{i}")
            scene["visual_prompt"]=st.text_area("Illustration prompt",scene["visual_prompt"],key=f"prompt{i}")
            scene["approved"]=st.checkbox("Approve scene",value=scene["approved"],key=f"approve{i}")
    characters=st.text_area("Character Bible (JSON array)",json.dumps(project.get("characters",[]),indent=2),height=160)
    if st.button("Save storyboard"):
        try:
            parsed=json.loads(characters)
            if not isinstance(parsed,list):raise ValueError("Characters must be a JSON array")
            project["characters"]=parsed
            save_project(project,base);st.success("Saved")
        except ValueError as exc:st.error(str(exc))
with tabs[1]:
    st.subheader("Generate or assign illustrations")
    st.warning("Procedural previews are not AI illustrations. OpenVINO diffusion is available through the CLI after optional model setup.")
    scene_id=st.selectbox("Scene",[s["id"] for s in project["scenes"]])
    scene=next(s for s in project["scenes"] if s["id"]==scene_id)
    if st.button("Generate offline concept preview"):
        relative=f"images/{scene_id}.png"
        concept_art(scene["visual_prompt"],base/relative)
        scene["image"]=relative;scene["approved"]=False
        save_project(project,base);st.success("Preview created. Review before approval.")
    replacement=st.file_uploader("Replace with your own or API-generated PNG/JPEG",type=["png","jpg","jpeg"])
    if replacement and st.button("Assign uploaded illustration"):
        try:
            # Never incorporate the client-provided filename into a project path.
            # Decode and re-encode uploaded images to discard unexpected payloads.
            if replacement.size > 30 * 1024 * 1024:
                raise ValueError("Image exceeds 30 MiB upload limit")
            raw = replacement.getvalue()
            with Image.open(BytesIO(raw)) as candidate:
                if candidate.format not in ("PNG", "JPEG"):
                    raise ValueError("Only genuine PNG/JPEG content is accepted")
                if candidate.width * candidate.height > 40_000_000:
                    raise ValueError("Image dimensions exceed 40 megapixels")
                validated = candidate.convert("RGB")
                validated.load()
            relative=f"images/{scene_id}-{uuid.uuid4().hex}.png"
            image_target=base/relative
            image_target.parent.mkdir(parents=True,exist_ok=True)
            validated.save(image_target, format="PNG")
            scene["image"]=relative;scene["approved"]=False
            save_project(project,base);st.success("Illustration assigned; previous image remains on disk")
        except (ValueError, OSError, UnidentifiedImageError) as exc:
            st.error(f"Invalid illustration: {exc}")
    if scene.get("image") and (base/scene["image"]).is_file():
        st.image(str(base/scene["image"]),width=410)
with tabs[2]:
    st.subheader("Quality review")
    issues=review_project(project,base)
    counts={level:sum(i["severity"]==level for i in issues) for level in ("error","warning","info")}
    st.write(counts)
    st.json(issues)
    st.caption("These are mechanical checks, not a substitute for human artistic, ethical, legal or child-development review.")
with tabs[3]:
    st.subheader("Optional paid text analysis")
    provider=st.selectbox("Provider",["openai","anthropic","gemini"])
    model=st.text_input("Model ID (blank uses adapter default)","")
    job=st.selectbox("Task",["Character Bible","Storyboard review","Literary edit","Age suitability review","Color/art direction review"])
    prompt=st.text_area("Exact request",f"Task: {job}. Book: {project['title']}. Scenes: "+json.dumps(project["scenes"],ensure_ascii=False)[:12000],height=240)
    st.warning("Costs vary by model. This MVP does not implement a hard financial budget or image-generation API. Never assume free requests.")
    approval=st.checkbox("I approve sending this manuscript material to this provider and accept possible API charges")
    if st.button("Run selected text task",disabled=not approval):
        try:st.text_area("Provider response",text_task(provider,prompt,base/"cache",model=model or None,approve_paid_request=True),height=300)
        except ProviderError as exc:st.error(str(exc))
with tabs[4]:
    st.subheader("KDP interior and proof")
    st.warning("Generated cover is DESIGN PROOF only. Do not submit it to KDP. The final wrap cover and final print review are not yet automated.")
    if st.button("Export interior PDF and proof"):
        try:
            out=base/"output"
            path=interior_pdf(project,base,out/"interior.pdf")
            proof_cover(project,out/"cover-design-proof.pdf")
            issues=review_project(project,base)+preflight_pdf(path,project)
            (out/"preflight.json").write_text(json.dumps(issues,indent=2))
            st.success("Created interior and proof. Inspect preflight findings and manual production checklist.")
        except Exception as exc:st.error(str(exc))
    for fname in ("interior.pdf","cover-design-proof.pdf","preflight.json"):
        p=base/"output"/fname
        if p.exists():st.download_button(f"Download {fname}",p.read_bytes(),file_name=fname)

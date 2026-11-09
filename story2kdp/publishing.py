"""Single-page picture-book PDF, proof cover, and conservative preflight."""
from __future__ import annotations
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
import fitz

PT = 72

def interior_pdf(project: dict, directory: str | Path, output: str | Path) -> Path:
    base = Path(directory).resolve()
    trim_w, trim_h = project.get("trim_inches", [8.5, 8.5])
    if (trim_w, trim_h) != (8.5, 8.5):
        raise ValueError("MVP supports 8.5 x 8.5 inch paperback only")
    bleed = bool(project.get("bleed", True))
    page_w = (trim_w + (.125 if bleed else 0))*PT
    page_h = (trim_h + (.25 if bleed else 0))*PT
    page_count = project["page_count"]
    target = Path(output); target.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(target), pagesize=(page_w,page_h), pageCompression=1)
    c.setTitle(project.get("title", "Story2KDP"))
    by_page = {s["page"]: s for s in project.get("scenes", [])}
    for page in range(1,page_count+1):
        c.setFillColor(HexColor("#F9F6ED")); c.rect(0,0,page_w,page_h,fill=1,stroke=0)
        scene = by_page.get(page)
        if page == 1:
            _fit_center(c, project.get("title", "Untitled"), page_w/2, page_h*.61, 27)
            _fit_center(c, project.get("author", ""), page_w/2, page_h*.47, 15)
        elif scene:
            img_name = scene.get("image")
            if img_name:
                img_path = (base / img_name).resolve()
                if not img_path.is_relative_to(base):
                    raise ValueError("Unsafe illustration path")
                if img_path.is_file():
                    with Image.open(img_path) as im:
                        image = im.convert("RGB")
                        # Letterbox to preserve the entire illustration; never silently crop artwork.
                        art_box = (page_w*.10,page_h*.29,page_w*.80,page_h*.62)
                        x,y,w,h = art_box
                        ratio = min(w/image.width,h/image.height)
                        iw,ih = image.width*ratio,image.height*ratio
                        c.drawImage(ImageReader(image),x+(w-iw)/2,y+(h-ih)/2,iw,ih)
            else:
                c.setFillColor(HexColor("#E1ECDD"))
                c.roundRect(page_w*.1,page_h*.29,page_w*.8,page_h*.62,12,fill=1,stroke=0)
                _fit_center(c,"ILLUSTRATION PENDING",page_w/2,page_h*.6,11)
            _draw_wrapped(c,scene.get("text", ""),page_w*.14,page_h*.245,page_w*.72,15)
        elif page == page_count:
            _fit_center(c,"The End",page_w/2,page_h*.55,27)
        c.showPage()
    c.save()
    return target

def _fit_center(c, text: str, x: float, y: float, size: int) -> None:
    while size > 9 and c.stringWidth(text,"Helvetica",size)>c._pagesize[0]*.8:
        size -= 1
    c.setFont("Helvetica",size); c.setFillColor(HexColor("#334A40"))
    c.drawCentredString(x,y,text)

def _draw_wrapped(c, text: str, x: float, y: float, max_width: float, size: int) -> None:
    # Explicitly fail on overflow instead of dropping text without notice.
    words = text.split(); lines=[]; line=""
    for word in words:
        proposal=(line+" "+word).strip()
        if c.stringWidth(proposal,"Helvetica",size)>max_width and line:
            lines.append(line);line=word
        else:line=proposal
    if line:lines.append(line)
    if len(lines)>8:
        raise ValueError("Text overflows allotted story area; edit or split the scene")
    c.setFillColor(HexColor("#334A40"));c.setFont("Helvetica",size)
    for i,line in enumerate(lines):
        c.drawString(x,y-i*size*1.4,line)

def proof_cover(project:dict,output:str|Path) -> Path:
    """Clearly labeled REVIEW PROOF; not a production cover or KDP upload asset."""
    target=Path(output);target.parent.mkdir(parents=True,exist_ok=True)
    w=h=8.5*PT
    c=canvas.Canvas(str(target),pagesize=(w,h))
    c.setFillColor(HexColor("#D9EADA"));c.rect(0,0,w,h,fill=1,stroke=0)
    _fit_center(c,project.get("title","Untitled"),w/2,h*.58,30)
    _fit_center(c,project.get("author", ""),w/2,h*.47,16)
    c.setFillColor(HexColor("#AA3344"));c.setFont("Helvetica-Bold",11)
    c.drawCentredString(w/2,h*.08,"DESIGN PROOF — NOT A KDP COVER")
    c.save()
    return target

def preflight_pdf(pdf:str|Path,project:dict) -> list[dict]:
    issues=[]
    with fitz.open(pdf) as doc:
        if len(doc)!=project["page_count"]:
            issues.append({"severity":"error","code":"PAGE_COUNT","message":f"Expected {project['page_count']} pages, got {len(doc)}"})
        bleed=project.get("bleed",True)
        exp_w=72*(8.5+(.125 if bleed else 0))
        exp_h=72*(8.5+(.25 if bleed else 0))
        for i,p in enumerate(doc):
            if abs(p.rect.width-exp_w)>1 or abs(p.rect.height-exp_h)>1:
                issues.append({"severity":"error","code":"PAGE_SIZE","message":f"Page {i+1} has incorrect media size"})
            for im in p.get_images(full=True):
                xref=im[0]
                pixels=doc.extract_image(xref)
                # Effective DPI depends on rendered placement; evaluated in manual final print check.
                if not pixels.get("image"):
                    issues.append({"severity":"error","code":"BAD_IMAGE","message":f"Page {i+1}: unreadable image"})
    issues.append({"severity":"warning","code":"KDP_FINAL","message":"Final KDP compliance requires current official template, embedded fonts, full-wrap cover, proofing and KDP Previewer."})
    return issues

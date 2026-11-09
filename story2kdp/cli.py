from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import read_manuscript,build_project,save_project,load_project
from .illustration import concept_art,openvino_sd15
from .review import review_project
from .publishing import interior_pdf,proof_cover,preflight_pdf

def main(argv=None):
    p=argparse.ArgumentParser(description="Story2KDP local-first publishing studio")
    sub=p.add_subparsers(dest="command",required=True)
    init=sub.add_parser("init",help="Create a new book project")
    init.add_argument("manuscript");init.add_argument("--title",required=True)
    init.add_argument("--author",default="");init.add_argument("--pages",type=int,default=32)
    init.add_argument("--out",default="projects/my-book")
    demo=sub.add_parser("concept",help="Generate offline procedural preview (not neural art)")
    demo.add_argument("project");demo.add_argument("scene_id")
    sd=sub.add_parser("diffuse",help="Run optional OpenVINO CPU image generation")
    sd.add_argument("project");sd.add_argument("scene_id");sd.add_argument("--model-dir",required=True)
    sd.add_argument("--size",type=int,default=384);sd.add_argument("--steps",type=int,default=15)
    for name in ("review","export"):
        z=sub.add_parser(name);z.add_argument("project")
    args=p.parse_args(argv)
    if args.command=="init":
        project=build_project(read_manuscript(args.manuscript),args.title,args.author,args.pages)
        print(save_project(project,args.out));return
    base=Path(args.project);project=load_project(base)
    if args.command in ("concept","diffuse"):
        scene=next((s for s in project["scenes"] if s["id"]==args.scene_id),None)
        if scene is None:p.error("Unknown scene ID")
        relative=f"images/{args.scene_id}.png";output=base/relative
        if args.command=="concept":concept_art(scene["visual_prompt"],output)
        else:openvino_sd15(scene["visual_prompt"],output,args.model_dir,args.size,args.steps)
        scene["image"]=relative;scene["approved"]=False
        save_project(project,base);print(output);return
    if args.command=="review":
        print(json.dumps(review_project(project,base),indent=2));return
    out=base/"output"
    interior_pdf(project,base,out/"interior.pdf")
    proof_cover(project,out/"cover-design-proof.pdf")
    findings=review_project(project,base)+preflight_pdf(out/"interior.pdf",project)
    (out/"preflight.json").write_text(json.dumps(findings,indent=2))
    print(f"Created {out/'interior.pdf'} and DESIGN PROOF. Review {out/'preflight.json'}")
if __name__=="__main__": main()

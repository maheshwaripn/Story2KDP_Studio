"""Offline original deterministic concept art plus optional OpenVINO generation."""
from __future__ import annotations
import hashlib
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


def concept_art(prompt: str, output: str | Path, size: int = 768) -> Path:
    """Generate new procedural *concept placeholder*, not a neural illustration."""
    rng = random.Random(int(hashlib.sha256(prompt.encode()).hexdigest()[:16], 16))
    image = Image.new("RGB", (size, size), (203, 230, 222))
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, size, size * 0.67), fill=(188, 224, 239))
    sun_x, sun_y = int(size * 0.75), int(size * 0.2)
    d.ellipse((sun_x-75, sun_y-75, sun_x+75, sun_y+75), fill=(255, 227, 162))
    for layer in range(5):
        y = int(size * (0.53 + layer * .075))
        color = (104+layer*9, 153+layer*6, 117+layer*4)
        pts = [(0, size), (0, y)]
        pts += [(int(size*x/12), int(y + 22*math.sin(x*.8 + layer))) for x in range(13)]
        pts.append((size, size))
        d.polygon(pts, fill=color)
    for _ in range(9):
        x = rng.randint(25, size-25); y = rng.randint(int(size*.45), int(size*.83))
        scale = rng.randint(22, 58)
        d.line((x, y, x, y-2*scale), fill=(96, 89, 62), width=7)
        d.ellipse((x-scale, y-3*scale, x+scale, y-scale), fill=(rng.randint(65,105),rng.randint(145,190),rng.randint(82,123)))
    # Unique procedural rounded character, deterministic per prompt.
    cx, cy = int(size*.5), int(size*.64)
    coat = (rng.randint(155,240), rng.randint(85,160), rng.randint(95,160))
    d.ellipse((cx-73,cy-110,cx+73,cy+65), fill=coat)
    d.ellipse((cx-64,cy-215,cx+64,cy-83), fill=(236,183,136))
    hair = (rng.randint(55,105), rng.randint(35,75),rng.randint(35,75))
    d.pieslice((cx-67,cy-225,cx+67,cy-82),180,357,fill=hair)
    for sign in (-1,1):
        x = cx+sign*23
        d.ellipse((x-5,cy-150,x+5,cy-141),fill=(48,48,55))
    d.arc((cx-18,cy-145,cx+18,cy-117),0,160,fill=(124,72,67),width=3)
    result = image.filter(ImageFilter.GaussianBlur(.6))
    target = Path(output); target.parent.mkdir(parents=True, exist_ok=True)
    result.save(target, format="PNG")
    return target


def openvino_sd15(prompt: str, output: str | Path, model_dir: str | Path,
                  size: int = 384, steps: int = 15) -> Path:
    """Optional CPU diffusion; only invoked explicitly, no download or conversion here."""
    if size not in (384, 512):
        raise ValueError("CPU preset supports 384 or 512 px")
    if not Path(model_dir).is_dir():
        raise FileNotFoundError("Provide a locally downloaded, compatible OpenVINO SD 1.5 model directory")
    try:
        from optimum.intel.openvino import OVStableDiffusionPipeline
    except ImportError as exc:
        raise RuntimeError("Install optional dependencies with pip install -e '.[intel]'") from exc
    pipeline = OVStableDiffusionPipeline.from_pretrained(str(model_dir), device="CPU", compile=True)
    result = pipeline(prompt, height=size, width=size, num_inference_steps=steps).images[0]
    path = Path(output); path.parent.mkdir(parents=True, exist_ok=True)
    result.save(path)
    del pipeline
    return path

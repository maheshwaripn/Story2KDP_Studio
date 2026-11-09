# Illustration strategy: originals, consistent characters, gentle hand-painted look

## Artistic direction

Create distinct characters per book. Use a **broad original hand-painted family animation aesthetic**: soft gradients, organic outlines, expressive kind faces, pleasant harmonious palettes, natural environments and reassuring lighting. Do not copy specific proprietary movie frames, trademarked characters, or artist signatures. A style brief alone cannot assure image consistency or originality.

## Working modes

1. **Offline procedural concept** (installed by default): `story2kdp concept projects/demo scene-001`. Creates an original deterministic, simple 2D preview from the prompt hash. It does **not** understand the story in detail and is not a neural illustration, and is not commercial final artwork.
2. **Offline OpenVINO Stable Diffusion 1.5** (experimental): install optional dependencies and supply an already-converted model directory. Test one small image on an 8 GB VPS; it may exhaust RAM or take many minutes. Review the model license carefully for commercial use. No model files are downloaded by the app.
3. **Uploaded final illustration**: upload your commissioned, licensed, externally generated or manually created image via the UI. The final image is referenced in project JSON and used in the draft interior PDF.

## Experimental OpenVINO mode

```bash
source .venv/bin/activate
pip install -e '.[intel]'
# Obtain/convert an OpenVINO-compatible SD1.5 pipeline on sufficiently equipped hardware,
# and copy the complete compatible model directory to the VPS (for example ~/models/sd15-openvino).
story2kdp diffuse projects/demo scene-001 --model-dir ~/models/sd15-openvino --size 384 --steps 15
```

Some supported model layouts expect specific precompiled shapes or Python package versions. This integration is not validated on your particular Intel CPU; a matching converted pipeline must be supplied. Start with a basic import smoke test, monitor `free -h`, and stop if memory exhausts. Not suitable for multiple parallel diffusion workers. Benchmark image time and quality before running a book batch.

## Character consistency (current and future)

Each book has a `characters` JSON array for visual references, color/wardrobe notes, expressions and approved versions. Save one main character reference per protagonist before rendering scenes. Current procedural previews do **not** condition on a character sheet, so **do not expect visual identity preservation**. Later implement img2img/control-conditioning or image-edit providers that accept reference imagery, plus separate review steps.

## Print quality

For an 8.5 inch interior at 300 DPI, full-frame imagery is around 2600 px per dimension. A native 384/512 px generated image is **not** suitable for final full-page print without quality evaluation. Pixel upscaling does not manufacture details; use high-resolution licensed outputs and inspect actual effective DPI. Current interior uses art inside page margins, not edge-to-edge bleed.

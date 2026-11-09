# Amazon KDP publishing checklist — current MVP and remaining work

**The current export is a drafting and proofing tool, not automatically upload-ready.** Review the current [KDP paperback formatting documentation](https://kdp.amazon.com/en_US/help/topic/G201834190), [cover calculator](https://kdp.amazon.com/cover-calculator) and [print previewer](https://kdp.amazon.com/en_US/help/topic/G202131400) at the time of publication.

## Interior dimensions (illustrative 8.5 x 8.5 paperback)

- Trim: 8.5 x 8.5 in.
- Bleed media size used by MVP: 8.625 x 8.75 in (outside bleed 0.125 in, vertical bleed 0.125 in each side).
- Typical target for full-frame print images: ~300 effective DPI. Check image placement, not metadata alone.
- Individual PDF pages, not double-page spreads.
- Production must support safe zones, odd/even gutter, page-count-specific interior margins, no unintended crop, embedded licensed fonts, final color proofing, and KDP Previewer checks.

## Current PDF limitation

The generated PDF is **not full-bleed in appearance**: the art is letterboxed within the page and a background color extends to the media edge. It must not be represented as a fully bleed-compliant final template without verification. The built-in `preflight_pdf()` checks page count and media size, but does **not** test every printing requirement. The basic Helvetica font may not support all languages or typography requirements.

## Production cover is NOT built yet

`cover-design-proof.pdf` is a separate, watermarked **front-cover design proof** only; it is **not** a KDP full-wrap back-spine-front cover. Actual KDP production requires paper-type-specific spine width, overall cover geometry, safe areas, barcode allocation, cover bleed and print PDF checks. Use KDP's official cover calculator/template and a separate approved cover workflow until support is implemented. Do not upload the proof file.

## Publishing review checklist

1. Choose paperback/paper/color/trim/bleed/page count in KDP and confirm that combination is currently supported.
2. Review actual image provenance, usage permissions, AI-generated content disclosures, authorship and manuscript rights.
3. Ensure all pages are intentional, texts fit comfortably and all planned illustrations are present.
4. Make sure all images are professionally reviewed at **effective printed resolution**; enlarge only with appropriate quality checks.
5. Verify precise gutter, odd/even safe margins, bleed, typography and embedded fonts.
6. Create a proper single-piece back/spine/front production cover from the official template (not the design proof).
7. Open the print PDF in KDP Print Previewer and fix errors; order/inspect a physical proof where applicable.

KDP's requirements may change. The provided checks do not guarantee acceptance.

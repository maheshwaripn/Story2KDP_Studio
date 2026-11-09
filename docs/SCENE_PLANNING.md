# Scene planning and long manuscripts

## Why the 179-chunk error occurs

The original Story2KDP import uses the deterministic `segment()` function, which divides paragraphs and long sentences into chunks of up to roughly 370 characters. On a 32-page preset, four pages are reserved for non-story content, leaving 28 scene/page slots. **179 input chunks cannot occupy 28 slots one-to-one.**

## Auto-group mode (free, offline)

1. Upload TXT, MD or DOCX, choose a page count and enter book metadata.
2. Select **Auto-group all text into story scenes**.
3. Choose the target story-scene count, from 1 through available slots.
4. Create the project; open Storyboard and edit page text and illustration prompts.
5. Review word density and exported proof before deciding whether to shorten prose, change the format, or expand the book.

Auto-group preserves all *parsed chunks*, their content and their order; the source manuscript is also saved in the local project JSON. It **does not** perform literary editing, AI summaries, semantic scene detection, automatic text-fitting, or professional illustration generation. Blank-line layout and whitespace may be normalized by the original segmentation method. In particular, grouping 179 chunks into 28 scenes often produces too much text for readable picture-book pages. The app warns about scenes over 120 words, but this is only a heuristic, not typography validation. **Always visually inspect the PDF.**

Use **Strict: one chunk per scene** to reproduce the original validation behavior. Existing CLI callers retain strict mode unless they supply explicit grouped scenes.

## Privacy, deployment and GitHub

Keep project files and manuscripts local to your VPS. The `projects/` folder must not be committed to GitHub. The repository contains the code and help docs; GitHub Pages can host static documentation, **not the Python Streamlit server**. Run Streamlit bound to `127.0.0.1` and access it through a restricted SSH tunnel; do not open port 8501 to the internet without adding authentication and deployment hardening.

## Current product limitations

- This is a manuscript-to-proof MVP, **not verified KDP-ready print production**.
- No local neural illustration model is required or installed by this feature.
- Commercial provider calls remain disabled by default.
- An editable drag-and-drop visual scene planner, reorder/merge UI, smarter semantic scene detection, automatic typography overflow checks, and professional print files remain future enhancements.

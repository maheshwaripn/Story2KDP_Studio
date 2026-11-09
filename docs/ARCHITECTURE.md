# Architecture and data flow

## Scope and principles

This is a local-first **modular monolith** suitable for Ubuntu VPS instances with Intel CPU and 8 GB RAM. Python handles manuscript segmentation, image assignment, mechanical reviews, and PDFs. Opt-in cloud providers are separate adapters. Each project resides in `projects/<slug>/` and holds its own `project.json`, `images/`, `output/` and optional `cache/`.

```
Streamlit / story2kdp CLI
    -> core.py (read, split, editable project JSON)
    -> illustration.py (offline procedural preview OR explicit OpenVINO)
    -> providers.py (explicitly approved outbound text API)
    -> review.py (mechanical and editorial warning lists)
    -> publishing.py (interior draft, proof cover, PyMuPDF checks)
```

## Core JSON contract

The `project.json` file contains `title`, `author`, `trim_inches`, `page_count`, `characters`, `scenes` and `approval_gates`. Each scene has `id`, `page`, `text`, `visual_prompt`, `image`, `approved` and `review`. Image values are relative project paths; avoid editing IDs once images are assigned. These are editable data, not generated model weights.

## Security, access and reliability

- Project slugs are validated in the UI. Never expose Streamlit without an authenticated reverse proxy or SSH tunnel. File import accepts manuscript formats only.
- API keys are read from environment variables; do not place them in project.json or Git.
- Provider requests are manual and no automatic retries are performed. Cache entries are keyed by provider, model and prompt; this cache contains manuscript/AI content and must be protected.
- Local image paths are validated to remain in the project directory before rendering/review.
- PDF rendering avoids silently cropping illustrations; oversize text raises an exception instead of being truncated.
- More rigorous authentication, database migrations, audit logs, job queue, error handling and financial limits are future work.

## Why not rely on CPU diffusion?

SD 1.5 is the smallest widely documented baseline, not a guarantee of viable inference on 8 GB RAM. On a small VPS, swap usage can make generation unacceptably slow. Production work should use already-created/licensed images or a separately implemented cloud generation adapter until benchmarks justify deployment.

## Future hardening

Move long image jobs into a one-worker process queue; add image reference conditioning, character sheet versioning, signed provider cost estimates, proper job cancellation, provenance metadata, independent per-page approvals, and change impact tracking. Do not claim image consistency is solved by prompt repetition alone.

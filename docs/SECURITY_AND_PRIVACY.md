# Security, privacy, publishing rights and API safety

## Threat model
Untrusted input: user-supplied manuscript/docx/images, file names, project metadata, AI prompts/outputs, provider responses and third-party models. Risks: path traversal, malicious image decompression, remote API data leakage, key exposure, prompt injection, unintended billing, DoS/OOM on 8 GB VPS, public interface takeover and licensing violations.

## Deployment
- Bind Streamlit only on `127.0.0.1:8501` and connect via SSH tunnel. No public 0.0.0.0 bind until reverse proxy + TLS + authentication + rate limits + CSRF/session assessment are implemented.
- Run as non-root account in dedicated working directory. Restrict home/project permissions; avoid committing `.env`, API keys, downloaded models, personal manuscripts or output books.
- Back up database and project files together; encrypt off-host backups where feasible. Test restore.
- Use systemd only after local service operation is verified; add MemoryMax, CPUQuota, RuntimeDirectory where appropriate. A large CPU model may exceed MemoryMax.
- Prefer known dependency hashes/lockfiles; do not execute arbitrary model-supplied code or `trust_remote_code` without review.

## API opt-in and budget
- Default deny outbound network inference. No API calls from opening a project or viewing a page.
- Show vendor/model/task, exact data shared, estimated cost, current spend, remaining cap, and explicit permission before request.
- Use environment/secret manager for keys; never print them, cache them, export them in JSON or share in screenshots.
- Separate text, vision and image-generation capabilities. Claude's ability to analyze images does not imply native image-generation API.
- For image generation, quote by provider-specific unit/resolution/model and reserve conservative spend *before* sending. If pricing unknown, disallow paid execution.
- Rate-limit, cap token/output/image counts, disable automatic paid retries by default; log request ID/cost only, not sensitive content.

## Project and asset validation
- Canonicalize and validate every read/write path under project root, reject symlink escapes and paths containing traversal.
- Check uploads by content and extension, hard file and pixel dimensions, parse errors and decompression bombs. Store under generated opaque IDs, not raw filenames.
- Make saved asset writes atomic; preserve versions on regeneration, not destructive overwrite.
- Treat AI-generated text as untrusted *content*, never instructions overriding tools/security or file access.
- Avoid content disclosure in CI logs and issue reports; use synthetic example fixtures.

## Publishing and image rights
- Record model ID, model artifact checksum, usage license, provenance, source reference and user-approved rights. Open weights do not automatically imply unrestricted commercialization.
- Style direction may be soft, hand-painted and optimistic; do not intentionally copy existing film characters or reproduce copyrighted scenes.
- Review current Amazon KDP print and AI-generated-content disclosure requirements before publication. KDP is final authority; auto preflight is advisory.

## Current v0.1 limitations
No UI authentication, no hard API budget enforcement, no full model sandboxing, incomplete production preflight and no audited third-party model license. The initial app is for trusted/private VPS use only.

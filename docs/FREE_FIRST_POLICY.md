# Story2KDP Studio — permanent FREE WITH ALL FEATURES policy

Status: **Owner-approved product requirement, 2026-11-09.** Applies to all future changes, versions and contributor PRs. This is a product policy, not a claim that every planned feature is currently implemented.

## Non-negotiable product model
1. One official, free-to-use open-source application edition with **all** features. No Pro, Creator Pro, Studio, freemium, SaaS unlock, monthly subscription, commercial license code, credit purchases, usage-trial expiry, watermarks on paid-only paths or mandatory authentication to billing.
2. Core workflow remains local-first. Every functional stage (manuscript creation/editing, character development, visual planning, asset creation/management, editorial review, print compliance, interior/cover exports) needs a **working no-charge path**, even when that path uses a manual review or externally authored/owned illustration.
3. No mandatory paid AI API or internet service. Commercial text/image APIs are optional adapters, **disabled by default**. The app must never invoke them because an API key is present; enabling one is a conscious user's decision and may result in provider fees. They may not be required to export a full book.
4. Never bundle model weights, fonts, images or templates lacking no-fee legally permitted use; document commercial publishing rights separately. Open-source program code does not automatically confer rights to all outputs.
5. No hidden usage metering, feature quotas, telemetry, manuscript uploads or advertising as prerequisites. Any opt-in network work must be transparent and consent-driven.
6. End-to-end free workflow and free-source licensing are release gates. For each planned feature, document an equivalent workflow (including manual assistance) and regression-test it without keys and without external requests.

## Free software versus zero total cost
- The application code is free under the repository's MIT license. MIT permits redistribution and commercial resale by third parties; it does **not** impose a no-resale or forever-free obligation on them. The maintainers' official distribution commitment is free and feature-complete.
- The user might still incur **Ubuntu VPS, computing, power, network, printing, KDP proof, font acquisition if chosen, or optional paid AI** costs. These are not software feature unlocks.
- Open-source CPU diffusion may require large weights and more RAM. On 8 GB RAM/no GPU, fully automatic, visually consistent, high-resolution professional artwork may be infeasible. No promise of equal neural quality to commercial providers.
- No-charge workflow fallback: original character/reference templates, manual drawing or authorized uploaded artwork, open-source postprocessing, human approval and free publishing validation.
- Do not imply generated images are automatically copyright-safe, legally licensed for commerce, or KDP-compliant.

## Engineering test of this policy
A fresh installation with **no cloud API keys, no internet access at runtime, no local diffusion model** must still import a manuscript, edit a page plan, enter or import an original character card, assign legal local artwork, run deterministic reviews, and generate available local book proofs. Future character continuity, advanced reviews and print exports must have similarly testable local/manual paths.

A user starting the product must not see any disabled feature because they lack payment. Feature availability can depend on local model/hardware/required authored inputs, with clear explanation and free fallback, not a checkout flow.

## Conflict resolution
If an external reviewer recommends monetization tiers or a paid image-generation dependency, reject that recommendation. Build the free/manual workflow first, then consider a separately optional provider adapter after transparent consent and budget checks. If a feature cannot be provided for free with current capabilities, mark it **NOT IMPLEMENTED**, not "premium".

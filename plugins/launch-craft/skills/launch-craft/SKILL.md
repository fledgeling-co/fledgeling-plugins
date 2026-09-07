---
name: launch-craft
description: >-
  Turn repository briefs, plans, code and mocks into traceable OVERVIEW.md and PRD.md documents, then an interactive launch site grounded in the actual product. Runs four phases: product synthesis, positioning and copy, implementation through design-craft:design-craft and ux-craft:ux-craft, and rendered acceptance. Uses the project's confirmed audience, pricing and supported platforms. Use for "build a launch site for this repo", "update the PRD and marketing website", or "turn these product briefs into a launch page".
---

# Launch craft

Deliver `OVERVIEW.md`, `PRD.md`, a feature-to-source trace matrix, and a working launch site in the project's existing site directory or the output path in the brief. Publishing is a separate action: carry it out when the user has authorized it, otherwise provide the local preview and files. A source file, mock or backlog entry establishes a different product state; keep those states distinct in both the PRD and public copy.

## Phase 1 — Project and backlog synthesis

1. Read the project's current overview, PRD, positioning and design decisions. Inventory briefs in `docs/features-to-triage/`, plans and specs, mocks, application code and manifests. Discover the actual paths when the repository uses another layout.
2. For every brief in scope, record its source path, feature ID, requirement and status. A mock proves a design exists; a plan proves intent; code plus relevant execution evidence supports an implemented claim. Do not turn a backlog request into a shipped feature.
3. Write `OVERVIEW.md` with the product purpose, architecture, stack, modules and key workflows. Write `PRD.md` with the audience, requirements and acceptance criteria. Preserve existing decisions unless the task authorizes changing them. Cite the source for each feature row and mark unknowns explicitly.

Use the user's chosen model division. For example, Opus 5 can own intake, triage and the accepted plan, Gemini 3.8 can implement from it, and GPT-6 can orchestrate. These are workflow roles, not API identifiers: obtain the exact model and effort settings from the current harness. An unavailable lane is a named limitation, never a reason to invent a model alias.

`scripts/run_synthesis.py --root <project> --dry-run` inventories conventional source paths. It does **not** read the source content, call a model, generate documents or prove completeness. Read and synthesize the inventory in the session or send the bounded task to an available runner. `references/synthesis-protocol.md` defines that handoff.

## Phase 2 — Positioning and copy

1. Read `docs/positioning/00-decision.md` and relevant territory documents when they exist. If positioning is missing and deciding it belongs to this request, use `positioning:positioning` with the product truth and the user's existing research budget. Otherwise carry an explicit positioning assumption into the draft.
2. Take audiences, prices, billing periods, entitlements and supported platforms from the brief or decision of record. Omit an unconfirmed price or label it as a proposal for review. Never infer an OS version, performance claim or lifetime entitlement from a mock.
3. Use `trawl:trawl` for an unresolved positioning or visual direction. Discover available reference-search tools and inspect useful sources; Mobbin is an optional source, not a required tool name to guess.
4. Draft copy with `create-luke-content:create-luke-content` when Luke's voice is requested or the established project voice. Otherwise follow the project's actual voice. Each headline and feature claim must be traceable to the product evidence.

Keep the claim decisions in `references/positioning-and-pricing.md`'s ledger shape. Reuse approved decisions rather than asking the same question at every phase.

## Phase 3 — Implement the launch site

Load `design-craft:design-craft` for visual direction and `ux-craft:ux-craft` for navigation, states and accessible controls. Reuse the existing stack and design system. Give the implementer a complete brief containing:

- the approved copy and claims, source paths and chosen direction;
- the output directory and files they own;
- the page sections, interactions and responsive states that actually belong to the brief;
- the acceptance commands and visual criteria;
- a return contract: changed files, preview command, checks performed and unresolved limits.

Use GSAP or Three.js when requested or when motion/3D explains the product. Name the behavior an interaction demonstrates; library presence is not an interaction. Keep a static fallback, working keyboard controls and reduced-motion behavior. Label simulated data as a demonstration. Add platform badges only for confirmed support. `references/site-craft-and-gsap.md` gives the implementation and acceptance criteria.

**Using Gemini?** Read `gemini.md` for task-specific calibration. Its Gemini 3.7-era measurements do not establish Gemini 3.8 limits or override the user's selected implementation lane. Preserve concrete artifact checks and apply model-specific routing only when the current model or an observed failure supports it.

## Phase 4 — Accept and deliver

1. Reconcile the feature inventory with the PRD: every in-scope brief has a requirement row or an explicit exclusion. Check that public claims match their recorded status and sources.
2. Run the project's relevant build or type checks. For a standalone HTML file, `scripts/validate_site.py <site-path>` performs a narrow source check; optional `--require-text` values come from approved copy. Its success does **not** prove WCAG compliance, supported platforms, loaded dependencies or working interactions.
3. Open the rendered site in an available, permitted browser. At the target desktop and mobile viewports, inspect the actual layout, fonts, images, contrast, focus and keyboard controls. Exercise each promised interaction and reduced-motion fallback. Record unavailable checks as unverified. Reuse design-gate evidence; after repairs, recheck the changed behavior and affected layout rather than restarting every review.
4. Deliver links to the documents, trace matrix and site, the preview command or URL, the acceptance result and any material limitation. Do not claim a deployed site until the deployment was authorized and the live URL was checked.

## References

- `references/synthesis-protocol.md`: evidence inputs, runner brief and document criteria.
- `references/positioning-and-pricing.md`: approved claim and commercial terms ledger.
- `references/site-craft-and-gsap.md`: interaction, motion and rendered acceptance.
- `references/evidence.md`: historical research and calibration; it is not a source of this project's product facts.

# Changelog

## 0.3.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

## 0.2.0 - 2026-08-27

- **Integrated `/positioning:positioning` Pipeline**: Phase 2 now actively audits `docs/positioning/` for `00-decision.md` or `10-territory-*.md`. If missing, it invokes the newly rebuilt `positioning` skill to run Dossier deep-research panels, claim-ledger truth binding, and produce the 9-document report suite before drafting copy.
- **Positioning-Grounded Copywriting**: Anchors Luke-voice copywriting and feature hero claims directly to the recommended territory from `docs/positioning/00-decision.md`.

## 0.1.0 - 2026-08-26

Initial release of `launch-craft`:

- **4-Phase Product Synthesis & Launch Pipeline**:
  1. Automated scanning of `docs/features-to-triage/*.md`, mock HTML, and application code, synthesizing into `OVERVIEW.md` and `PRD.md` using Gemini 3.7 Flash High via `agy`.
  2. Product positioning tailored for Home Network Administrators and Gamers, drawing UI patterns via Mobbin MCP, divergent hooks via `/trawl:trawl`, and authentic Luke Rhodes copywriting via `/create-luke-content:create-luke-content`.
  3. Dual-model pricing architecture ($9.99 perpetual BYOK/self-hosted vs $4.99/mo SaaS).
  4. Interactive marketing website generation via `/design-craft:design-craft` and `/ux-craft:ux-craft` utilizing GSAP animations, a Three.js 3D telemetry/topology hero canvas, interactive mock UI slices, and 5-platform badges (Windows, Mac, iPad, iPhone, Linux).
  5. Deterministic validation gates via `validate_site.py` enforcing WCAG contrast, em-dash elimination, and cross-platform presence.
- **Full Brand & Asset Suite**:
  - Telemetry Gantry icon across 1024, 256, 128 raster renders and layered SVG master.
  - 3200x1040 launch banner with linked web fonts and verified contrast.

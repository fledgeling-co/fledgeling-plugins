# Changelog

## 1.0.0 - 2026-11-23

First release, built through `create-skill:create-skill` from the MW4 Season 1 Field Guide production runs and a three-family cross-genre research pass.

- Nine-stage conductor in `skills/guide-craft/SKILL.md` (186 lines) backed by five reference playbooks: `cross-genre-apis-and-compliance.md`, `research-playbook.md`, `page-and-app-blueprints.md`, `polish-and-ship-playbook.md`, and `evidence.md`.
- Four-tier cross-genre data plane covering shooters, MOBAs, fighting games, CCGs, ARPGs, MMOs, extraction shooters, and sim racing: backend-proxied official APIs, client-side deck/build/loadout codecs and 60 Hz UDP telemetry, MediaWiki Cargo frame wikis, and clean-room editorial plus lab measurements.
- Four self-tested zero-dependency Python gate scripts (`check_html.py`, `audit_sources.py`, `check_briefing.py`, `check_compliance.py`) covering HTML validity, citation resolution and independent-publisher deduplication, Wilson confidence bounds, voice briefing payload caps and entity retention, and Apple Guideline 4.1(c)/4.2/5.2 plus nine-publisher IP rules.
- Three-family Phase 1 research corpus archived in `docs/deep-research/` (Gemini, Perplexity, xAI) with citation verification (`38/47` live URLs on xAI, `2` dead URLs caught and dropped on Perplexity).
- Seven cross-genre eval prompts with checkable assertions in `evals/evals.json`, including an adversarial Capcom monetisation and hitbox-overlay refusal case.
- Porcelain gel-glass icon (`Folio and season tab`, `assets/build_icon.py`, three engines, `audit.html` 11/12) and derived `3200x1040` banner (`assets/banner-src.html`, `banner-audit.html` 12/12).

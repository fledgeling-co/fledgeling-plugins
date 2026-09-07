<p align="center">
  <img src="assets/banner.png" alt="launch-craft: a porcelain icon of a telemetry gantry holding an amber-gilded multi-platform beacon, beside the wordmark and the line 'product synthesis and interactive launch conductor'" width="100%">
</p>

<h1 align="center"><img src="assets/icon-256.png" alt="" width="34" valign="middle" /> launch-craft</h1>

<p align="center"><strong>From raw project intelligence to PRDs and interactive launch sites.</strong><br />
Brief files and codebase in; traceable product documents and an interactive launch site out.</p>

<p align="center">
  <img alt="Version 0.3.3" src="https://img.shields.io/badge/version-0.3.3-D33C21">
  <img alt="Skill: launch conductor" src="https://img.shields.io/badge/skill-launch_conductor-434A55">
  <img alt="Phases: 4" src="https://img.shields.io/badge/phases-4-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## What it delivers

`launch-craft:launch-craft` turns briefs, plans, code and mocks into traceable `OVERVIEW.md` and `PRD.md` documents, a feature-to-source matrix, and a working launch site. Its four phases are synthesis, positioning and copy, implementation, and rendered acceptance.

The site uses the project's confirmed audience, prices, entitlements and supported platforms. Design routes through `design-craft:design-craft` and `ux-craft:ux-craft`; Luke-voice copy uses `create-luke-content:create-luke-content`. GSAP and Three.js are available techniques when motion or 3D belongs in the brief.

The pipeline preserves the user's model division, including Opus 5 planning, Gemini 3.8 implementation and GPT-6 orchestration, using identifiers supported by the current harness.

## Quick start

Run `/launch-craft:launch-craft` in the project and provide the intended launch audience, output location and any approved positioning or commercial decisions. Existing project context supplies the rest; unresolved facts stay explicit.

## Verification and limits

The inventory helper lists conventional brief, plan, spec and mock paths. It does not invoke a model or write the documents:

```bash
python3 plugins/launch-craft/skills/launch-craft/scripts/run_synthesis.py --root . --dry-run
```

The source checker can enforce approved text in standalone HTML:

```bash
python3 plugins/launch-craft/skills/launch-craft/scripts/validate_site.py launch.html --require-text "Approved product name"
```

Its exit code covers only the reported source checks. Browser inspection establishes layout, accessibility, dependency loading and interactions. The skill reports unverified checks and never invents shipped features, prices or support claims. Deployment follows the user's authorization.

## Install

```bash
/plugin add fledgeling-co/fledgeling-plugins
/plugin install launch-craft@fledgeling-plugins
```

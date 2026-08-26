# Changelog

## 1.12.0 - 2026-08-27

- **Positioning Audit & Integration**: The launch pipeline now checks for existing positioning documents in `docs/positioning/` (e.g. `00-decision.md` or `10-territory-*.md`) and invokes `/positioning:positioning` if absent, ensuring all product messaging and feature value propositions are evidence-grounded before drafting copy.
- **Initial Comprehensive Technical `PRD.md` Generation**: Added `PRD.md.tmpl` to template base and updated the launch pipeline (Phase O) to generate an initial comprehensive technical requirements document covering **ALL** briefs in `docs/features-to-triage/*.md` with complete feature traceability matrices, persona mappings, and non-functional requirements.
- **Enhanced `OVERVIEW.md` Architecture & Context**: Added structured Mermaid system architecture and direct grounding pointers to `docs/positioning/00-decision.md` and `docs/deep-research/`.

## 1.11.0 - 2026-08-22

- Initial launch pipeline and multi-platform scaffolding architecture.

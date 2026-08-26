# launch-craft, calibrated for Gemini

Read this once before executing `SKILL.md`. This file converts narrative standards into enumerated ledgers, file-gated milestones, and verified execution bounds.

## What transferred intact

- **The 4 distinct phases** — Document Synthesis, Positioning/Ideation/Copy, Site Crafting, Validation Gates.
- **Objective counts** — Exactly 5 platforms supported (Windows, Mac, iPad, iPhone, Linux), dual pricing tiers ($9.99 BYOK vs $4.99/mo), zero em-dash policy.
- **Deterministic verification commands** — `validate_site.py`, `check-conformance.mjs`, and schema validation.

## Override 1 — Execution Ledger

Complete every cell in this ledger during execution:

| Scope | Requirement | Verification Target | Status |
|---|---|---|---|
| Phase 1: Feature Briefs | Trace all `docs/features-to-triage/*.md` | Every brief ID/title present in `PRD.md` | Required |
| Phase 1: Overview Specs | Document stack, modules, architecture | `OVERVIEW.md` matches `package.json` / code | Required |
| Phase 2: Dual Pricing | $9.99 self-hosted vs $4.99/mo hosted | Exact prices in copy and comparison table | Required |
| Phase 2: Copywriting Voice | Luke Rhodes voice rules | 0 em dashes, marketing tone verified | Required |
| Phase 3: 5 Platforms | Windows, Mac, iPad, iPhone, Linux | 5 distinct platform badges and mock slices | Required |
| Phase 3: Three.js & GSAP | 3D Hero canvas + GSAP timelines | Canvas initialised + interactive mock slices | Required |
| Phase 4: Validation Gate | Script exit code | `validate_site.py` exits 0 | Required |

## Override 2 — Sequential File Gate Chain

Do not attempt to generate marketing HTML markup before the prerequisite documents exist:

```
Step 1: run_synthesis.py -> OVERVIEW.md & PRD.md
Step 2: /create-luke-content -> copy-draft.md
Step 3: /design-craft + /ux-craft -> launch-site.html
Step 4: validate_site.py launch-site.html (exit 0)
```

## Override 3 — Anti-Hallucination & Quote Verification

When invoking `gemini-3.7-flash-high` via `agy`, run with `--new-project` from `/tmp` to prevent cwd leakage:
```bash
perl -e 'alarm shift @ARGV; exec @ARGV' 900 agy --new-project --model gemini-3.7-flash-high -p "<prompt>" > /tmp/synthesis.md 2>/tmp/synthesis.log
```
Inspect `/tmp/synthesis.md` to confirm topic fidelity before writing `OVERVIEW.md` and `PRD.md`.

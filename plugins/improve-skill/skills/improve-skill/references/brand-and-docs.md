# Brand and docs — shipping the improved skill like a product

## The user checkpoints (hard gates, in this order)

1. **Name**: 3–4 candidates via AskUserQuestion, each with a one-line
   rationale, one marked recommended. Mine the marketplace's existing
   naming threads. The plugin directory is created/renamed only after
   the answer.
2. **Icon concepts**: 2–3 subject-mined directions described in words
   (register, glyph device, signature move) via AskUserQuestion. No
   icon or banner generation before the answer. The user chooses the
   concept, not just the rendering.

## Icon

Spawn an **Opus agent** that reads mac-design-studio's SKILL.md and
icon-directions.md (the hardened version: three engines are a floor —
under any budget cut iterations, never engines — and `audit.html` from
`assets/icon-audit-template.html` is a required on-disk deliverable).
The brief carries: the chosen concept, the sibling icons' registers to
avoid, the 16px survival requirement, retina audit renders, and NO git
operations. Expect: layered SVG master + Arrow vector take + raster
takes with corpus referenceImages (media-gen-pro), every take scored on
the sheet including losers, known liabilities stated.

## Banner

Composed HTML via design-craft with ux-craft's Read-mode lens — never a
generated image standing in for typography:

- The **real icon asset** beside a **set wordmark** (a deliberate,
  defensible font choice; never the model's default reach), one-line
  essence, subject-mined palette.
- `banner-src.html` kept in assets/ so it's editable forever; rendered
  via agent-browser at `viewport 1600 520 2` (verify 3200×1040), on a
  **port no sibling agent is using**.
- Look at the render before accepting it.

media-gen-pro is for imagery a design genuinely needs (icon engines,
scene art); diagrams are mermaid, natively rendered and maintainable —
never raster.

## README and EVALS.md

Both through **create-luke-content** (marketing persona over the base
voice), then `voice_lint.py --format marketing` until hard-checks clean.
The em-dash ban covers alt text, table cells, and the GitHub repo
description. Ground every claim in the built artifacts; numbers come
from the evals, never from enthusiasm.

Structure for a **non-technical reader**:

- README: banner, badges, the problem in plain words, how it works
  (one mermaid if it earns its place), install block, "does it actually
  work" told as report-card + blind-taste-test, a **succinct comparison
  table vs the original** near the top, credit to the original's
  authors by name, links into the deep material.
- EVALS.md: the deep half of the comparison — full tables, judge
  families and harnesses, costs, the flip story, caveats stated rather
  than buried.

## Root README and shipping

- Add the skill's row to the marketplace root README: icon (128px
  raster), description in the table's established voice, README link.
- Commit at checkpoints (skill built · evals graded · panel judged ·
  brand landed), push when pushing is in scope, update the portfolio
  manifest if the marketplace is tracked in one, and fix the GitHub
  repo description if the roster changed (`gh repo edit`).

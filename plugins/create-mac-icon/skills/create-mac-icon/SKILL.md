---
name: create-mac-icon
description: Create a macOS app icon end-to-end — direction chosen from a 532-icon corpus catalogue, subject-mined glyph, three generation engines (hand-authored layered SVG, Arrow vector, corpus-referenced raster), a written audit.html contact sheet, and a measured fidelity loop that iterates the SVG master against the winning raster reference until the material matches. Use whenever the user asks for a mac app icon, dock icon, macOS icon, app icon for a Mac tool, an icon "in the macOS style", asks to improve or iterate an existing icon against a reference image, or asks to make a vector icon look like a raster/generated one — including when they just say "make an icon for my app" on a Mac-adjacent project.
---

# Create Mac Icon

Design a macOS app icon that is **native to the platform** (correct era
grammar), **committed to one direction** (ownable), and — the part most
pipelines skip — **materially rich in the shipped vector master**, proven by
scoring it against a raster reference rather than by eyeballing it.

The whole skill exists because of one repeated observation: hand-authored
SVG masters win composition and 16px survival but lose *material* (volumetric
shading, lighting, translucency) to diffusion rasters at equal audit scores.
The fix is not "try harder" — it's a measured loop. Deep-research evidence
base: `docs/svg-icon-fidelity-plan.md` at the marketplace root.

## Knowledge sources

1. `references/icon-directions.md` — **read before designing.** The style
   catalogue from three corpora (134 macapp.supply digests, 500
   macosicongallery icons, 32 ground-truth macOS 26 captures): the Tahoe
   gel-glass grammar, 8 directions with palette/composition recipes, the
   direction picker, the 12-point rubric, the 26-device subject-mining bank,
   the anti-sameness rules, the failure-mode anti-checklist, and the
   three-engine pipeline spec.
2. `references/corpus/` — the evidence: `SYNTHESIS.md` (aggregate census +
   era fingerprints), `apple-2026.md` (the Tahoe answer key), and
   `apple-2026/` (32 ground-truth captures at 512px — the raster engine's
   `referenceImages`).
3. `references/fidelity-loop.md` — **read whenever a raster take wins the
   material judgment** (it usually does): the bounded render-score-edit loop
   that rebuilds the SVG master to match, and how its wins feed back into
   this skill.
4. `references/material-recipes.md` — raster looks as layered SVG
   constructions. Read during Engine A authoring and every loop material
   round; append to it when a loop confirms a new recipe.

## Procedure

1. **Brief.** The app's subject, personality (3 committed adjectives), brand
   colour constraints, and any raster reference the user already has. Ask
   only what's genuinely open.
2. **Direction + device** from `icon-directions.md`: era + direction (the
   catalogue is calibration, not a whitelist — hybrids and novel compositions
   are legitimate when the subject earns them; state choice + runner-up),
   then a subject-mined glyph device with a named signature move. Calibration
   warnings live in the reference: blue/indigo grounds and stock category
   glyphs need positive justification.
3. **Silhouette first.** The glyph as a solid shape that names the subject;
   mental 16px squint before any styling.
4. **The shared spec** (icon-directions.md § Generation pipeline, Step 0):
   1024 canvas, squircle-mask discipline (`assets/squircle-path.txt` is the
   exact path for masking raster takes), optical centring, one light model,
   ≤2 hue families, and the #10 layer plan (bg / mid / fg / highlight).
5. **Three engines — a floor, not a target.** Under any budget cut
   iterations, never engines; a missing engine is a named deviation the user
   agreed to.
   - **Engine A — hand-authored layered SVG** (always; the canonical master
     that ships). Author it through a build script — geometry and material
     as named constants, script emits the SVG — so later fidelity rounds are
     parameter edits, not path surgery. Apply `material-recipes.md` from the
     first draft; a master born flat starts the loop further behind.
   - **Engine B — media-gen-pro `generate_image` with `svg: true`** (Arrow):
     an independent vector take from the spec-as-brief; salvage winning
     shapes into the master.
   - **Engine C — media-gen-pro raster** (material-realism engine): 1-2
     takes, passing 2-4 same-register exemplars from
     `references/corpus/apple-2026/` as `referenceImages`. The raster is the
     material target, never the shipped master.
   - media-gen-pro unavailable → say so, widen Engine A to 2-3 genuinely
     different hand-authored takes.
6. **Audit — written, not narrated.** Render every take at 1024/128/32/16
   and write `audit.html` from `assets/icon-audit-template.html` (2× retina
   sources shown at half size, pixelated ×6 squint magnification, losers
   stay scored, recommendation names known liabilities). The 12-point rubric
   bar: ≥10/12, checks 1-4 non-negotiable. A commission without `audit.html`
   on disk is incomplete.
7. **The fidelity loop** (`references/fidelity-loop.md`) — when a raster
   take wins the material read, or the user supplies a reference to match:
   `scripts/fidelity.py` scores the master against the reference at five
   sizes (structure gate → score → Pareto gate per round), bounded rounds
   with one edit class each, until the gate stops accepting or the material
   gap closes. For judged rounds and shipping decisions the same reference
   describes `scripts/review_sheet.py` (a served, click-first human review
   page that writes feedback to disk) and `scripts/judge_panel.py` (a blind
   three-family model panel). Re-render the audit sheet with the final
   master. This step is what makes "rebuild the raster's material into the
   master" a measurement instead of a vibe.
8. **Deliver**: the layered SVG master (+ build script), the alternates, the
   audit sheet, the fidelity run directory, and — if the loop confirmed a new
   construction — the `material-recipes.md` addition, stated in the summary.

## Iterating an existing icon against a reference

When the ask is "make this icon look like that image" (no new commission),
skip to steps 4/7: normalise the reference, run `structure` + `score` for the
baseline, then loop. The same bounded schedule applies; the audit sheet at
the end shows before/after rows.

## Boundary conditions

- **mac-design-studio installed** (diolog-plugins): it covers full app-UI
  design and delegates icon work to the same pipeline this skill carries;
  for pure icon commissions this skill is the more complete tool (it adds
  the fidelity loop). Don't run both on one commission.
- **User has an existing brand mark:** re-materialise, never redraw
  (icon-directions device #19) — silhouette kept exactly, material swapped.
- **Asked to clone a specific app's icon:** decline; offer its direction
  family instead.
- **Trajectory data is a deliverable.** The loop's `runs/` directories are
  future training data (marketplace plan, Phase 4); leave them in the
  commission's working directory rather than cleaning them up.

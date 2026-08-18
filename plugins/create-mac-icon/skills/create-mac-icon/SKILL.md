---
name: create-mac-icon
description: >-
  Create a macOS app icon end-to-end — direction chosen from a 532-icon corpus catalogue, subject-mined glyph, three generation engines (hand-authored layered SVG, Arrow vector, corpus-referenced raster), a written audit.html contact sheet, and a measured fidelity loop that iterates the SVG master against the winning raster reference until the material matches. Use whenever the user asks for a mac app icon, dock icon, macOS icon, app icon for a Mac tool, an icon "in the macOS style", asks to improve or iterate an existing icon against a reference image, or asks to make a vector icon look like a raster/generated one — including when they just say "make an icon for my app" on a Mac-adjacent project.
---

# Create Mac Icon

Design a macOS app icon that is **native to the platform** (correct era
grammar), **committed to one direction** (ownable), and — the part most
pipelines skip — **materially rich in the shipped vector master**, proven by
scoring it against a raster reference rather than by eyeballing it.

The whole skill exists because of one repeated observation: hand-authored
SVG masters win composition and 16px survival but lose *material* (volumetric
shading, lighting, translucency) to diffusion rasters at equal audit scores.
The fix is not "try harder" — it's a measured loop.

**First, two quick exits.** If the request is empty, ask in one line what the
app is and what it does, then stop. If it is exactly one of `structure`,
`score`, `gate`, `check`, `render` or `iterate`, it is a subcommand or a
workflow name and not a brief — say which command you think they meant and
confirm. But **do not design an icon named "score"**: if what follows describes
something an icon could be *for* — a cashflow tracker, an export tool, a
pottery-studio booking app — it is a brief, so design it.

## Where a commission lands

Learn the anatomy before building it. Everything below sits in the commission
directory you were given:

```
icon.svg                  the layered master that ships (glob-required name)
build_icon.py             the generator: geometry + material as named constants
icon-<engine>-<id>.svg    the Arrow take
icon-<engine>-<id>.png    the raster take (+ -masked.png)
audit.html                the contact sheet — a gated deliverable, not a note
audit-renders/            <take>-{1024,256,128,96,64,32}.png
  render-manifest.json    what was rendered, from what, as what kind
loop-runs/rNN/            score.json · residual-1024.png · edges-{candidate,reference}.png
                          candidate-1024.png · reference-1024.png · brief.md
                          gate.txt · review.html · review-feedback.json · _before/
                          panel/{bundle/, bundle-swapped/, verdict-*.json, panel.json}
loop-runs/last-accepted/  the gate's rollback point
loop-runs/best-promoted/  the best take a blind panel ever preferred — what ships
```

**Reading the instruments at the shell.** Exit codes carry the severity: **0**
pass, **1** fail, **2 refused — a comparison that must not be made at all**,
which is not the same as one the candidate lost. `FAIL`, `NOTE` and `?` lines go
to **stderr** so redirecting stdout cannot lose them; measurements stay on
stdout. A clean exit does not mean there was nothing to read — a `NOTE` is a
real finding that did not rise to a refusal. Check `$?` itself, never a pipe's:
piping a gate through `grep` reports grep's status, and that is how a hard
failure has been read as a pass here before.

Deep-research evidence base for the loop's design:
`docs/svg-icon-fidelity-plan.md` and `docs/deep-research/` in the
**fledgeling-plugins repository** — these are not bundled in the installed
plugin, so cite them as provenance rather than sending a runner to open them.
The findings that changed this skill's own rules are restated in
`references/evidence.md`, which does ship.

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
5. `references/evidence.md` — **read before changing a gate threshold, the
   panel protocol, or the stopping rule.** What the outside literature
   establishes about perceptual metrics, blind pairwise judging and stopping
   under a noisy objective; where it contradicts a published rule this skill
   rejected; what a two-family panel can and cannot support; and which of this
   skill's numbers are transferred evidence rather than measured here.

## Procedure

0. **Look at the icons this one will sit beside — by default, without being
   asked.** An icon is never judged alone; it is judged in a Dock, a Finder
   list, or a marketplace lineup next to its siblings. Before the brief, read
   the repository you are adding to: any `CLAUDE.md` or brand doc for a stated
   icon family rule and the **required export sizes**, the existing
   `assets/icon*.png` set, whatever generator or `icon-src.svg` sits beside
   them, and `assets/squircle-path.txt`. Lift exact values — the accent's hex,
   the ground register, the corner geometry — rather than eyeballing or
   rounding them.

   This step exists because of a specific gap: for `fledgeling-plugins`, whose
   every icon this skill generates, the family rule and the export sizes (1024
   as `icon.png`, plus 256 and 128) are written in that repo's own `CLAUDE.md`,
   and the skill did not read them. Say in one line what you matched
   ("matching the fledgeling set — porcelain ground, one ember accent, shared
   squircle from `assets/squircle-path.txt`"). If a genuine search turns up no
   family and no palette, say that you looked and that you are setting the
   precedent.

1. **Brief.** The app's subject, personality (3 committed adjectives), brand
   colour constraints, and any raster reference the user already has. Ask
   only what's genuinely open.
2. **Direction + device** from `icon-directions.md`: era + direction (the
   catalogue is calibration, not a whitelist — hybrids and novel compositions
   are legitimate when the subject earns them; state choice + runner-up),
   then a subject-mined glyph device with a named signature move. Calibration
   warnings live in the reference: blue/indigo grounds and stock category
   glyphs need positive justification.

   **Settle the direction before spending the engine budget.** Three engines
   run against one direction, so a wrong direction costs the whole budget —
   while the decision itself only needs a shape. Where the direction is
   genuinely open, put 2-3 **low-fi silhouette sketches** in front of the user
   first: solid black glyph shapes at 128px, each exploring an axis you can
   name ("the ledger line" vs "the coin edge"), each with an honest motivation
   and its main tradeoff. Decision fidelity is not deliverable fidelity, and
   three shades of one idea is no choice at all. Step 3 already makes exactly
   this artifact; this is the same artifact used as a decision instrument
   instead of a private check. Once a direction is settled it stays settled —
   keep each option's name and identity stable across turns, and don't re-ask
   on a later turn.
3. **Silhouette first.** The glyph as a solid shape that names the subject;
   mental 16px squint before any styling.
4. **Look at real icons before authoring anything.** Open 4-6 exemplars from
   `references/corpus/apple-2026/` in the register you chose and *sample
   values out of them*: the ground's luminance range, where its brightest
   point sits relative to the key light, the accent's saturation, the hue of
   the darkest pixel in a shaded face, how the rim light is treated, how the
   contact shadow falls. Write those numbers into the spec.

   This step exists because the master that ships was, until it was added,
   built entirely from prose descriptions of what a macOS icon looks like.
   Reading *about* icons is not the same as looking at them, and every
   material failure this skill has recorded traces to an assumed
   relationship that a glance at the corpus would have corrected: shadows
   authored blue in a warm-lit scene, a curl drawn lighter than the ground
   when the reference draws it darker, a "highlight" that the reference does
   not have. The loop later catches these at roughly four rounds each. The
   corpus catches them for free, before the first line.

5. **The shared spec** (icon-directions.md § Generation pipeline, Step 0):
   1024 canvas, squircle-mask discipline (`assets/squircle-path.txt` is the
   exact path for masking raster takes), optical centring, one light model,
   ≤2 hue families, and the #10 layer plan (bg / mid / fg / highlight).
6. **Three engines — a floor, not a target.** Under any budget cut
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
7. **Audit — written, mechanically checked, and looked at.** Render every take
   and write `audit.html` from `assets/icon-audit-template.html` (2× retina
   sources shown at half size, pixelated ×6 squint magnification, losers stay
   scored, recommendation names known liabilities). The 12-point rubric bar:
   ≥10/12, checks 1-4 non-negotiable.

   Three steps, in this order, because the first two have each been skipped on
   a real commission and the third is what the sheet is *for*:

   ```bash
   python3 scripts/audit_sheet.py render <commission-dir>   # retina sources for every take
   #   ... write audit.html from the template ...
   python3 scripts/audit_sheet.py check  <commission-dir>   # must exit 0
   python3 scripts/fidelity.py structure --candidate icon.svg   # check runs this too
   ```

   `check` reads the sheet, resolves every `<img src>` against the directory, and
   fails on a missing image, an unfilled placeholder of **any** form, a missing
   master, a take short of its retina sources, or a hidden 1024 hero. It also
   refuses three things it used to pass silently, each measured:

   - **a stale sheet** — every render must be newer than the source it came
     from, because the fidelity loop *guarantees* the master changes after the
     sheet is first written, and a sheet showing the pre-loop icon beside a
     post-loop master used to pass cleanly;
   - **a sheet that has not met the bar** — a rubric score of the form
     `N / 12` must appear in each take's score cell and the best take must
     clear 10/12, so `check` proves the commission *passed* rather than merely
     that the sheet was populated;
   - **an unmasked raster** — a take rendered as kind `png` whose corners are
     opaque ships as a square tile beside squircle siblings, and only `render`
     knew the kind while only `check` saw the output. `render` now records both
     in `audit-renders/render-manifest.json` and `check` verifies against it.

   This is not ceremony: writing the file tells you nothing about whether its
   paths resolve, and a sheet whose images 404 is precisely the artifact that
   ships unseen. Twice on record the user asked *"why no audit.html? doesn't the
   skill say to create one?"* and *"I don't see any audit.html or the various
   icon versions"* — the instruction was already here both times, which is why
   it is now a command with an exit code.

   Then **open the sheet in a browser and read it.** `check` proves the files
   exist; only looking proves the icons are good. Ask each row *"what is wrong
   with this?"*, not *"is this done?"*

   **Sizes are retina pairs: 256 / 128 / 96 / 64 / 32 sources shown at 128 / 64
   / 48 / 32 / 16 css px**, plus the 1024 hero. The 48px row is there because a
   Finder list and a plugin marketplace tile render at it, and an icon that
   survives 128 and 16 can still collapse between them.

   **One silhouette across the set.** Every icon in a family, variant row, or
   marketplace lineup shares the same outer shape from
   `assets/squircle-path.txt`. A single icon whose corner radius or outline
   differs from its siblings reads as an error at every size; that has been
   caught by the user rather than by this pipeline.

   A commission without a passing `check` is incomplete — say which step is
   outstanding rather than reporting the icon done.
8. **The fidelity loop** (`references/fidelity-loop.md`) — when a raster
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

   **Two authority rules, both bought with wasted rounds.** The 12-point
   rubric outranks the gate: the reference can itself fail checks the master
   passes, so converging on it can drag the master below the floor. And the
   blind panel outranks a run of gate ACCEPTs: on one fixture the composite
   climbed 15% across eight consecutive rounds while the panel preferred the
   previous take in seven of them, crazing the ground and flattening a curl
   that had been measured correctly. `PANEL_VETO` now ends a fixture after
   three consecutive panel losses regardless of what the score says. A gate
   ACCEPT is evidence, never a verdict.

   **The gate refuses a degraded metric tier, in both paths.** LPIPS engages
   only at 256 and 1024 — exactly where material lives — so without torch the
   gate cannot see what it is grading and is confidently wrong rather than
   merely uncertain. Measured: eight rounds ran on the numpy-only tier, the
   composite went backwards at every size, and the gate accepted its way to the
   worst take of the run. `gate` exits **2** on a degraded tier;
   `--allow-degraded-tier` proceeds and records that the verdict covers
   structure and small-size legibility only.

   **Promote on the panel, stop on promotion-armed patience, ship the best-ever
   promoted take** — never the latest. On the improve-skill trace that ships r11
   over r19: the composite says r19 is 4% better and the judges say r11 is the
   artifact. Patience is two consecutive non-wins **armed only after the first
   promotion**; the naive form fires at r04, before all three of that run's
   genuine wins, and ships nothing the panel ever preferred. Every judge is
   asked in **both orders** (a swap-flip is recorded as a tie, not a winner),
   and the generator's own family — `claude`, since the round agent is
   `claude -p` — is recorded but excluded from the majority. Mechanism, effect
   sizes and citations: `references/fidelity-loop.md` and
   `references/evidence.md`.
9. **Deliver**: the layered SVG master (+ build script), the alternates, the
   audit sheet, the fidelity run directory, and — if the loop confirmed a new
   construction — the `material-recipes.md` addition, stated in the summary.

   **Say it in the user's words, not the instrument's.** This pipeline
   generates more mechanism vocabulary than anything else in the set, and it
   leaks into commit messages and handovers. Narrate the icon, not the harness:

   | Internal | What the user hears |
   |---|---|
   | composite / edge_f1 / SSIM / LPIPS / mask_iou | how close the master got to the reference |
   | the blind panel preferred the candidate | three independent judges picked the new one |
   | gate ACCEPT / REJECT / Pareto gate | the measurements agreed / disagreed it improved |
   | metric tier, degraded tier | never named — say the material could not be measured, so the number is not trustworthy |
   | PROVISIONAL, PANEL_VETO, r11, render_hash | never named — say it needs your eye, or that the loop stopped improving |

   The skill's most important claim has to survive that translation: *a gate
   ACCEPT is evidence, never a verdict* becomes "the measurements liked it,
   which is not the same as it being right — have a look."

## Targeted edits — a one-constant change is a one-constant change

"Make the accent warmer", "the shadow is too heavy", "lift the glyph a little"
are single named constants in the build script. Change that constant,
regenerate, re-render the affected rows, and say what moved. Do **not** open a
round schedule, a structure gate, a scorer and a three-model panel for a request
that named its own fix — the build-script discipline exists precisely so this
kind of edit is exact. Leave every other constant alone, including ones you
think could be better; finish what was asked and *suggest* the rest rather than
applying it. The loop is for closing a material gap against a reference, which
is a different job from honouring a stated preference.

## Known limits (so nothing gets promised that isn't there)

- **The loop measures similarity to a reference that can itself be wrong.** The
  raster engine routinely renders frost at ~1.4:1 figure-ground, which
  dissolves at 32px; converging on it drags the master below the rubric floor.
  That is why the rubric outranks the gate rather than the reverse.
- **Without torch, the gate is blind to material** (LPIPS runs only at 256 and
  1024). It now refuses rather than guessing — but the honest version of "we
  could not install torch" is that the material was never measured.
- **`self_contrast` catches gross collapse, not localised flattening.** On r01
  it did not fire (drops of 2.7% and 1.6%) because a whole-image spread is
  dominated by the tile ground rather than the object the judges were
  describing. The threshold was left at its principled value rather than tuned
  until it fired on one case, which would be exactly the metric-gaming this
  skill forbids implement agents. For object-level flattening the panel is the
  authority, and an undecidable case ships PROVISIONAL to a human queue.
- **A gate cannot see a self-consistent defect.** When a superseded agent's
  ~120 stray lines collided with its replacement, every gate said ACCEPT either
  way, because both versions were internally consistent. Only the agent caught it.
- **The panel is a handful of model calls and can be wrong,** and it is not a
  stand-in for a person: on r04, the one round carrying both signals, the human
  preferred the candidate and the panel the baseline. Two families cannot form a
  majority — `references/evidence.md` says what a two-family panel does and
  does not support.
- **`rsvg-convert` is the scoring renderer and it is not a browser.** A
  construct that renders differently across the two is itself a finding.
- **The stopping rule is ours, not the literature's.** Promotion-armed patience
  comes from one replayed trace; the published families it resembles arm after a
  fixed iteration count, not after a verified success. A production policy with
  a measurement behind it, not an established algorithm.

Don't promise past these.

## Iterating an existing icon against a reference

When the ask is "make this icon look like that image" (no new commission),
skip to steps 5/8: normalise the reference, run `structure` + `score` for the
baseline, then loop. The same bounded schedule applies; the audit sheet at
the end shows before/after rows.

## Boundary conditions

- **Know which of two things you are making, because they have opposite rules.**
  A *production Mac app icon* ships to Icon Composer, which owns blur, shadow,
  specular, translucency and the mask — Apple's own guidance is to leave them
  out, and a baked rounded mask damages system highlight rendering. Author one
  of those flat, opaque and layered (four groups is the working ceiling, from
  WWDC25 session 361), unmasked, and validate it across the six appearance
  variants. Bake the glass and the system applies it a second time.

  A *decorative icon* — a README mark, a marketplace tile, anything rendered as
  a PNG by something that is not macOS — has no compositor downstream, so the
  material has to be in the file. Every icon in this marketplace is this second
  kind, which is why `material-recipes.md` reads the way it does. Do not apply
  the Icon Composer rules to one of these; you would strip the material and
  nothing would put it back.

  When a commission is genuinely both, deliver both: a flattened
  reference-fidelity preview and a layered production package. Provenance for
  the Apple rules: `references/evidence.md` § Apple / Icon Composer, distilled
  from `docs/deep-research/visual-analysis/FINDINGS.md` §4 in the
  fledgeling-plugins repository (not bundled with the installed plugin).
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

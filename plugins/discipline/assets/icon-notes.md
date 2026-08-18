# discipline icon notes

**Direction: "The Set Stop".** The studio's *Tahoe Gel-Glass* sub-register (a), porcelain cushion tile carrying a coloured gel object, crossed with device bank **#16** (the icon performs the verb) and **#21** (authored overlap). The subject is a session-start block whose whole argument is that it governs how much the model *writes* and never how much work it *does* — a limit that was set and held — so the icon is a shaft that has travelled, and the thing that stopped it. Runner-up: *Two Columns, One Cut* (a shortened prose column beside a full-height work column on one shared floor bar). It was the most explanatory option and was rejected on silhouette: two objects is the weakest carrying shape in the set, and a side-by-side pair collapses into a bar chart at 16px, which the corpus names as the stock category trap for anything touching data. Also considered: *The Drawn Level*, a vessel drawn down to a glowing floor plate, dropped for neighbouring `braindump`'s sediment cylinder too closely.

**Glyph (subject-mined, device bank #16 + #21 + #5):** a graphite gel shaft with a domed top and fine measurement graduations, descending through a frosted-glass guide block, with a thick vermilion collar clamped around it that has come to rest hard on the guide's top face. The silhouette steps *out* at the accent and back *in* below it, so the eye lands on the thing that ended the travel. Double read (#5): the collar is simultaneously a mechanical stop and a rule drawn across the shaft.

**Signature:** the seated contact. Vermilion blooms warmly into the frosted guide exactly where the collar meets it, and the shaft's tip stays dimly visible *inside* the translucent block. That is authored overlap — real transparency between real layers — and it is the one thing a flat pre-masked raster cannot fake. It is also the whole claim in one detail: the shaft went as far as it was allowed to and no further, and you can still see it in there doing its work.

**Palette:** two families only. Warm porcelain (`#EFECE4` ground with a soft vignette and inner rim light) and graphite (`#2E353D→#4A525B` shaft), with one vermilion reserved strictly for the collar (`#D8431F→#F0603A`, blooming to `#FB8A5E` at the contact). Shadow is warm (`#6E5636`) because nothing in this scene emits cool light — authoring a blue shadow in a warm-lit scene is the recorded failure the corpus-sampling step exists to prevent. One soft top light; zero hard speculars.

**Deliberate avoidances:** the dark deep-sea register (held by `trawl`), and every sibling glyph device — stacked page lines with a seal band (`armada-sync`), the sediment cylinder (`braindump`), the tile lifted from a mould (`create-mac-icon`), the hull entering water (`create-swe-project`), the folded sheet (`dossier-report`), the plane iron and shaving (`improve-skill`), the chart plate with three hulls (`ship-armada`).

## Engines and what each one taught

Three engines were run, per the pipeline floor.

| Take | Engine | Verdict |
| --- | --- | --- |
| **C — raster** (`icon-engineC-raster-*.jpg`, Gemini 3 Pro with two corpus exemplars as `referenceImages`) | **SHIPPED**, squircle-masked | Won the material read at 1024/256: its rendered glass and the bloom at the seated contact are more convincing than the master's. Note the loop qualifies this rather than confirming the usual story, see below. |
| A — hand-authored layered SVG (`icon.svg`, `build_icon.py`) | Retained, not shipped | Compositionally clean, squircle-correct, four layers mapping 1:1 onto `#bg/#mid/#fg/#highlight`. Took three rounds to stop reading as the wrong object. NOT materially flatter than C: the fidelity run below measures its self-contrast HIGHER than the reference at every size, which is the opposite of this skill's usual finding and worth carrying back to `material-recipes.md`. |
| B — Arrow vector (`icon-engineB-arrow-*.svg`) | Loser, scored and kept | Flat fills, a grey-green ground that is not the porcelain register, a perspective slab base, and no squircle. Useful only as evidence that the vector engine did not reach the material bar here. |

**Engine A's three rounds, recorded because each was found by looking at the render rather than reasoning about it:**

1. **Read as a chess rook.** The shaft stopped *at* the collar, so the parts stacked rather than one passing through the others. Fixed by running the shaft through the guide with its tip showing below — the difference between a stop and a stack.
2. **Read as a sword.** A long thin dark blade with a crossguard. Fixed by making the shaft stubbier and the collar the widest step.
3. **The frosted guide dissolved into the porcelain** and vanished entirely at 32px. The corpus is explicit that a white object separates from a white ground by shadow, thickness and rim, never by value; the guide gained a defined rim and a deeper contact shadow.

## Audit

`audit.html` carries every take at 1024/256/128/32/16 with ×6 squint magnification, losers scored.

**Known liabilities, stated rather than buried:**

- **The shipped master is a raster, not vector.** Every icon in this marketplace is a decorative mark rendered as a PNG rather than an Icon Composer package, so baked material is correct here — but the shipped file cannot be re-coloured or re-laid-out as shapes. `icon.svg` remains the layered vector alternative if that is ever needed.
- **The fidelity loop was run, and it says the gap is compositional rather than material.** `structure` passes (2 paths, 6 gradients, 4 named groups, 12 KB). Scoring Engine A against the shipped raster:

| size | composite | SSIM | edge F1 | mask IoU | self-contrast (A vs ref) |
| --- | --- | --- | --- | --- | --- |
| 1024 | 0.580 | 0.822 | 0.063 | 1.00 | 0.491 vs 0.450 |
| 256 | 0.560 | 0.693 | 0.192 | 1.00 | 0.472 vs 0.450 |
| 32 | 0.811 | 0.633 | 0.853 | 1.00 | 0.471 vs 0.447 |
| 16 | 0.881 | 0.687 | 1.000 | 1.00 | 0.469 vs 0.408 |

Two things fall out of that, and both change the verdict from the one this skill usually records.

**Mask IoU is 1.00 at every size and edge F1 is 1.00 at 16px**, so the two takes agree on silhouette exactly. The score is carried by the small sizes, which is where a marketplace icon actually lives.

**Engine A's self-contrast is HIGHER than the reference at every size** (0.491 vs 0.450 at 1024). The usual finding here is that a hand-authored master loses material to the diffusion raster; that did not happen. The master is not flat.

**Edge F1 of 0.063 at 1024 is the real gap, and it is not a material gap.** Engine A is orthographic and flat-on; Engine C drew a three-quarter perspective with a cylindrical collar and a box guide. Those are different drawings of the same object, so no amount of parameter editing converges one onto the other. Closing it would mean re-authoring A in perspective, which is a redraw and not a loop round. Recording that is more useful than grinding rounds against a target the harness cannot reach: a gate ACCEPT is evidence, never a verdict, and here the honest reading is that the two engines disagree about the camera.

- **The shipped master is still the raster.** That choice now rests on the material read at 1024/256 where C's rendered glass is richer, not on an unmeasured hunch.
- **A faint seam** from the source raster's own baked corner survives the porcelain fill at the extreme tile edge. Visible at 1024, gone by 256.
- **The guide's perspective** is a three-quarter view where the rest of the set is flat-on. It reads well but it is a register inconsistency.

## Rounds 4 and 5: the 16px weakness is real, and the gate cannot arbitrate it

Engine A's frosted guide washes out against the porcelain below 64px, so at 32 and 16px the take
reads as a shaft floating above a collar with no base under it. Two fixes were tried and measured.

| round | change | 16px to the eye | gate |
| --- | --- | --- | --- |
| 4 | guide given real value mass (opaque beige body, heavier rim) | fixed | **REJECT**, net composite −0.0372 |
| 5 | translucency kept, dark plinth band added along the guide's foot | fixed | **REJECT**, worse than 4 at 1024/256/128 |

Both improved small-size legibility and both were rejected, for the same reason: **the reference's
own base is translucent glass**, so any change that gives A's base solid value moves it away from
the thing the gate is scoring against. The gate here measures convergence to Engine C, not quality,
and Engine C is the take that ships. It cannot answer the question being asked of it.

Round 4 also cost the signature outright: an opaque guide erases the shaft-inside-the-glass overlap,
which is the one thing `icon-notes.md` names as A's signature move. Trading a stated signature for a
small-size gain in a take that does not ship is the wrong trade.

**Resolution: A stays at round 3 and carries the weakness, documented.** The skill's own authority
rule says the 12-point rubric outranks the gate, and check #4 (16px survival) is non-negotiable — but
that rule assumes the gate and the rubric disagree about the *same* artifact. Here they disagree
about which artifact is the target. The shipped icon (C) passes #4 comfortably, so nothing a user
sees is affected; what is affected is the vector alternative's usefulness at menu-bar sizes, and that
is now a stated liability rather than an undiscovered one.

The runs are kept in `fidelity/round0`, `fidelity/round4` and `fidelity/round5` as trajectory data.

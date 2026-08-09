# token-discipline icon notes

**Direction: "The Set Stop".** The studio's *Tahoe Gel-Glass* sub-register (a), porcelain cushion tile carrying a coloured gel object, crossed with device bank **#16** (the icon performs the verb) and **#21** (authored overlap). The subject is a session-start block whose whole argument is that it governs how much the model *writes* and never how much work it *does* — a limit that was set and held — so the icon is a shaft that has travelled, and the thing that stopped it. Runner-up: *Two Columns, One Cut* (a shortened prose column beside a full-height work column on one shared floor bar). It was the most explanatory option and was rejected on silhouette: two objects is the weakest carrying shape in the set, and a side-by-side pair collapses into a bar chart at 16px, which the corpus names as the stock category trap for anything touching data. Also considered: *The Drawn Level*, a vessel drawn down to a glowing floor plate, dropped for neighbouring `compaction-quality`'s sediment cylinder too closely.

**Glyph (subject-mined, device bank #16 + #21 + #5):** a graphite gel shaft with a domed top and fine measurement graduations, descending through a frosted-glass guide block, with a thick vermilion collar clamped around it that has come to rest hard on the guide's top face. The silhouette steps *out* at the accent and back *in* below it, so the eye lands on the thing that ended the travel. Double read (#5): the collar is simultaneously a mechanical stop and a rule drawn across the shaft.

**Signature:** the seated contact. Vermilion blooms warmly into the frosted guide exactly where the collar meets it, and the shaft's tip stays dimly visible *inside* the translucent block. That is authored overlap — real transparency between real layers — and it is the one thing a flat pre-masked raster cannot fake. It is also the whole claim in one detail: the shaft went as far as it was allowed to and no further, and you can still see it in there doing its work.

**Palette:** two families only. Warm porcelain (`#EFECE4` ground with a soft vignette and inner rim light) and graphite (`#2E353D→#4A525B` shaft), with one vermilion reserved strictly for the collar (`#D8431F→#F0603A`, blooming to `#FB8A5E` at the contact). Shadow is warm (`#6E5636`) because nothing in this scene emits cool light — authoring a blue shadow in a warm-lit scene is the recorded failure the corpus-sampling step exists to prevent. One soft top light; zero hard speculars.

**Deliberate avoidances:** the dark deep-sea register (held by `trawl`), and every sibling glyph device — stacked page lines with a seal band (`armada-sync`), the sediment cylinder (`compaction-quality`), the tile lifted from a mould (`create-mac-icon`), the hull entering water (`create-swe-project`), the folded sheet (`dossier-report`), the plane iron and shaving (`improve-skill`), the chart plate with three hulls (`ship-armada`).

## Engines and what each one taught

Three engines were run, per the pipeline floor.

| Take | Engine | Verdict |
| --- | --- | --- |
| **C — raster** (`icon-engineC-raster-*.jpg`, Gemini 3 Pro with two corpus exemplars as `referenceImages`) | **SHIPPED**, squircle-masked | Won the material read outright. It produced the seated bloom and the shaft-through-glass overlap more convincingly than the hand-authored master, which is the outcome this skill's own notes predict. |
| A — hand-authored layered SVG (`icon.svg`, `build_icon.py`) | Retained, not shipped | Compositionally clean, squircle-correct, four layers mapping 1:1 onto `#bg/#mid/#fg/#highlight`, and materially flatter than C. Took three rounds to stop reading as the wrong object — see below. |
| B — Arrow vector (`icon-engineB-arrow-*.svg`) | Loser, scored and kept | Flat fills, a grey-green ground that is not the porcelain register, a perspective slab base, and no squircle. Useful only as evidence that the vector engine did not reach the material bar here. |

**Engine A's three rounds, recorded because each was found by looking at the render rather than reasoning about it:**

1. **Read as a chess rook.** The shaft stopped *at* the collar, so the parts stacked rather than one passing through the others. Fixed by running the shaft through the guide with its tip showing below — the difference between a stop and a stack.
2. **Read as a sword.** A long thin dark blade with a crossguard. Fixed by making the shaft stubbier and the collar the widest step.
3. **The frosted guide dissolved into the porcelain** and vanished entirely at 32px. The corpus is explicit that a white object separates from a white ground by shadow, thickness and rim, never by value; the guide gained a defined rim and a deeper contact shadow.

## Audit

`audit.html` carries every take at 1024/256/128/32/16 with ×6 squint magnification, losers scored.

**Known liabilities, stated rather than buried:**

- **The shipped master is a raster, not vector.** Every icon in this marketplace is a decorative mark rendered as a PNG rather than an Icon Composer package, so baked material is correct here — but the shipped file cannot be re-coloured or re-laid-out as shapes. `icon.svg` remains the layered vector alternative if that is ever needed.
- **The fidelity loop was not run.** `scripts/fidelity.py` would score the hand-authored master against the winning raster and close the material gap over bounded rounds. It was skipped, so Engine A ships *unmeasured* against its reference and the decision to ship C rests on a read rather than a score. This is the single largest gap in this commission.
- **A faint seam** from the source raster's own baked corner survives the porcelain fill at the extreme tile edge. Visible at 1024, gone by 256.
- **The guide's perspective** is a three-quarter view where the rest of the set is flat-on. It reads well but it is a register inconsistency.

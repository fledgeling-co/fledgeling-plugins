# improve-skill — icon notes

**Direction: "The Honed Edge".** The studio's *Tahoe Gel-Glass* sub-register (a), porcelain cushion tile carrying a coloured gel object, crossed with device bank **#16** (the icon performs the verb) and **#5** (dual-function primitive). The subject is a pipeline that takes a skill which already exists and makes it measurably better, so the tile is not a background: it is the workpiece. A worn plane iron lies mid-pass on a rising diagonal, and the surface behind it is visibly brighter and truer than the surface still to come.

Runner-up, and the near-neighbour worth naming: **Direction 7, Diagonal Tool**, which the catalogue calls the single most template-worn move in the corpus. This icon enters that territory deliberately rather than by reflex, and inverts it. In Direction 7 a tool crosses an inert field and the tool is the identity; here the tool has *changed* the field, and the identity is the change. Also considered and dropped: Direction 8 *Instrument Emblem*, because improve-skill has no gauge or chart to quote; its in-product artifact is an eval table, and a table is failure mode #4.

**Glyph (subject-mined, device bank #16 + #5 + #20):** one plane iron and the shaving it took off. The iron is authored as a real extruded solid — a 640 × 152 top face at 33° lifted clear of the ground, with a front face dropping back down to it — occupying 58.7% of the tile. Since round 6 that lift is *pitched*: 48px at the leading end where the iron is buried in the timber, 132px at the trailing end, so the front face is a wedge and the block rides nose-down at a working angle rather than sitting level. Crisp corners on the honed edge because it is sharpened, worn rounding and a shallow sag on the back because it is used. Underneath it, one family of grain lines runs along the travel direction and **crosses the boundary** — torn and broken above it, continuous and fine below it. That continuity is what makes the split read as one surface in two states rather than as two different materials, which is the whole argument: same skill, better. Rising off the iron's top rear edge is the shaving — a ribbon swept along the blade's own axis through an open hook of 0.78 of a turn, 262 × 250 against the blade's 601 × 590, so the blade stays the hero.

**Signature:** the before-and-after boundary *is* the diagonal, and the one vermilion hone line *is* that boundary. Since the round-4 rebuild a single shape does four jobs: the tool's cutting edge, the division between the two states, the icon's only accent, and the line where the solid meets the ground. **Risk taken:** walking into the corpus's most worn composition on purpose, on the bet that inverting it is stronger than avoiding it.

**Palette:** two families only. Warm-neutral porcelain (`#D8D2C4→#ABA391` un-planed, `#FFFDF6→#F1EAD9` trued) and achromatic graphite (`#5D636B→#181B20`), with one vermilion reserved strictly for the honed edge (`#C4341A`/`#FA6231`/`#FF9159`). One soft top-left light plus the sanctioned second source, an emissive interior; here the hone itself, spilling onto the surface it has just cut and lighting the underside of the iron's front face.

**Audit — A ships at 11/12.** `icon.png`, `icon-256.png` and `icon-128.png` all render from `icon.svg`. The one deduction is at #4, and it is the price of the shaving; see below. Full scores, verdicts and evidence: `audit.html`.

## Round 4 — the material rebuild, and what it fixed

For three rounds the sheet carried a split: the highest-scoring take was the vector master A, and the take the user chose on look was the raster C2. The split is now closed, and it closed by **rebuilding A rather than re-scoring anything**. The brief was to pull the vector toward the best of both rasters — C2's whetstone mass, both rasters' warm textured ground, a genuinely emissive hone, a deep soft contact shadow — while fixing the flaw the rasters shipped with.

**What materially changed.** The flat bar became a solid. It is now an extruded body: the top face is lifted 88px clear of the ground and a front face drops back to it, with a chamfer highlight between the two faces and a rim light along the worn back. The geometry is derived, not drawn twice — the outline is flattened to a polyline in the blade's local frame, the lower silhouette chain is swept straight down, and the ground contact of that sweep *is* local y=0, so the solid physically cannot drift out of register with the boundary or the hone. Both ground planes gained warm mottle pushed through a heavy blur over the boundary-crossing grain. The hone became real light: a heavily blurred spill on the trued plane, a warm bounce running up the front face, and a hot core line. The shadow became a deep soft cast plus a tight contact occlusion.

**What got fixed.** Polarity — the flaw C2 shipped with. The trued side now measures **L 0.920 against the un-planed side's L 0.746, +0.174 the right way round**, where C2 measured 0.653 against 0.696, **−0.043 inverted**. The side that is meant to be better now reads better. Measured by `measure.py` on the real render, every iteration, not eyeballed.

**The #10 point, earned back on evidence.** Every previous round deducted a point at variant robustness: under an aggressive monochrome tint that collapses mid-tones, the blade and the un-planed field flattened to one value and the cutting edge was lost. Rendered side by side with the old master under both a mono and a dark tint, the old one still collapses and the rebuilt solid holds. The reason is structural: identity is now a **form** relationship — a lit solid casting a shadow onto a two-state ground — rather than a colour relationship. The raw field ratio under that tint is a modest 1.69:1; what carries the read is the chamfer, the rim light and the cast shadow, none of which a tint can remove.

**Measured on the shipped renders:** focal 58.7% of tile, optical centre (508, 479), safe-zone margins L207 R216 T184 B250 — re-measured after the round-6 pitch. Figure-ground was 4.67:1 against the un-planed side and 7.56:1 against the trued side with the fields 1.62:1 apart when this was first taken at round 4, and the pitch leaves all three unchanged within measurement noise (see round 6 below). Four real layers named `#bg` / `#mid` / `#fg` / `#highlight`, mapping 1:1 onto Icon Composer. Full-bleed 1024 artwork with the squircle as a *clip*, no baked corners or shadow. Edit `build_icon.py`, never `icon.svg`.

**The shaving curl, cut three times, and what made the fourth work.** Three rounds failed because a spiral **outline** is the wrong model. An outline is a closed curve with a hole in it — a shell — and no amount of redrawing it makes it material. What ships is a swept **surface**: one cross-section curve (a nearly straight tail leaving the blade, easing tangentially into a loose open hook) swept along the blade's own axis by the ribbon's width, then cut into 96 bands, each shaded by its real facing angle to the single top-left light. Bands whose outer face turns toward the viewer are lit; the ones on the far side are seen from the *inside*, through the open end of the roll, so they take the shadow family plus a transmitted lift where the outer face is in light. The free end tapers in opacity, because that is the thinnest, most-curled material and the ground has to show through it.

Two things were measured off C2 rather than invented. **Its cross-section is a circle seen obliquely**, so the section here is compressed to 0.54 along the roll's axis; drawn as a true circle the mouth traces a full ellipse and the whole thing reads as a capped tin can. And **its curl is not a pale shape on a dark ground** — its lit top measures L 0.576 against ground of L 0.635 right beside it, falling to L 0.27 at the bottom, so it reads by form-shading and hairline cut edges, never by a value jump. That is the trap all three failed attempts fell into. This one measures **1.25:1 against the un-planed ground it was shaved from, against an internal modelling range of 3.66:1** — nearly all of its legibility is its own shading. Staying under a full turn matters twice: past one turn the swept ribbon closes into a tube and reads as a roll of tape, and an open hook is what *partially unrolled* actually looks like.

**What it costs, honestly: one point, at #4.** Rendered at 16px beside the no-curl master, the blade's dark diagonal, the vermilion hone and the two-state split are all completely intact — identity is not damaged, which is why this is a deduction and not a hard fail — but the curl contributes a small low-information tan patch above-left of the blade where the previous master had clean empty ground. It simplifies to a soft pale note, as intended, and it is still noise. It repays that at #11: the tile now carries the physical evidence that the plane cut. Polarity is unharmed and marginally better at **+0.184** (trued L 0.920, un-planed L 0.737), up from +0.174, and the blade and both fields are geometrically untouched so figure-ground is unchanged. `SHAVING=0` in `build_icon.py` rebuilds the round-4 two-object tile.

## Round 6 — the pitch: why it still didn't look like planing

The whole brief was one sentence: *"It doesn't look like wood is being planed because the angle of the block is flat unlike C2."* That was right, and the diagnosis was cheap once stated. Round 4 lifted the top face by **one constant rise**, so the top face was a parallel copy of the footprint and the front face was a band of even height. The iron had mass and no attitude: a bar lying on the boards, not a tool taking a shaving off them.

**What was measured off C2 rather than invented.** Its ground/hone line runs **38.9°**, its top-face shoulder runs **41.9°**, and its front face grows from about **55px deep at the near end to 90px at the far end**. The front face is a *wedge*, not a band, and that wedge is the entire tell — it says the block is riding nose-down, buried in the timber at the leading end and lifted behind. (Two independent detectors on C2 bracket the taper at 1.6:1 to 2.6:1 and the shoulder-vs-ground offset at +3.0° to +5.8°; the shipped value sits inside both.)

**What changed, and only this.** The lift is now **linear in local x**: `RISE_NEAR = 48` at the leading end, `RISE_FAR = 132` at the trailing end, **2.75:1**. Because a linear lift stays affine, the lifted top face is still **one matrix** — `MATRIX_TOP`, a screen-vertical shear of the blade's own frame — so the stone texture, the top-face gradient, the grind striations and the rim light all ride it with no second transform and no chance of drifting off the metal. The chains and faces are now derived by *index* so each top-face point drops to its own footprint point rather than to a constant offset. Top-face edges come out at **38.9° against the hone's 33°, +5.9° of pitch**, matching C2's shoulder-versus-ground offset. The front-face gradient is re-anchored by *absolute distance from the cutting edge* rather than by fraction of the rise, so the hone's falloff is identical whether the wedge is 48px deep or 132px there.

**What deliberately did not move.** The footprint, the cutting edge and the before/after boundary all live at local y=0 and the shear leaves local y=0 fixed, so the signature line cannot drift — and the banner's derived split needed no re-derivation. `ANGLE` stays 33° and `EDGE_MID` stays (543, 604) for the same reason: changing them is a different edit class and would kink the banner. The curl construction is untouched; its base is now held in the blade's *local* frame (`CURL_BASE_L = (289, 130)`) and mapped through `to_top`, so the tail's exit point rides the pitch instead of floating off the metal. Verified on a 4× crop of the junction — the tail still plunges behind the worn back edge exactly as it did before.

**Scored, not asserted.** Against C2 (`icon-engineC-f5665d-2.png`) on the create-mac-icon fidelity harness, runs in `fidelity-runs-block/`:

| size | before (flat) | after (pitched) | delta |
|---:|---:|---:|---:|
| 1024 | 0.3504 | **0.3623** | +0.0119 |
| 256 | 0.3334 | **0.3495** | +0.0161 |
| 128 | 0.3436 | **0.3567** | +0.0131 |
| 32 | 0.6747 | **0.6898** | +0.0151 |
| 16 | 0.7500 | **0.7595** | +0.0095 |

Every size improves; the Pareto gate **ACCEPTs at +0.0657 net** with nothing regressing. A parameter sweep over seven near-neighbour pitches picked 48/132 on the small-size floors (32 and 16 are its best sizes of the whole sweep) with the taper landing at the top of C2's measured range rather than past it.

**Polarity is untouched: +0.177** (trued L 0.920, un-planed L 0.743), against **+0.178** for the flat build measured the same way — `measure.py icon.png 33.0 543 604 640`. Figure-ground is unchanged within noise: one sampler reads 6.20:1 against the un-planed side after the pitch versus 6.34:1 before, and the two fields sit 1.75:1 apart either way.

**What it costs.** The trailing end stands 42px taller, so the top safe-zone margin goes **226 → 184** (L207 R216 B250 unchanged) and the optical centre lifts to **(508, 479)**; focal is still 58.7% of the tile. 184px is 18% of the canvas, so this is budget spent rather than a deduction. **Audit holds at 11/12** — the #4 deduction is the curl's small-size noise and the pitch neither worsens nor repairs it. At 32px and 16px the dark diagonal, the vermilion hone and the two-state split are all intact, and the wedge is still legible at 32.

**One latent bug fell out of the same edit.** The `topFace` gradient was still anchored to the *un*-lifted blade frame, so it had been 88px out of register with the face it filled since round 4. Rebuilding the flat geometry (`RISE_NEAR = RISE_FAR = 88`) with the fix in place scores **+0.0246 net** on its own — the pitch's +0.0657 includes it.

## The banner

`banner.png` is 3200 × 1040, rendered from `banner-src.html` at 1600 × 520 × 2. Its ground split was originally derived from C2's 40° cut; since A ships, it was **re-derived on A's 33° boundary** and now runs from (0, 475.5) to (731.9, 0) — the exact extension of the icon's own cut through the icon's placed position. Verified continuous to within 0.1px at both ends of the tile, and checked on a 2× crop of the junction rather than assumed. The pass runs off the tile and keeps going across the banner. Any future change to the icon's angle or placement must be re-derived there, or the cut kinks visibly. The banner no longer has to compensate for the icon's lighting the way it did for C2.

## The other takes

**Three engines, all four takes on the sheet.** Engine A now takes 12/12. Engine C raster took 9/12 (C1) and 7/12 (C2); both stay on disk as the reference takes the rebuild was judged against, and both hard-fail #10 as flat pre-masked rasters — the corpus's single most common failure. C1 additionally fails #11: its two sides sit only 0.09 L apart, so its improvement is present but too faint to be the read. Engine B (Arrow vector) came last at 5/12 with hard fails on silhouette and 16px: the blade forked into a wishbone and the vermilion hone line, the entire signature, was absent. Its steeper, flatter diagonal was the one thing worth salvaging.

**Register note:** five of the six sibling plugins share this porcelain ground, which makes it the marketplace's house register rather than a borrowed one (trawl owns the dark deep-sea register). Differentiation is carried entirely by the split, which no sibling uses, and by the fact that this is the only icon here whose tile is the thing being acted on rather than the stage the subject stands on.

## Files

| File | What it is |
|---|---|
| `build_icon.py` | The generator. **Edit here.** `SHAVING=0` rebuilds the round-4 tile without the shaving. |
| `icon.svg` | The layered master, generated. Four planes: `#bg` / `#mid` / `#fg` / `#highlight`. |
| `icon.png` / `icon-256.png` / `icon-128.png` | Shipped renders of the master. |
| `banner-src.html` / `banner.png` | README banner source and its 3200 × 1040 render. |
| `measure.py` | Split-polarity check. Trued side must measure brighter than un-planed. |
| `compare.py` | Renders the master beside both rasters at 256 with a 16px squint row. |
| `fidelity-runs-block/` | Fidelity harness runs for the round-6 pitch: `baseline/` is the flat master, `final/` is what ships. Score with `create-mac-icon/skills/create-mac-icon/scripts/fidelity.py`. |
| `render_audit.py` | Re-renders every take at 1024/256/64/32 and the three shipped PNGs. |
| `audit.html` / `audit-renders/` | The contact sheet, scores and verdicts. |
| `icon-engineC-*.png`, `icon-engineB-*.svg` | Reference takes, kept for comparison. |

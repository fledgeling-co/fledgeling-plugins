# improve-skill — icon notes

**Direction: "The Honed Edge".** The studio's *Tahoe Gel-Glass* sub-register (a), porcelain cushion tile carrying a coloured gel object, crossed with device bank **#16** (the icon performs the verb) and **#5** (dual-function primitive). The subject is a pipeline that takes a skill which already exists and makes it measurably better, so the tile is not a background: it is the workpiece. A worn plane iron lies mid-pass on a rising diagonal, and the surface behind it is visibly brighter and truer than the surface still to come.

Runner-up, and the near-neighbour worth naming: **Direction 7, Diagonal Tool**, which the catalogue calls the single most template-worn move in the corpus. This icon enters that territory deliberately rather than by reflex, and inverts it. In Direction 7 a tool crosses an inert field and the tool is the identity; here the tool has *changed* the field, and the identity is the change. Also considered and dropped: Direction 8 *Instrument Emblem*, because improve-skill has no gauge or chart to quote; its in-product artifact is an eval table, and a table is failure mode #4.

**Glyph (subject-mined, device bank #16 + #5 + #20):** one plane iron, authored as a real extruded solid — a 640 × 152 top face at 33° lifted 88px clear of the ground, with a front face dropping back down to it — occupying 58.7% of the tile. Crisp corners on the honed edge because it is sharpened, worn rounding and a shallow sag on the back because it is used. Underneath it, one family of grain lines runs along the travel direction and **crosses the boundary** — torn and broken above it, continuous and fine below it. That continuity is what makes the split read as one surface in two states rather than as two different materials, which is the whole argument: same skill, better.

**Signature:** the before-and-after boundary *is* the diagonal, and the one vermilion hone line *is* that boundary. Since the round-4 rebuild a single shape does four jobs: the tool's cutting edge, the division between the two states, the icon's only accent, and the line where the solid meets the ground. **Risk taken:** walking into the corpus's most worn composition on purpose, on the bet that inverting it is stronger than avoiding it.

**Palette:** two families only. Warm-neutral porcelain (`#D8D2C4→#ABA391` un-planed, `#FFFDF6→#F1EAD9` trued) and achromatic graphite (`#5D636B→#181B20`), with one vermilion reserved strictly for the honed edge (`#C4341A`/`#FA6231`/`#FF9159`). One soft top-left light plus the sanctioned second source, an emissive interior; here the hone itself, spilling onto the surface it has just cut and lighting the underside of the iron's front face.

**Audit — A ships at 12/12.** `icon.png`, `icon-256.png` and `icon-128.png` all render from `icon.svg`. Full scores, verdicts and evidence: `audit.html`.

## Round 4 — the material rebuild, and what it fixed

For three rounds the sheet carried a split: the highest-scoring take was the vector master A, and the take the user chose on look was the raster C2. The split is now closed, and it closed by **rebuilding A rather than re-scoring anything**. The brief was to pull the vector toward the best of both rasters — C2's whetstone mass, both rasters' warm textured ground, a genuinely emissive hone, a deep soft contact shadow — while fixing the flaw the rasters shipped with.

**What materially changed.** The flat bar became a solid. It is now an extruded body: the top face is lifted 88px clear of the ground and a front face drops back to it, with a chamfer highlight between the two faces and a rim light along the worn back. The geometry is derived, not drawn twice — the outline is flattened to a polyline in the blade's local frame, the lower silhouette chain is swept straight down, and the ground contact of that sweep *is* local y=0, so the solid physically cannot drift out of register with the boundary or the hone. Both ground planes gained warm mottle pushed through a heavy blur over the boundary-crossing grain. The hone became real light: a heavily blurred spill on the trued plane, a warm bounce running up the front face, and a hot core line. The shadow became a deep soft cast plus a tight contact occlusion.

**What got fixed.** Polarity — the flaw C2 shipped with. The trued side now measures **L 0.920 against the un-planed side's L 0.746, +0.174 the right way round**, where C2 measured 0.653 against 0.696, **−0.043 inverted**. The side that is meant to be better now reads better. Measured by `measure.py` on the real render, every iteration, not eyeballed.

**The #10 point, earned back on evidence.** Every previous round deducted a point at variant robustness: under an aggressive monochrome tint that collapses mid-tones, the blade and the un-planed field flattened to one value and the cutting edge was lost. Rendered side by side with the old master under both a mono and a dark tint, the old one still collapses and the rebuilt solid holds. The reason is structural: identity is now a **form** relationship — a lit solid casting a shadow onto a two-state ground — rather than a colour relationship. The raw field ratio under that tint is a modest 1.69:1; what carries the read is the chamfer, the rim light and the cast shadow, none of which a tint can remove.

**Measured on the shipped renders:** focal 58.7% of tile, optical centre (508, 500), safe-zone margins L207 R216 T226 B250, figure-ground 4.67:1 against the un-planed side and 7.56:1 against the trued side, the two fields 1.62:1 apart. Four real layers named `#bg` / `#mid` / `#fg` / `#highlight`, mapping 1:1 onto Icon Composer. Full-bleed 1024 artwork with the squircle as a *clip*, no baked corners or shadow. Edit `build_icon.py`, never `icon.svg`.

**The shaving curl, cut for the third time.** It was authored properly this round — a tapering spiral ribbon rather than the annulus that read as a coat hanger in rounds 2 and 3 — and rendered against the rasters as a fair test, because both of them keep theirs and in a photographic material it works. It failed again: on the real render it reads as a flat white snail shell sitting on the surface rather than as material that came away, and at 16px it is a pale smudge competing with the block. Three attempts, three constructions, three failures. The two-state split is already the evidence that something came off, so the tile keeps two objects: surface and blade. The flag survives in `build_icon.py` as `SHAVING=1` if anyone wants to see it fail again.

## The banner

`banner.png` is 3200 × 1040, rendered from `banner-src.html` at 1600 × 520 × 2. Its ground split was originally derived from C2's 40° cut; since A ships, it was **re-derived on A's 33° boundary** and now runs from (0, 475.5) to (731.9, 0) — the exact extension of the icon's own cut through the icon's placed position. Verified continuous to within 0.1px at both ends of the tile, and checked on a 2× crop of the junction rather than assumed. The pass runs off the tile and keeps going across the banner. Any future change to the icon's angle or placement must be re-derived there, or the cut kinks visibly. The banner no longer has to compensate for the icon's lighting the way it did for C2.

## The other takes

**Three engines, all four takes on the sheet.** Engine A now takes 12/12. Engine C raster took 9/12 (C1) and 7/12 (C2); both stay on disk as the reference takes the rebuild was judged against, and both hard-fail #10 as flat pre-masked rasters — the corpus's single most common failure. C1 additionally fails #11: its two sides sit only 0.09 L apart, so its improvement is present but too faint to be the read. Engine B (Arrow vector) came last at 5/12 with hard fails on silhouette and 16px: the blade forked into a wishbone and the vermilion hone line, the entire signature, was absent. Its steeper, flatter diagonal was the one thing worth salvaging.

**Register note:** five of the six sibling plugins share this porcelain ground, which makes it the marketplace's house register rather than a borrowed one (trawl owns the dark deep-sea register). Differentiation is carried entirely by the split, which no sibling uses, and by the fact that this is the only icon here whose tile is the thing being acted on rather than the stage the subject stands on.

## Files

| File | What it is |
|---|---|
| `build_icon.py` | The generator. **Edit here.** `SHAVING=1` toggles the cut shaving test. |
| `icon.svg` | The layered master, generated. Four planes: `#bg` / `#mid` / `#fg` / `#highlight`. |
| `icon.png` / `icon-256.png` / `icon-128.png` | Shipped renders of the master. |
| `banner-src.html` / `banner.png` | README banner source and its 3200 × 1040 render. |
| `measure.py` | Split-polarity check. Trued side must measure brighter than un-planed. |
| `compare.py` | Renders the master beside both rasters at 256 with a 16px squint row. |
| `render_audit.py` | Re-renders every take at 1024/256/64/32 and the three shipped PNGs. |
| `audit.html` / `audit-renders/` | The contact sheet, scores and verdicts. |
| `icon-engineC-*.png`, `icon-engineB-*.svg` | Reference takes, kept for comparison. |

# Fledgeling brand icon — design notes

**Direction:** Tahoe Gel-Glass (`icon-directions.md` §2), **dark sub-register (c)** — warm variant.
**Runner-up:** Monochrome Logomark (§3) — rejected because it is roughly what already ships, and it is the family that hard-fails variant robustness (14 of 15 corpus members), which is precisely the gap this refinement exists to close.

This is a **refinement, not a redesign.** The silhouette, the three-colour palette and the warm register are the brand and were preserved deliberately. What changed is material, optical balance and layer structure.

---

## Shared spec (all three engines briefed from this)

| | |
|---|---|
| Canvas | 1024 × 1024, full bleed |
| Ground | warm charcoal cushion tile — `#3B362D` top → `#2A2620` mid → `#211E19` bottom, plus a rim light and a 10% corner vignette |
| Glyph | frosted cream `#EFE7D8`, poured gel: `#FFFCF5` lit → `#EFE7D8` body → `#D3C6AF` shaded |
| Accent | ember `#C4622D`, hot core `#F8B978`, deep edge `#9C4A1E` |
| Light | one soft top-left source; rim highlights on lit edges only; soft cast shadows; no hard speculars |
| Device | subject-mined — a form that reads at once as a sprouting shoot and a fledgeling bird, plus one released ember |
| Signature | the ember as an **emissive interior under glass** (device bank #22), released past the upper wing tip |

**Layer plan (#10):** `bg` cushion tile · `mid` object shadow + ember halo (both droppable) · `fg` the poured object · `highlight` rim light, ember bloom and specular.

---

## What actually changed from `apps/website/app/icon.svg`

**Optical balance.** The old glyph's bounding box sat +2.25% right and +5.75% low of centre and filled only 46.5% of tile width — under the 55–65% composition band. The new mark sits +1.4% / −0.8% and fills 55.7%.

**Stroke confidence.** The stalk was a uniform 4.5%-wide stroke with a slight kink; it is now a filled tapered path, 7.9% at the base narrowing to 3.3% at a fine sprouting tip that clears the upper leaf. At 16px that is 1.26px of stalk instead of 0.72px — the single change that most improves small-size survival.

**Material.** Flat fills became the Tahoe grammar: a cushion tile with an inner rim light and a corner vignette (tell 1), poured gel gradients rather than flat shapes (tell 3), rim light on lit edges only with one soft top source (tell 6), and a sanctioned second light in the ember's emissive interior (tell 6).

**Squircle.** The old `rx="26"` is a circular corner. The tile is now a true Apple-style superellipse (|x/a|⁵ + |y/b|⁵ = 1), generated and fitted to cubics, which is the continuous-curvature corner the current era uses.

**Layer structure.** One flat path set became four named groups. Identity now rides on shape and value rather than a colour relationship, so it survives Dark / Clear / Tinted — the corpus's highest-leverage gap (76% of shipping icons fail it).

---

## Two decisions worth arguing with

**1. The overlap is deliberately quiet.** The brief asked for authored translucency where the wings cross the stalk, and Tahoe tell 5 calls authored overlap the era's signature craft moment. Two earlier iterations pushed it hard — wings sailing across the stalk at 0.84–0.89 opacity — and both read as a muddy grey X-knot rather than glass. It was rejected in review. The leaves now **emerge from** the stalk (blunt ends tucked inside its width, rims only on the outer lit edges), and the translucency survives only as the upper leaf at 0.95 letting a whisper of the stalk through, plus its cast shadow onto the stalk. This is the icon's one scored deduction (11/12, on era coherence). Getting the overlap to full strength means redrawing leaf and stalk as one continuous poured ribbon — the Engine C idea below — which is a redesign, not a tweak.

**2. The tile ships a baked squircle.** Normally a hard mask-discipline failure. It is correct here because the rounded charcoal tile *is* the brand mark on the website. The tile is a single referenced `<path id="tileShape">`, so a macOS Icon Composer submission swaps it for `<rect width="1024" height="1024">` in one line. No drop shadow is baked anywhere.

---

## Engines

- **A — hand-authored layered SVG.** `fledgeling-icon.svg`. **11/12, ships.** Four named layers, Icon-Composer-ready.
- **B — Arrow 1.1 vector.** `fledgeling-icon-engineB.svg`. **5/12, lost.** Baked corner radius *and* baked drop shadow (check 1, twice); non-square 144.9×150 canvas; both blades resolved into one leaf pointing the same way, which killed the bird reading; palette drifted off-brand. Nothing salvaged — its contribution was negative evidence that a symmetric two-leaf arrangement destroys the fledgeling reading, which is why the master keeps the blades asymmetric.
- **C — GPT Image 2 raster**, referenced against four dark-register corpus exemplars (`apple-21` charcoal gel, `apple-03` translucent panels, `apple-16` Weather's hue bleed at overlap, `apple-10` ChatGPT's shaded crossings). `fledgeling-icon-c1.png`. **8/12, lost.** Best-looking take at 1024 and the worst at 16px — the emissive glow blows out to an unnameable blob. Also drifted to Direction 4 Dark-Field Emissive rather than the gel register specified. **Its one great idea, not taken:** it draws the wing crossing the body as a single continuous poured ribbon rather than two blades over a stalk. That is the most elegant answer to the overlap problem any engine produced and is the obvious basis for a future *redesign* pass.

---

## Files

| File | What it is |
|---|---|
| `fledgeling-icon.svg` | the layered master — Engine A, 1024, `bg`/`mid`/`fg`/`highlight` |
| `fledgeling-icon-256.png`, `-128.png` | shipping rasters of the master |
| `fledgeling-icon-engineB.svg` | Engine B take (lost, kept for the record) |
| `fledgeling-icon-c1.png` | Engine C take (lost, kept for the record) |
| `audit.html` | contact sheet, all four rows scored, recommendation + liabilities |
| `audit-renders/` | every take at 1024 / 256 / 64 / 32, plus the existing mark as baseline |

Rebuild the master with `build_icon.py` (geometry is parameterised: `S` scale, `DX`/`DY` optical centring, one path constant per form).

## Not checked

Rendering was verified in **librsvg only**. The `feGaussianBlur` rim and cast-shadow filters should be spot-checked in Safari, in Icon Composer, and against a real Dock/menu-bar tint before release.

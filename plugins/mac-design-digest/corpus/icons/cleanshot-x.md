# Icon: CleanShot X

- **Era:** big-sur (Big Sur unified — squircle tile, front-facing, soft top-down light, baked micro-shadows, a material-overlay device) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/cleanshot-x/icon.webp`, a **102×102 WebP web render**; hex/geometry cross-checked against the sharper 1200×630 `cover.png` where the icon renders ~350px) · **Category:** Utility
- **Subject the icon must communicate:** a pro Mac screen-capture tool ("Capture your Mac's screen like a pro").

| Dimension | Reading |
|---|---|
| Background | **scene** — a charcoal "desktop" base plane (ramp `#383D48` lower-left → `#565B65` upper `(measured)`) almost entirely covered by a bright **cyan→blue screenshot sheet** (diagonal ramp `#37D0FE` top → `#0981F3` mid → `#0054EB` bottom-right `(measured)`). Both bleed full to the squircle mask. |
| Glyph | **object** — a blue screenshot *sheet* being **peeled off** the desktop from the lower-left corner. The lifted corner curls toward the viewer, its pale underside (`#CBE6F5`) catching light; the peel reveals the dark desktop beneath scattered with 5 confetti "app" dots. Focal peel-apex sits near optical centre; composition split on a lower-left→upper-right diagonal `(measured)`. |
| Overlay device | **other — peeling-sheet ("capture-as-peel")**. Not a diagonal tool crossing the plane; the sheet *is* the plane, lifted at one corner. |
| Light model | soft **top-down (slightly top-left)**; short baked micro-shadow beneath the lifted corner and along the peeled edge, cast onto the dark base; gentle specular sheen on the curl underside. Big Sur baked-shadow idiom — no long dramatic shadows. `(estimated)` |
| Layer stack | charcoal desktop base (back) → 5 confetti app-dots on the base → cyan→blue screenshot sheet (covers ~75% of canvas) → peeled corner with pale underside `#CBE6F5` + its cast shadow (front). |
| Palette economy | **2 base hue families** (blue ramp + neutral charcoal) — disciplined for the dominant field — **plus a 5-hue confetti accent set** (mint, orange, pink, purple, magenta). The confetti breaks the ≤2-family letter but stays tiny/peripheral/low-salience (see #6 soft pass). |

## Palette
- **Screenshot sheet (glyph):** ramp `#37D0FE` (55,208,254) cyan top → `#0981F3` (9,129,243) mid → `#0054EB` (0,84,235) deep blue bottom-right — diagonal, sky-logic rotated `(measured)`
- **Curl underside highlight:** `#CBE6F5` (203,230,245) pale ice-blue `(measured)`
- **Desktop base:** charcoal ramp `#383D48` (56,61,72) → `#565B65` (86,91,101) `(measured)`
- **Confetti app-dots (revealed content):** mint/teal `#24F3DC`, orange `#F97B00`, pink/red `#FF2B4C`, purple `#755CFC`, magenta triangle `#FF2B4C` `(measured, small-target so ±soft)`
- **Accent:** no single accent — the confetti is a bounded multi-hue set standing in for a colourful Mac desktop

## Signature devices
- **[GOLDEN-NUGGET] Capture-as-peel.** The screenshot is rendered as a physical blue sheet being peeled off the screen, revealing the desktop underneath. The icon animates the app's own verb (capture) in a static mark — the whole identity is this one committed decision, not a template glyph-on-gradient.
- **Confetti-desktop reveal.** The five saturated dots (mint/orange/pink/purple + a tiny triangle) are abstract stand-ins for a colourful desktop of app icons — they exist only to give the peel something worth revealing. Purposeful scatter, not focal collision.
- **Diagonal cyan→blue sheet ramp.** Sky-logic (light-at-top) rotated onto a lower-left→upper-right diagonal so the ramp tracks the peel direction, not gravity.
- **Curl-underside gloss.** The pale `#CBE6F5` back-face sheen sells the sheet as a lifted material and is the single strongest value contrast in the mark (8.38:1 vs the base).

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black the artwork collapses to a plain squircle: identity is carried entirely by internal value/colour contrast (blue-vs-charcoal split + the curl), not by any external or two-value silhouette. Typical of full-bleed scene icons — nameable only in colour.
- **#10 Variant robustness (Liquid Glass) — FAIL.** The mark leans on the specific bright-blue-sheet-vs-dark-desktop colour split; a tinted/mono system render collapses that relationship and the peel loses legibility. Authored for Big Sur, not for macOS 26 glass/tinted appearances — no layer separation that would survive de-colouring.

### Soft passes (flagged, scored as pass)
- **#2 Grid adherence — soft.** No centred glyph to grid; the diagonal split is optically balanced and the peel-apex sits near centre, but "safe-zone margin" is moot for a full-bleed scene.
- **#4 16px squint — soft.** Survives as a distinctive blue tile with a curl swoosh (not generic), but the 5 confetti dots smear to near-invisible specks and the specific *screenshot-peel* metaphor softens to "blue tile with a light streak" at menu-bar size.
- **#6 Palette economy — soft.** Base is a disciplined 2-family (blue ramp + charcoal); the 5 multi-hue confetti dots exceed the ≤2-family rule but stay small, peripheral, and low in the value hierarchy — they don't compete with the blue focal field, so it reads as bounded confetti rather than accent sprawl.
- **#7 Figure-ground — soft.** Blue focal vs dark base measures **3.16:1** — clears the 3:1 icon floor but only just; the curl-vs-base (8.38:1) is what actually carries the read. Survives grayscale on the value split.

## Rhymes with
- **Big Sur glossy-blue utility tiles** that state their verb with a **skeuomorphic material-quote overlay** on a saturated field — the "content-on-a-surface" family (Preview/Photos-adjacent, screenshot/capture tools).
- Icons whose subject is communicated by a **peeled/lifted/torn material** revealing something beneath (sticker-peel, page-curl, screen-reveal motifs).
- Cross-note for synthesis: sits opposite the transparent free-form utility glyphs (e.g. AutoShelf) — this one is a fully-committed squircle tile with a scene. If 2+ more "saturated-field + material-overlay Big Sur tile" icons appear, that is a nameable icon cluster distinct from both Liquid-Glass and floating-object utilities.

## Notes (resolution & synthesis)
- **Resolution caveat:** the digest subject (`icon.webp`) is only **102×102** — a small web render. All hex and layer-order readings were taken from the sharper `cover.png` (icon renders ~350px) and agree with the small icon; but sub-2% gradient banding, exact peel-edge geometry, and the confetti-dot hues (each only a few px) are **soft** — no 1024 master to confirm. Treat interior fills as reliable, fine edges as estimated.
- **Both failures (#3, #10) share one root cause:** identity lives in colour, not shape. A Liquid-Glass re-author would need to move the blue/dark split into separable Icon Composer layers (or add a shape-legible peel edge) to survive tinted/mono and the solid-black silhouette.
- **Brand coherence with the cover is strong:** the identical icon headlines the cover hero on a light confetti-of-glyphs backdrop; the cyan→blue and the confetti-dot palette are the app's brand signature. The icon is a faithful brand mark, not a detached render.
- **Era note:** unambiguously Big Sur unified (squircle, front-facing, top-down baked light, material overlay). The page-curl is a skeuomorphic *quote* executed in Big Sur's flat-material idiom — consistent, not mixed-era. Not updated for Liquid Glass.
</content>
</invoke>

# Icon: Cursor

- **Era:** Custom (flat brand-mark-on-dark-tile; era-agnostic — commits to neither Big Sur soft-depth nor Liquid Glass translucency) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (Cursor, "AI coding agent", Dev). Icon render is 204×204 webp — a resized web asset, **not** the 1024 master. All px/positional reads are `(estimated)` at low res; hex values sampled from the 204px render (anti-aliased edges, values reliable at facet centres). The pixels outside the squircle flatten to `#FFFFFF` — the source is a **pre-masked squircle PNG**, i.e. a cross-platform/Electron brand tile, not an unmasked full-bleed layer handed to the system to mask.

| Dimension | Reading |
|---|---|
| Background | **Flat** warm near-black `#13120B` (olive-tinted charcoal — R>G>B). Truly flat: nine samples across the field are identical, no ramp, no vignette (the apparent halo behind the cube in an upscale is a NEAREST artifact, not in the source). No glass rim. |
| Glyph | **Abstract geometric mark:** an isometric cube (hexagonal outer silhouette) rendered as three tonal facets, with a bright inverted-triangle "blade" down the centre-front. Achromatic grayscale ramp: back/right faces `#43413D` → left face `#555450` → front blade `#D9D7D3` → top highlight `#FFFFFD`. Optically centred, sits a hair high; occupies ~central 60% of the canvas (generous safe-zone margins). |
| Overlay device | **None.** No diagonal tool, badge, or frame — the cube is the whole composition, floating on the tile. |
| Light model | **Object-internal** directional light from upper-front-left: top face and central blade brightest, side faces progressively darker, back-right face darkest. Flat *faceted vector shading* — **no cast shadow on the tile, no ambient occlusion, no specular/glass**. Coherent on the object, but it is self-lit brand illustration, not a Big Sur baked-micro-shadow render nor a Liquid Glass environmental render. |
| Layer stack | (back→front) 1. flat warm-black `#13120B` squircle tile → 2. cube dark/back facets (`#43413D` right, `#555450` left) → 3. bright front blade + top highlight (`#D9D7D3`→`#FFFFFD`). Two planes only: tile + one grouped faceted glyph. |
| Palette economy | **Fully achromatic** — a single grayscale ramp on a warm-black ground, zero hue, zero accent. Maximally economical (arguably austere: nothing is reserved *for* an accent because there is none). Cover art confirms the brand is deliberately monochrome (white "CURSOR" wordmark + same cube on the same near-black). |

## Signature devices
- **[GOLDEN-NUGGET] Dual-read cube-cursor.** The bright inverted triangle reads simultaneously as (a) the cube's near vertical edge / front facet and (b) a downward-pointing cursor/pointer blade. One geometric move carries both "3D environment/agent" and "cursor". Committed direction, not template glyph-on-gradient — though the second reading is subtle and tonal (see #16px and silhouette).
- **[GOLDEN-NUGGET] Tonal ramp as self-lighting, zero hue.** A monochrome facet ramp (`#43`→`#55`→`#D9`→`#FFF`) does all the 3D work; the icon proves a faceted object can read dimensional with no colour at all — the opposite pole from the LLM-era violet→blue glass blob (cf. Codex).
- **Vanishing back-faces.** The darkest facets (`#43413D`) sit only ~1.5:1 against the `#13120B` tile, so the cube's far edges melt into the ground and it reads *open / floating* rather than a solid block — deliberate, and it lets the bright blade dominate.

## Failures
- **#10 Variant robustness (Liquid Glass).** The composition is defined *against* its baked near-black tile: the dark cube facets (`#43413D`) are legible only because the ground is darker still. On a Liquid Glass **clear / tinted / light** render the opaque black tile can't take the system tint, and if the ground lightens the dark back-faces lose figure-ground and the cube collapses toward a flat white silhouette. The white glyph would survive tinting (achromatic), but the icon as a whole does not participate in the current era's material system — it is a self-contained brand tile.

### Soft passes (counted as passes, flagged)
- **#4 16px squint.** The hexagonal cube **outline** survives at menu-bar size and is nameable as "a cube," but the two mid-dark facets (`#43` vs `#55`, ~1.2:1 apart) merge and the bright-blade *cursor* dual-reading smears out — at 16px it's a generic gray cube, its wit dropped. Survives as a shape; loses its concept. Structural (achromatic + low internal contrast on the dark faces), partly aggravated by the 204px source.
- **#2 Grid adherence.** Optical centring and safe-zone margins look right and the cube sits marginally high (correct optical bias), but the true Apple grid can't be overlaid on a 204px render — `(estimated)`.
- **#3 Silhouette (borderline pass).** Filled solid black the mark is a clean hexagon → nameable as "a cube," but the *cursor* half of the concept lives entirely in the tonal facets and vanishes in pure silhouette; subject identity at silhouette level is "cube," not "Cursor."

## Rhymes with
- **Achromatic dev/AI-tool logo-on-near-black tiles** — the "company wordmark's glyph dropped on a flat dark square" family (cf. the darker end of the corpus's Dev icons; contrast with Codex, which takes the opposite light-ground + saturated-glass route for the same "AI coding agent" brief).
- **Isometric-cube brand marks** — geometric-primitive-as-logo lineage (cube/box = "environment", "package", "build").
- Style family (hint, confirm against ≥3 independent icons before any canon): *flat faceted brand-mark on flat dark tile, achromatic, no system-material participation* — the cross-platform/Electron brand-tile pattern, distinct from native Big Sur/Liquid Glass icon craft.

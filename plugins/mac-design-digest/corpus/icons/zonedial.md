# Icon: Zonedial

- **Era:** flat-transition (nearest bucket) — really a generic flat / iOS-tile glyph, not a mac-native Big Sur or Liquid Glass design · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (Codenta app suite) · icon.png 1024×1024, vector-crisp edges, high colour confidence (not a resized web render)
- **Category:** Utility (timezone converter — "Timezone math made effortless")

| Dimension | Reading |
|---|---|
| Background | flat `#3D65D9` royal/periwinkle blue — no ramp (top `p{512,150}` and bottom `p{512,880}` sample identically) (measured) |
| Glyph | object — white monoline clock: thin ring + two round-capped hands meeting at a centre hub, reading a stylised ~10:10-ish angle. `#FFFFFF` (measured). Ring outer Ø ≈ 655px (~64% of canvas), optical centre ≈ (510, 521) vs canvas (512,512) — near-centred, ~9px low (estimated) |
| Overlay device | none (no diagonal tool, no badge, no frame) |
| Light model | none — zero gradient, shadow, specular or bevel; flat fill + flat glyph. Consistent by absence, but carries no mac-native depth (measured) |
| Layer stack | back→front: (1) flat royal-blue squircle field, pre-masked with alpha-transparent corners; (2) white monoline clock ring; (3) two white round-capped hands + centre hub |
| Palette economy | 1 hue family (royal blue) + white glyph, no accent — disciplined, ≤2 families (measured) |

## Signature devices
- **Round-terminal monoline clock at a stylised angle** — the hands sit at a watch-advert ~10:10-ish spread rather than a literal 3-o'clock, with fully rounded caps. This is the only committed move, and it is faint: the glyph reads as a lightly-restyled SF Symbol `clock` recoloured white. `[GOLDEN-NUGGET]` value is low — closer to template-default than to a signature.

## Failures
- **#1 Mask discipline (FAIL):** artwork is a pre-rounded squircle baked into the raster's alpha — corner `p{5,5}` is fully transparent, fill is a rounded square. HIG asks for a **square, unmasked** layer so macOS 26 applies its own squircle; a pre-baked corner radius risks double-rounding / a thin double-contour in the Dock, and forfeits system light/dark/clear/tinted layering.
- **#11 Personality (FAIL):** no distinctive device beyond a glyph-on-solid-tile. A near-stock monoline clock centred on one flat blue field is the archetypal template composition (`template-default` in aesthetic-direction terms) — nothing subject-mined from "timezones" (no globe, dial, multi-zone, split-face, or numerals cue) survives into the mark.

## Soft passes (scored pass, flagged for synthesis)
- **#4 16px squint:** the circular silhouette survives, but the ring stroke (~30px on 1024 → ~0.5px at 16px) and thin hands thin out to a hairline at menu-bar/Spotlight size; white-on-saturated-blue contrast is what rescues legibility.
- **#5 Light model / #8 Depth:** trivially consistent because there is *no* lighting or depth — flat, single-plane; not a defect but not mac-native dimensionality either.
- **#9 Era coherence:** internally coherent flat language, but the flat-fill + monoline-glyph vocabulary reads iOS/web, not Big Sur material or Liquid Glass.
- **#10 Variant robustness:** a white glyph transplants cleanly onto any dark ground, but no dark/clear/tinted layers are authored — the composition, not Icon Composer, would have to be re-derived.

## Passes (clean)
- **#2 Grid** (optically centred, ~18% safe-zone margins) · **#3 Silhouette** (filled solid = instantly "a clock") · **#6 Palette economy** (one hue + white) · **#7 Figure-ground** (`#FFFFFF` on `#3D65D9` ≈ 5:1, survives grayscale) · **#12 No-text** (no words/photos/UI).

## Brand coherence (icon ↔ cover)
- Cover uses the same royal blue as the icon field and an electric-blue-on-navy scheme — palette coheres. But the cover's hero is a **3D dimensional clock** (specular disc, cast shadow) while the shipped app icon is dead flat; the marketing render promises a depth the icon doesn't deliver. Note for synthesis: dimensional-cover / flat-icon mismatch is a recurring indie tell.

## Rhymes with
- (hint only) Flat glyph-on-solid-tile utility family — recoloured-system-symbol clocks/weather/timer tiles; iOS default Clock lineage. Awaits ≥2 more members before any cluster claim.

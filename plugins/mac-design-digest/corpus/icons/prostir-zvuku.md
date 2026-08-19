# Icon: prostir zvuku

- **App:** prostir zvuku — a spatial nature-sound mixer for macOS · **Category:** Lifestyle
- **Source:** macapp.supply (icon.png, 1024×1024 native PNG, SHA-1 `bf5e2729`)
- **Era:** custom (atmospheric monochrome; sits in the modern uniform-squircle envelope but declines both the Big Sur tool-on-gradient and the Liquid Glass layered-glass vocabularies) · **Rubric:** 10/12 · **Digested:** 2026-07-19

| Dimension | Reading |
|---|---|
| Background | flat pure black — corners `#000000` (measured), interior `#090A0A` (measured); no ramp, no scene |
| Glyph | abstract emissive bloom — a soft, gestural waveform/plume (tall central peak, left dip + secondary lobe, low tail pulling right). Neutral grayscale ramp, brightest core `#DFDFDF` (measured, channel spread 0). Figure is defined by luminance, not by a hard edge |
| Overlay device | none |
| Light model | emissive / self-luminous — no directional key light; radial luminance falloff from the bright core out to pure black, with film-grain dither baked into the ramp. No cast or top-down baked shadow |
| Layer stack | back→front: (1) pure-black field `#000→#090A0A`; (2) grainy emissive grayscale bloom, core `~#DFDFDF`. Two planes only |
| Palette economy | zero hue families — a single neutral grayscale ramp (`#000000 → #404040 → #848384 → #A8A7A7 → #DFDFDF`). Accent: none. Maximally economical |

## Signature devices
- **Emissive waveform/aurora bloom on void black** — the entire icon is one glowing gestural form; the audio-waveform envelope reads as light rather than as an object. Spatial-audio metaphor rendered atmospherically.
- **Film-grain / dithered gradient** — the ramp carries an analog airbrush grain (intentional dither, not compression; source is PNG), which gives the form a volumetric, backlit-smoke quality instead of clean vector falloff.
- **Total monochrome restraint** — zero color in an app whose brand (see cover) is a saturated royal-blue gradient. Coherence with the app is carried by the dark canvas and the waveform motif, *not* by hue — a deliberate, nameable divergence.
- **Figure by luminance, not silhouette** — the form has no defined boundary; it exists only as a gradient. This is the icon's whole personality and also the root of its two rubric misses.

## Failures
- **#3 Silhouette test** — the bloom has no hard edge; imagined filled solid black it vanishes into the background. The subject is nameable ("a waveform / a plume of light") only through its internal gradient, never through shape. No crisp silhouette exists.
- **#10 Variant robustness (Liquid Glass era)** — the composition depends entirely on a pure-black background. A pale-gray emissive form has almost no contrast on a light, clear, or tinted render, and this is a fixed raster (not a layered Icon Composer doc), so macOS 26 cannot auto-generate valid dark/clear/tinted appearances. The glyph is hostage to one background color.

## Soft passes (flagged, scored as passes)
- **#2 Grid adherence** — the bright core sits slightly left and high of optical centre and the tail pulls right; it reads balanced on the symmetric black field but is not grid-precise.
- **#4 16px squint test** — at Dock/Spotlight size the grain and the left-dip/right-tail detail smear into an indistinct gray smudge; the *waveform semantics* are lost, but the high luminance contrast (`#DFDFDF` on `#000`) means the icon still survives as a distinct luminous mark against neighbouring Dock icons. Presence survives; meaning does not.
- **#9 Era coherence** — internally consistent within its own custom atmospheric idiom, but it quotes neither current-era vocabulary (no baked tool lighting, no glass layers).

## Rubric ledger
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Mask discipline | pass | full-bleed black, no corner-radius mismatch, nothing fights the squircle |
| 2 | Grid adherence | soft pass | core slightly left/high, tail right; balanced on black but not grid-precise |
| 3 | Silhouette | **fail** | no hard edge; fills to nothing on black — figure is pure gradient |
| 4 | 16px squint | soft pass | smears to a gray smudge; presence survives via contrast, semantics lost |
| 5 | Single light model | pass | consistent emissive radial falloff throughout |
| 6 | Palette economy | pass | zero hue families, one grayscale ramp, no accent |
| 7 | Figure-ground contrast | pass | core `#DFDFDF` on `#000` ≈ 13:1+; is grayscale so survives grayscale trivially |
| 8 | Depth coherence | pass | 2 clean planes, no z-fighting, shadow logic consistent (emissive) |
| 9 | Era coherence | soft pass | one custom idiom, but declines both modern-era vocabularies |
| 10 | Variant robustness | **fail** | depends wholly on black bg; won't survive light/clear/tinted; not layered |
| 11 | Personality | pass | strong nameable device set; far from template glyph-on-gradient |
| 12 | No-text | pass | no words, no UI, no photo (grain is texture) |

**Score: 10/12 — failures on #3 and #10.** As a *shipping* third-party icon it is characterful and high-contrast; as a *generation target* it would not clear the bar (#3 is one of the non-negotiable 1–4), so its moves are worth quoting only with a real silhouette added and a layered, appearance-aware build.

## Rhymes with (hint for synthesis)
- Dark-ambient / spatial-audio / meditation icons — the Siri-orb and audio-visualizer lineage: an abstract emissive form floating on void black (family neighbours: Endel, Dark Noise, Oak, Portal-class ambient apps). Explicitly *not* the Big Sur tool-on-gradient tradition, and not Liquid Glass layered glass.

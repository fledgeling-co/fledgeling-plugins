# SYNTHESIS — 532-icon corpus (500 macosicongallery + 32 Apple Tahoe captures)

> Aggregated 2026-08-07 from a 500-icon macosicongallery census (2022-02 → 2026-07) and 32 ground-truth macOS 26 captures. **Only the captures are bundled here:** `apple-2026.md` plus the 32 tiles in `apple-2026/`, upsampled to ~512px so a raster engine can take them as style references. The gallery census below is a **finding retained from that analysis**, not a corpus this plugin can re-open — its 500 source PNGs were deliberately dropped, because at 256px they are 27 MB that cannot do the style-reference job the captures were upsampled for. Per-app evidence for the exemplar roster is being consolidated as `exemplar-index.md` in the sibling `mac-design-studio` skill (diolog-plugins), one line per app naming its era and the single move it demonstrates — **not bundled here**, and not a path this plugin can open.

## Era census (n=500 gallery)

| era | n | share |
|---|---|---|
| big-sur | 232 | 46% |
| skeuomorphic | 89 | 18% |
| liquid-glass | 93 | 19% |
| flat-brand | 53 | 11% |
| custom-web | 33 | 7% |

**Adoption timeline (the load-bearing finding):** liquid-glass is ~0% of the gallery through 2024 (batches 7–10: 0/200). First trickle mid-2025 (batches 5–6: 13/100). The macOS 26 Tahoe release wave, Nov 2025, spikes to **64/100** (batches 3–4, dominated by Apple's own system set — batch-04 alone is 43/50). Then the 2026 indie tail (batches 1–2) falls back to **16/100**. Read: **Apple has fully moved; third parties have not.** A generated icon that authentically wears Tahoe gel-glass still beats the overwhelming majority of the 2026 shipping field — the same conclusion the original 134-icon corpus reached, now confirmed at 4× the sample and with the system-set answer key in hand.

## The two eras' fingerprints (cross-batch consensus)

**Tahoe / Liquid Glass (target)** — consistent across Apple's Nov-2025 system set, the Feb-2026 pro-app refresh, the Microsoft Office refresh, and the best indies (darkroom, elytra, mindnode, multi, dropzone-5):
1. Two ground registers only: **porcelain near-white** carrying a colored gel object with a soft cast shadow, or **saturated single-hue vertical-gradient gel tile** carrying a **white frosted glyph**. (Dark charcoal is the pro/system minority register, carrying tinted glass or emissive marks.)
2. The tile itself is a cushion — inner rim light, gentle edge vignette, never a dead-flat print.
3. Glyphs are **frosted/tinted translucent gel**: the ground's hue visibly bleeds through white objects; rim highlights and internal luminance replace outlines and hard drop shadows.
4. **Authored overlap is the era's signature craft moment** — where glass crosses glass the junction visibly blends (additively lightens or multiplies darker): App Store's sticks, Shortcuts' diamonds, Photos' petals, QuickTime's Q, Weather's sun-through-cloud, Game Center's bubbles.
5. One soft top light; zero hard lacquer speculars; emissive interiors under glass are the sanctioned second light (Siri orb, Tips bulb, Home's glow, Activity Monitor's trace).
6. Legacy brand marks are **re-materialised, not redrawn** — silhouettes kept, material swapped (News N, Slack pinwheel, Keynote, the whole iWork set).
7. 3D object miniatures survive in matte-satin/clay with real contact shadows (loupe, tower, calculator, binoculars) — never chrome-gloss.
8. Sanctioned garnish: micro diegetic engraved text (Mail's address, "PREVIEW 10×"), ultra-low-contrast patterned grounds (blueprint grid, sparkle stars), edge-bleed devices treating the mask as a physical object boundary (Contacts' tabs, photo-printer's slot).
9. Radical flat abstraction is tolerated only when the artifact silhouette is iconic (Calendar's dot-matrix, Notes, Clock).

**Big Sur (the lagging default)** — saturated gradient squircle + one rendered hero object, top-down baked light, glossy/candy gel, diagonal tools, stuffed folders, blueprint dev-tool costume. Competent, everywhere, and now visibly previous-generation. Hard gloss sweeps, lens flares, metal bevel frames, and baked photo texture are instant "old" tells.

## Batch-04's explicit warning for generators

Rendering the white-object-on-hue formula **without the translucency cues** — ground-hue bounce into the white, rim light, frosted underlay showing the ground through thinner areas — produces a flat Big Sur re-tread, not a Tahoe icon. The cues ARE the era.

## A-grade exemplar roster (cite these when designing)

- **Layered translucency masters:** Apple Shortcuts, App Store, Photos, Game Center, Configurator, Finder (opaque-vs-frosted split face), Contacts (frost over colored tabs); indie: mindnode, multi (refraction under a cursor, 2023!), darkroom, WhisperType, elytra.
- **Porcelain-ground + gel object:** Safari, News, Slack, Reminders, Find My, Home, ChatGPT-knot; indie: iA Writer (caret-as-mark), CleanMyMac (wiped-glass specular performs the product), copilot, pasta, parcel (all-warm clay), mercury-weather (frosted cloud, 2023).
- **Saturated tile + white frost:** Mail, App Store, Weather, Keynote, Messages/Phone/FaceTime formula, Games' rocket (pink bounce-light underside).
- **Dark-ground discipline:** Passwords, Icon Composer, Activity Monitor (neon trace), Instruments (emissive wireframe), flighty (x-ray technical drawing), prompt-3/codepoint (emissive dev marks).
- **Concept/metaphor perfection:** CleanShot X (page-curl enacts capture), PDF Squeezer (machine squeezes the format), unfolder (3D→papercraft nets), betterzip-6 (archive as bound bundle), PixelGriddle (pixel-grid waffle), hex fiend (crowbar through hex dump), TablePlus (facet-plane shading), klack (one keycap), Octavo (museum skeuomorph, one red accent), Plugin Station (plug→plugins), corridorkey (chromatic dispersion in a glass sphere), Couverture (name told in chocolate viscosity), The Unarchiver (matte cardboard honesty), Dropzone (hover-stack diagrams the behaviour).

## Failure modes (recurring across all 10 batches — the anti-checklist)

1. Template genericism: saturated gradient + stock gel glyph/checkmark/magnifier/wrench with no ownable idea.
2. White-on-hue without translucency cues (the flat re-tread; see above).
3. Tone-on-tone silhouette collapse (blue-on-blue, navy-on-navy) — glyph dissolves into ground.
4. Baked text, wordmarks, screenshots, or data tables — dead at Dock sizes (exception: sub-legible diegetic engraving).
5. Metaphor pile-ups: 3+ props/ideas per tile that never resolve into one object.
6. Legacy-era drag: hard gloss sweeps, lens flares, Aqua glass, heavy metal bevel frames, page curls, freeform overhangs.
7. Photo/photoreal texture that bakes to mud at 32px; game key-art transplanted with zero macOS grammar.
8. Sibling-SKU non-differentiation; Apple-template mimicry (blueprint dev costume) with nothing owned.
9. Rainbow without semantics — multi-hue is earned only by data/color-domain meaning, then quarantined inside one shape.
10. Flat pre-masked raster delivery — identity as a colour relationship that dies under Dark/Clear/Tinted (the #10 epidemic, unchanged).

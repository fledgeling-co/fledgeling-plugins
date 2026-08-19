# Icon: Backdrop

- **Era:** Liquid Glass (atmospheric / moody interpretation) · **Rubric:** 11/12 (4 soft passes, 1 failure) · **Digested:** 2026-07-19
- **Source:** macapp.supply / user · **Subject:** Utility — "Stunning live wallpapers to your Mac desktop" (Cindori Backdrop)
- **Resolution caveat:** 204×204 **WebP** web render (Apple masters at 1024). This is a small source — the value ramp inside the droplet reads cleanly, but specular micro-structure, refraction detail, and true Icon-Composer per-layer glass separation are **not verifiable**, only inferred. The file's corners are baked **opaque white** (alpha=255 everywhere), i.e. the squircle was flattened onto white for the web — so the mask discipline of the real full-bleed layers cannot be confirmed, only that the composition sits well inside the mask. All hexes are `(measured)` from the render but treat as low-res approximations.

| Dimension | Reading |
|---|---|
| Background | Dark navy **radial vignette** `(measured)` — lifted at top `#272E45`/`#232535`, settling to `#1B1D2C` at the edges, darkest at the bottom corners `#13141D`, with a faint purple lift under the drop `#221530`. Near-black, single cool (navy ~225°) family; not the Big-Sur sky-ramp (light-at-top) — a moody floor for a self-lit object |
| Glyph | A **water droplet / teardrop** (pointed tip up, round bulb below), translucent glass, optically centred horizontally; mass sits centre-to-low (tip ~22% down, bulb base ~83%). Carries a vertical **iridescent ramp**: cyan tip `#B6F5F9` → sky blue `#91C9FA` → periwinkle-violet `#9675EE` → purple `#CE81E0`/`#9958EC` at the flanks → warm magenta-pink `#EB9AF3` and peach `#F3BAAB` in the bulb |
| Overlay device | None — no diagonal tool, badge, or frame. The luminous drop *is* the whole composition |
| Light model | **Self-illuminated / internal luminescence** — the droplet glows from within and casts a soft outer **bloom** (halo of lifted navy `#1A1C2D`) into the dark field; the cyan tip reads as the specular/refraction highlight. No top-down cast shadow — the light comes from the object, not from above. One coherent atmospheric model |
| Layer stack | 1) dark navy radial-vignette field → 2) soft outer bloom/halo around the drop → 3) the iridescent translucent glass droplet (own cyan→pink vertical ramp) → 4) implied specular sheen at the cyan tip |
| Palette economy | **Deliberately high hue count** — the droplet sweeps ~4–5 hue families (cyan→blue→violet→purple→magenta→peach) as a single oil-slick/holographic material. Background is desaturated near-black, so the intent-clause (saturation reserved for the focal object) holds strongly — but the ≤2-family guideline is exceeded on purpose. See Failures |

## Signature devices
- **Iridescent glass droplet** `[GOLDEN-NUGGET]` — a single translucent teardrop carrying a full cyan→magenta spectral sweep, reading as oil-slick / holographic refraction through water. The entire brand lives in this one object; the multi-hue ramp *is* the promise of "colourful live wallpapers."
- **Self-lit bloom on near-black** — no top-down lighting; the drop glows and blooms into a dark navy vignette. This is what pushes the reading from Big-Sur opaque-object toward an atmospheric glass/liquid material.
- **Aurora vertical ramp** — cool at the tip (cyan/blue), warming to magenta/peach at the bulb, the way light disperses through a hanging water drop. Thermal-vertical, not radial.
- **Name-as-glyph pun** — "Backdrop" → a **drop**; the literal object puns the name while the iridescence stands in for the wallpapers. Indirect subject communication (a droplet doesn't say "wallpaper" — it says colour + liquid + fluid), carried by association, not depiction.

## Failures
- **#6 Palette economy — FAIL (as signature).** The droplet objectively spans ~4–5 hue families (cyan `#B6F5F9` → violet `#9675EE` → magenta `#EB9AF3` → peach `#F3BAAB`); the rubric's ≤2-hue-family guideline is exceeded and no framing changes the count. Recorded as a failure for measurement honesty — but per the defect/signature test it is **systematic, purposeful, and accessible**, so it is a *signature that costs a rubric point*, not a defect. A generating AI should learn: a multi-hue focal object on a desaturated field is a legitimate move, not an automatic error.

**Soft passes** (pass, but flagged for synthesis):
- **#10 Variant robustness** — the icon's *meaning* is hue-encoded (colourful wallpapers = the spectral ramp). Under tinted/mono system variants the gradient collapses to a single tint; the droplet **silhouette + luminance** survive (bright drop on dark), so it doesn't break, but the communicated identity thins to a plain teardrop. Borderline for an icon whose job is to advertise colour.
- **#4 16px squint** — silhouette holds and stays nameable as a glowing drop; the internal cyan→pink detail smears to a generic soft multicolour bloom at menu-bar size. The shape carries it.
- **#2 Grid** — horizontally optically centred; mass is centre-to-low and the tall narrow teardrop is not geometrically centred (tip-heavy shapes balance this way, but noted).
- **#8 Depth coherence** — layer order reads sensibly (vignette → bloom → drop → sheen), but true glass layering / refraction at this material can't be verified at 204px; extrapolated.

## Rhymes with
- Dark-field **single-luminous-object** icons; **holographic / iridescent-gradient** icons (oil-slick, aurora); glass/liquid **blob-or-orb** material icons where one translucent object glows on near-black. Style-family hint only — no ≥3-icon cluster confirmed yet; flag for synthesis as a possible "aurora-gradient / dark-atmospheric" family alongside any other dark-glow icons in the corpus.

## Cross-icon / brand notes
- **Palette coherence with cover:** the cover is a dark violet/navy field carrying a MacBook whose wallpaper runs blue→pink iridescent, plus a lock-screen tag in cyan→purple. The icon's cyan→magenta droplet is the exact same spectral vocabulary compressed into one object — **tight coherence**. Brand = iridescent blue-to-pink deployed as a glowing focal object against a dark cool ground; the icon is a faithful miniature of the product's core show (vibrant colour on dark desktop).
- **Era honesty:** classified Liquid Glass on the translucent/refractive/self-lit reading, but this is an *atmospheric* take (dark, bloomy, self-illuminated) rather than the crisp multi-layer Icon-Composer specular look — it could equally be logged as **custom** brand direction. Recorded liquid-glass with custom as the honest adjacent reading.

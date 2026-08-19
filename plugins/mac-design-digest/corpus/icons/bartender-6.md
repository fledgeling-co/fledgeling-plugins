# Icon: Bartender 6

- **Era:** skeuomorphic (genuine photoreal; enum-mapped to `skeuomorphic-quote`) · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, 1024², converted to PNG) · **Category:** Utility
- **⚠ Provenance mismatch — read before trusting this digest:** the file served as Bartender 6's icon is the **legacy photoreal black-tuxedo** icon, *not* the app's current shipping icon. `cover.png` (icon at left) shows the real Bartender 6 icon: a Big-Sur/Liquid-Glass **squircle with a white, soft-embossed monochrome tuxedo**. This digest characterises the legacy artefact honestly and must not stand in for Bartender 6's actual Liquid-Glass icon (see Notes).

| Dimension | Reading |
|---|---|
| Background | Full-bleed dark vertical ramp #313131 (top) → #131313 (bottom) — not a distinct field; the jacket/shoulders *are* the background (photoreal scene, edge-to-edge) `(measured)` |
| Glyph | `object` — a black tuxedo torso, vertically symmetric about the shirt placket (x≈0.50), filling the entire frame with no safe-zone margin. Shirt #F0F0F0→#ECECEC, bow tie/buttons #090909–#252525, satin lapel #545454, waistcoat #3D3D3D, jacket #262626 `(measured)` |
| Overlay device | none (no diagonal tool / badge / frame) |
| Light model | Single top-down soft studio key: broad soft highlight down the shirt placket, specular sheen on satin lapels, short soft contact shadows under buttons and bow tie. One consistent photographic light `(measured)` |
| Layer stack | dark environment ramp → jacket body + satin lapels → navy pen tucked at right pocket → white shirt front → waistcoat V + lower button → three cross-stitched shirt buttons → black bow tie (frontmost, top) |
| Palette economy | Effectively achromatic (black/grey/white) + **one** desaturated-navy accent (the pen, #2C3444). ≤2 hue families; accent reserved for a single focal detail — textbook economy |

## Signature devices
- **Tuxedo-as-mascot** — the app's "menu-bar butler / maître d'" concept rendered literally as formalwear. The single strongest thing about the icon: subject *communicates function* (Bartender organises your menu bar the way a bartender/butler organises a room).
- **Photoreal material contrast** — glossy satin lapel sheen played against matte cotton shirt; the whole icon's tactility lives in that one material juxtaposition `[GOLDEN-NUGGET]`.
- **Cross-stitched black buttons** as focal detail, each with its own micro-shadow.
- **Lone desaturated-navy pen** — the only chromatic note in an otherwise monochrome field; accent-as-jewelry, not accent-as-CTA.
- **Vertical mirror symmetry** about the placket — gives the object icon a stable, formal, "buttoned-up" posture.

## Failures
- **#1 Mask discipline** — artwork bleeds to all four edges; the bow tie is **clipped at the top edge** (non-background pixels at y=1) and there is no squircle safe-zone margin. Designed as a filled object, not for the system squircle. (Partly a crop artefact — see Notes — but nothing in-frame is mask-aware.)
- **#3 Silhouette test** — filled solid black it collapses to an amorphous dark rectangle: jacket + dark background are one mass. The subject reads *only* through internal tonal contrast (the white shirt V), never through outline.
- **#7 Figure-ground contrast** — jacket #262626 on background #313131 measures **1.16:1**, far under the 3:1 floor; the dark tux nearly merges into the dark ground. Only the white shirt (11.4:1 vs ground) separates figure from field.
- **#10 Variant robustness (Liquid Glass)** — a flat photoreal raster with no layer separation. A tinted / clear / dark system render would destroy the baked tonal modelling it depends on; it cannot survive the current-era appearance matrix.

## Soft passes (scored pass, flagged)
- **#2 Grid adherence** — cleanly optically-centred and mirror-symmetric on the placket axis, *but* it fills the frame with no Apple-grid safe zone; passes on centring, not on margin discipline.
- **#4 16px squint test** — the bow-tie + white-V gestalt survives to menu-bar size and still reads "formalwear"; buttons, pen, and satin sheen all smear away. Gestalt yes, detail no.
- **#12 No-text check** — free of words/UI, but the **photoreal rendering** runs against current HIG ("prefer illustrations to photos") — native for its own skeuomorphic era, anti-pattern for today's.

## Clean passes
- **#5 Single light model**, **#6 Palette economy**, **#8 Depth coherence** (layer order and contact shadows are physically plausible; no z-fighting), **#9 Era coherence** (every device is one coherent skeuomorphic language), **#11 Personality** (an unusually on-concept, memorable device).

## Rhymes with
- **Classic macOS skeuomorphic object-icons** — literal real-world objects in photographic materials (the felt/leather/wood/glass lineage: early Calendar, Game Center, Reminders, indie-era Transmit/Coda). Instantly kin to that pre-Yosemite family.
- **Forward rhyme:** its own successor — the white soft-embossed Bartender 6 squircle in `cover.png` — carries the tuxedo signature into the **soft-monochrome Big-Sur relief** family (tone inverted black→white, materials swapped photoreal→gentle emboss). *Hint for synthesis; confirm when that icon is digested directly.*

# Leafy: Vocabulary Builder for Mac — profile

- **Source:** macapp.supply (`leafy-vocabulary-builder-for-mac`) · **Surfaces digested:** none (no app UI supplied — see below) · **Last updated:** 2026-07-19
- **One-sentence identity:** Unresolvable from evidence — the supplied assets show a brand identity at war with itself (a crude neon-graffiti app icon beside a refined high-contrast editorial serif wordmark), but not a single frame of the actual application.
- **Cluster:** unassigned (no UI evidence)
- **Lineage:** unknown (low) — no window chrome, controls, or content surface appears in either input; framework lineage is undeterminable
- **Era (chrome):** unknown for the app UI. The *icon* reads legacy-skeuomorphic (glossy top-lit gradient, hand-painted artwork) rather than current Big Sur / Liquid Glass icon grammar — but that is icon (Workflow B) evidence, out of scope for this UI digest.

## Evidence inventory (what was actually supplied)

Two files, both brand material, neither an app screenshot:

1. **`cover.png` — 1200×630 marketing composite.** Standard Open-Graph / social-share ratio (1.90:1), not a window capture. Contents: pure-black backdrop (`#000000` measured), the app icon centred-left with a faint green radial glow bleeding beneath it, and the wordmark "Leafy" set in a high-contrast display serif in near-white to its right. No traffic lights, no toolbar, no sidebar, no content — **zero app UI**.
2. **`icon.png` — 180×180 app icon.** Low-resolution (a real @1x/@2x macOS icon master is 512–1024px), so all icon colour values are `(estimated)`. Rounded-square with a glossy charcoal→near-black gradient and hand-drawn bulbous lime-green "LEAFY" lettering slashed by a diagonal leaf-stem/key stroke (a "LEAF-KEY" pun echoing the `⌥A` hotkey in the tagline).

The gallery array in `meta.json` is empty. **No UI surface exists to classify for lineage/era or to run the 14-point rubric and 10-point native-tells audit against.** Everything below is brand evidence, explicitly not app-UI canon.

## Tokens

Brand-layer only. None of these are UI-control tokens (no controls were seen). Provenance is honest about the low-res icon and the compressed cover.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/icon-green | ~#A6EE54 (avg RGB 166,238,84; range R107–203 G151–255 B52–157) (estimated)(inferred) | icon.png @180px | Bright chartreuse/lime; the sole identity hue |
| brand/icon-bg | charcoal→near-black gradient, ~#2D2D2D top → ~#131313 base (estimated)(inferred) | icon.png | Top-lit gloss = legacy skeuomorphic light model |
| brand/backdrop | #000000 (measured)(inferred) | cover.png corners | Pure black cover ground — harsh (see note) |
| brand/wordmark-ink | ~#F5F5F7 near-white (measured)(inferred) | cover.png | High-contrast display serif |
| brand/glow | very low-value green halo ~#0B0F04 under icon (measured)(inferred) | cover.png | Neon-on-black bloom |
| type/wordmark | high-contrast Didone/transitional display serif (Canela/Didot-class); descending swash `f`, curved `y` tail (estimated)(inferred) | cover.png wordmark | Editorial/luxury register |

## Layout skeletons

None — no application surface was supplied. The `cover.png` layout is a marketing lockup (icon left, wordmark right, centred vertically on black), not an interface.

## Signature moves

- **[GOLDEN-NUGGET] Register clash as (accidental?) identity.** The brand pairs two aesthetics that normally never meet: a *Playful/toy + terminal-neon* app icon (hand-drawn graffiti letterforms, acid lime on black) and a *Luxury/fashion editorial* wordmark (high-contrast serif with a descending `f` swash). This is the one memorable thing in the assets — but it reads as an unresolved brand rather than a deliberate high/low remix, because nothing mediates between the two. Recorded as brand observation, not UI taste.

## Defects

- **No UI evidence supplied** — the primary "defect" for corpus purposes: a marketing-only cover with an empty gallery. Cannot assess grid, hierarchy, native fidelity, accessibility, or lineage. Request actual app screenshots (main window / lookup popover / menu-bar extra).
- **Icon off current macOS grammar** (brand-level, not a UI defect, not counted toward canon): glossy top-lit gradient + raster hand-art is the pre-Big-Sur iOS idiom; current macOS icons use the flat-squircle / layered Icon Composer light model. Flag for a future Workflow B icon digest.
- **Contrast Dilution risk (cover)**: pure `#000000` ground with a near-`#000` icon background gives the icon almost no figure/ground separation except via the green glyph — the glow is doing all the lifting.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| (none) | n/a | No app UI window supplied — 14-point rubric and 10-point native-tells audit not applicable to a marketing composite or a bare icon |

## Notes for synthesis

Marketing-only inputs. Do **not** let brand-layer colours (acid green, black) leak into any UI cluster — they are logo palette, not interface palette. The tagline ("Press ⌥A to lookup any word on mac, auto save in vocab") implies a menu-bar-extra + lookup-popover utility, but that is inference from copy and must not be recorded as design evidence. This app cannot advance the corpus until real screenshots arrive.

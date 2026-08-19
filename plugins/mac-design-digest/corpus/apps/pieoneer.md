# Pieoneer — profile

- **Source:** macapp.supply (`sources/pieoneer/`) · **Surfaces digested:** none (no app UI supplied) · **Last updated:** 2026-07-19
- **One-sentence identity:** A glossy obsidian-chrome utility icon — a camera-aperture "pie" pun on the name, rendered skeuomorphic in a Liquid-Glass world; icon/brand evidence only, **no UI seen**.
- **Cluster:** unassigned (no UI evidence to cluster on)
- **Lineage:** unknown (low) — cannot be classified: the inputs contain no window, chrome, controls, or text. Framework lineage is unrecoverable from an icon. Nothing here may feed macOS UI canon.
- **Era (chrome):** not observable (no app chrome). **Icon aesthetic:** skeuomorphic glossy-3D (legacy/custom) — pre-flat, off-platform for the macOS 27 / Liquid Glass icon grammar.

## Input reality (read this first)

The `sources/pieoneer/` folder ships exactly two images, and both are **the same subject — the app icon**:

- `cover.png` (1920×1080) — a **marketing composite**: one large 3D render of the app icon, centred on a gray radial-gradient backdrop with visible film grain and a corner vignette. No app window is embedded. The backdrop + render treatment is **brand evidence**; there is no design evidence of the application UI.
- `icon.webp` (204×204) — the shipping **app icon** itself, flatter than the hero render.

`meta.json` `shots: []` — no screenshots exist. Per the covers rule (analyse the window inside a composite, never the backdrop), there is **no window to analyse**. This profile therefore records the icon and the marketing backdrop only, and explicitly withholds every UI/native judgement. The tagline ("Switch, launch, and control apps") is marketing copy, not evidence — but it does explain the motif (see Signature moves).

## Tokens

All tokens below describe the **icon and its marketing backdrop**, not any UI. Values are `(measured)` from pixel samples where noted, else `(estimated)` from the render.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| icon/tile-fill | near-black `#000000`→`#181818`, high-gloss | (measured)(inferred) | shipping webp: corner `#000`, body `(24,24,24)`; obsidian, not matte |
| icon/tile-silhouette | rounded-square (squircle) | (estimated)(inferred) | flat squircle in the webp; **inflated to a 3D pillow** in the cover render |
| icon/glyph | camera aperture / iris "pie", ~7 tapered chiral blades + open centre | (estimated)(inferred) | silver metallic, beveled rims, subtle top-bright gradient; sweeps clockwise |
| icon/glyph-fill | silver→white `#C5C5C5`→`#F1F1F1` | (measured)(inferred) | webp blade `(197,197,197)`; cover blade `(241,241,241)` |
| icon/palette | fully achromatic (black + silver + white) | (measured)(confirmed) | R=G=B at every sample; **zero hue by choice** |
| icon/glyph-diameter | ~55–60% of tile width | (estimated)(inferred) | aperture optically centred, fills the tile face |
| icon/light-model | top-lit glossy specular + soft bottom reflection | (estimated)(inferred) | skeuomorphic 3D; specular sheen across upper third |
| brand/backdrop | gray radial gradient, center `~#AFAFAF` → corners `~#404040` | (measured)(inferred) | desaturated; film-grain noise + corner vignette |
| brand/composition | single object, dead-centre, ~32% of frame width | (estimated)(inferred) | icon-as-hero; no headline, no device frame, no UI |

## Layout skeletons

None. No UI surface was supplied, so there is no toolbar / sidebar / content region / inspector to skeleton. The only composition present is the marketing cover: a single centred icon render on a radial-gradient ground (hero-object layout, not an app layout).

## Signature moves

- **[GOLDEN-NUGGET] The name is the glyph.** "Pie·oneer" → a camera **aperture / "pie" of blades**. The iris doubles as the visual for a radial/pie-menu app-launcher ("switch, launch, control apps"): the blades are the pie-menu wedges. Motif and product concept are one decision — the strongest thing in the whole submission.
- **Committed monochrome.** Black tile + silver glyph, **no hue anywhere**. In a corpus era where the platform palette is 12 saturated system hues, choosing full achromatic is a deliberate, disciplined identity stance — mechanical, tool-like, restrained.
- **Chrome-on-obsidian material story.** Glossy black pillow + beveled silver metal reads as a precision instrument (a lens barrel, a machined dial). It borrows the *aesthetic-usability* halo of a polished physical object.

## Defects

These are **icon/brand** observations (no UI exists to carry UI anti-patterns):

- **Off-era for the platform** → glossy skeuomorphic 3D on a macOS 27 / Liquid Glass system → current icon grammar is flat, layered translucent glass authored in Icon Composer (1024² flat canvas, front-facing, no baked gloss). This render reads dated against the platform. *Judgement:* deliberate house style, but a lineage/era mismatch a redesign would likely resolve.
- **Cover pillow-inflation** → the hero render bulges the squircle into a 3D pillow with wrap-around gloss → breaks Apple's flat, front-facing icon convention. Marketing-render artifact; the shipping webp is flatter and closer to convention.
- **Motif information-scent mismatch (Jakob's Law)** → a camera aperture trains the "photo/camera app" schema, not "app switcher/launcher" → first-glance meaning may misdirect. The pun rewards the informed, but costs the cold-open user a beat of recognition.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.png (marketing icon render — **no app UI**) | n/a | 14-point UI rubric and 10-point native-tells audit are **inapplicable**: no window, chrome, text, controls, or layout to score. Composition-only read: single centred focal object, clean figure-ground, achromatic discipline — competent as a hero, but not a UI. |

> **Corpus note:** Pieoneer contributes **icon/brand evidence only**. It must not be counted as a digested *app UI*, must not feed a style cluster, and must not promote any UI/native canon. If UI screenshots surface later (this looks like a menu-bar or global-hotkey radial-launcher utility), re-digest under Workflow A and supersede this profile's UI section.

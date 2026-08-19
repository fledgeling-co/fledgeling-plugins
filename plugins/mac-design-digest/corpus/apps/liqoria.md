# Liqoria — profile

- **Source:** macapp.supply (cover composite + icon only; no in-app gallery shots) · **Surfaces digested:** floating now-playing mini-player (HUD panel), 1 surface · **Last updated:** 2026-07-19
- **One-sentence identity:** A streaming aggregator (Apple Music / Spotify / YouTube) that presents itself not as a windowed library app but as an ambient Liquid Glass now-playing HUD — the macOS Control Center "Now Playing" tile grown into a standalone product, with a per-source badge as its only chroma.
- **Cluster:** unassigned (candidate: *liquid-glass-ambient* — system-vibrancy HUDs)
- **Lineage:** native (med confidence) — Liquid Glass material, SF Symbols transport, secondary-label de-emphasis all read AppKit/SwiftUI Tahoe-era; confidence capped because the only evidence is an idealized marketing render of one chromeless surface, not a literal windowed screenshot.
- **Era (chrome):** Liquid Glass native (macOS 26+/Tahoe). NB the **app icon contradicts this** — see Brand context.

## Evidence caveat
The single UI artifact is the floating player card composited over a pink/lavender floral Tahoe wallpaper on a "Touch ID or Enter Password" lock-screen backdrop. The card is the design evidence; the wallpaper, lock-screen text, and drop shadow are brand/backdrop and are not conflated with it. No main window, library, sidebar, toolbar, settings, or service-picker surface is shown — the corpus learns Liqoria's *ambient* face only, not how it browses a catalog. All pixel values are `(estimated)` from a downscaled 964×578 composite; proportional relationships are more trustworthy than absolute px.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| material/panel | Liquid Glass — translucent, wallpaper lenses through, bright refractive rim highlight tracing every edge | (estimated)(inferred) | Glass on a *floating functional layer* (mini-player HUD) — glass-correct per the golden rule; content within (album art) stays opaque |
| radius/panel | large continuous rounded-rect, ≈ panel-height / 8–9 (~28–34px in composite space) | (estimated)(inferred) | reads as concentric parent for album art |
| radius/album-art | rounded square, concentric child (~10–14px composite) | (estimated)(inferred) | steps down from panel radius — concentric discipline present |
| type/title | "Headlights" bold white, ~17–20pt-equiv | (estimated)(inferred) | Title2/Title1-class emphasized; anchors hierarchy |
| type/artist | "Alex Warren" regular, secondary/vibrant white ~55–70%, ~14–15pt-equiv | (estimated)(inferred) | de-emphasis via weight + opacity, not size alone |
| type/time | "1:19" / "2:53" ~13pt-equiv secondary white | (estimated)(inferred) | flank the progress capsule |
| label/color | vibrant WHITE labels over glass (over-glass duality), no dark-ink tier used | (estimated)(inferred) | this is the kit's "Over-glass" vibrant-white treatment, not content-area ink |
| accent/app | **none** — controls are monochrome white on glass | (measured)(inferred) | zero app accent; recessive controls are vibrant white, not tinted — correct native restraint |
| accent/source-badge | Spotify green (`~#1DB954`) circle badge, bottom-left of album art | (estimated)(inferred) | identity color for the *streaming source*, not the app accent — behaves like a calendar dot / chart-series hue |
| control/transport | backward.fill · pause.fill (center, emphasized) · forward.fill — white SF Symbols, borderless, evenly spaced | (estimated)(inferred) | pause is the single emphasized control (Von Restorff) |
| control/progress | thin capsule track; solid-white filled portion, translucent-white remainder; no visible knob | (estimated)(inferred) | filled/unfilled contrast is low over light glass — see Defects |
| glyph/nowplaying | white equalizer/waveform bars, top-right | (estimated)(inferred) | "now playing" affordance |
| chrome/window | none — chromeless HUD, no titlebar, no traffic lights | (measured)(inferred) | legitimate for a floating panel/HUD; not a faked frame |

## Layout skeletons

**Floating now-playing HUD (sole surface).** One horizontal glass card, loose density.
- Left region: album-art tile (opaque rounded square, source badge overlaid bottom-left corner).
- Upper-center: two-line stack — title (bold) over artist (secondary), left-aligned; equalizer glyph pinned top-right on the same baseline band.
- Mid band: full-width progress capsule with time labels flanking left/right, insets aligned to the title's left edge and the card's right padding.
- Lower band: three transport glyphs centered as a peer group, generous inter-glyph spacing, center (pause) emphasized.
- Vertical rhythm: title/artist tight-coupled; progress and transport each their own separated band (Gestalt proximity honored).

## Signature moves
- **[GOLDEN-NUGGET] The aggregator-as-ambient-glass-widget.** Liqoria's whole product face is a chromeless Liquid Glass now-playing panel rather than an iTunes-style windowed library — it collapses "which service is this?" into a single per-source badge on the album art and keeps everything else pure white-on-glass. The boldness budget is spent entirely on the material; every control stays quiet.
- **Single-chroma discipline.** Exactly one color moment (the Spotify-green source badge) against an otherwise monochrome white-on-glass field. This is textbook accent restraint — the source identity reads instantly because nothing else competes.

## Defects
- **Contrast Dilution / glass-legibility risk (rubric #9).** Vibrant-white *secondary* labels (artist "Alex Warren", the time stamps) sit over a light pink/lavender translucent glass; in the brightest wallpaper regions the ratio likely dips below 4.5:1. The bold white title survives on weight; the thin secondary text is the exposed edge. Canon fix: a stronger material darkening/scrim under the label band, or a dark-vibrant fill behind text, so legibility doesn't depend on the wallpaper behind the glass.
- **Low UI contrast on the progress track (rubric #10, borderline).** The unfilled (translucent-white) portion vs the light glass reads near or below 3:1 — the remaining duration is hard to gauge. Canon fix: give the unfilled track a defined recessive fill tier rather than relying on translucency.
- **Not a defect but a finding — Jakob's-Law proximity to the system tile.** The card is close enough to macOS's own Control Center "Now Playing" module that its native-ness doubles as anonymity: little here distinguishes it from the OS widget except the source badge. Legitimate as a familiarity play; worth noting the app buys instant comprehension at the cost of a distinct visual identity.

## Brand context (icon — not a UI surface, Workflow A scope)
- The app **icon** is a glossy grayscale "play" orb — a beveled silver/white circular button with a specular highlight and a charcoal play triangle, on a pale glossy rounded-square. This is a **legacy skeuomorphic** treatment (Web-2.0 / iOS-6-era glossy media-player button), fully desaturated, following neither Big Sur squircle-material conventions nor Icon Composer / Liquid Glass layering. It reads dated and generic ("stock media player"). **Contradiction worth recording:** the app's face is dated while its UI is current-native — the icon undersells the glass product it opens.

## Rubric history
| Surface | 14-pt Rubric | 10-pt Native audit | Failures |
|---|---|---|---|
| now-playing HUD panel | 12/14 | 8/10 (2 N/A: selection grammar, sidebar headers) | #9 white secondary labels over light glass likely <4.5:1; #10 unfilled progress track vs glass borderline <3:1 |

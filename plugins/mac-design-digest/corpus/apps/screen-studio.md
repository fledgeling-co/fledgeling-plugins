# Screen Studio — profile

- **Source:** macapp.supply (cover composite only) · **Surfaces digested:** editor main window (dark) — from marketing cover · **Last updated:** 2026-07-19
- **One-sentence identity:** Descript's cinematic timeline confidence applied to screen recordings — a near-black creative-tool chrome built so the vivid, wallpaper-padded canvas is the only thing that glows (peers: Descript, CapCut, Final Cut Pro's dark editor, CleanShot X).
- **Cluster:** unassigned (proposed: `dark-creative-pro` / "editor-noir")
- **Lineage:** native (med-high) — genuine coloured traffic lights, near-black AppKit chrome, centered window title, borderless SF-Symbol toolbar button, arrow-cursor platform; the editor body is a heavily custom-drawn creative-tool surface (canvas + timeline) layered on native chrome. Non-native evidence: none observed. The Linear-looking UI *inside the canvas is recorded content, not Screen Studio's own UI* — excluded from all readings below.
- **Era (chrome):** big-sur-era native chrome (flat opaque near-black, rounded-rect ~8pt control bezels, no Liquid Glass) wearing a custom dark creative-tool theme; pre-Tahoe material language. Glass absence is legitimate for a pro tool, not a defect.

## Provenance caveat

Single surface, and it is a **marketing composite**: the app window bleeds off the right edge and sits at a **sub-1× render scale** (traffic-light coloured cluster measures ~41px where the native cluster is ~52–54pt → ~0.77× downscale). Every pixel value below is therefore `(estimated)` with wide ranges; where noted "(shown Npx)" the real-pt figure is ~1.3× the shown value. No settings, empty-state, light-mode, or focus-state evidence.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window-chrome | `#0C0D0F` (measured)(inferred) | | near-black, very slightly lifted from pure black — the whole app ground |
| bg/timeline | `#0C0D0F` (measured)(inferred) | | timeline lane shares the window ground; no separate panel fill |
| brand/backdrop | `#0A0A0A` (measured)(inferred) | | left marketing panel — **brand evidence, not app UI**; pure-black vs the chrome's lifted black |
| type/title | ~15pt (Title3-class) Semibold, white (estimated)(inferred) | | centered window title "New Recording" |
| type/control-label | ~13pt (Body-class) Medium, white (estimated)(inferred) | | "Auto", "Crop", clip labels |
| type/ruler | ~10–11pt (Footnote/Caption-class), secondary gray (estimated)(inferred) | | timeline time labels at 1.6s increments; low-contrast de-emphasis |
| accent/brand | `#4429F3` electric indigo (measured)(inferred) | | zoom-effect clip fill + indigo playhead; the app's **own** accent, NOT bound to system controlAccentColor |
| clip/recording | fill `#775500` dark gold, left-cap `#E5A000` bright amber (measured)(inferred) | | source-recording track segment; brighter amber "handle" cap on left |
| clip/zoom | fill `#4429F3` indigo, white label (measured)(inferred) | | zoom-effect segment; cursor-in-box leading glyph + sliders trailing glyph (opens effect settings) |
| radius/control | ~8pt rounded-rect (estimated)(inferred) | | Auto/Crop button bezels — rounded-rect, not macOS-27 capsule |
| radius/clip | ~6–8pt (estimated)(inferred) | | timeline segment corners |
| control/bezel | translucent white ~6–8% fill + hairline border (estimated)(inferred) | | Auto/Crop pills — very faint on black (see Defects, contrast) |
| control/height | ~28–32px shown → ~36–40pt real (estimated)(inferred) | | control-bar buttons; toolbar-tier height |
| track/height | ~33–34px shown → ~40–44pt real (estimated)(inferred) | | recording + zoom lanes; generous creative-tool rows |
| chrome/titlebar | ~38–40px shown, centered title, compact-unified-toolbar read (estimated)(inferred) | | single row: traffic lights + folder symbol (leading), centered title, empty trailing |
| toolbar/symbol | borderless monochrome SF Symbol (folder; transport ►◄) (estimated)(inferred) | | secondary-label tint |

## Layout skeletons

**Editor main window (dark)** — three horizontal bands stacked in one opaque near-black window:
1. **Title/toolbar band** (top, ~40pt): traffic lights + a borderless folder symbol at the leading edge; centered title "New Recording"; trailing empty. Hairline divider below.
2. **Canvas/preview band** (largest, center): the recorded window auto-zoomed, corner-rounded, drop-shadowed, and floated with generous padding on a **full-bleed colourful gradient wallpaper**; a rounded/squircle **webcam bubble** overlaps bottom-left; a dark rounded **caption panel** ("roadmaps or views. I can click") sits low-center with karaoke word-brightening.
3. **Control + timeline band** (bottom): a control bar with three alignment zones — leading group (Auto pop-up + Crop button), centered transport triad (rewind-to-start / play-in-circle / forward-to-end, borderless symbols), trailing fit/resize arrows; below it a time ruler (1.6s ticks) with an indigo playhead (line + round knob), then stacked tracks: amber **Recording Clip – 0:26s** lane full-width, and a zoom lane carrying two indigo **Zoom** segment pills.

## Signature moves

- **The padded-wallpaper canvas** — the recorded window is auto-zoomed, rounded, shadowed and floated with big padding on a vivid gradient backdrop. This *is* the product ("beautiful recordings") cashed out as an editor surface; the dark chrome exists to make it the sole light source. `[GOLDEN-NUGGET]`
- **Semantic timeline hue language** — segment colour encodes type: amber/gold = source recording, electric indigo = zoom/effect. Two glances tell you what every block does, with no legend. `[GOLDEN-NUGGET]`
- **Committed brand accent over the system accent** — indigo `#4429F3` drives zoom clips and the playhead instead of the user's `controlAccentColor`. A deliberate deviation from the native "accent is the user's" rule, systematic and purposeful (brand identity for a creative tool) → signature, not defect. It also matches the purple-gradient app icon.
- **Effect-as-content grammar** — zooms and captions are timeline objects with inline settings glyphs (the sliders icon on each zoom pill), not modal dialogs; editing effects means selecting a coloured block.
- **Near-black figure-ground discipline** — chrome, timeline, and control bezels are all within a few percent of `#0C0D0F`, so nothing competes with the canvas. Hierarchy is carried almost entirely by the two saturated clip hues and white/secondary-gray text.

## Defects

- **Contrast Dilution (UI, mild)** → the Auto/Crop control bezels are a translucent white ~6–8% fill with a hairline border on near-black; the border likely falls under the 3:1 non-text floor, so the buttons read as faint ghosts until hovered. Canon fix: lift the border to ≥3:1 or use a filled bordered-tinted bezel. (Consistent with the app's "recede everything but the canvas" logic, so a tasteful risk rather than sloppiness — but still a WCAG non-text miss.)
- **Ruler label legibility (borderline)** → ~10–11pt time labels in a low tertiary gray on black sit near the 4.5:1 small-text floor. Intentional de-emphasis, but at the edge.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| editor main window (dark, cover composite) | 12/14 | #10 UI contrast — faint control-button bezels likely <3:1; #14 focus appearance — no focused control visible, unassessable |

**14-point notes:** #1–3 grid/alignment/proximity pass (on-grid controls, evenly-spaced 1.6s ruler, grouped control zones); #4 modular scale pass (≈3 sizes: ~15/13/10–11pt); #7 de-emphasis pass (secondary ruler gray vs white titles); #8 action singularity pass (transport monochrome; play is the one emphasized control); #9 text contrast pass (white on near-black); #11 Fitts pass (~28–44pt controls, pointer platform, 24px floor); #5/#6/#12/#13 n/a (no paragraphs, inputs, or form labels in view).

**Native-tells audit: 7/10** — pass: #1 lineage (native chrome+symbols), #2 glass discipline (flat opaque, no glass-in-content, no glass-on-glass), #5 density (13pt-class labels, 28–44pt controls, desktop rows), #7 one prominent action, #8 concentric-ish corners, #9 borderless grouped toolbar symbols, #10 real coloured traffic lights (focused). Deviation: #6 accent bound to brand indigo, not the system accent (signature). n/a: #3 selection grammar & #4 sidebar headers — Screen Studio's own chrome has no source list/selectable list to judge (the sidebar in-frame is *recorded* Linear content).

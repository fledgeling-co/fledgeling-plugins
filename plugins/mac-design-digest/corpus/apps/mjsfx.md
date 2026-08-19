# MJSFX — profile

- **Source:** macapp.supply (mjsfx.app) · **Surfaces digested:** workspace window (hero + full), 4 marketing feature composites, brand cover · **Last updated:** 2026-07-19
- **One-sentence identity:** jsfxr/ChipTone's retro-SFX generator reimagined as a neon-dark synth workstation — Vital's instrument-panel density with a Vercel-dark marketing skin, wrapped in a *faked* Mac window.
- **Cluster:** unassigned — proposed non-native contrast cluster `neon-instrument-dark`
- **Lineage:** **web-electron (high confidence)** — non-native evidence; feeds contrast/aesthetic record only, never macOS canon.
- **Era (chrome):** custom (no macOS era) — flat dark web aesthetic; traffic-light frame is decorative, not system-drawn.

## Lineage determination (why web, not native)

Judged from the body, not the frame (macos-native-analysis §1). The marketing eyebrow literally claims "NATIVE MACOS · 8-BIT SOUND STUDIO" — treated as marketing copy, not evidence — and the body contradicts it on every native tell:

- **Faked window chrome.** Traffic lights are three flat monochrome discs `#8C8C8C / #8C8C8C / #515252` (measured) — grey, uneven, no red/yellow/green even in a hero shot where a real key window would be lit; title "MJSFX" is dimmed grey `#95989C` (measured). This is the classic web "draw three grey dots to evoke a Mac window" cliché, not a screenshot of an active `NSWindow`.
- **No native toolbar.** Content begins immediately under a plain ~35pt titlebar with a content-area segmented tab row (Analytical/Dominant/Blended). Native apps of this scale carry a unified toolbar with borderless SF Symbols; there is none.
- **Non-system typography.** UI numerics and labels are a **monospace** face (JetBrains/Plex Mono class, estimated); display is a **geometric grotesque** (Space Grotesk / General Sans class, estimated). No SF Pro anywhere — the single loudest native-absence tell.
- **Web control grammar.** Primary button is a Tailwind-ish blue `#2F6DF0` (measured) with a blue glow/bloom shadow — native buttons never glow, and macOS blue is the cyan-leaning `#0088FF`. Segmented toggles are dark tab-groups with one lighter selected segment + hairline border, not native capsule `NSSegmentedControl`.
- Custom canvas everywhere (rotary knobs, ADSR/LFO curve panels). Alone this is normal for audio tools; combined with the above it confirms a Web-Audio-API app in a decorative Mac frame.

Verdict: digested as **contrast evidence**. The audio-plugin skeuomorphism and the neon-dark aesthetic are the transferable learning; nothing here informs native macOS canon.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/backdrop-marketing | `#1D1119` → radial magenta/teal glows (measured)(confirmed) | | dark magenta-tinted hero canvas behind the window |
| bg/window-content | `#1C1F24` (measured)(confirmed) | | dark blue-grey; darker than native dark `#1E1E1E`, same family |
| bg/panel-card | `#282C31` (measured)(confirmed) | | elevated layer/effect cards, one tonal step up |
| bg/scope-inner | `#0D0F12` (measured)(confirmed) | | near-black oscilloscope / curve wells (recessed) |
| accent/primary-cyan | `#2EC6DA` (measured)(confirmed) | | knob arcs, active toggles, links, eyebrows; also the app-icon sine |
| action/save-blue | `#2F6DF0` (measured)(inferred) | | filled primary "Save" w/ blue glow — a *second* action hue |
| action/play-green | `#37C46E` (measured)(inferred) | | filled "Play" — a *third* action hue |
| identity/voice-pink | `#FF4E7E` (estimated)(confirmed) | | "zapper" layer dot + waveform trace |
| identity/voice-purple | `#6D7CFF` (estimated)(inferred) | | "swoosh" |
| identity/voice-green | `#3ECf6E` (estimated)(inferred) | | "digital dirt" |
| identity/voice-orange | `#FFA23E` (estimated)(inferred) | | "noise wave" |
| text/primary | `#F3F5F8` (measured)(confirmed) | | near-white, headline & values |
| text/secondary | `#8A8F98` (estimated)(confirmed) | | subheads, knob Title-case labels |
| text/label-micro | `~#6B7079` (estimated)(confirmed) | | tracked UPPERCASE micro-labels — low contrast, see Defects |
| type/display | geometric grotesque, Bold, ~64–80pt marketing (estimated)(confirmed) | | Space Grotesk / General Sans class |
| type/eyebrow | mono/geometric, ~11pt, UPPERCASE, ~+0.15em tracking, cyan/green (estimated)(confirmed) | | |
| type/ui-numeric | monospace Bold, ~15pt readouts (estimated)(confirmed) | | tabular value pills "1110" "1.36" |
| type/ui-label | Title case (knob labels) + tracked UPPERCASE (panel titles) (estimated)(confirmed) | | mixed casing system |
| radius/window | ~10–12pt (estimated)(inferred) | | rounded window corners |
| radius/card | ~10–12pt (estimated)(confirmed) | | layer & effect panels |
| radius/button | ~8pt (estimated)(confirmed) | | Save / segmented groups |
| control/segment-h | ~17pt (estimated)(confirmed) | | compact tab segments — below native 24pt Rg |
| control/knob-dia | ~20–23pt (estimated)(confirmed) | | rotary, cyan arc + white pointer |
| space/base | 8px grid, 4px micro (estimated)(confirmed) | | within-panel 4–6px label gaps; panel↔panel ~16px |

## Layout skeletons

**Workspace window (shot-6, shot-1 — same surface, full vs hero-cropped):** single-window, no sidebar. Top→bottom: (1) faux titlebar with grey traffic lights + "MJSFX"; (2) content-area toggle row — three segmented groups (analysis mode / scope type / render style) leading, elapsed-ms readout + a panel-toggle glyph trailing; (3) large oscilloscope well (near-black, per-voice colored traces overlaid, +/- zoom rail on the right); (4) full-width waveform strip + MUTATE/RANDOM + AUTO-LENGTH knob; (5) **LAYERS** row — 4 voice cards (drag handle · colored dot · name · ‹ › · mute · ✕ / waveform select / three value pills / three knobs) + dashed "+ Layer" + a MAIN/CLIP meter column on the right; (6) **OSCILLATOR** expander → 5 module panels (Pitch/Amp Envelope/Filter/Modulation/Flanger), each a curve well over a knob row; (7) collapsed FX CHAIN / LFOS disclosure rows; (8) bottom bar — FORMAT + bit-depth segmented choosers leading, ZOOMPLAY/AUTOPLAY toggles + green Play + blue Save trailing; right-edge VOLUME meter.

**Marketing feature composites (shots 2–5):** left-column editorial stack (tracked cyan/green eyebrow → 1–2 line grotesque headline with one colored word → grey subhead) beside floating, frameless UI fragments — a waveform panel + template chip row (2), a voice card + 5 module panels with a big "+" (3), a 3×2 grid of effect/LFO panels (4), two effect panels + an EXPORT/bit-depth/Save control strip (5). These are component showcases, not app surfaces.

**Brand cover (1200×630):** logo lockup (cyan sine mark + "MJSFX") top-left, `mjsfx.app` top-right, tracked eyebrow, "From blank to **bleep** in seconds." headline with cyan accent word, subhead, and a framed "SOUND PORTRAIT" oscilloscope card with pink→purple→green multi-voice waveform.

## Signature moves

- **[GOLDEN-NUGGET] Per-voice color identity, threaded end to end.** Each layer owns a hue (pink "zapper", purple "swoosh", green "digital dirt", orange "noise wave"); that hue appears on the card dot, the card's selection border, and — the payoff — the voice's trace inside the shared oscilloscope. The composited multi-hue waveform *is* the product's face, promoted to the marketing centerpiece as "SOUND PORTRAIT." This is a disciplined use of the isolation effect: in a dense multi-object workspace, color is doing the object-tracking that labels can't.
- **Playful voice naming over generic slots.** "zapper / swoosh / digital dirt / noise wave" instead of "Osc 1–4" gives a technical tool a warm, arcade-adjacent personality without touching the layout.
- **Semantic action-color triad.** Play=green, Save=blue, active-state=cyan — three fixed meanings a game-audio user reads pre-attentively (also a rubric risk, see Defects).
- **App icon rhymes the canvas.** A single bright-cyan `~#2EC6DA` sine wave on near-black — the oscilloscope reduced to one glyph. (Icon noted as brand evidence only; not run through the icon rubric — this was a UI-only digest.)

## Defects

- **Faked / inactive window chrome** → grey monochrome traffic lights + dimmed title, presented as a hero. Reads as an unfocused or non-native window; directly contradicts the "NATIVE MACOS" marketing claim. Canon: a real key window shows lit red/yellow/green and a primary-color title, or don't frame it as a window at all.
- **Contrast Dilution** → tracked UPPERCASE micro-labels `~#6B7079` on `#1C1F24` read ~2.5–3:1, and panel/card borders `~#2A2E34` on `#1C1F24` fall below the 3:1 non-text floor. Fix: lift secondary labels to `~#9AA0A8`; strengthen dividers to ≥3:1.
- **Focal Collision (soft)** → the bottom bar fires green Play + blue Save + cyan ZOOMPLAY as three saturated filled controls at once. Defensible as distinct semantic actions, but the first-glance read has no single winner. Canon: one filled primary per region; demote the toggle to a quiet fill.
- **Target Starvation** → the layer-card header controls (‹ › ● ✕, ~12–14pt hit) and ~17pt segmented segments sit under the 24px WCAG floor on a pointer-first surface. Pad hit areas.
- **Tracked-UPPERCASE section headers** ("LAYERS", "OSCILLATOR", "FX CHAIN") — a web/non-native tell, though here a deliberate hardware-panel convention consistent across the app.

## Rubric history

| Surface | 14-pt rubric | Native-tells | Failures |
|---|---|---|---|
| Workspace (shot-6) | 9/14 | 1/10 | 14-pt: #9 label contrast ~2.5:1, #10 border <3:1, #11 tiny header targets, #12 sub-24pt fields, #14 no visible focus (n/a static). Native: fails lineage/frame/selection/accent-binding/typography/action-singularity; #2 glass & #9 toolbar n/a (app makes no native attempt). |
| Hero window (shot-1) | 9/14 | 1/10 | Same surface, re-evidences tokens & voice-color signature. |
| Feature composites (shots 2–5) | ~10/14 (component-level) | n/a | Marketing showcases, not full surfaces; strong editorial hierarchy, same token set. |

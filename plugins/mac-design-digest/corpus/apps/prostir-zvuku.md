# prostir zvuku — profile

- **Source:** macapp.supply · **Surfaces digested:** main window (spatial mixer, dark) — 1 marketing-composite still; app icon (brand/icon evidence) · **Last updated:** 2026-07-19
- **One-sentence identity:** Endel's ambient calm rendered as a literal spatial console — a near-black "void" canvas where you drag nature-sound emitters around a wireframe head, with all colour drained out except a single amber timer and a green head-tracking pulse.
- **Cluster:** unassigned (candidate seed for a "nocturnal-immersive / dark ambient-media" cluster — peers: Endel, Dark Noise, Portal, moody end of Halide's icon language)
- **Lineage:** native (med confidence) — SwiftUI most likely, over a Metal/SceneKit or SwiftUI-Canvas spatial stage. Decisive native signal: **Head Tracking** (AirPods head-tracked spatial audio via Apple's CMHeadphoneMotionManager / PHASE) is a platform capability Electron apps effectively never ship. But the app is a **fully bespoke dark skin**: not one stock AppKit control is visible, and it imports iOS idioms (carded list rows, horizontal filter-chip strip). So it reads native-*built* but not native-*grammared* — most of its taste evidence is custom-theme, not platform-standard, and must not feed macOS canon.
- **Era (chrome):** custom bespoke dark theme (not Liquid Glass — opaque dark pills, no lensing/refraction, no scroll-edge glass; not legacy-native either). Genuine traffic lights, borderless unified dark toolbar, no title text.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#111111` | (measured)(inferred) | dark window ground — **darker than macOS-27 kit dark window `#1E1E1E`**; deliberate "void" ground, deviation logged |
| bg/canvas-panel | `~#111–#151515` w/ ~1px hairline border | (measured)(inferred) | spatial stage panel, barely lifted from window |
| bg/row | `#141414` | (measured)(inferred) | list row card, near-invisible against window (~3–4 L over bg) |
| bg/row-selected | `~#272728` | (measured)(inferred) | selection = luminance lift (~2×) + title→bold white |
| text/primary | white `~#F5F5F5` | (estimated)(inferred) | list titles, button labels |
| text/secondary | gray `~#8A8A8A` | (estimated)(inferred) | category sublabels ("Fire", "Ocean"); borderline contrast on `#141414` |
| accent/amber | `~#FF9E33` monospace digits | (estimated)(inferred) | the `00:58.55` timer — the single warm accent in a monochrome UI |
| accent/green | `~#7CCB4E`→olive gradient | (estimated)(inferred) | Head-Tracking headphone glyph + "Evening" preset orb; status jewelry, not the system accent |
| selection grammar | inset rounded fill + white bold title, **no accent tint** | (measured)(inferred) | monochrome/luminance-only selection — house signature |
| control/pill | dark fill `~#1E1E1E`, radius ~8–10px (buttons); capsule (chips, volume, transport) | (estimated)(inferred) | custom-drawn; abandons AppKit control appearance |
| icon-badge | circular ~36–40px, dark glass fill, monochrome SF-Symbol-like glyph | (estimated)(inferred) | category icons in list + emitter nodes on canvas |
| row-height | `~64–68px` generous | (estimated)(inferred) | title + sublabel, tall carded rows |
| type/list-title | `~14–15px` semibold | (estimated)(inferred) | |
| type/list-secondary | `~11–12px` regular gray | (estimated)(inferred) | |
| type/header | "Sounds" `~15px` semibold + gray count "41" | (estimated)(inferred) | sentence case, native-leaning |
| brand/gradient | `#002EBF`→`#226FB7` royal→azure diagonal | (measured)(inferred) | **MARKETING backdrop, not app** — do not conflate with the app's dark palette |
| brand/wordmark | "prostir zvuku" lowercase geometric sans, medium | (estimated)(inferred) | custom brand face |
| brand/headline | "Spatial nature sounds for Mac" — SF-Pro-Display-like humanist sans, Regular, large, tight tracking | (estimated)(inferred) | editorial restraint (regular, not bold) |
| icon/bg | `#0D0D0D` pure near-black | (measured)(inferred) | full-bleed squircle, transparent canvas |
| icon/glyph | grayscale luminous-fog wavelet, peak `~#A0A0A0` (never blows to white), film grain | (measured)(inferred) | self-illuminating audio-waveform envelope |
| icon/corner | full-bleed squircle, radius `~300/1024` (~0.29) | (estimated)(inferred) | a hair rounder than the iOS superellipse; lacks the macOS icon-grid padding — a raw/marketing export |

## Layout skeletons

**Main window — spatial mixer (dark):** borderless unified dark toolbar, genuine traffic lights top-left, no title text. Three zones:
- *Toolbar row:* leading `Save new preset` pill; far-trailing cluster = amber monospace timer pill `00:58.55` + `/` separator + `Head Tracking` pill (green headphone glyph + label).
- *Body (split):* **left/centre = polar spatial stage** — quadrant crosshair grid + faint concentric orbit rings; a central wireframe/topographic 3D **head** (the listener), viewed from behind; 7–8 **emitter nodes** (dark glass circles with monochrome category glyphs — dove, flame, paw, city, waves, beetle, hummingbird) sit on radial connector lines at varying radii = spatial position + distance. **right = "Sounds 41" panel:** header + count → horizontal **filter-chip strip** (`All` selected as white pill / `Birds` / `City` / `Crickets…`, each icon+label) → vertical scroll list of **carded rows** [circular badge · title · category sublabel]; selected row lifts fill + bolds title white.
- *Bottom transport bar:* leading preset selector [green gradient orb · `Evening` / `7 sounds` · up-chevron] + `Update Evening` pill; trailing transport [speaker-low · white capsule volume slider · speaker-high · circular pause].

## Signature moves
- **The polar spatial stage** — a wireframe listener head at centre with nature-sound emitters on concentric orbit rings and radial connector lines: drag-to-position 3D audio made literal and beautiful. Natural mapping (UI position = audio position). This is the app's entire identity in one surface. [GOLDEN-NUGGET]
- **Colour abstinence as house style** — the in-app UI is grayscale-luminance-only; selection, iconography and hierarchy carry with light, never with the system accent. The two colour moments (amber timer, green head-tracking/preset dot) are jewelry, made loud precisely because everything around them is monochrome (Von Restorff by subtraction).
- **Luminous-fog icon** — a soft grayscale audio-waveform envelope that *emits* light on pure black (no bevel, no scene, no badge, no colour), grain-textured. Austere to the point of being anti-iconographic; reads as a premium-audio signal.
- **Amber monospace timer** as the single warm counterpoint — the only "instrument-panel" moment in an otherwise silent-dark interface.

## Defects
- **iOS-idiom list construction** — every row is a persistent rounded card; native macOS source lists use full-bleed rows with hairline separators and inset-rounded selection *only on selection*. Carded-per-row is an inset-grouped-table import. Native fix: full-bleed rows, hairline dividers, selection as the only rounded fill.
- **Contrast Dilution / over-de-emphasis** → non-text contrast fail: unselected row cards (`#141414` on `#111`) and dark-glass node badges sit **below WCAG 3:1** for UI elements — affordances nearly vanish. Category sublabels (`~#8A8A8A` on `#141414`) are borderline on the 4.5:1 text floor. The de-emphasis doctrine is pushed past legibility.
- **Filter-chips for scope** instead of a native segmented control (native-tell #7) — an iOS/web idiom on a Mac.
- **Accent not bound to system accent** (native-tell #6) — recorded as a *signature deviation*, not a defect: it's systematic, purposeful (nocturnal mood), and stays legible via luminance. But it means none of this app's selection/accent grammar feeds native canon.
- **Icon small-size legibility** — the soft low-contrast fog holds at 32px but degrades to an unidentifiable smudge at 16px (Dock/Spotlight squint test). Mood traded for silhouette.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark, marketing composite) | 11/14 | #10 UI/border contrast (row cards + node badges <3:1); #9 borderline secondary-label text contrast. (#6/#12/#13/#14 n/a — no long measure, no text fields, no visible focus state) |

**Native-tells audit:** 6/10 — pass: #2 glass discipline (no glass, content opaque), #4 sentence-case header, #5 native-plausible density, #7 no focal collision, #8 concentric-plausible radii, #10 genuine chrome/traffic-lights. fail/partial: #1 reads custom not standard-native (carded list is iOS idiom), #3 selection shape right but accent tint dropped, #6 accent not bound to system accent, #9 toolbar is custom pills not borderless-symbol groups.

## Notes
- Only ONE app surface available (a single marketing composite), and the window's right/bottom edges are cropped by the composite frame — sidebar width and full transport are partially inferred. All app-UI values are `(inferred)`; nothing here is confirmable across surfaces. Ask for in-app screenshots (settings, the drag interaction, light mode if any, an empty/onboarding state) to promote anything.
- Brand layer (royal-blue gradient + `prostir zvuku` wordmark + SF-Pro-like headline) is analysed as brand evidence and kept strictly separate from the app's own black-void palette — the deliberate bright-blue-marketing / black-app contrast is itself a brand choice.
- Lineage is native but the taste is a bespoke skin: treat this app as evidence for a *dark-ambient-media cluster* aesthetic, **not** as macOS native-grammar canon.

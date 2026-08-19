# Orbs — profile

- **Source:** macapp.supply (cover.png marketing composite; app UI = right ~48% of the canvas) · **Surfaces digested:** radial launcher HUD (dark, over desktop) · **Last updated:** 2026-07-19
- **One-sentence identity:** a two-ring radial pie-menu launcher invoked by a hold-⌥-flick-release gesture — Raycast's keyboard-first launch speed re-expressed as a game-style spatial-memory wheel, dressed in a strict black/white/silver monochrome system.
- **Cluster:** unassigned (candidate: monochrome-HUD / spatial-launcher — synthesis pass to decide)
- **Lineage:** native (high) — custom-drawn SwiftUI/AppKit canvas; SF Pro labels, borderless monochrome SF Symbols, genuine per-app macOS squircle icons (Ghostty/Notes/Chrome/Spotify/Claude), system materials, frameless overlay HUD with no window chrome. No web/Electron tell present (no 16px body, no card grid, no kebab, no pointer-hand affordance).
- **Era (chrome):** Liquid Glass native (macOS 26/Tahoe). Strongest glass evidence = the fully transparent Clear-glass centre hub (desktop rock texture fully visible through it); sector fills read as dark Regular glass or a dark scrim — indistinguishable from a still (dark-mode humility).

## Surface classification

This is not a windowed surface — it is a **HUD-style panel** (HIG: "a darker, translucent variant for media-oriented or immersive apps"), correctly frameless (HUDs/panels carry no traffic lights). Because the whole surface is one bespoke radial canvas, most standard-component grammar (sidebar headers, toolbar regions, form labels, list selection) is **N/A**, and the cartesian 8pt-grid checks are reinterpreted **radially** (angular division + concentric rings). Scored on that basis, not penalised for absent chrome it was never meant to have.

## Tokens

All pixel values `(estimated)` — the input is a 1600×900 marketing composite of unknown retina scale with no standard chrome (traffic lights / titlebar) to calibrate against. Type sizes given as SF-Pro-class reads, not asserted points.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| structure/rings | 2 concentric bands: inner app-launch ring (9 items) + outer utility-action ring (7 items) around a central hub | (estimated)(inferred) | radial equivalent of a layout grid |
| structure/sectors | inner ring ~9 wedges ≈40° each; outer wedges wider | (estimated)(inferred) | even angular rhythm = radial grid adherence |
| selection/aim | selected wedge = **solid white fill** (#FFFFFF-class) with near-black glyph + label | (estimated)(inferred) | the "flick target" highlight; NOT accent-tinted — see Signature/Defect |
| material/sector | dark translucent wedge fill (Regular dark glass or dark scrim) over desktop | (estimated)(inferred) | wallpaper + stars visible through unselected wedges |
| material/hub | **Clear glass** disc, ~1px hairline ring border | (estimated)(inferred) | rock texture fully lensed through; the clearest Liquid-Glass tell |
| divider/spoke | ~1px hairline, white @ ~10–15% | (estimated)(inferred) | radial spokes + arc rings; low contrast (see Defects #10) |
| type/label-inner | ~11–12pt SF Pro Semibold, white | (estimated)(inferred) | app names under each icon |
| type/label-outer | ~11pt SF Pro, secondary white (~55–70%) | (estimated)(inferred) | utility-action labels, de-emphasised vs inner ring |
| type/hub-title | ~13–15pt SF Pro Semibold white ("Utility") | (estimated)(inferred) | current-category name in hub |
| type/hub-pager | ~17pt SF Pro Bold white ("8 / 9") flanked by ‹ › chevrons | (estimated)(inferred) | value outranks its label — pager reads as primary in the hub |
| badge/shortcut | ~14–16px circular disc, ~50% grey fill, ~9–10pt white numeral (1–9, "C") | (estimated)(inferred) | keyboard-shortcut hints; inverts (light disc) on the white selected wedge |
| icon/app | genuine macOS app-icon squircles, ~32–40px | (estimated)(inferred) | only source of chroma in the whole UI |
| icon/utility | white monochrome SF Symbols (eyedropper, gauge, glasses, clock, camera, chevron, tray, grid) | (estimated)(inferred) | outer ring + monochrome inner items |
| legibility/scrim | white label text carries a soft dark shadow/halo | (estimated)(inferred) | the key move for a HUD floating over arbitrary desktop content |
| submenu/marker | "•••" under Folders / System / Utility | (estimated)(inferred) | wedge opens a nested sub-wheel |

### Brand tokens (left composite — brand evidence, NOT app UI; excluded from canon)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/ground | near-pure black #0A0A0A→#151515 subtle vertical gradient | (estimated) | matches the icon's black field |
| brand/headline | "Ten apps. One orb." heavy grotesk (Helvetica-Now/Söhne-Black class), white, ~64–72px, tight tracking | (estimated) | Swiss/neo-grotesque display |
| brand/subtitle | ~20–22px regular, white ~85% ("A radial launcher for macOS. Hold ⌥, flick, release.") | (estimated) | |
| brand/mono | "orbs.studio" ~16px monospace, grey | (estimated) | utility mono face; committed monochrome |
| brand/icon | glossy silver-on-black orb in a Big Sur squircle (see icons/ pass) | (estimated) | icon material is legacy Aqua-gloss — lags the app's own Clear-glass era |

## Layout skeletons

**Radial launcher HUD (dark, over live desktop):** centred wheel, no window frame. Concentric structure, hub outward:
1. **Centre hub** — Clear-glass circular disc, hairline ring. Stack: category title ("Utility") over a pager row `‹ 8 / 9 ›`. Acts as both status readout (which item is aimed / which page) and page control.
2. **Inner ring (launch)** — 9 wedges radiating from the hub, each a vertical stack: app icon (top) → label (mid) → the wedge's numbered shortcut badge (inner corner near hub). Full-colour app squircles for real apps; white SF Symbols for internal actions (Clipboard, Folders•••, System•••, Utility•••). The aimed wedge is inverted to a solid-white spotlight.
3. **Outer ring (utility actions)** — 7 wider wedges arcing over the top and down the left: Color Picker, Focus, System Glance, Volume, Timer, Keep Awake, Mirror. Monochrome glyph over de-emphasised label; visually recessive vs the inner launch ring.
4. **No global backdrop dim** in this render — each wedge supplies its own dark fill; the desktop shows through the gaps and the hub.

Alignment axes are **concentric rings + radial spokes**, not vertical/horizontal edges; icon/label/badge triads are proximity-grouped inside each wedge with clear inter-wedge separation.

## Signature moves
- **[GOLDEN-NUGGET] The wheel itself as a spatial-memory launcher.** Fixed wedge positions + a hold-flick-release gesture turn app-launch from a read-then-click search (Raycast/Alfred/Spotlight) into pure motor memory: aim a direction, release. Fitts's Law at its best case — wedges are enormous angular targets radiating from a common origin, so every app is roughly equidistant and acquired by *direction*, not pointing precision. The gesture is the product; the UI is the muscle-memory map.
- **[GOLDEN-NUGGET] Solid-white "aim" selection instead of accent-blue.** The selected wedge inverts to a full-white fill with near-black contents — a spotlight/reticle, not a list highlight. Deliberately *not* bound to the system accent: it reads as "this is where the flick will land" and keeps the monochrome system pure. House style for a HUD, defensible as a deviation (see Defects for the audit implication).
- **Clear-glass status hub.** The centre lenses the live desktop through it while doubling as category label + `8/9` pager — a genuine Liquid-Glass Clear surface used as functional chrome, with the pager value bolded above its whispered label (correct value-outranks-label hierarchy).
- **Chroma only from borrowed app icons.** The app draws zero colour of its own — every hue on screen is a third-party app squircle. Monochrome discipline enforced by never introducing a brand accent.
- **Number/letter badges as a second, expert input path** (Tesler): flick for discovery, press 1–9/C for speed — dual affordances on the same map.

## Defects
- **Contrast Dilution (non-text) — #10 UI contrast.** Sector spokes and arc-ring dividers are ~1px white @ ~10–15% over dark glass — below the 3:1 non-text floor. Intentional quiet structure, but by the letter a fail; a HUD could afford a slightly firmer divider without losing calm.
- **Label-over-photography legibility risk — #9 (borderline).** With no global backdrop scrim, outer labels ("System", "Keep Awak", "Mirror") sit over the bright sunlit rock and lean entirely on the per-wedge dark fill + text halo to hold contrast. On a *light* wallpaper the thin-fill outer ring could wash out. The marketing shot's busy wallpaper actually stress-tests this; the app likely dims the backdrop more in practice, but the still shows the risk. Canon fix: a single global dim behind the wheel, or firmer wedge fills.
- **Label truncation.** "Keep Awak"(e) and possibly "Volume"/glyph mismatch (a magnifier glyph beside "Volume") — minor; wedge width is truncating labels rather than wrapping/abbreviating deliberately.
- **Selection grammar deviates from native (native-audit #3 & accent-binding #6).** Solid-white non-accent selection is not the macOS inset-rounded accent-tinted grammar. Classified a **signature**, not a defect (systematic, purposeful, high-contrast, accessible) — but recorded here so the native-tells audit reads honestly: it fails #3 and #6 by the letter.

## Rubric history
| Surface | Score | Failures / notes |
|---|---|---|
| radial launcher HUD (dark) | 12/14 | #10 divider contrast <3:1 (fail); #9 label-over-photo contrast (borderline); #5/#6-measure/#12-input N/A (no paragraphs, no inputs) — treated as pass. Strong passes: #11 Fitts (wedges are ideal radial targets), #14 focus (white aim = extreme contrast shift), #3/#7 grouping + de-emphasis. |
| — native-tells audit | ~7/10 | Pass: #1 native, #2 glass-on-chrome (mild glass-in-glass caveat: Clear hub inside dark wheel — insufficient-evidence), #5 density, #7 one prominent action, #10 correctly frameless HUD. Deviate (house style): #3 selection grammar, #6 accent binding (white, not system accent). N/A: #4 sidebar, #8 concentric corners, #9 toolbar. |

## Notes for synthesis
- **Icon-vs-UI era contradiction (cross-pass):** the icon pass classified the app icon as **big-sur / baked glossy-Aqua quote (legacy)**, yet this UI is **Liquid-Glass-era (Clear-glass hub)**. The brand mark's material lags its own app by an era — worth flagging if a "monochrome-HUD" cluster forms.
- Single surface, single mode (dark), marketing-composite provenance, unknown retina scale → everything `(inferred)`/`(estimated)`; no promotions possible from this app alone. To level up: a real screenshot at @2x over a plain/light wallpaper (to test the legibility risk), any sub-wheel ("•••") state, and a settings/preferences surface.

# Icon: Usage

- **Era:** skeuomorphic-quote (modern CG revival — machined-device faceplate, not genuine photoreal) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, **400×400** web render, converted to PNG) · **Category:** Utility · App: "Usage — System Activity Monitor" (usage.pro)
- **⚠ Resolution caveat:** the served asset is a **400px** render, not the 1024² master. Circuit-trace hairlines sit at the resolution floor and the violet glow shows mild webp banding. All hex values are `(measured)` off the 400px render — treat as compression-shifted by a few levels.

| Dimension | Reading |
|---|---|
| Background | Full-bleed **machined graphite faceplate** etched with a tone-on-tone **PCB circuit-trace** pattern (right-angled traces, via-dots). Not a sky ramp — a flat lit metal plate. Etched valleys #0D0C13, plate face ~#38373C, bezel highlights up to #4F5056; whole plate carries a cool violet cast `(measured)` |
| Glyph | `abstract` — a recessed **segmented turbine / camera-aperture dial** of ~13 tapered spoke-blades ringing a dark central well. Unlit blades read mid-gray; the focal blades are lit by an internal **violet emissive glow** #6C43F9→#7E65FD that pools brightest lower-right and dims to #27234D at the top-left. Optical centre ~(215,195) on the 400 canvas — nudged **~15px right, ~5px up** of true centre `(measured)` |
| Overlay device | none diagonal — instead **four corner hardware devices**: rounded-square screw/button (TL), twin capsule heatsink slots (TR), 3×2 vent-dot grid (BL), twin circles (BR). Faceplate furniture, not a tool-across-the-squircle |
| Light model | **Dual, coherent:** top-down environmental key on the raised bezel (light top edge #323047, shadowed bottom) + an **internal emissive source** in the dial well (the glow). Emissive-plus-directional is physically consistent for a glowing-display object — not a lighting conflict `(measured)` |
| Layer stack | back → front: (1) graphite faceplate + etched PCB traces → (2) raised bevelled bezel frame carrying the four corner devices → (3) recessed circular aperture well (near-black #04050C) → (4) ring of ~13 top-lit gray spoke-blades → (5) violet emissive glow rising through the lower-right blades (the "active/load" indicator) |
| Palette economy | **2 hue families:** cool graphite/gunmetal neutrals + one violet-indigo accent. Saturated violet is reserved strictly for the emissive dial — textbook display-glow de-emphasis logic. Pass |

## Signature devices
- **Etched PCB faceplate** — the entire background is a tone-on-tone circuit-board relief. Cheapest "this is a system-internals tool" signal in the icon; low-contrast so it never fights the dial. `[GOLDEN-NUGGET]`
- **Emissive turbine-as-gauge** — a segmented aperture/fan dial where the violet glow *is* the reading: brighter, more-lit blades = more activity. Subject communicates function (cooling-fan / activity meter for a system monitor). The dock render (`cover.png`) confirms the fan reading.
- **Faceplate hardware furniture** — corner screw, twin heatsink slots, vent-dot grid, twin ports. Sells the "physical instrument panel" fiction; a committed cyber-industrial direction, not template glyph-on-gradient.
- **Violet-on-graphite emissive focal** — accent-as-light-source, not accent-as-fill; the only chroma in an achromatic machined field.

## Failures
- **#4 16px squint test** — the icon front-loads fine detail that becomes pure noise at menu-bar size: the PCB hairlines and all four corner devices smear to mud, and the segmented dial collapses into a broken ring. Only the lower-right violet glow-arc survives, giving Dock-distinguishability but **not** subject identity — you cannot read "fan / activity monitor" at 16px, only "dark thing with a purple glow."
- **#10 Variant robustness (Liquid Glass)** — a baked raster with hand-painted bevels, shadows, and a background-dependent glow. There is no layer separation for the system to recompose; a dark/clear/tinted system render would destroy the modelling it depends on. It cannot survive the macOS 26 appearance matrix (light/dark/clear/tinted) the current era expects.

## Soft passes (scored pass, flagged)
- **#2 Grid adherence** — the dial is the anchor and roughly centred, *but* it sits ~15px right / ~5px up of true centre, pulled off-axis by the asymmetric corner hardware (screw TL vs heatsink slots TR). Passes on centring, flagged on optical balance.
- **#3 Silhouette test** — filled solid black it is just a squircle; the subject carries **entirely through internal luminance contrast**, never through outline (the full-bleed-plate case). Reads because the dial's figure-ground is strong (#7), not because the silhouette is nameable.

## Clean passes
- **#1 Mask discipline** (designed to the squircle; bezel follows the corner radius, no baked corner-radius mismatch), **#5 Single light model** (top-down + emissive, coherent), **#6 Palette economy**, **#7 Figure-ground** (lit blades ≥3:1 over the near-black well in grayscale; PCB texture kept sub-threshold so it never competes), **#8 Depth coherence** (plate < bezel < well < blades < glow, shadows track the top light, no z-fighting), **#9 Era coherence** (every device speaks one machined-skeuomorphic language — a consistent quotation, cleanly committed), **#11 Personality** (unusually strong; the whole icon is signature devices), **#12 No-text check** (no words / UI / photographic elements — a rendered illustration).

## Rhymes with
- **Hardware / system-internals utility icons** — the gunmetal-faceplate-plus-glow lineage: iStat Menus, Macs Fan Control, TG Pro, older CleanMyMac skeuo, gaming-peripheral suites (Razer Synapse / Corsair iCUE). Same "physical instrument panel for your Mac's guts" fiction.
- **Cyberpunk / sci-fi HUD glyphs** — the emissive-ring-on-dark-tech-surface family (loading-spinner, reactor-core, aperture-HUD motifs).
- **Cross-era note:** shares the *baked-photoreal, background-dependent, non-layered* structural weakness with Bartender 6's legacy skeuo icon — both fail #4 (partly) and #10 for the same reason: they model light instead of letting the system apply it. Different subject, same era-fit liability. *Hint for synthesis; confirm as the skeuomorphic-quote cluster grows.*

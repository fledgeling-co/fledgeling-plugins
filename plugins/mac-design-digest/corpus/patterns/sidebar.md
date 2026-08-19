# Pattern: sidebar

Cross-app synthesis of the source-list / navigation sidebar. Evidence is native-lineage apps only (canon gate = ≥3 independent native apps, no contradiction). Kit floor: `kit/macos-27.md` — sidebar **256pt wide** example, rows full-bleed minus 4px insets (248 wide), **selection radius 8**, row heights Small **24** · Medium **32** · Large **40**, section headers 18–20.

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Letterboxx | 3-pane mail reader (light) | ~160–200pt wide; rows ~28–32pt (Medium); **solid accent-blue inset-rounded selection, white label, r~6–8, ~4px inset** (Mail/Reminders "prominent" style); section headers `Filters`/`Letterboxxes` ~11pt SF Pro Semibold secondary grey, **sentence case**; neutral-grey selection when unfocused | (measured)(confirmed) |
| Vocal Notes | Apple-Notes 3-pane (light) | ~220–240pt; **~40pt Large rows**, leading SF Symbol + label + trailing count; gray inset-rounded inactive-pane selection r~8, ~4px inset; sentence-case header "Saved on this Mac" | (estimated)(inferred) |
| Grape | 4-pane notes (dark) | ~240pt; ~38–40pt rows (Large); **neutral gray `#3C3C3C` inset selection r~8, white label (no accent tint)**; `Folders` header secondary, sentence case; amber folder glyphs (identity, not selection) | (measured/estimated)(confirmed) |
| Resurf | 3-pane library (light) | ~200pt; ~24–28pt rows; **neutral grey inset fill r~8 (no accent tint)**; collapsible sentence-case headers `Triage`/`Library`/`Areas` w/ disclosure chevrons; right-aligned count badges | (estimated)(inferred) |
| Bartender 6 | System-Settings clone (dark) | ~200–210pt; ~28–32pt Medium rows; **solid accent-blue selection r~8, full-width minus ~4px inset**, white symbol-tile + white text (System Settings house style); flat list, no headers; mutes to no-fill when inactive | (estimated)(confirmed) |
| Codeshot | 3-pane utility (light) | ~140–150px; header `Editor` secondary, **sentence case**; inset-rounded selection ("Themes"); nav-only | (measured/estimated)(inferred) |
| Glyph | 3-pane markdown (light) | ~230–256pt; **roomy ~34–40pt rows**; solid steel-blue `#5E9DC0` selection + white text (brand, not system accent); sidebar header "Notes" sentence-case secondary + disclosure chevron | (estimated)(inferred) |
| Canary Mail | 3-pane mail (dark) | **~140pt compact**; native flat neutral inset selection `#2C3235`; sentence/title-case account/section headers | (measured)(inferred) |
| Room Service | dashboard (dark) | ~200–230px; ~32pt Medium rows; neutral `#242424` inset selection r~8 (no accent tint); `DEVELOPER` **tracked-uppercase header — flagged defect** | (estimated)(inferred) |
| Sketch | canvas tool (light) | ~256pt-class; ~28–34pt layer rows; two selection treatments — native flat inset lavender `#F0EFFF` + indigo text (document) vs saturated indigo capsule (layer, deviation) | (measured)(inferred) |
| Autoshelf | rules list (dark) | ~256pt; ~40pt rows; **solid saturated orange-red selection**, white glyph+label; `ORGANIZERS` **tracked-uppercase header — flagged tell** | (estimated)(inferred) |

## Converged rules

- **Section headers are sentence/title case, secondary grey, system font — never tracked uppercase** — apps: Letterboxx, Vocal Notes, Grape, Resurf, Codeshot, Glyph, Canary Mail — **(canon)**. This is the #1 sidebar-authenticity tell; the corpus's tracked-uppercase headers (Room Service `DEVELOPER`, Autoshelf `ORGANIZERS`, plus Cachesweep/Satu/Hora on other surfaces) are all logged as native-tell *defects*, so the rule stands uncontradicted among compliant natives.
- **Selection is an inset-rounded fill at radius ~8, inset ~4px from the row edge** (matches kit's specified 8) — apps: Letterboxx, Vocal Notes, Grape, Resurf, Bartender 6, Room Service, Codeshot — **(canon)**. The *shape* is invariant even where the *fill hue* diverges (see Divergences).
- **Row anatomy = leading monochrome SF Symbol + label + optional right-aligned count badge** — apps: Letterboxx, Vocal Notes, Resurf, Glyph, Purge, Autoshelf — **(canon)**.
- **Row height tracks the kit Medium(32)/Large(40) tiers; compact apps run 24–28** — apps: Vocal Notes (40), Grape (38–40), Glyph (34–40), Bartender (28–32), Resurf (24–28), Room Service (32) — **(canon)**.
- **Two-tone chrome: sidebar sits a step off the content pane** (lighter or darker) — apps: Fantastical (dark agenda vs light grid), Grape (`#262626` vs `#1E1E1E`), Resurf (`#F4F4F4` vs `#FCFCFC`), Glyph (warm `#F8F7F5` vs white), Canary (`#1B2124` vs `#1E1E1E`) — **(canon)**.
- **Width runs 140–256pt; 200–256 is the comfortable default, kit example is 256** — apps: Vocal Notes (220–240), Grape (240), Sketch (256), Glyph (230–256), Autoshelf (256), Bartender (200–210), Resurf (200), Canary (140 compact), Codeshot (140) — **(canon)**.

## Divergences

- **Selection fill hue splits along cluster lines.** Native-correct **accent-tinted / solid-accent** selection: Letterboxx (system blue, Mail-prominent), Vocal Notes (system blue), Bartender (system blue). **Neutral-grey (accent-withheld)** selection: Grape, Resurf, Room Service, Codeshot, Canary(sidebar) — this tracks the calm/monochrome & graphite-dashboard clusters, where withholding the accent is a deliberate signature (Grape, Room Service) recorded with its tradeoff. **Brand-hue solid** selection: Glyph (steel-blue), Autoshelf (orange-red), Sketch(layer, indigo) — these override the user's system accent (a logged tell). The *inset-rounded shape at r8* survives all three readings; only the fill differs.
- **Selection-grammar consistency within one window.** Correct dual-level focus (solid-accent list + muted-grey sidebar when unfocused) is done well by Vocal Notes and Letterboxx; split/inconsistent grammar (sidebar neutral vs content accent-ring, or two selection languages) is a recurring defect (Resurf, Canary, Codeshot, Sketch).
- **Headers present vs flat list.** Grouped collapsible sections with disclosure chevrons (Resurf, Letterboxx, Glyph) vs a single flat nav list (Bartender, Autoshelf) — a density/IA choice, not a lineage split.

## Generation guidance

Build a source-list sidebar as `NavigationSplitView`'s leading column:

- **Width** 220pt default (200–256 range); the content pane must read a tonal step apart — in light mode sidebar `~#F4F4F6` translucent vs content `#FFFFFF`; in dark, sidebar one step off content (`#262626` vs `#1E1E1E`).
- **Rows** at the Medium (32pt) or Large (40pt) kit tier: `[monochrome SF Symbol] [label, 13pt SF Pro] … [secondary-grey count badge]`. Keep glyphs monochrome (identity colour belongs on data, not chrome).
- **Section headers** in **sentence case**, secondary-grey (`#000`@50% light / `#FFFFFF`@55% dark), 11pt SF Pro Semibold — never tracked uppercase. Add a disclosure chevron if the section collapses.
- **Selection** = inset-rounded fill, **radius 8**, inset ~4px. Default to the user's system accent: for a "prominent" list (Mail/Reminders register) use a solid accent fill + white label; for the general case use a low-alpha accent-tinted fill with accent-tinted text. Reserve neutral-grey selection only if you are deliberately building a calm/monochrome cluster app, and then apply it *consistently* across sidebar and content (the #1 recurring defect is mixing two selection languages in one window).
- **Two-level focus:** when the content list is first responder, mute the sidebar selection to neutral grey and give the list the solid-accent fill — never paint both panes accent-blue at once (Vocal Notes is the reference).
- Do **not** override the user's `controlAccentColor` with a brand hue unless the brand override is a stated, systematic signature; if you do, it will not survive a native-tells audit.

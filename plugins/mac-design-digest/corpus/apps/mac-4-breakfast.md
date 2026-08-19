# Mac 4 Breakfast — profile

- **Source:** macapp.supply (cover composite only; no standalone shots supplied) · **Surfaces digested:** menu-bar-extra panel — "Mac" tab, dark mode · **Last updated:** 2026-07-19
- **One-sentence identity:** coconutBattery's telemetry-forward menu-bar readout given a graphite-dark SwiftUI skin — raw electrical data (watts, volts, mAh, °C, cycles) treated as first-class content.
- **Cluster:** unassigned → proposes `graphite-menubar-utility` (first member)
- **Lineage:** native — SwiftUI (med-low confidence). Density and palette read Mac-native (13pt-class body, system SF, system color set), but the solid-accent segmented selection and segmented-control-as-primary-nav are iOS/SwiftUI-flavored tells; classify native pending a second, un-tilted surface.
- **Era (chrome):** Big Sur–Sequoia dark native (flat graphite panels, no observable Liquid Glass lensing). Glass presence `(insufficient-evidence)` — large dark surfaces read near-opaque and the marketing tilt obscures material; do not assert either way.

> **Evidence caveat:** the only asset is a marketing cover composite. The app window is rendered at a ~2.4° clockwise perspective tilt (measured off the tab-bar baseline: "Insights" sits ~25px above "Mac" across ~600px). All pixel measurements are therefore `(estimated)` with wide ranges, and the apparent right-column "rise" versus the left labels is **explained by the tilt, not a real baseline defect** (see Defects). Cover is 2400×1260 (likely @2x marketing render → ~1200pt logical); the app panel is ~330–360pt wide, corroborating a menu-bar panel rather than a primary window.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | ~#1A1A1C–#1E1E1E graphite (estimated)(inferred) | | dark-mode panel ground; near-black, not pure #000 (kit dark window is #1E1E1E — consistent) |
| bg/card | ~#242426 subtle-elevated (estimated)(inferred) | | faint rounded containers behind the charge card and health table |
| type/hero | ~24–30pt Bold SF Pro (estimated)(inferred) | | "8h 12m", "24%" — LargeTitle/Title1-bold tier |
| type/subhead | ~15–17pt Bold SF Pro (estimated)(inferred) | | "Charging with 14.5 W" — Title2/Title3-bold |
| type/section-header | ~13pt Bold SF Pro (estimated)(inferred) | | "Using Significant Energy" — Headline tier |
| type/body | ~13pt Regular SF Pro (estimated)(inferred) | | row labels/values (Condition/Normal, Firefox…) |
| type/caption | ~11pt Regular SF Pro (estimated)(inferred) | | "Until full", "11.38 V", "Relative battery use right now" — Subheadline, secondary/tertiary color |
| label/primary | #FFFFFF (estimated)(inferred) | | values column, section headers |
| label/secondary | ~#8E8E93 gray (estimated)(inferred) | | left-column labels — de-emphasis honored |
| label/tertiary | ~#6A6A6E dim gray (estimated)(inferred) | | "Relative battery use right now" — likely <4.5:1 (see Defects) |
| accent/selection | ~#2E7DF6 system blue (estimated)(inferred) | | selected tab fill; the one bound accent |
| status/good | ~#34C759 system green (estimated)(inferred) | | charge pill, "100%" health value, hero lightning |
| status/energy | ~#FF9F0A system orange (estimated)(inferred) | | energy-hog lightning glyphs + relative-use bar meters |
| radius/selection-pill | ~8–10px (estimated)(inferred) | | selected-tab fill; not full capsule |
| radius/panel | ~16–20px (estimated)(inferred) | | all-corners rounded popover; measure precisely from a clean shot |
| chrome/frame | none — borderless popover, no traffic lights (estimated)(inferred) | | menu-bar-extra panel |

## Layout skeletons

**Menu-bar-extra panel — "Mac" tab (dark), top→bottom:**
1. **Segmented tab bar** (primary nav): Mac · Power · Devices · History · Insights — equal-ish text segments with faint 1pt vertical separators; selected = solid-blue rounded-rect fill, white bold; below it a 1pt hairline divider.
2. **Hero status row:** left "8h 12m" (bold) + "Until full" caption under it; right "⚡24%" (green lightning + bold %). Left/right axes.
3. **Charge card:** green lightning glyph + "Charging with 14.5 W" (bold) + "11.38 V" caption.
4. **Charge track:** full-width capsule dark track with a green "⚡24%" capsule pill occupying ~24% at the leading end (label sits *inside* the fill).
5. **Health table:** two-column key/value — left secondary-gray labels (Condition, Battery health, Cycle count, Capacity, Temperature), right primary-white values (Normal, 100% in green, 102, 8575/8579 mAh, 32.6°C).
6. **"Using Significant Energy":** bold header, then app rows (Firefox, Claude, logioptionsplus_agent) each = orange lightning-in-circle glyph + name; trailing horizontal amber bar meters (relative draw); dim caption "Relative battery use right now".
7. **Disclosure row:** ⓘ + "Battery details" (bold) + trailing chevron "›".

## Signature moves
- **[GOLDEN-NUGGET] Telemetry-as-identity.** Raw electrical readouts — 14.5 W, 11.38 V, 8575/8579 mAh, 32.6 °C, cycle count 102 — are promoted to plainly-set primary content, not buried in an "advanced" pane. The app's "insights no other app has" claim is cashed out as numeric density in the hero itself. This is the whole character; it rhymes with coconutBattery / iStat Menus.
- **Label-inside-fill charge pill.** The "⚡24%" status pill sits *within* the leading end of the progress track rather than beside it — a compact indicator that fuses value, label, and fill into one object.
- **Disciplined status-color triad:** blue = selection only, green = good/charging, orange = energy cost — each identity color kept to one meaning, and every status color paired with a glyph (color-never-alone honored).

## Defects
- **Contrast Dilution (mild):** the tertiary caption "Relative battery use right now" (~#6A6A6E on ~#1A1A1C) likely falls below 4.5:1. Fix: lift tertiary captions to the dark secondary-label tier.
- **Selection grammar deviation (native-tell, not a hard rubric fail):** the selected tab is a solid saturated-blue fill with white text — iOS/SwiftUI-segmented styling, not the native macOS tinted-inset-fill selection grammar. Canon would use a lighter raised/tinted segment with accent-tinted text.
- **Segmented-control-as-primary-navigation (native-tell):** Mac/Power/Devices/History/Insights is the app's main nav rendered as a segmented tab bar. HIG reserves segmented controls for in-view scope switching; a menu-bar panel is a forgiving context, but on a larger window this would want a tab view or sidebar.
- **NOT a defect (recorded to prevent future mis-reads):** the right-column values appearing higher than their left labels is the ~2.4° marketing perspective tilt, not a real misalignment — verified against the tab-bar baseline slope.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar panel (Mac tab, dark) | 12/14 | #9 tertiary caption contrast (est. <4.5:1); #10 subtle track/divider borders borderline <3:1 |

## Native-tells audit
| Surface | Score | Fails |
|---|---|---|
| menu-bar panel (Mac tab, dark) | 8/10 | #3 selection grammar (solid-blue fill vs tinted inset); #9 no true toolbar — n/a/partial |

## Brand evidence (cover composite — NOT app UI, excluded from macOS canon)
- Hero backdrop: dark navy→violet radial gradient. Headline "Your one battery app that does it all." in heavy white sans, "all" in blue.
- Wordmark "Mac 4 Breakfast" in a violet→pink gradient ("4" set green) — a purple/violet brand identity distinct from the app's graphite-neutral UI.
- Outlined pill badges: "Native for macOS" (green status dot), "No subscription", "One-time price" — capsule outline chips.
- App icon (in composite + icon.png, not digested here — Workflow A scope): blue→violet squircle, white battery with green fill + charge bolt, plus a strip of colored dots (macOS traffic-light / accent-dots motif) — reads Big Sur-era layered-glass. Flag for a future Workflow B icon digest.

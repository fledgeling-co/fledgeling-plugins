# Room Service — profile

- **Source:** macapp.supply · **Surfaces digested:** Health Check dashboard (main window, dark) — from marketing cover composite · **Last updated:** 2026-07-19
- **One-sentence identity:** Linear/Raycast's flat-graphite dark product language applied to a Mac dev-cleanup utility — an Apple-Health-style score ring and triage stat-tiles over a near-monochrome field punctuated by a single warm orange.
- **Cluster:** unassigned (proposed cluster hint: `graphite-dashboard` / flat-dark-product)
- **Lineage:** native — SwiftUI, likely (med confidence). Native-reading evidence (13pt body, genuine 12pt traffic lights, ~32pt source-list rows, inset-rounded selection, SF Symbols, arrow cursor, system-palette status hues) may feed macOS canon; the web-influenced *skin* choices below are recorded as tells/signatures, not canon.
- **Era (chrome):** custom — custom-drawn dark theme, no Liquid Glass (no lensing/translucency/scroll-edge effect; flat opaque graphite cards). Depth is signalled by hairline borders, not glass or shadow.

**Provenance/scale note:** single surface, extracted from a marketing cover (app window on a #0B0B0B backdrop; the backdrop is brand, the window is the design evidence). The window is rendered at **~1.67× in the composite** (traffic-light dot diameter 20px = 12pt; center spacing 33.5px = 20pt — both agree). All px→pt conversions below use ÷1.67, so token values carry wider ranges than a clean @2x capture would allow.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | `#171717` (measured)(inferred) | | window content + sidebar share one field |
| bg/card | `#181818` (measured)(inferred) | | cards sit only ~1 lightness step above canvas — elevation carried by border, not fill |
| bg/row-elevated | `#1C1C1C` (measured)(inferred) | | finding/disclosure rows |
| bg/backdrop (brand, not app) | `#0B0B0B` (measured)(inferred) | | marketing composite ground — exclude from UI tokens |
| sel/sidebar-fill | `#242424` (measured)(inferred) | | inset rounded fill, **neutral** — NOT accent-tinted; label stays white |
| border/hairline | ~`#1F–24` on `#171717`, 1px (estimated)(inferred) | | ~1.1–1.3:1 contrast — below the 3:1 non-text floor (see Defects) |
| accent/primary | `#FF9300` (measured)(inferred) | | score ring, badges, "Needs attention", CTA labels — matches system Orange (dark `#FF9230`) |
| status/red | ~`#FF3B30` (estimated)(inferred) | | Action-Needed glyph — system Red class, always paired with ✕ glyph |
| status/orange | `#FF9300` (measured)(inferred) | | Warnings — **same hue as brand accent** (semantic overload, see Defects) |
| status/blue | ~`#0A84FF` (estimated)(inferred) | | Review Notes ℹ — system Blue class |
| status/green | ~`#30D158` (estimated)(inferred) | | Healthy ✓ — system Green class |
| identity/dots | 12-hue system palette (measured: purple `#BC6AFF`) (estimated)(inferred) | | per-category sidebar dots (Xcode/Docker/Packages…) — separate from accent, correct native usage |
| type/body | ~13pt SF (Health Check label cap-band 15px ÷1.67 → 9pt cap → 13pt) (estimated)(inferred) | | the native-density tell; sidebar labels + row text |
| type/secondary | ~11–12pt, secondary gray (estimated)(inferred) | | category labels ("Project Health"), unit sizes |
| type/card-heading | ~15–17pt semibold (Title2/3 class) (estimated)(inferred) | | "Priority Findings", "Storage" |
| type/title | ~26–30pt bold (LargeTitle/Title1 class) (estimated)(inferred) | | "Needs attention" |
| type/section-header | tracked UPPERCASE, secondary gray — "DEVELOPER" (measured)(inferred) | | **non-native tell**, see Defects |
| space/sidebar-row | ~32pt row height (estimated)(inferred) | | kit "Medium" tier (32) — comfortable, native-plausible |
| radius/sidebar-sel | ~8pt (estimated)(inferred) | | matches kit sidebar-row selection radius (8) |
| radius/card | ~10–12pt (estimated)(inferred) | | outer cards / finding rows |
| radius/icon-chip | ~6–8pt (estimated)(inferred) | | tinted-square SF-Symbol containers; steps down concentrically inside cards |
| radius/badge | capsule (measured)(inferred) | | count pills ("6", "2"), status pills ("Needs attention") |
| chrome/traffic-lights | genuine, 12pt dots @ 20pt center spacing (measured)(confirmed) | | real window frame, top-left |
| chrome/top-bar | custom: leading `PRO`+version badge, trailing borderless SF-Symbol cluster (⌘K, dark-mode, quick-actions, doc, terminal) in a capsule group (measured)(inferred) | | replaces a standard unified toolbar |
| chrome/sidebar-toggle | SF Symbol, trailing top of sidebar (measured)(inferred) | | |

## Layout skeletons

**Health Check dashboard (main window, dark):**
- Two-pane: fixed **source-list sidebar** (left) + scrolling **content** (right).
- Sidebar top→bottom: traffic lights + sidebar-toggle · primary nav (Home, Health Check[sel, badge 6], Space Map, Clean Up, Applications, Recipes, Projects[badge 2], Startup Items, Privacy, Performance, Duplicates) · `DEVELOPER` tracked-uppercase section header · storage-category list (icon-dot + label left, right-aligned size value: "Xcode 99,46 GB"… — European comma-decimal locale) · pinned **Settings** row at the very bottom.
- Content top→bottom: custom top bar (PRO/1.3.0/Room Service leading; icon cluster trailing) · **hero card** [left: orange score ring "59 / score" (~60% arc); two context chips "Health Check", "Generated 13:09"; large "Needs attention" title. right: two equal secondary buttons "Save Report", "Refresh Check"] · **4-up stat-tile row** [Action Needed 0 / Warnings 6 / Review Notes 6 / Healthy 5 — each a tinted-square status glyph + big number + secondary label; equal widths on shared axes] · **Priority Findings** section [lightbulb-chip header + subtitle + trailing "Needs attention" pill; then disclosure rows: warning-triangle chip + bold title + inline "Needs attention" badge + secondary category label + trailing chevron; "Show 5 More ⌄" full-width ghost row] · **Storage** section (same row grammar, drive-chip header).

## Signature moves
- **[GOLDEN-NUGGET] Borders-as-elevation, near-monochrome graphite.** The entire depth model is 1px hairlines — cards (`#181818`) sit a single lightness step above the canvas (`#171717`), with no shadow and no tonal-elevation ramp. A committed neo-grotesque-product (Linear/Vercel) refusal of shadow, executed to the point of flatness. This is the app's whole visual identity in one decision — and its main accessibility liability (borders below 3:1).
- **Orange as the sole chromatic event.** One warm accent (`#FF9300`) carries the score ring, every count badge, the primary-action labels, and the "Needs attention" verdict; everything else is grayscale + glyph-paired system status hues. Restrained-strategy color (accent ≪10% of pixels).
- **Health-triage pattern transplant.** Apple-Health-style score ring + a 4-up severity stat-tile row (Action Needed / Warnings / Review Notes / Healthy) gives a dev-cleanup utility an at-a-glance "is my machine OK?" read. Strong Jakob's-Law familiarity.

## Defects
- **UI contrast (rubric #10 / native #2-adjacent).** Card & tile hairline borders measure ~1.1–1.3:1 against the canvas — cards nearly merge into the field. Fix: raise separator to the kit's Fills tier (Dark `#FFFFFF`@8–10%) or a ≥3:1 hairline.
- **Sidebar authenticity — tracked-uppercase header.** `DEVELOPER` is tracked all-caps; the native grammar is sentence/title-case, system-font, semibold, secondary. The #1 sidebar non-native tell. Fix: "Developer" (Subheadline/Footnote emphasized, secondary label).
- **Selection missing accent tint (native #3).** Sidebar selection is the correct inset-rounded shape (~8pt) but a *neutral* `#242424` fill with white label — native selection tints the label/glyph with the system accent. House-style deviation; systematic, so borderline-signature, but recorded as a tell.
- **Accent/semantic overload (Von Restorff dilution).** Brand orange == warning orange, so the score ring and CTA share a hue with every warning badge — the "one memorable thing" is spread across the warnings, weakening the focal pull of the score. Fix: give the brand a hue distinct from the warning semantic, or demote warnings to a paired glyph without the saturated pill.
- **Dimmest tertiary metadata (rubric #9, soft).** Category labels / unit sizes read ~2.5–3.5:1 on the dark cards — below 4.5:1 for the faintest tier.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Health Check dashboard (dark) | 12/14 | #9 dimmest tertiary text ~2.5–3.5:1; #10 hairline borders ~1.1–1.3:1 (<3:1). (#12/#13 n/a — no fields; #14 focus not shown) |

## Native-tells audit (10-pt)
| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | AppKit/SwiftUI native | PASS (med) | 13pt body, genuine 12pt traffic lights, 32pt rows |
| 2 | Glass only on chrome, content opaque | PASS (legit absence) | no glass anywhere — flat graphite; legitimate for a custom pro theme |
| 3 | Selection = inset rounded + accent text | SOFT-FAIL | shape correct (~8pt) but neutral fill, white label — no accent tint |
| 4 | Sidebar headers sentence-case system font | FAIL | "DEVELOPER" tracked uppercase |
| 5 | Density 13pt body / 20–28pt controls / desktop rows | PASS | 13pt body, 32pt rows confirmed |
| 6 | Accent bound consistently | SOFT-FAIL | accent not on selection; brand orange overloads warning semantic |
| 7 | One prominent action; dialog grammar | PASS | two equal secondaries in hero — no Focal Collision |
| 8 | Concentric corners, child < parent | PASS | icon-chips (~6–8) inside cards (~10–12); capsule badges |
| 9 | Toolbar borderless symbols, grouped, one primary | PASS | monochrome SF Symbols in a capsule cluster; PRO badge leading |
| 10 | Real chrome, genuine traffic lights | PASS | genuine 12pt lights, real frame |
**Native audit: 7/10** (fails #3 soft, #4, #6 soft).

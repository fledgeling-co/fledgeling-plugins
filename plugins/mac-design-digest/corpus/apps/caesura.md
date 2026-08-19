# Caesura — profile

- **Source:** macapp.supply (`caesura.app` / `caesura.rest`) · **Surfaces digested:** menu-bar-extra "Up Next" dropdown + status capsule (1 surface, light, from marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** A menu-bar break-reminder that recolors the clinical Time-Out/Stretchly category into warm paper and terracotta — Things' calm restraint crossed with an editorial-literary brand, where the app's name (a *caesura* = a rhythmic pause) becomes the entire design language.
- **Cluster:** unassigned — opens a candidate "warm-paper utility" cluster (sole member).
- **Lineage:** native (med) — behaviors read AppKit/SwiftUI menu-bar-extra: floating popover with no window chrome/traffic-lights (correct for menus/popovers), monochrome SF-Symbol-class line icons, a real `⌘,` command-symbol glyph, inset-rounded selection. The two tells against native are cosmetic house style (tracked-uppercase section headers; brand accent overriding the system accent), not framework tells. Marked medium because the surface is a marketing render, not a captured screenshot.
- **Era (chrome):** custom (Tahoe-compatible geometry) — opaque cream popover with generous radii (~18pt card, ~10pt selection) and a capsule status pill; no visible Liquid Glass lensing/translucency. Absence of glass on a content-bearing popover is legitimate, so this is a themed-opaque surface, not legacy-native and not committed liquid-glass.

> **Evidence caveat:** the only app UI is the panel *inside a 1200×630 marketing OG banner* (`cover.png`) — a stylized product render at unknown logical scale, not a screenshot. All panel metrics are ratios/estimates; no true point sizes are claimed. Everything on the left half (the `//` wordmark lockup, the serif headline "Six healthy breaks, backed by science.", the `caesura.rest` subtitle) and the app icon are **brand evidence**, kept separate from the app-UI tokens below. Per Workflow A (UI only) no `icons/caesura.md` is written — the `//` mark is recorded here as brand context.

## Tokens

### App UI — the menu-bar dropdown (all `(estimated)(inferred)` — single stylized render)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/popover | cream `#FDFAF5` opaque | (estimated)(inferred) | Card fill; sits ~1 lightness step **above** the page cream `#FBF6EE` — minimal tonal elevation + soft shadow, no glass |
| bg/status-capsule | cream `#FBF7F0`, capsule (radius = h/2) | (estimated)(inferred) | Compact status row: `//` mark + "12m" (bold ink) + "87%" + "14:30" (secondary); right-aligned cluster |
| accent/primary | terracotta / burnt sienna `#B35A3C` | (measured)(confirmed) | Selection fill; identical hex to the icon stroke — one brand hue across icon + UI. **Overrides the system accent** (see Signature/Defects) |
| ink/primary | warm near-black `#2B2620` | (measured)(inferred) | Labels, bold "12m"; warm dark-brown-black, not pure #000 (avoids Contrast Dilution) |
| ink/secondary | warm taupe `#8A8073` | (measured)(inferred) | "in N min" values, "UP NEXT"/"SNOOZE ALL" headers, "87%"/"14:30" — strong de-emphasis, but see Defects (contrast) |
| type/label | sans (system/SF-class), ~20–22px @canvas, Regular, `#2B2620` | (estimated)(inferred) | Break names; large in the marketing canvas — true pt unknowable |
| type/secondary | sans ~17–18px @canvas, `#8A8073` | (estimated)(inferred) | Right-aligned "in N min" trailing metadata |
| type/section-header | tracked UPPERCASE ~11–12px @canvas, ~+0.12em, `#8A8073` | (estimated)(inferred) | "UP NEXT" / "SNOOZE ALL · 5M" — editorial house style; a native-tell deviation (HIG wants sentence/title case) |
| selection/fill | `#B35A3C`, inset ~12px L/R, radius ~10px, ~47px tall | (estimated)(inferred) | Correct **inset-rounded** grammar; solid saturated fill + knockout text (System-Settings-style), recolored to brand |
| selection/text | paper cream `#FBF6EE` (knockout) | (measured)(inferred) | White-ish label + "in 12 min" + drop glyph; cream-on-terracotta ≈ 5.3:1, passes 4.5:1 |
| icon/list | monochrome line icons ~20px, ~1.5px stroke, `#2B2620` | (estimated)(inferred) | drop / eye / seated-figure / hands / figure.walk / concentric-target — SF-Symbol-class, consistent stroke |
| radius/card | ~16–20px | (estimated)(inferred) | Popover corner; window corner radius kit-gap, so this is a useful data point (themed, not the ~system value) |
| row/height | ~51px pitch @canvas, full-width click target | (estimated)(inferred) | Comfortable consumer density; well above the 44px Fitts floor for a pointer popover |
| divider/footer | hairline, very low-contrast warm gray | (estimated)(inferred) | 1px separator above the "Snooze all" footer |

### Brand (marketing composite — NOT app-UI tokens, kept separate)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | warm paper `#FBF6EE` | (measured)(inferred) | Marketing ground, not the app surface |
| brand/headline | high-contrast serif display (transitional/modern, Times/Charter/Tiempos class), `#2B2620` | (estimated)(inferred) | "Six healthy breaks, backed by science." — carries the editorial-literary voice the UI itself does not |
| brand/mark | `//` two rust `#B35A3C` diagonal strokes, rounded caps, slight right slant | (measured)(inferred) | The **caesura mark** (musical/prosodic pause) — literal name-to-glyph; reused as the in-UI status glyph |
| icon/bg | cream squircle, transparent outside | (measured)(inferred) | Big-Sur-era flat single-layer icon; no gradient, no glass layering — the `//` mark centered |

## Layout skeletons

**Menu-bar-extra dropdown (cover.png, right half):** two stacked floating cards over the marketing cream.
- *Top — status capsule:* a full-capsule cream pill, contents right-aligned: `//` mark · **12m** (bold ink, next-break countdown) · 87% (secondary) · 14:30 (secondary clock). Reads as the menu-bar item's status echoed into the popover.
- *Below — the popover card* (~18px radius, soft shadow): (1) tracked-uppercase muted header "UP NEXT"; (2) a 6-row list — each row = left monochrome icon on a shared left axis, a break label on a second left axis, and a right-aligned "in N min" on a shared right axis; the first row (Water) is the selected/next item painted in a terracotta inset-rounded fill with knockout cream text; (3) a hairline divider; (4) a footer row: "SNOOZE ALL · 5M" (tracked caps, left) and `⌘,` (trailing shortcut hint). No traffic lights, no toolbar, no sidebar — the popover is the whole surface, which is native-correct for a menu-bar extra.

## Signature moves
- **[GOLDEN-NUGGET] The name is the design system.** "Caesura" is the literary/musical term for a pause; the app about *rest* mines that concept end-to-end: the `//` caesura mark is logo + status glyph, the marketing voice is serif-editorial, and the palette is warm paper + terracotta — the color temperature of a paper notebook, deliberately opposite the cold clinical blue of Time Out / Stretchly / LookAway. This is subject-mined, committed direction (warm / literary / calm), not the reflexive AI warm-editorial default: the editorial family is *earned* by the subject. The load-bearing UI decision is the terracotta selection fill standing in for the system accent — the one saturated moment per view lands the eye on "what's next."
- **[GOLDEN-NUGGET] De-emphasis discipline via one warm-taupe token.** Every non-primary string — trailing "in N min", both section headers, the "87%/14:30" status — is the single taupe `#8A8073`, letting the near-black break names and the one terracotta row own all attention. Hierarchy is carried by two ink tiers + one accent, not by size inflation.

## Defects
- **Accent-binding override (signature, not anti-pattern) — excluded from macOS canon.** Selection uses the app's brand terracotta, not the user's `controlAccentColor`. Systematic + purposeful (the warmth *is* the product) + accessible (cream-on-terracotta ≈5.3:1) → recorded as a signature per defect-vs-signature, but its grammar (brand hue replacing system accent) must never be learned as native "mac taste."
- **Tracked-uppercase section headers — mild non-native tell.** "UP NEXT" / "SNOOZE ALL" are tracked caps; HIG wants sentence/title-case system-font headers (the #1 sidebar/list authenticity tell). Here it is deliberate editorial styling on a consumer popover, so low-stakes, but it is the clearest web-leaning choice on the surface.
- **Contrast Dilution (mild) at the smallest labels.** The taupe `#8A8073` on cream ≈ ~3.5:1 — fine as large/non-text (passes 3:1) but below 4.5:1 for the ~11–12px tracked-caps headers. Fix: darken headers toward `#000@50%`-equivalent while keeping the trailing metadata muted.
- **Possible information-scent inconsistency (likely marketing placeholder data).** The highlighted "next" row is Water "in 12 min", yet Wrists shows "in 04 min" — a sooner break that is not the one flagged. Either the list is category-ordered with Water pinned/scheduled-next, or the render used inconsistent placeholder timings. Recorded as a content note, not a design law; unverifiable from one render.
- **Evidence poverty (not the app's fault):** one surface, one state, from a marketing render — settings/onboarding, the actual break overlay, dark mode, real pt sizes, and strict 8pt-grid verification are all unseen.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar dropdown (light composite) | 12/14 | #1 grid — ~51px row pitch not verifiably on 8pt at marketing scale (soft/estimated) · #9 text contrast — taupe `#8A8073` headers ≈~3.5:1 below 4.5:1 for small text. Passes: #2 three clean alignment axes (icons/labels/trailing) · #3 proximity (icon↔label tight, rows + header/footer separated) · #4 ~3–4 sizes · #7 strong de-emphasis · #8 action singularity (one terracotta row) · #11 ~51px full-width targets. N/A→pass: #5/#6 (no paragraphs) · #12/#13 (no inputs/form labels) · #14 (no focus state in a still) |
| — native-tells audit | 8/10 | Fails: #4 tracked-uppercase headers (not sentence/title case) · #6 accent bound to brand terracotta, not system accent. Passes: #1 native-reading behaviors · #2 no glass, opaque content (legitimate absence) · #3 inset-rounded selection grammar · #5 comfortable consumer density · #7 one prominent action · #8 concentric radii (selection 10 < card 18) · #10 genuine menu-bar-extra chrome (correctly no traffic lights, no faked frame). N/A: #9 toolbar (menu popover has none) |

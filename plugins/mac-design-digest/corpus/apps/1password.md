# 1Password — profile

- **Source:** macapp.supply (cover composite only — no standalone shots supplied) · **Surfaces digested:** main window (three-pane vault browser), light mode · **Last updated:** 2026-07-19
- **One-sentence identity:** a conscientious Electron app that emulates Mail/Finder's three-pane native chrome more faithfully than almost any web-lineage peer — then signs its work in periwinkle-violet field labels no AppKit app would ever draw.
- **Cluster:** unassigned (candidate seed for a *non-native, brand-tinted Electron utility* cluster — a tells-and-corrections record, not macOS canon)
- **Lineage:** web-electron (high) — non-native evidence, excluded from macOS canon; recorded as tells + corrections
- **Era (chrome):** Electron-drawn, targets the Big Sur→Sonoma native visual language (rounded chrome, capsule search, soft translucency). **Not** Liquid Glass — no lensing, no over-glass container morphing, no scroll-edge effect visible.

## Provenance caveat

Evidence is a single **marketing cover composite** (1200×630, JPEG, ~1× render), not a retina screenshot. The app window occupies the right ~560px and is cropped at the right edge. All pixel/type/spacing values are `(estimated)` with wide ranges; colours are JPEG-shifted (sampled hexes carry ±one step of error). The left half of the cover — icy-mint→periwinkle diagonal gradient, deep-navy wordmark + "Download 1Password for Mac" headline — is **brand** evidence, analysed separately below, never conflated with the app UI.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/sidebar | `#E1E1E1` light gray (estimated)(inferred) | | vibrancy-style source-list panel; sits under coloured traffic lights |
| bg/content | `#FEFEFE` near-white (estimated)(inferred) | | item list + detail panes |
| sel/sidebar-fill | `#CAD1DB` soft blue-gray, inset rounded, dark text (estimated)(inferred) | | correct macOS **source-list** selection (non-first-responder soft fill) |
| sel/list-fill | `#0073ED` saturated accent, **white** text, inset rounded (estimated)(inferred) | | correct macOS **focused-table** selection (emphasized). Reads as system blue (kit light blue `#0088FF`), JPEG-shifted greener |
| accent/primary | system blue ~`#0073–0088FF` (estimated)(inferred) | | bound to selection + search + link colour — accent binding is correct |
| label/field-violet | `~#8A80E0` periwinkle-violet, lowercase (estimated)(inferred) | | **signature** — every detail field label (username/passkey/password/website). Brand-owned, NOT a system semantic colour |
| label/section-header | `~#A9A9A9` mid-gray, **TRACKED UPPERCASE** (estimated)(inferred) | | CATEGORIES / VAULTS + A–Z index letters — the #1 non-native sidebar tell |
| text/primary | near-black, ~medium weight (estimated)(inferred) | | list row titles |
| text/secondary | `~#8A8A8E` gray (estimated)(inferred) | | emails, "917 bytes" metadata; de-emphasis is present |
| type/body | ~14–15px system sans (estimated)(inferred) | | reads a touch larger than native 13pt Body — an Electron density tell |
| type/section-header | ~11px, tracked (estimated)(inferred) | | |
| chrome/sidebar | ~220–230px render width; full-height; account switcher + source list (estimated)(inferred) | | proportionally consistent with native 256pt sidebar; can't map to points from a 1× render |
| chrome/traffic-lights | red `#FF5D54` / yellow `#FABA32` / green `#2CC841` — all coloured (estimated)(inferred) | | genuine, **focused** window; JPEG-shifted from `#FF5F57/#FEBC2E/#28C840` |
| control/search | capsule field, "Search in Brightside Systems" hint, leading magnifier (estimated)(inferred) | | correct hint-placeholder + capsule bezel; ~28–32px tall |
| radius/item-icon | ~14px squircle on 64px item hero (estimated)(inferred) | | brand favicons per row/item |
| field-group/card | rounded container, hairline-separated stacked rows (estimated)(inferred) | | **iOS/web inset-grouped card** — native macOS would use flat labels on one surface |

## Layout skeletons

**Main window — three-pane vault browser (master → list → detail):**
- **Pane 1 — Sidebar (source list, ~225px render):** traffic lights top-left → account switcher ("Brightside Systems" + building glyph + single down-chevron pull-down) → source rows (Profile, **All Items** [selected, soft inset fill], Favorites [yellow star identity glyph], Watchtower) → collapsible section `CATEGORIES` (chevron) → section `VAULTS` (chevron + trailing `+`) with coloured-circle vault rows each trailing a gray "people" shared-glyph → Archive, Recently Deleted at foot. Section headers TRACKED UPPERCASE.
- **Pane 2 — Item list (~230px render):** header = 2×2 grid glyph + "All Categories" pull-down (down-chevron) + trailing borderless search-scope + sort-order symbols → alphabetical **jump index** (`#`, `A`, `C`, `G`… tracked gray letters) sectioning two-line rows: brand favicon + primary title (dark) over secondary subtitle (gray email/size). Selected row = saturated blue rounded fill, white text.
- **Pane 3 — Detail (cropped):** mini vault-context bar (building | gear "Employee" vault) → large ~64px item icon → grouped field **card** (violet lowercase label + value per hairline-separated row: username / passkey / password[dots]) → ungrouped fields below (website: violet label + blue link value) → expandable "Last edited" history row with `>` disclosure.

## Signature moves
- **[GOLDEN-NUGGET] The violet field-label system.** Every detail-pane field label (username, passkey, password, website) set in periwinkle-violet `~#8A80E0`, lowercase — a deliberate, systematic, brand-owned typographic decision. No native macOS app labels fields this way (native = secondary-gray, title-case, colon-terminated). It is simultaneously the app's strongest identity signal *and* its clearest departure from the platform. This is the choice that makes a 1Password screen recognizable at a glance.
- **[GOLDEN-NUGGET] Faithful selection-duality emulation.** The Electron UI correctly renders the macOS two-body selection grammar: sidebar shows the *soft inset* source-list fill while the content list shows the *solid accent* focused-table fill with white text — because only one pane holds first-responder focus. Most web apps flatten these to one style; 1Password reproduces the real AppKit behaviour. A textbook case of "match the system" done in Electron.
- **Brand-warm consumer chrome over a security tool.** Coloured per-item favicons, a yellow-star favorite, a friendly account-switcher emoji-glyph — warmth deployed to make a security utility approachable (aesthetic-usability buying trust).

## Defects
- **Non-native: tracked UPPERCASE section headers** → `CATEGORIES`, `VAULTS`, and the A–Z index letters are tracked uppercase → HIG `sidebars.md`/`lists-and-tables.md` explicit "common non-native mistake" (native = system-font, semibold, secondary-colour, sentence/title case). Correction: sentence-case, SF Pro Semibold, secondary label tier.
- **Contrast Dilution (partial)** → violet field labels `~#8A80E0` on light card measure ~2.6–3.0:1, below WCAG 4.5:1 for text; secondary gray subtitles borderline ~3.5–4:1. De-emphasis achieved partly by dropping a brand hue under the contrast floor. Correction: darken labels to a ≥4.5:1 violet or move to the secondary-label alpha.
- **iOS-style inset-grouped field card** → detail fields wrapped in a rounded, hairline-separated card → native macOS forms use flat labels on one opaque surface, not iOS inset-grouped cards. A UIKit/web-derived pattern.
- **Density tell** → body ~14–15px vs native 13pt Body → the classic Electron "runs one size loose" signature.

## Rubric history
| Surface | 14-pt Score | Native-tells | Failures |
|---|---|---|---|
| main window (light) | 12/14 | 7/10 | 14-pt: #9 violet-label contrast ~2.8:1; #10 hairline field separators <3:1. Native: #1 lineage web-electron; #4 tracked-uppercase headers; #5 density ~14–15px (borderline). |

## Brand evidence (cover backdrop — NOT app UI)
- Backdrop: soft diagonal gradient, icy-mint `#E9F9F9` (top-left) → periwinkle-blue `#AECFF2` (bottom-right).
- Wordmark + headline: deep navy/indigo `#1A2553`, heavy geometric sans, left-aligned, ranged-left three-line headline "Download / 1Password / for Mac".
- The backdrop's periwinkle relates chromatically to the in-app violet field labels — a coherent brand-colour thread from marketing surface into product.

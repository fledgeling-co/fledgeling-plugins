# Resurf — profile

- **Source:** macapp.supply (`sources/resurf/`) · **Surfaces digested:** main window (three-pane, light) from marketing cover · **Last updated:** 2026-07-19
- **One-sentence identity:** mymind's visual everything-bucket rebuilt on a genuinely native macOS shell — a Pinterest-style card library wearing a real source-list sidebar, borderless SF-Symbol toolbar, and an AI inspector, with all editorial warmth quarantined to the marketing serif.
- **Cluster:** unassigned (candidate: *calm-neutral library* — soft near-white grounds, masonry card capture, one system-blue functional accent)
- **Lineage:** native (med confidence) — non-native evidence never feeds macOS canon
- **Era (chrome):** Liquid-Glass-era aesthetic (2026, capsule token bezels, soft radii) **but chrome renders flat/opaque** — no Liquid Glass material shown; glass-discipline checks are therefore N/A, and the surface would read equally as late Big-Sur.

## Evidence caveat
Single surface, and it is a **marketing composite**: a serif headline + sans subhead sit on a warm-grey backdrop above the app window, and a floating white "Resurf" brand pill is composited over the content grid (excluded from app evidence). The window is scaled for the composite (traffic-light cluster measures ~56px against a ~2085px-wide window — not a clean @1x or @2x), so **absolute pt values are `(estimated)` with a scale caveat; proportions and ratios are the reliable readings.** Everything below is one-surface `(inferred)`.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/content | ~#FCFCFC near-white | (estimated)(inferred) | content pane |
| bg/sidebar | ~#F4F4F4 warm-grey | (estimated)(inferred) | subtly grayer than content — native two-tone chrome |
| bg/backdrop (marketing) | ~#F9F9F9 warm-neutral | (estimated) | composite ground, not app |
| text/primary | ~#1D1D1F near-black | (estimated)(inferred) | sidebar labels, card titles, assistant body |
| text/secondary | ~#8A8A8E system grey | (estimated)(inferred) | section headers, count badges, card type-icons |
| text/tertiary (dimmed) | ~#B0B0B4 | (estimated)(inferred) | faint "Areas" items (Add Item / Personal / Design Engineering) — borderline legibility, see Defects |
| accent/functional | system blue ~#0088FF | (estimated)(inferred) | content-card selection ring; matches kit Blue-light `#0088FF (specified)` |
| accent/brand | pink/magenta ~#E15A95–#FF3B8F | (measured)(inferred) | "Beta" pill + Assistant sparkle only — jewelry, never a CTA |
| identity/area colours | low-sat pastels (mint, amber, green) | (estimated)(inferred) | per-area sidebar icons — separate from accent, from a muted palette |
| selection/sidebar | neutral grey fill ~#000 @6–8%, inset rounded, radius ~8pt | (estimated)(inferred) | NOT accent-tinted; matches kit sidebar-selection radius 8 `(specified)` |
| selection/content | ~2px system-blue ring on the card | (estimated)(inferred) | different grammar from sidebar — see Defects |
| radius/card | ~12pt | (estimated)(inferred) | outer content cards |
| radius/inner-preview | ~8pt | (estimated)(inferred) | rendered preview inside a card (concentric step-down) |
| radius/chip + search | capsule (token) / ~10–12pt (field) | (estimated)(inferred) | "Recent ✕" filter token is a capsule |
| border/card | ~#000 @8%, 1px | (estimated)(inferred) | ~1.1:1 — well under 3:1, see Defects |
| type/body | ~13pt-class SF Pro Regular, lh ~1.5 | (estimated)(inferred) | maps to kit Body 13pt `(specified)` |
| type/card-title | ~14–15pt SF Pro Medium | (estimated)(inferred) | card footer label |
| type/caption | ~11pt | (estimated)(inferred) | count badges (14, 17) |
| brand/display (marketing) | transitional **serif**, ~48–56pt, near-black | (estimated) | headline only; app UI carries no serif |
| chrome/sidebar | ~200pt wide, full-height, flat opaque, ~24–28pt rows | (estimated)(inferred) | kit example is 256pt; width varies by app |
| chrome/toolbar | flat opaque, borderless mono SF Symbols, ~40–52pt tall | (estimated)(inferred) | no glass, no scroll-edge effect visible |

## Layout skeletons

**Main window — three-pane master/inspector.**
- **Window chrome:** genuine coloured traffic-lights top-left (window is key). Toolbar leading cluster = back (enabled) / forward (disabled, dimmed) / sidebar-toggle, then a **breadcrumb path** `Library › All` (secondary "Library", primary-bold "All"). Trailing cluster = `+` (new item) / `✦` (Assistant) / `…` (overflow) — three borderless symbols.
- **Left — source list (~200pt):** flat rows, leading mono SF Symbol + label. Order: Home, Assistant · section `Triage ⌄` → Inbox (14), Later · section `Library ⌄` → **All (selected)**, Pinned, Archive, Tags (17) · section `Areas ⌄` → Add Item, Mac Apps, Personal, Design Engineering. Section headers are **sentence-case, system font, secondary grey, with disclosure chevrons** (collapsible). Count badges right-aligned, secondary. Selection = neutral grey inset-rounded fill.
- **Centre — card library:** an **in-content search/filter row** (capsule search field holding a removable `Recent ✕` token + "Search anything…" placeholder) with four trailing borderless view-controls (filter / focus / sort ↕ / grid ⊞), over a **masonry (variable-height) grid of preview cards**. Each card = a rich rendered preview (image collage, icon strip, phone mockup, widget render, dark code snippet) + footer (type-icon + title). One card ("Understanding Gradients") carries the blue selection ring.
- **Right — Assistant inspector (opt-in):** floating rounded panel. Header = `✦ Assistant [Beta]` + trailing history / `+` / filled-circle `✕`. Body = a chat/AI response: bold pull-quote, "More specifically:", then a bulleted list with **bold lead-in labels** (Palette / Form language / Rendering / Mood / Composition / System vibe) + regular descriptions — textbook de-emphasis.

## Signature moves
- **[GOLDEN-NUGGET] The masonry visual library as the primary content surface.** The whole product is a heterogeneous *visual* everything-bucket, so it borrows the web/Pinterest card-wall pattern deliberately — systematic, purposeful, and the thing that gives Resurf its face. Native alternative (NSCollectionView gallery) reaches the same place; the choice is a signature, not a defect.
- **AI copilot in the inspector slot.** The "Assistant" lives as a right-side embedded inspector panel (HIG's preferred spot over a floating utility panel), not a modal — with its own reserved pink identity.
- **Two-hue accent discipline:** system **blue** carries every functional moment (selection/focus ring); a single **pink** is reserved purely for AI/Beta identity (the Beta pill, the sparkle) — used as jewelry, never on an action. Per-area icons draw from a separate muted pastel identity palette.
- **Serif brand / sans app split.** The editorial warmth (serif display headline) exists only in marketing; the app itself is disciplined all-SF-Pro. The warmth is a costume worn outside the window, not inside it.

## Defects
- **Split selection grammar.** Sidebar selection = neutral grey inset fill (no accent tint on text/glyph); content selection = blue accent ring. Two languages for one concept. Canon wants one accent-bound selection grammar across sidebar and content (native-tell #3). Defensible as nav-vs-selection, but logged.
- **Contrast Dilution (borders + faint labels).** Card borders ~#000 @8% (~1.1:1) sit far under the 3:1 non-text floor; the dimmed "Areas" items (~#000 @25–30%) hover near the 4.5:1 text floor. The soft aesthetic is bought partly with legibility — aesthetic-usability has limits.
- **Minor iOS-flavoured tell:** filled-circle `✕` close on the Assistant panel reads slightly UIKit; a native panel closes via plain chrome. Not systematic enough to reclassify lineage.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (light) | 12/14 | #9 faint "Areas" labels near text-contrast floor; #10 card/divider borders ~1.1:1, under 3:1 |
| main window (native audit) | 8/10 | #3 split selection grammar (sidebar grey vs content blue); #6 partial — functional accent consistent but selection hue split undercuts binding |

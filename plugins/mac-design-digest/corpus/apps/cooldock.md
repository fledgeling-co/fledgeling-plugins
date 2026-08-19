# Cooldock — profile

- **Source:** macapp.supply (dock.cool, paid, shipping) · **Surfaces digested:** product dock bar (cover), dock appearance variants (shot-1), widget catalog grid (shot-2), business-widget showcase (shot-3) · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple's WidgetKit glance-language reimagined as a horizontal *Dock-shaped* widget strip on a wallpaper-lensing glass bar — Widgetsmith's card vocabulary meets the MacBook Touch Bar, marketed in full Apple-keynote cosplay.
- **Cluster:** unassigned (candidate seed: "glanceable-widget-dark" / non-native consumer-widget canvas)
- **Lineage:** unknown (low) — these are widget-catalog composites with **no window chrome** (no traffic lights, menu bar, sidebar, or toolbar) to classify the host framework. The visible design language is unmistakably **WidgetKit / iOS-widget grammar** (glance-value-over-caption faces, saturated per-app hues, today-chip selection), rendered as **custom-drawn faces** (flip-clocks, contribution heatmaps, analog dials) beyond stock system widgets. **This evidence must NOT feed macOS native canon** — a widget-catalog surface with bespoke faces is not window-native evidence regardless of the host's true framework.
- **Era (chrome):** custom — bespoke dock shell + custom widget faces; the **bar itself shows Liquid-Glass-style lensing** (desktop wallpaper visibly refracts/bends through the bar in shot-1), so it is liquid-glass-*influenced* but not stock-material.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| canvas/catalog | `#000000` true black (measured)(confirmed) | | shot-2 / shot-3 gallery ground — pure black, marketing/OLED presentation |
| bg/widget-card-dark | `#0A0A0C`–`#1A1A1E` (measured)(confirmed) | | card fill sampled `#0A0A0A` on `#000` = ~4% lift → cards barely separate from canvas (see Defects #10) |
| bg/bar-glass-dark | dark translucent, wallpaper-lensing (estimated)(inferred) | | cover + shot-1 rows 1–2: refractive glass, not flat opaque |
| bg/bar-light | `#F2F2F4` bar / `#FFFFFF` cells (estimated)(inferred) | | shot-1 row 3 light appearance variant |
| bg/bar-opaque-dark | `#0C0C0E` flat (estimated)(inferred) | | shot-1 row 4 opaque dark variant (glass disabled) |
| type/glance-value | ~28–40pt-equiv, Bold, SF-family (rounded-leaning) (estimated)(confirmed) | | 16:04 · 34° · 100 · 6 042 US$ — glanceable, tabular numerics; NOT the 13pt macOS Body ramp (surface-appropriate for widgets) |
| type/caption | ~10–13pt-equiv, Regular, secondary gray (estimated)(confirmed) | | "Mon, Jul 6" · "42 orders · last 7d" · "net revenue · last 30 days" |
| type/label-mid | ~13–15pt-equiv, Regular/Medium (estimated)(inferred) | | "Sales / Orders / AVG Order" rows, "Sent today / Delivered" |
| accent/system-green | `#3DB45B` (measured)(confirmed) | | streak heatmap + battery/charge ring — **system-green adjacent** (kit dark Green `#30D158`): platform-palette fidelity |
| accent/status-green | `#2BA03A` (measured)(confirmed) | | positive delta arrows "↑ 22%", stock "+1.12%" — paired with value (good) |
| accent/status-red | ~`#FF453A`-class (estimated)(inferred) | | stock "-3.79%" — paired with value/glyph |
| accent/status-orange | ~`#FF9F0A`-class (estimated)(confirmed) | | "Overdue", "In Progress · Today" (Linear widget) — paired with label |
| accent/today-chip-blue | ~`#0A84FF`-class (estimated)(confirmed) | | calendar "18" + weather "Thu 18" solid-fill today chip — iOS-widget selection (kit dark Blue `#0091FF`, near) |
| identity/brand-hues | per-widget (Shopify `#619129`, TikTok/X mono, PayPal blue, Zoom `#0B5CFF`) (measured/estimated)(confirmed) | | app/brand icons carry their own hue — correctly separate from system accent |
| radius/bar-outer | ~28–34pt (estimated)(inferred) | | dock pill outer radius (display scale; halve if @2x) |
| radius/widget-card | ~16–22pt (estimated)(confirmed) | | inner cell radius — steps down under bar radius (concentric-ish) |
| radius/chip | ~8–10pt (estimated)(inferred) | | today-chip / small pills |
| divider/cell | hairline dark-on-dark, <3:1 (measured)(confirmed) | | inter-cell separators on the bar barely visible — UI-contrast risk |

## Layout skeletons

**Cover — product dock bar (glass, dark), over AI-nature hero.** Single horizontal capsule bar, full-width-centered, ~5 widget groups left→right: [clock 16:42 + date] · [weather 26° Today + 3-day column forecast] · [2×2 app-launcher grid] · [battery/charge ring "57" green] · [Now-Playing: artwork + title/artist + scrubber + 3 transport controls]. Serial-position layout (time leads, media trails). Brand layer above (separate evidence): Apple logo + "Your smart second Dock" eyebrow, then a ~2-line Helvetica/Neue-Haas-Black keynote headline "A useful Dock for live widgets."

**shot-1 — appearance variants.** Four identical widget sets stacked, each over a different wallpaper, demonstrating the material system: (1) dark glass over wildflowers, (2) glass over blue-streak wallpaper with **visible lensing/refraction of the wallpaper through the bar**, (3) light/white opaque, (4) dark opaque over daisies. Widget order per bar: clock · analog clock · weather 34° · 2×2 launcher · battery ring 100 · "Thinking… 1m 39s" AI-status widget · dotted countdown ring 16:04 · inbox glyph.

**shot-2 — widget catalog grid (dark, on #000).** Dense masonry-ish gallery of ~50 widget faces at mixed sizes (1×1, 2×1, 2×2, wide): mail-unread, contribution/attendance heatmaps with % , meeting/Zoom, calendar week-strip + agenda-dots, notes, CPU sparkline + ring, network up/down graph, compass, digital + analog + flip clocks, sunrise arc, weather hourly/daily, stock rows + sparkline + hero-quote, revenue, visitors, quick-action button clusters, media scrubber + waveform recorder, emoji strip, social-follower counts (TikTok/X), flip-digit clock, contact avatars + call/video/message pills, timers (0:13.0, focus 2/4), currency converter. Browse surface — option density is the point.

**shot-3 — business-widget showcase (dark, on #000).** ~8 hero-styled prosumer cards on a looser grid: Shopify sales (3 layout variants: label-value rows / big-number / number+trend-line), PayPal visitors, contribution-streak heatmap ("5 today · 23 week · 🔥 streak"), Resend email stats (Sent/Delivered/This month), Dub clicks/leads/sales, and a **Linear issue widget** ("ENG-128 · Fix dock tooltip clippin… · In Progress · Today"). Each card: brand icon (corner-badged "7D"/"TDY") + de-emphasized caption + dominant value.

## Signature moves
- **[GOLDEN-NUGGET] The desktop-lensing glass bar.** The dock's defining choice is a floating glass strip that *refracts the wallpaper behind it* (shot-1 row 2 bends the blue-streak wallpaper through the bar) — the desktop becomes the bar's material. In Liquid-Glass grammar terms it is (in spirit) correct: the **floating bar is glass, the widget faces are opaque content** — the Golden Rule read backwards but honored.
- **[GOLDEN-NUGGET] Dock-as-widget-canvas.** Reframing the horizontal Dock/Touch-Bar footprint as a live-widget strip is the whole product thesis; the layout inherits Dock muscle memory (Jakob's Law) while delivering glance data.
- **Glance-first tabular typography.** Every face pairs one Bold tabular-numeric value with a quiet secondary caption — textbook de-emphasis (label whispers, number speaks), applied ~50 times consistently.
- **Real dogfooding as demo data.** The Linear "ENG-128 · Fix dock tooltip clipping · In Progress" card uses the dev's own live issue tracker — evidence of a genuinely shipping tool, and a quiet flex.
- **Apple-keynote cosplay (brand, not app).** Cover apes Apple marketing exactly: Apple logo eyebrow, ultra-bold black keynote headline, hyperreal Apple-wallpaper-style nature hero. Effective; also trademark-cheeky.

## Defects
- **Contrast Dilution (borderline)** → tertiary gray captions on pure `#000`, and glance text on the glass bar over *busy* wallpapers (clock over wildflowers, shot-1 row 1), approach the 4.5:1 floor → readability depends on wallpaper. Canon: solidify/firm the bar material behind text, or keep a legibility floor per label tier.
- **UI Contrast (#10)** → widget-card fill `#0A0A0A` on `#000` canvas (~4% lift) and hairline dark-on-dark inter-cell dividers fall <3:1 → cards/cells separate almost only by radius. Canon: raise card fill or add a ≥3:1 hairline.
- **Target Starvation (mild)** → 2×2 app-launcher glyphs (~20px) and small transport/edit/pencil circles are small pointer targets; fine for a glance widget but near the 24px WCAG floor.
- **Glass-on-glass risk (insufficient evidence)** → per-cell lensing on the bar (shot-1 row 2) could read as glass-in-content; can't confirm from stills whether it's one bar glass layer or per-cell glass. Recorded, not asserted.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| cover — product dock bar (glass, dark) | 12/14 | #10 sub-3:1 cell dividers; #9 borderline glance-text over busy wallpaper |
| shot-1 — appearance variants | 11/14 | #9 light-variant + text-over-wallpaper contrast; #11 small launcher targets |
| shot-2 — widget catalog grid | 12/14 | #10 card-on-#000 separation <3:1; #11 sub-24px sub-glyphs |
| shot-3 — business-widget showcase | 12/14 | #10 low card/canvas contrast; #9 dim tertiary captions on black |

**Native-tells audit (all four surfaces):** ~3/10 *applicable* — the audit targets window surfaces and is **N/A-dominant here** (no chrome, sidebar, toolbar, or menu to score). Applicable reads: glass-only-on-floating-chrome **passes in spirit** (bar glass, faces opaque); concentric corners **pass** (bar radius > cell radius); native-lineage **unverified**; 13pt/24pt density **fails but surface-appropriate** (WidgetKit glance type); single-accent binding **N/A** (per-widget identity hues are legitimate). Do not treat the density/selection reads as macOS defects — they are widget-surface properties.

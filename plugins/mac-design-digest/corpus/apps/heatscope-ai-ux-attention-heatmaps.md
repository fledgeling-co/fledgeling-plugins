# HeatScope AI UX Attention Heatmaps — profile

- **Source:** macapp.supply (meta.json) · **Surfaces digested:** 1 (marketing OG cover composite; no in-app screenshots supplied) · **Last updated:** 2026-07-19
- **One-sentence identity:** A thermographic brand system (heat-gradient icon + rainbow attention overlay) wrapped around a **stock web SaaS dashboard used as a demo canvas** — the memorable part is HeatScope's product overlay, not any app chrome; think "Framer/Gumroad indie-Mac launch card" hosting a Hotjar-style heatmap.
- **Cluster:** unassigned (candidate: `gradient-marketing-composite` — a non-native brand/marketing cluster, not a macOS UI cluster)
- **Lineage:** **web-electron** (high confidence) for the only "app UI" present; the wrapping window is a decorative mockup frame, not a real macOS surface — **excluded from macOS canon** (contrast evidence only)
- **Era (chrome):** custom / web-dashboard (flat, elevated-card; not Liquid Glass, not legacy AppKit). Brand icon is Big-Sur-era gradient squircle, not layered Liquid Glass.

## Evidence integrity (read first)

The inputs are **cover.png + icon.png only — zero real app screenshots.** `cover.png` is a **1200×630 Open Graph marketing composite**, not a screenshot. It contains three distinct evidence layers that must never be conflated:

1. **Brand layer** (HeatScope-authored, real evidence): mint mesh-gradient ground, "Heat Scope" geometric-grotesk wordmark, gradient-bolt squircle icon, glossy black pill "Download HeatScope" CTA with Apple logo.
2. **Product-overlay layer** (HeatScope-authored, real evidence): a full-spectrum thermal attention heatmap (blue→green→yellow→orange→red) blended over a UI, plus circular numbered attention-rank badges (1→10) and a "65.1% attention" annotation pill. This is the actual product output and the app's true signature.
3. **Host-UI layer** (NOT HeatScope's design): the window interior is a generic third-party admin-dashboard template branded "AlphaVault" — a demo surface the heatmap is painted onto. It is web/dashboard trade dress, obscured ~40% by the overlay, and is recorded as contrast evidence only. Do not attribute its tokens to HeatScope.

All measurements are `(estimated)`/`(assumed)`: sub-retina composite, downscaled inner UI, heatmap obstruction. No native-canon evidence is produced by this app.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop-gradient | mint `#CEF0BF` → green `#74D895`, diagonal mesh (lighter top-left, more saturated right) | (measured)(inferred) | composite ground; consumer-fresh, single-hue green family |
| brand/cta-fill | `#000000` pill, ~56pt tall, capsule radius, white label + Apple glyph | (measured)(inferred) | one saturated dominant CTA — Von Restorff done right |
| brand/wordmark | "Heat Scope" black geometric grotesk, Regular, ~two-word split with wide space | (estimated)(inferred) | not a native SF face; marketing display type |
| icon/ground-dark | `#2E2E2E` charcoal (left half + bolt negative form) | (measured)(inferred) | grainy/noise texture throughout |
| icon/thermal-gradient | top `#F6F8F7` → green `#88BE66` → amber `#FCBB0B` (warm-side thermal, no blue) | (measured)(inferred) | heat ramp revealed by the bolt cut |
| icon/shape | rounded squircle, ~22% corner radius, single flat gradient layer + grain | (estimated)(inferred) | Big-Sur-era consumer icon, NOT layered Liquid Glass |
| product/heatmap-ramp | thermal spectrum blue→cyan→green→yellow→orange→red, soft-blended blobs | (measured)(confirmed) | the product's core visual grammar; matches Hotjar/Crazy Egg convention |
| product/rank-badge | white disc ~22–26px, dark centered numeral, ranked 1→10 | (measured)(inferred) | imposes an explicit attention eye-path |
| product/annotation-pill | dark `#333`-ish capsule, white text "65.1% attention" | (estimated)(inferred) | over-content callout |
| host/window-canvas | outer strip `#F0F0F5`, content `#FEFDFC` near-white | (measured)(inferred) | host template, not HeatScope |
| host/sidebar-selection | **elevated white pill** (border + subtle shadow) on gray sidebar | (measured)(inferred) | web pattern — the anti-native tell; macOS uses inset accent-tinted fill |
| host/card | white, ~12px radius, colored status pill top-right + large numeric value + gray description + arrow | (estimated)(inferred) | generic dashboard card anatomy |
| host/body-density | ~14–16px web body, ~18–20px bold card titles, ~40px sidebar rows | (estimated)(inferred) | web density — NOT macOS 13pt/24pt |

## Layout skeletons

**cover.png — marketing OG composite (1200×630):**
- Top-center: icon + "Heat Scope" wordmark lockup, y≈30–90.
- Center: a mac-style window mockup (traffic-light cluster top-left, no toolbar, no menu bar) filling most of the frame, tilted flat/front, wrapping the host dashboard.
  - Host dashboard: left sidebar (logo "AlphaVault" + 5 line-icon nav items: Dashboard [selected white pill], Roles & Permissions, Audit Log, Alerts & Requests, Access Control); top bar (centered "65.1% attention" pill, bell + avatar trailing); 4-up stat-card row (Users 495 / High Impact Change 05 / Access Requests 19 / System Health 95%), each with tinted status pill; bottom row = multi-series smooth line chart ("Permissions Changes Over Time", 3-series legend) + donut/ring chart ("Users Overview", center total).
  - Heatmap overlay + numbered badges 1–10 blended across the whole dashboard.
- Bottom-center: black capsule CTA "Download HeatScope" with Apple logo, y≈525–610.
- Faint ghosted second UI bleeds in at the very bottom edge.

No macOS app surface (settings / toolbar / real sidebar) is present to skeleton.

## Signature moves
- **[GOLDEN-NUGGET] Thermal gradient as a total brand system.** The same heat ramp appears three times at three scales: the product's attention heatmap (full spectrum), the icon's bolt-cut fill (warm side: green→amber), and — inverted to fresh mint — the marketing backdrop. Icon, output, and ground all "speak heat." This is the one genuinely owned decision.
- **Numbered attention-rank badges (1→10)** layered on the heatmap turn a passive color-blob into an explicit, sequenced eye-path — the product literally renders the F/Z-pattern reading order as UI. Strong, on-brief for an "attention" tool.
- **One black pill against a mint field** — disciplined single-CTA marketing hierarchy; the only saturated filled control in the frame.

## Defects
- **Faked / decorative window chrome (native-tell failure)** → mac traffic lights sit on a browser-style content frame with no toolbar and no menu bar; the frame is a Figma "mac window" mockup asset, not a real macOS window → canon would show a genuine unified toolbar (52/40pt) or no faux frame at all. (Marketing-composite convention, but recorded as a non-native tell.)
- **Host selection grammar is web, not macOS** → the selected "Dashboard" row is an *elevated white pill with border/shadow*; macOS uses a flat inset-rounded **accent-tinted** fill (radius 8 on the row). Attributed to the borrowed template, not to HeatScope.
- **Legibility sacrifice by design** → the heatmap + badges obscure ~40% of the underlying content to illegibility. This is intentional product demonstration, not a layout defect — but it means the cover teaches nothing about HeatScope's own information design.
- Not a defect but a gap: **no HeatScope-authored app UI exists in the corpus** — everything "app-like" here is a stock demo host.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| cover composite (host dashboard, as a *web* design) | ~11/14 (est., several N/A) | #1 grid unverifiable under overlay; #10 sidebar-icon contrast borderline (~3:1); #14 no visible focus state (static) — evaluated as web, does not feed macOS canon |
| cover composite (10-pt native-tells audit) | **~1/10** | #1 lineage web not native; #3 selection = elevated white pill (no accent fill); #5 web density (14–16px/40px rows); #6 no system-accent binding; #9 no toolbar; #10 faked/decorative frame, no menu bar |

**Corpus note:** First app profile in the corpus (previously kit-only). It is non-native + marketing-only, so it contributes **zero macOS canon** and cannot open a macOS UI style cluster. Its usable value is a brand/marketing-composite datapoint and a clean example of the web-vs-native selection tell.

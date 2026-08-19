# Runey — profile

- **Source:** macapp.supply (cover composite only; no standalone shots) · **Surfaces digested:** dashboard/overview (light) · **Last updated:** 2026-07-19
- **One-sentence identity:** Revolut's rounded-sans consumer warmth applied to a freelancer business-ops dashboard — Cleo/Copilot Money's playful money-tool voice, not the cold Inter-grotesque fintech default.
- **Cluster:** unassigned (candidate: "playful-fintech-dashboard" — non-native/web cluster, does not feed macOS canon)
- **Lineage:** web-electron (high) — a web SaaS dashboard shown in a frameless marketing render; non-native evidence, excluded from macOS canon. See Native audit.
- **Era (chrome):** custom (web) — no macOS chrome, no traffic lights, no OS material; decorative liquid-glass imagery is brand art, not the platform material.

## Provenance note
The cover is a marketing composite: the app **window** (light dashboard, perspective-tilted) is design evidence; the **backdrop** (black ground + green iridescent liquid-glass waves + white rounded headline "Run your business in one place") is brand evidence. Because the window is Y-axis-tilted in 3-D, every pixel value below is `(estimated)` with wide ranges — no clean orthographic measurement is possible. A separate 2400×1260 "Revone" macOS image surfaced during a bad webp decode; it is a *different product* (different name, blue theme, real traffic lights) and was discarded as a decode artifact — not Runey.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | #F7FAF3 warm green-tinted off-white, subtle gradient toward the chart (estimated)(inferred) | | content area, light mode |
| bg/card | #FFFFFF, soft ambient shadow + hairline border (estimated)(confirmed) | | KPI + content cards |
| bg/rail | #0B0B0C near-black (estimated)(inferred) | | fixed icon nav rail |
| bg/hero | #0A0A0A drenched black + green liquid-glass fluid render (estimated)(inferred) | | cashflow Von-Restorff card |
| text/primary | ~#161616 near-black (estimated)(confirmed) | | greeting, values |
| text/secondary | ~#6E7379 gray (estimated)(confirmed) | | labels, captions, timestamps |
| accent/brand | lime→green ~#8CCB4A line / area fill (estimated)(inferred) | | app's own brand accent, NOT system accent |
| badge/positive | text ~#3E9B2D on ~#E7F6DD pale-green pill (estimated)(confirmed) | | "↗ 24%" momentum pills |
| badge/negative | text ~#E1503A on ~#FBE7E2 pale-coral pill (estimated)(confirmed) | | "↘ 61%" pills |
| viz/expense | ~#D69A5E orange-tan columns (estimated)(inferred) | | coin-stack chart, expense series |
| type/display | ~34–40px, bold/heavy, rounded-geometric sans (estimated)(confirmed) | | KPI + section values (€110.8k, €23.2k) |
| type/greeting | ~28–32px bold (estimated)(inferred) | | "Good morning, Solt" |
| type/body | ~15–16px, rounded sans, regular/medium (estimated)(confirmed) | | labels, activity lines — web density, not 13pt |
| type/caption | ~13px (estimated)(confirmed) | | timestamps, badges, legend |
| type/family | rounded-geometric sans (double-story a/g, rounded terminals) — brand webfont, NOT SF Pro (estimated)(confirmed) | | Poppins/Onest/Gordita register |
| radius/card | ~18–20px (estimated)(confirmed) | | soft, generous web cards |
| radius/hero | ~22px (estimated)(inferred) | | |
| radius/pill | capsule (estimated)(confirmed) | | badges, buttons, "Last 30 Days" picker |
| chrome/rail | ~56–64px wide, full-height, black, monochrome line icons, no labels (estimated)(confirmed) | | web icon rail — not a macOS source list |

## Layout skeletons

**Dashboard / overview (light):** Three zones.
- **Icon nav rail** (far left, ~56–64px, black, full-height): R logo (white oval) → `+` new (capsule button) → grid/dashboard (selected, rounded-square fill) → people/clients → folder/projects → checklist/tasks → document/invoices → wallet/expenses → pencil/proposals → import tray → box/products → bar-chart/reports. Monochrome white line glyphs, icon-only.
- **Content area** (fluid): header row = greeting block (title + subtitle, left) opposite a trailing cluster (search glyph, bell w/ "3" badge, avatar) and a capsule "Last 30 Days" period picker. Below: **KPI row** = 4 equal cards (Revenue / Open / Paid / Overdue), each label + optional trailing %-badge, large value, sub-caption, faint sparkline. Below that a two-column split: **left ~65%** = "Balance €23.2k" with a red −61% pill, a legend row (Paid/Invoiced/Quoted/Expenses colored dots + counts), and the coin-stack area chart; **right ~30%** = black cashflow hero card (name / €82.6k / "Total cashflow" / New Invoice [white filled] + New Expense [green ghost]) stacked above an Activities feed (avatar + bold-lede line + timestamp, newest first).

## Signature moves
- **[GOLDEN-NUGGET] The coin-stack revenue chart.** Every x-axis point is a vertical stack of rendered 3-D coin tokens, topped with the client/tool's brand logo (Notion, Adobe, Framer…) and a "+N" counter, planted on a green area chart. It turns an abstract balance line into a tactile coin-pusher metaphor — a gamified, physical money visualization that is the app's entire personality in one component. Green stacks = paid, orange-tan = expenses.
- **[GOLDEN-NUGGET] The single drenched-black liquid-glass hero card** among all-white cards: the lone dark element (Von Restorff) carries the primary CTAs and echoes the marketing backdrop's black+green fluid motif into the product itself — brand continuity from store art to running UI.
- **Rounded-geometric brand sans everywhere.** A friendly rounded webfont (not the reflexive cold Inter/grotesque of fintech) makes a money/invoicing tool feel approachable — warmth carried by the typeface, deliberately anti-intimidating.

## Defects
- **Contrast Dilution (mild)** → hairline card borders and light-gray sparkline strokes read <3:1; small pale-tint badge text (green-on-pale-green, ~13px) is borderline <4.5:1 → canon would deepen the hairline/badge text or enlarge the badge.
- **Recognition-over-recall risk (UX)** → the nav rail is icon-only with no visible labels; 11 destinations rely on memorized glyph meaning → weak information scent (Pirolli/Card); labels-on-hover or a wider labelled rail would fix it.
- **Non-native as a "Mac app"** → zero macOS chrome/conventions; it is a web dashboard in a frameless frame. A finding for a macapp.supply "Business" listing, not a design flaw of the web product.

## Native audit (10-pt, macOS) — 1/10
Fails as native by design (web/Electron): #1 lineage web not AppKit · #2 decorative glass sits in content (brand art) · #3 selection is a web rounded-square, not inset-accent grammar · #5 web density (~16px body, not 13pt) · #6 accent is the app's own green, not the system accent · #9 no macOS toolbar (web rail) · #10 no traffic lights / frameless render. Only the action-singularity principle (#7, one primary per region) transfers. Correctly excluded from macOS canon.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| dashboard (light) | 12/14 | #9 pale-badge text contrast borderline <4.5:1; #10 hairline borders + sparkline strokes <3:1 |

# SessionWatcher — profile

- **Source:** macapp.supply (`sources/sessionwatcher/`) · **Surfaces digested:** cover.png (web marketing hero — *no app UI*) · **Last updated:** 2026-07-19
- **One-sentence identity:** A menu-bar usage-meter for AI coding tools whose only public design evidence is an Apple.com-cosplay dark-hero landing page — Raycast/Vercel marketing dressed in Apple Store trade dress; the actual app is unseen.
- **Cluster:** unassigned — and *not eligible* for a macOS UI cluster (no native surface shown; the digested surface is a website).
- **Lineage:** **unknown (low)** for the app itself — no app window appears in any source. The digested surface (the cover) is **web** marketing, contrast evidence only, excluded from macOS canon. (The product is described as a native macOS menu-bar extra, but no screenshot corroborates its lineage.)
- **Era (chrome):** unknown for the app. Cover is a custom dark-web aesthetic. The app *icon* (not formally digested — Workflow B) reads **Big Sur-era** (squircle tile, brushed-aluminium extruded bars, glossy inner shadow) — legacy layered-material, not Liquid Glass.

> **Provenance flag:** This profile records **brand/web evidence**, not native craft. Nothing here may feed macOS TASTE canon, native clusters, or pattern files. It is logged so the synthesis pass knows this app was seen and yielded no native-UI signal. If the menu-bar dropdown / panel is later supplied, re-digest under Workflow A and supersede.

## Tokens

All from the cover (a 2400×1260 web asset; scale-to-design unknown, so type sizes are asset-px ranges, not pt). Colours are clean pixel reads; type is estimated.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | `#0A0A0A` near-black, subtle cool lift to ~`#14181F` toward centre + faint magenta/green radial glows behind the icon row | (measured)(inferred) | "Drenched dark" — the surface *is* the colour. Not a neutral document ground. |
| text/primary | `#FAF8F8` near-white | (measured)(inferred) | Headline + wordmark + CTA text. |
| text/secondary | `#A6A6A6` mid-gray | (measured)(inferred) | Subhead + nav links; ~8:1 on the black — clean de-emphasis. |
| accent/primary | `#0071E3` blue | (measured)(inferred) | **Signature:** this is **apple.com's store-blue**, NOT macOS systemBlue (`#0088FF` light / `#0091FF` dark per kit). A deliberate Apple-marketing borrow. |
| accent/on-accent | `#FFFFFF` | (measured)(inferred) | CTA label; white-on-`#0071E3` ≈ 5.0:1, clears 4.5:1 by a hair. |
| radius/cta | capsule (pill) on both CTAs | (measured)(inferred) | Nav "Get from $2.99" and hero "Get SessionWatcher" both fully-rounded. |
| type/display | ~140–160px asset-px, heavy grotesque (SF Pro Display Bold-class), tracking tight (~−0.02em), leading ~1.05, centred | (estimated)(inferred) | "Never Lose a Coding Session to Rate Limits" — 2 lines. Family not definitively identifiable; reads system-grotesque, not a distinctive display face. |
| type/subhead | ~44–52px asset-px, regular, leading ~1.4, centred | (estimated)(inferred) | |
| type/nav | ~30–36px asset-px wordmark bold; ~22–26px gray links | (estimated)(inferred) | "v6.0" set as a small superscript badge in `#656666`. |
| chrome/nav | full-width top bar: logo-tile + wordmark leading, Features · Pricing + blue CTA pill trailing | (measured)(inferred) | Standard SaaS marquee, not app chrome. |

## Layout skeletons

**cover.png — web marketing hero (single centred column, ~drenched-dark):**
- Top nav bar: leading = app-icon tile (~44px) + "SessionWatcher" wordmark + "v6.0" superscript badge; trailing = "Features", "Pricing" text links then a capsule CTA "Get from $2.99" (`#0071E3`).
- Trust row (centred): 5 provider glyphs at even gaps — Claude (orange sunburst), Codex (OpenAI), Copilot, Cursor (black cube tile), Gemini CLI (spectrum spark) — each ~72px with a gray caption 4–8px beneath. Reads as "works with your tools" social proof.
- Hero headline (centred, 2 lines): oversized heavy grotesk, `#FAF8F8`, loss-framed copy.
- Subhead (centred, 2 lines): `#A6A6A6`, ≤65ch.
- Primary CTA (centred): large capsule `#0071E3` pill with Apple logo + "Get SessionWatcher — from $2.99".
- No app window, no device frame, no product screenshot anywhere. The composite is 100% backdrop + brand typography.

## Signature moves
- **[GOLDEN-NUGGET] Apple Store cosplay.** The CTA blue is `#0071E3` — the exact apple.com buy-button blue — paired with an  Apple logo on the button. The site deliberately borrows Apple's own retail trade dress to read as "official/trusted Mac software" (Jakob's Law + authority transfer). It pointedly is *not* macOS systemBlue, so this is a marketing choice, not a platform default.
- **Provider-logo trust row as the hero's second act.** Five recognised AI-tool glyphs sit above the headline — genuine social proof ("it tracks the tools you already run") doing work before a single word of copy is read.

## Defects
- **Focal Collision (soft)** → two saturated `#0071E3` CTA pills share one viewport (nav "Get from $2.99" + hero "Get SessionWatcher"). Same action, repeated accent → dilutes Von Restorff "one different thing." Canon: keep the nav CTA quiet (ghost/text) so the hero pill is the sole saturated focus, or drop the nav price pill to secondary styling.
- **Template-default aesthetic** → dark-near-black ground + one electric-blue accent + oversized bold grotesk headline is the *current-model unprompted reflex* for dev-tool landing pages (design-craft flags "Neo-grotesque product, dark neutral + one electric accent" as a warned default). Competent and on-trend, but carries no committed, subject-mined direction — a neighbouring dev-utility's site would fit this exact treatment unchanged (fails the swap test).
- **No product evidence** → the design-corpus takeaway is a gap, not a lesson: the cover teaches nothing about the app's native craft, density, or menu-bar-extra layout. Biggest missing surface.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| cover (web hero) | 11/14 | #8 action singularity — dual blue CTAs in one viewport (soft Focal Collision). #12/#13/#14 N/A (no inputs/forms/observable focus). Everything structural (grid, proximity, scale, de-emphasis, contrast) passes for a competent SaaS hero. |
| cover (native-tells audit) | ~0–1/10 | **Not a native surface** — the 10-point audit is the wrong instrument for a website. No toolbar/sidebar/selection/real-chrome to score; recorded as contrast evidence, not a native failure. |

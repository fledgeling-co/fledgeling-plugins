# Dia — profile

- **Source:** macapp.supply (meta.json + 2 image files) · **Surfaces digested:** none (no app UI supplied) · **Last updated:** 2026-07-19
- **One-sentence identity:** A browser (The Browser Company) whose *marketing* commits to an editorial-cinematic register — a characterful serif wordmark on near-black with full-bleed emotional photography — but whose **in-window UI is not evidenced by any supplied file**, so no design read of the product surface is possible yet.
- **Cluster:** unassigned — no UI evidence to cluster on
- **Lineage:** unknown (low) — a browser renders web content in its viewport by definition, but the *app chrome* (tab strip, sidebar, toolbar, address bar) appears in none of the inputs; native-vs-Electron cannot be judged. Non-native evidence never feeds macOS canon; here there is no UI evidence of any kind.
- **Era (chrome):** unknown for UI. The **icon** reads current Liquid-Glass / Icon-Composer era (translucent gradient lozenge on a soft light ground) — a brand-timing signal, not a chrome-era measurement.

> **Digest honesty note.** This task ran Workflow A (digest a UI screenshot). The two files provided are (1) `cover.png` — a **1200×630 Open Graph social-share card** (marketing composite: black ground, logo, wordmark, tagline, portrait photograph), which contains **zero app UI**, and (2) `icon.png` — the **app icon**, which is Workflow B material and out of scope for a UI digest. The cover backdrop and typography are **brand evidence**; there is no **UI evidence** to conflate them with. The 14-point rubric and the 10-point native-tells audit are **not applicable** to either file — neither is a UI surface. Everything below is recorded as brand/icon evidence with explicit marks, and none of it may feed macOS UI canon or style clusters.

## Tokens

All tokens below are **brand or icon** tokens, not UI-chrome tokens. Marked accordingly.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg-black | `#040509` (measured)(inferred) | | cover ground; near-pure black, faintly cool (R4 G5 B9). Drenched-dark brand surface, not a window background |
| brand/logo-white | `#FFFFFF` (measured)(inferred) | | logo mark + wordmark are pure white knockout on black |
| brand/tagline-gray | ~`#8A8B8E`–`#9A9B9E` (estimated)(inferred) | | secondary light-gray sans tagline; de-emphasised vs the white wordmark |
| brand/wordmark-face | Custom high-contrast **serif**, bracketed old-style/transitional serifs, double-story `a`, round `i`-dot, wide round `D` (estimated)(inferred) | | characterful, bookish/editorial display face — a committed brand typeface, NOT a system font. The app's entire warmth lives here |
| brand/tagline-face | Humanist **grotesque sans**, Regular weight, single-story `a`, curly apostrophe (estimated)(inferred) | | calm neo-grotesque; deliberate contrast-axis pairing (serif display + sans text) |
| brand/logo-glyph | Solid-white **dome** silhouette: rounded top, base scooped concave in the centre (estimated)(confirmed) | | the same silhouette as the icon's coloured dome — logo and icon share one mark. Reads as speech-bubble-minus-tail / rising dome |
| icon/bg | Pale warm off-white → faint lavender, soft top-light + base ambient occlusion (estimated)(inferred) | | ~`#F0EFF2`; gives the icon a domed glassy-card depth |
| icon/motif | Translucent **daybreak spectrum** dome, vertical gradient top→base (estimated)(confirmed) | | blue → sky-blue → pale cream band → yellow → orange → coral/red at base; a sunrise over a curved horizon |
| icon/grad-stops | ~`#4D88DF` blue · `#A7C7E4` sky · `#E1E3C7` cream · `#F4D765` yellow · `#F59440` orange · ~`#E86B6B` coral (measured@mid / estimated@ends)(inferred) | | sampled down the icon centre axis; base coral is inferred from render, not cleanly sampled |
| icon/finish | Soft blurred outer edge, faint top specular sheen — a glass lozenge (estimated)(inferred) | | Liquid-Glass / Icon-Composer aesthetic |

## Layout skeletons

**cover.png — marketing composite (NOT a UI surface).** 1200×630 OG card. Vertical centre-stacked brand lockup in the top ~40%: [dome logo mark] + [serif "Dia" wordmark] on one baseline, centred horizontally; tagline "A browser you won't dread opening." two lines of centred grey sans directly beneath. Bottom ~55% is a full-bleed colour **portrait photograph** (a woman mid-scream, warm skin, green shirt) fading edge-to-black — the "dread" emotional device. No window chrome, no traffic lights, no toolbar/sidebar/content region. **No UI layout skeleton is derivable.**

**icon.png — app icon (Workflow B scope).** Squircle · soft light ground · centred translucent daybreak-gradient dome occupying ~65% of the canvas · concentric soft shadow. Not a UI layout.

## Signature moves

All brand/icon signatures — recorded for brand reference, **not** promotable to macOS UI canon:

- **[GOLDEN-NUGGET] The daybreak-spectrum dome.** "Dia" = *day*; the icon is a sunrise (blue dawn sky → warm horizon) rendered as a translucent glass lozenge. Concept, colour, and name resolve into one mark — and it pays off the tagline's promise of a fresh, dread-free start.
- **One mark, two renders.** The black-and-white logo glyph on the cover is the exact silhouette of the icon's coloured dome. Identity is carried by a single reusable shape — economical and confident.
- **Serif-display-over-grotesque-tagline.** A characterful bookish serif for the name paired on a contrast axis with a plain humanist sans for the sentence — the pairing is where the brand's editorial warmth comes from, and it deliberately reads *unlike* a typical dev-tool.
- **Dread-relief emotional framing.** The photograph sells the *problem* (a scream) so the product can be the *relief* — brand storytelling, not a product screenshot.

## Defects

- None assessable. No UI surface was supplied, so no UI anti-pattern (Magic Number Spacing, Focal Collision, Contrast Dilution, etc.) can be confirmed or cleared. The cover's near-pure-black ground (`#040509`) would be a Contrast-Dilution concern only if it were a *content* surface; as a marketing ground it is a legitimate drenched-dark brand choice.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.png (marketing composite) | n/a | Not a UI surface — 14-pt rubric + 10-pt native audit not applicable |
| icon.png (app icon) | n/a (UI rubric) | Belongs to the 12-pt icon rubric (Workflow B), not the UI rubric |

## What the corpus still needs from Dia

To digest Dia as a macOS UI, real in-window screenshots are required: the browser window (tab strip / sidebar, toolbar + address bar), the new-tab surface, and any AI/chat panel. Only those can settle framework lineage (native chrome vs Electron/Chromium wrapper), run the native-tells audit, and yield UI tokens. Until then Dia contributes **brand + icon evidence only**.

# Pixelcasso — profile

- **Source:** macapp.supply (meta.json) · **Surfaces digested:** cover.png (marketing composite, dark) · **Last updated:** 2026-07-19
- **One-sentence identity:** A Paint.NET-for-Mac raster editor that dresses itself in fine-art editorial clothing — classical serif on drenched navy, a Picasso-pun icon — positioning a utilitarian pixel tool as a gallery object. Brand register rhymes with a museum exhibition poster more than with typical Mac-utility marketing.
- **Cluster:** unassigned (brand/marketing evidence only — no UI surface to place in a macOS style cluster)
- **Lineage:** unknown (low) — the cover contains **no captured app UI**; the "window" on the right is a stylized brand illustration, not a screenshot. Marketing copy ("Native image editor", "Made for macOS") asserts native, but a marketing claim is not design evidence. Nothing here may feed macOS canon.
- **Era (chrome):** unknown — the illustrated frame gestures at current-era native (coloured traffic lights, dark chrome, exaggerated ~28–32px window radius) but is drawn, not real; radius and materials are illustration choices, not measurable shipped chrome.

## What this input is (read before trusting any token below)

The only supplied images are `cover.png` (1200×630 — a standard OG/social-share ratio, i.e. a **marketing card**) and `icon.png` (a separate Workflow-B subject, not digested here). The cover is a brand composite: dark navy backdrop with two faint tonal circles, a wordmark, a tracked small-cap eyebrow, a serif display headline, a serif subhead, a footer line, and — on the right — an **illustrated app-window mockup**. The mockup's tells that it is illustration, not UI:
- The **"3 layers" pill and its text are set in the brand serif**, not SF Pro; a real macOS layer count would be sans and would live in a panel, not a floating capsule.
- The **marquee** is a perfectly geometric static dashed circle (decorative), the canvas is placeholder two-tone artwork, and the titlebar carries no toolbar, title, or controls.

So: **brand evidence is real and analysable; UI evidence is essentially absent.** Tokens below are brand-surface tokens, all `(estimated)(inferred)`, and must not be conflated with app chrome.

## Tokens (brand/marketing surface — NOT macOS UI canon)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/backdrop | `#132238` navy, subtle vignette to ~`#0F1B2E` | (estimated)(inferred) | drenched dark ground, near-monochrome |
| bg/tonal-shapes | `#253851` (top-right), `#262E3F` (bottom-left) | (estimated)(inferred) | two faint low-contrast circles = quiet geometric depth |
| brand/window-chrome | `#0A1626` near-black navy | (estimated)(inferred) | illustrated frame sits *darker* than the backdrop |
| type/display | classical high-contrast serif, ~72px, tight leading, `#F8FBFF` | (estimated)(inferred) | "Switch platforms. Keep your instincts." — old-style/transitional serif (Georgia/Source-Serif class) |
| type/eyebrow | tracked uppercase sans small-cap, ~13px, +0.12em, `#99C4EB` | (estimated)(inferred) | the one chromatic type moment — light sky-slate |
| type/subhead | serif, ~19px, loose leading, muted | (estimated)(inferred) | "A familiar, powerful workflow made native for Mac…" |
| type/footer | ~13px muted, `#525B6A` | (estimated)(inferred) | "pixelcasso.app · Made for macOS" — de-emphasised |
| type/wordmark | serif "Pixelcasso" + serif "P" in cream badge | (estimated)(inferred) | badge `#F8FBFF` rounded square, ~12px radius |
| accent/type | `#99C4EB` sky-slate | (estimated)(inferred) | brand accent, appears only on the eyebrow |
| canvas/placeholder | diagonal split `#BCD5DB` cream-blue → `#142B43` steel | (estimated)(inferred) | illustrative artwork inside the mockup, not UI |

## Layout skeletons

**cover.png (marketing composite, dark):** Two-column social card. Left column (left axis ~64px, shared by wordmark / eyebrow / headline / subhead / footer) carries the type stack top-to-bottom: wordmark → (gap) → eyebrow → serif display headline (2 lines) → subhead → footer pinned near the bottom edge. Right column holds the illustrated window mockup, floated with a soft drop shadow, bleeding toward the right edge; window contains a rounded canvas + decorative marquee + "3 layers" pill (bottom-right of canvas). Backdrop carries two faint tonal circles for depth. **No real app regions (toolbar / sidebar / inspector / controls) are present to skeleton.**

## Signature moves

- **[GOLDEN-NUGGET] Fine-art register for a utility.** The entire brand system — classical serif display, drenched navy museum ground, the Picasso-portrait icon, "Keep your instincts" — reframes a Paint.NET clone as a gallery object. This is a *brand* signature, committed and systematic across cover + icon + copy; it is the app's whole personality in one decision. (It is not, however, evidence about the UI.)
- Serif carried all the way into the illustrated HUD ("3 layers" pill) — a consistent, if non-native, brand flourish.

## Defects

- **No app-UI evidence supplied** — this is a limitation of the input (marketing-only cover), not a defect of the product. Do not infer app defects from an illustration.
- (Illustration-only, not a shipped defect) The mockup's serif HUD text and exaggerated window radius are non-native; if these motifs ever migrated into the real app they would read as web/brand-drift, but there is no evidence they do.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.png (marketing composite) | 8/14 applicable-as-composition · native-audit 2/10 | Checks 8, 11–14 **N/A** (no interactive controls, inputs, or focus states — static marketing image); native audit largely N/A (no real native surface to audit; only drawn traffic-lights + dark chrome gesture at native). Composition itself is disciplined: shared left axis (#2), tight-eyebrow/spaced-subhead proximity (#3), ~4-size serif scale (#4), strong white-on-navy contrast (#9). |

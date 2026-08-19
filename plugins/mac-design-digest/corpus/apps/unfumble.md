# Unfumble — profile

- **Source:** macapp.supply (`sources/unfumble/`) · **Surfaces digested:** none (no app UI supplied — marketing cover + app icon only) · **Last updated:** 2026-07-19
- **One-sentence identity:** A menu-bar language-switcher utility whose *brand* reads friendly-and-technical — a dark slate neo-grotesque surface carrying one electric-blue accent and a rounded, almost toy-friendly wordmark; its actual app UI is unseen.
- **Cluster:** unassigned (no UI evidence to place it)
- **Lineage:** unknown (low) — a marketing composite and an icon cannot classify framework. No body text, no controls, no chrome, no menu-bar rendering was supplied; density (the strongest discriminator) is unmeasurable.
- **Era (chrome):** unknown for the app UI (unobserved). The **app icon** reads **Big Sur-convention** (flat gradient squircle + centred white glyph, pre-masked with a baked drop shadow) — i.e. *not* a Liquid Glass / Icon Composer layered icon.

> **Digest honesty note.** This profile is built entirely from brand + icon evidence. macapp.supply supplied only `cover.png` (a 1200×630 social/OG marketing card) and `icon.png` (the 512px app icon). The cover contains **no app window** — just a branded backdrop, the icon, a wordmark, and a tagline. No 14-point rubric or 10-point native-tells audit was run, because there is no app surface to audit. Tokens below are brand/icon values, useful for identity but **not** feeders for macOS UI canon. To advance this app past Novice, a real UI screenshot is needed — almost certainly a **menu-bar-extra dropdown** and/or a **Settings window** (see Knowledge gaps).

## Tokens

Brand (from `cover.png`, 1200×630 marketing composite) and icon (from `icon.png`, 512px) — **not** app-UI tokens.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg-dark | #12202C → #172430 (measured)(inferred) | | cover backdrop; very dark desaturated navy-slate (~hue 205°), near-flat vertical falloff |
| brand/keycap-texture | #1B2834 (measured)(inferred) | | offset rows of rounded-rect "keycaps" tiling the backdrop; only ~+9 L over bg — deliberately low-contrast texture, not noise. Subject-mining: the product switches *keyboard* language |
| brand/accent-periwinkle | #92AFFC (measured)(inferred) | | tagline text colour; soft cornflower/periwinkle blue, positively tracked |
| brand/wordmark | white, rounded geometric sans, lowercase w/ cap U, ~557px wide on cover (estimated)(inferred) | | Quicksand/Comfortaa/Poppins-round family or custom — consistent rounded terminals, single-story a; friendly register. Face identity estimated |
| brand/tagline-type | letterspaced small caps-ish sans, ~+tracking (estimated)(inferred) | | "Automatic keyboard language switcher"; even letter widths read near-mono |
| icon/bg-gradient | #0877FE (azure) → #5559F5 (indigo) diagonal TL→BR (measured)(inferred) | | committed brand blue→indigo; brighter/more saturated than macOS system blue (#0088FF light) |
| icon/glyph | white globe (line-art meridians+parallels) + 4-point sparkle, flat (measured)(inferred) | | globe ≈ SF Symbols "globe"; sparkle upper-right with a "liquid" drip fusing into the globe |
| icon/silhouette | continuous squircle, body 430×429 in 512 canvas (~8% margin), corner radius ~90–100px @512 (measured; radius estimated)(inferred) | | correct macOS Big-Sur superellipse proportion & margin — icon geometry is native-faithful |
| icon/depth-model | flat single layer; baked bottom drop shadow; no varied foreground opacity (measured)(inferred) | | pre-masked + baked shadow = Big Sur-era authoring, not Icon Composer layered glass |

## Layout skeletons

**None.** No app UI surface was supplied. The cover is a centred brand lockup on a textured backdrop: [icon ~230px] · [wordmark] stacked over [tagline], group optically centred in the 1200×630 frame, keycap texture bleeding edge-to-edge behind. That is a marketing composition, not an application layout — recorded for completeness, excluded from pattern evidence.

## Signature moves

- **[GOLDEN-NUGGET] The sparkle-with-a-liquid-drip fused into the globe.** The globe alone would be a stock "language/international" glyph; the four-point sparkle (the universal "automatic / magic" motif) trailing a liquid droplet down onto the globe is the one custom flourish that gives the mark character and encodes the product promise ("automatic" switching) in a single device. Everything else in the icon is convention.
- **Keyboard-keycap texture as subject-mining, held at whisper contrast (~+9 L).** The backdrop literally depicts the object the app operates on (a keyboard), but demoted to texture rather than illustration — a disciplined "designed, not decorated" signal.
- **Rounded-friendly wordmark over a dark technical surface.** A deliberate tension: the neo-grotesque dark-slate + electric-accent surface says "developer tool," the plush rounded lettering says "approachable." The pairing is the brand's whole personality.

## Defects

- **Pre-masked, baked-shadow app icon (Big Sur-era in the Liquid Glass era)** → the icon PNG ships with the corner mask and a drop shadow already rendered in, and is a single flat layer. Current macOS (26/27) app-icon guidance is to supply *square, unmasked, layered* art in Icon Composer and let the system apply corners, specular highlights, refraction, and shadow. What canon would do: author Default/Dark/Clear/Tinted layers, vary foreground opacity for depth, and drop the baked shadow. This is an **era mismatch / one-release-behind** finding, not a construction error — the icon is competently made *for its era*.
- No app-UI defects can be recorded — no app UI was observed.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| (none — no app UI surface supplied) | n/a | 14-point rubric and 10-point native-tells audit require an app surface; cover is marketing, icon is brand. Not scored. |

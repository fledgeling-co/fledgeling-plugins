# Icon: Tokens 4 Breakfast

- **Era:** flat-transition (flat-graphic vocabulary on a modern Big-Sur/Tahoe squircle — a hybrid; decisively **not** Liquid Glass) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 1024×1024, clean vector-origin render — flat fills and crisp token edges, not a lossy web thumbnail) · **App:** menu-bar AI-token / AI-spend tracker (Productivity)
- **Subject read:** a coffee cup + saucer (breakfast) with a silver poker-chip / coin — the "token" — sitting in the coffee. Double pun: *tokens for breakfast* literally, and *token = currency*, which is exactly what the app tracks (AI spend). Genuine subject-mining, not a generic glyph-on-gradient.

| Dimension | Reading |
|---|---|
| Background | Flat warm charcoal `#2F2929` (measured); no sky-ramp. Slight edge-darkening at the mask rim (`#211B1B`) and a soft contact-shadow band under the saucer (`#231C1C`) — the only background modulation. Corners fully transparent (pre-masked squircle). |
| Glyph | Object — coffee cup + saucer + handle, one flat orange `#F8900E`→`#FB9104` (measured). Front-facing 3/4 view (we see into the cup). Optically centred horizontally, weighted **low** (saucer near the bottom safe-zone, more headroom above). |
| Overlay device | None in the diagonal-tool sense; the differentiator is the **coin/chip "token"** — a short silver cylinder (lit top `#DFDFE0`, mid edge `#B2B1B0`, shadowed side `#3E3838`) resting in the dark coffee well. |
| Light model | **Mixed fidelity.** Cup/saucer/handle/coffee are flat, unlit fills (no highlight, no core shadow). The token is dimensionally rendered (top-lit cylinder) and the saucer casts a soft top-down contact shadow — a rendered coin dropped into a flat-graphic cup. No specular, no glass. |
| Layer stack | charcoal squircle field → baked contact shadow → orange saucer ellipse → orange cup body + handle → dark coffee well (`#2B2424`, reads as negative space held by the orange rim) → silver token disc (front) |
| Palette economy | One accent hue (orange) carries cup+saucer+handle; neutrals = silver token + charcoal field. ≤2 hue families, accent reserved for the focal object. Exemplary economy. |

## Rubric (12-point)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Mask discipline | PASS (soft) | Correct centred Apple superellipse (760px on 1024, ~132px margins), hard clean edges, no external shadow halo. **But pre-masked on transparent** with a ~132px margin — fights the "provide full-bleed square, let the system mask" contract; would double-mask / float inside a Tahoe or Icon Composer pipeline. Reads correct only when used as a static Dock PNG. |
| 2 | Grid adherence | PASS (soft) | Mask perfectly centred; cup+saucer optically centred on the x-axis but **bottom-weighted** — saucer sits low, headroom above. |
| 3 | Silhouette | PASS | Filled solid black it is instantly "coffee cup on a saucer." |
| 4 | 16px squint | PASS (soft) | Orange-on-charcoal cup survives menu-bar size; the token (~170px/1024 ≈ 2.7px @16) smears away — **the subject-differentiating detail is the first thing lost**, leaving only "a coffee cup," not "a token." |
| 5 | Single light model | **FAIL** | Flat unlit cup/saucer/coffee vs a dimensionally-shaded coin + a soft contact shadow. Mixed shading fidelity — the token belongs to a more rendered icon than the one it sits in. |
| 6 | Palette economy | PASS | One orange hue + neutrals; accent on the focal object only. |
| 7 | Figure-ground | PASS | Orange vs charcoal well above 3:1; silhouette survives grayscale. Coffee well ≈ background tone, so the opening reads as negative space held by the orange rim (reads intentional). |
| 8 | Depth coherence | PASS (soft) | Z-order sensible; the only incoherence is shading language, already logged in #5 — not the ordering. |
| 9 | Era coherence | PASS (soft) | Dominant flat-graphic language is consistent across field/cup/saucer/coffee; the dimensional coin is the one out-of-register element. Hybrid but reads unified. |
| 10 | Variant robustness | soft / era-gated | Single fixed-appearance flat PNG — no light/dark/clear/tinted layer separation. Composition **depends on the dark charcoal field** for orange+silver to separate; fragile if macOS 26 auto-generates a tinted/mono variant. Era-gated (Liquid-Glass check), so not counted as a hard failure for a flat-transition icon, but flagged forward-looking. |
| 11 | Personality | PASS | The coffee-with-a-token pun; a coin/chip that doubles as the app's literal subject. Strong, nameable, subject-mined `[GOLDEN-NUGGET]`. |
| 12 | No-text | PASS | No words, UI, or photography. |

**Score: 11/12** — one hard failure (#5), non-negotiables #1–#4 all pass (softly on 1/2/4), so it clears Dock/Spotlight duty.

## Signature devices

- **Token-in-the-coffee pun** `[GOLDEN-NUGGET]` — a poker-chip / coin ("token") sitting in the coffee. Works on two axes at once: *tokens 4 breakfast* literally, and *token = currency* (the app tracks AI spend). The rare case where the icon's cleverest detail is also its exact subject.
- **Coin as a short cylinder** — top face + visible side wall gives the disc a 3D read so it registers as a chip/coin, not a marshmallow or pill. It is also the icon's only dimensional element (and the source of the #5 failure).
- **Single-accent flat graphic on a dark field** — one amber-orange does cup+saucer+handle; bold, high-contrast, Dock-legible. The dark ground doubles as menu-bar context (see cover: the app's menu-bar pill is the same charcoal).
- **Orange rim as negative-space fence** — the coffee well is nearly the background tone; the orange rim is what turns it into a readable ellipse.

## Failures

- **#5 mixed light model** — flat cup + a dimensionally-shaded coin + a soft contact shadow. Fix: either flatten the token to match the graphic (a two-tone disc, no cylinder side), or model the cup with the same soft top-down light the token and shadow already imply. The former keeps the flat charm; the latter pushes it toward Big Sur.
- **#4 (soft)** — the token, the whole point of the icon, is the first casualty at 16px. A larger or higher-contrast token (e.g. a warmer/whiter chip, or bumping its diameter) would keep the differentiator alive at menu-bar size.
- **#1 / #10 (soft)** — pre-masked flat PNG with no layer separation; not authored for the layered / tinted macOS-26 pipeline. A static-Dock icon, not a Liquid-Glass one.

## Palette (measured, 1024 render)

- Background field: `#2F2929` flat (warm charcoal, R slightly > G=B)
- Coffee well: `#2B2424`
- Glyph (cup/saucer/handle): `#F8900E` – `#FB9104` amber-orange (the accent)
- Token: top `#DFDFE0` · edge `#B2B1B0` · shadow side `#3E3838`
- Contact/edge shadow: `#231C1C` – `#211B1B`

Icon↔cover coherence: the cover reuses the exact brand orange (`~#F8900E` wordmark, "across major AI platforms" gradient text) and shows the icon inside a dark rounded badge plus a charcoal menu-bar pill — inverse grounds (cream cover, charcoal icon) tied by the shared orange. Palette is coherent brand-to-icon.

## Rhymes with

- Flat single-object glyph marks on dark squircle fields (flat-transition vocabulary quoted on a modern squircle).
- Bold single-accent menu-bar utility icons (dark ground = menu-bar context).
- The coin/chip-as-token device rhymes with finance / currency / casino iconography — a useful cross-reference if a "spend"-tracking cluster ever forms.
- *Hint only (needs ≥3 icons to promote):* an "amber-on-charcoal dev-fuel" family (coffee/terminal motifs) may be emerging — hold until corroborated.

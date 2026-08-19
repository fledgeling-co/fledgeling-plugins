# Bauhaus Clock — profile

- **Source:** macapp.supply (cover.png only; no UI shots supplied) · **Surfaces digested:** marketing composite (screensaver canvas, dual day/night) · **Last updated:** 2026-07-19
- **One-sentence identity:** A Braun/Rams wall-clock rendered as a Mac screensaver — Dieter Rams' instrument restraint crossed with a Super-LumiNova watch dial, where "light/dark mode" is literalised as daylight-vs-night legibility.
- **Cluster:** modernist-instrument (proposed; sole member so far)
- **Lineage:** native (low confidence) — it is a Mac `.saver` (ScreenSaverView) by category, but **zero AppKit evidence is visible**: no window, toolbar, sidebar, controls, or traffic lights. Nothing to classify from. Excluded from macOS UI canon.
- **Era (chrome):** custom-drawn canvas — no macOS-era tells (the artwork is a self-contained clock face, not system chrome)

> ⚠ **This is not a UI surface.** The only image is a marketing composite (pale backdrop + centered headline + a black display mockup showing the screensaver in day and night states). A screensaver has no window chrome, no controls, no native patterns — so the 10-point native-tells audit is almost entirely N/A, and most of the 14-point rubric is N/A too. This app contributes **aesthetic/brand evidence only**, never macOS-UI-pattern evidence. Its actual configuration UI (the screensaver options sheet in System Settings) is unseen — a knowledge gap.

## Tokens

Two token sets: the **screensaver artwork** (the design object) and the **marketing/brand layer** (backdrop + headline). Kept separate per the cover-composite rule.

### Screensaver artwork

| Token | Value | Provenance | Notes |
|---|---|---|---|
| face/bg-day | `#C4ECEC` pale mint-aqua (measured)(inferred) | | daylight ground |
| face/bg-night | `#01131 7`→`#000000` near-black teal, radial (measured)(inferred) | | night ground; center slightly lighter than corners |
| ink/numeral-day | dark slate-navy ~`#12242B` (estimated)(inferred) | | hour numerals, day |
| lume/numeral-night | bright cyan ~`#4FE0E0` (estimated)(inferred) | | hour numerals + hands + markers glow cyan (Super-LumiNova cue) |
| marker/day | cream-white lume-fill, rounded-rect bars (estimated)(inferred) | | 12 fat 5-min bars + 4 hairline minute ticks between each |
| type/numerals | geometric sans, ~Semibold, single size (estimated)(inferred) | | hour ring; hybrid Arabic + stroke-glyphs (see Signature) |
| type/minute-track | same family, ~4× smaller, tangentially rotated (estimated)(inferred) | | labels 05–60; low-contrast gray → strong de-emphasis |
| hands/style | baton hour+minute with central lume channel; thin counter-weighted seconds (measured)(inferred) | | classic ~10:10 marketing position |
| center/cap | small silver pinion (day) (estimated)(inferred) | | |

### Marketing / brand layer

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | `#E8F0F2` cool ice-gray (measured)(inferred) | | flat, no gradient |
| brand/headline-ink | `#262E30` charcoal (measured)(inferred) | | contrast vs backdrop ≈ 11:1 |
| brand/headline-type | geometric-humanist sans, reads as SF Pro Display / Helvetica Now, Semibold (estimated)(inferred) | | two lines, centered, tight leading; NOT Futura — the geometric conceit lives in the clock numerals, not the wordmark |
| brand/device-bezel | black slab display on a gray stand (measured)(inferred) | | generic monitor mockup; not a real macOS window |

## Layout skeletons

**Marketing composite (cover.png, 1200×630):** vertically centered stack — (1) two-line headline "Bauhaus Clock / macOS Screensaver" occupying the top ~30%; (2) a single black display mockup, split vertically into a day half (left, mint) and night half (right, black), each rendering the full clock; (3) a gray monitor stand anchoring the base. Symmetric, centered, generous margins.

**Screensaver canvas (the artwork within):** three concentric rings around a common center — outermost = tangentially-rotated minute-track labels (05–60); middle = tick ring (12 fat 5-min bars + fine minute ticks); inner = 12 hour glyphs; over the top, three centered hands. Polar symmetry, optically centered in the frame. No 8pt grid applies (radial geometry).

## Signature moves

- **[GOLDEN-NUGGET] Hybrid graphic numerals.** The hour ring mixes Arabic (12, 2–9) with pure stroke-glyphs: `I` for 1, `II` for 11, `IC` for 10. It abandons arithmetic correctness (10 ≠ IC in Roman) in favour of the *shape rhyme* — a Bauhaus/typographic conceit that is the entire identity of the piece in one decision. The clock is instantly legible anyway because position, not the glyph, carries the hour (Jakob's Law does the reading).
- **[GOLDEN-NUGGET] Day/night as literal legibility, not appearance inversion.** The two modes aren't a UI light/dark theme — they are the *same dial* rendered under two lighting conditions: daylight (cream markers, slate ink, mint ground) and night (cyan Super-LumiNova luminescence on black). This is horological realism repurposed as a screensaver's ambient shift.
- **Tangential outer minute track.** Labels 05–60 rotated to follow the ring — a direct Braun/Rams wall-clock citation, held as recessive micro-typography so it never competes with the hours.
- **Lume-channel baton hands + counter-weighted seconds needle.** Watch-grade hand detailing; the thin seconds hand extends past the pinion as a counterweight.

## Defects

- **None as a UI** — a screensaver canvas isn't answerable to the interaction rubric, and faulting it for lacking controls would be a category error. The minute-track micro-labels fall below WCAG text contrast, but that is *intentional de-emphasis of decorative metadata*, not a Contrast Dilution defect.
- Verdict: **competent and characterful** — the opposite of "competent but anonymous." The numeral conceit is the signature; execution (lume, hands, de-emphasis discipline) is clean.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| marketing composite / screensaver canvas | 6/6 applicable (8 checks N/A) | #1,5,6,8,11–14 N/A — no UI, controls, text blocks, or interactive elements; #9 minute-track micro-labels ~2:1 but intentional decorative de-emphasis |
| native-tells audit | N/A (all 10) | no macOS chrome/controls/glass in a screensaver canvas — not auditable as native UI |

# Icon: TextSniper

- **Era:** liquid-glass (frosted-slab + floating glass lens) · **Rubric:** 12/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, 542×542 web render (SHA-1 `c814b723`). Category: Productivity. App: on-screen OCR — "Copy text from anywhere, Scan QR codes, Text-to-Speech" (drag a selection rectangle, capture text as an image).
- **Resolution caveat:** only a 542px render was available, not the 1024 master. The lens specular sheen and the frosted base's translucency are soft at this scale — glass-layer treatment is `(estimated)`, not `(measured)`. No dark/clear/tinted variant renders were supplied. The transparent margin carries a faint baked outer shadow (alpha fringe a≈18) — likely a macapp.supply composite, not necessarily in the master.

| Dimension | Reading |
|---|---|
| Background | Frosted ice slab, near-white with a cool tint: top **#F5F7FF→#FFFFFF**, edges cool to pale cyan **#D8F1FF** (measured). Reads as a translucent glass squircle, not a flat fill |
| Glyph | **White #FFFFFF** — four serif capital-**T** marks, each rotated ~45° with its stem pointing inward; the four stems converge into a central **X crosshair**, the four serif crossbars sit as corner brackets. Optically centred as a symmetric reticle on the lens |
| Overlay device | **Frame (viewfinder reticle)** — the reticle *is* the glyph; it doubles as a selection/crop marquee (corner brackets + centre crosshair) |
| Light model | Top-left environmental glass: soft top highlight on the frosted base, a diagonal specular sheen (baked) brightening the lens toward top-left, tone deepening to violet at bottom-right; short soft contact edge under the lens. Single consistent source |
| Layer stack | (system squircle mask + system shadow) → frosted ice-white squircle base slab (cyan-tinted edges) → circular glass **lens**, cyan→violet TL→BR gradient + specular gloss → white serif-T crosshair reticle |
| Palette economy | Desaturated frosted base + **one** analogous hue sweep in the lens (cyan **#00B9FF** → blue **#4E87FF** → violet **#8A68FF/#9B5FFF**). White glyph. Accent saturation reserved for the focal lens; base and glyph are neutral. Passes ≤2-hue economy |

## Signature devices
- **The serif-T capture reticle.** Four serif capital *T*s (T for **Text**) rotated so their stems meet as an X crosshair, their serif crossbars reading as the corner brackets of a screen-selection marquee. This is genuine subject-mining: the icon simultaneously says "text," "aim/target," and "drag a selection box" — the exact gesture the app performs. A committed direction, not a template glyph-on-gradient.
- **Floating glass lens on a frosted slab.** A saturated circular gradient disc set into a pale translucent squircle — the current Liquid-Glass "object-on-glass" composition (cf. Tahoe frosted-base icons), giving depth from two glass planes rather than a single flat field.
- **Cool cyan→violet diagonal ramp.** TL cyan → BR violet, a tech-instrument palette that also carries the light model (bright-cool where lit, deep-violet where shaded). The violet endpoint coheres with the app's purple marketing cover.

## Failures
- None. No hard failure on any of the twelve checks; three soft passes flagged below.

## Soft passes (flagged for synthesis)
- **#3 Silhouette test.** Filled solid, the reticle reads as a crosshair/target inside a disc — nameable as "capture/aim," but the *serif-T "text"* meaning is carried by fine terminal shapes that a pure silhouette discards. The "target" reading survives; the "text" reading does not.
- **#4 16px squint.** At menu-bar size the four thin diagonal stems and their serif caps merge toward a fuzzy X/asterisk and the base's frost flattens; the coloured disc + central mark still reads as a lens/target, but the four-mark structure and serif detail smear. Gestalt survives, detail does not.
- **#10 Variant robustness.** The white reticle sits on a mid-tone lens, so it isn't hostage to one background colour — but the icon's whole *personality* is carried by the cyan→violet gradient. In a tinted/mono render the disc collapses to a flat tone and the icon keeps only the reticle shape, losing the cool-instrument identity. Not confirmed as authored Icon-Composer light/dark/mono layers (no variant renders supplied).

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | pass (artwork sits well inside the squircle; base is the mask shape) |
| 2 | Grid adherence | pass (lens + reticle optically centred, safe-zone margins) |
| 3 | Silhouette | soft pass ("target" reads; "text" lost) |
| 4 | 16px squint | soft pass (disc+mark survive; serif detail smears) |
| 5 | Single light model | pass (consistent top-left glass light) |
| 6 | Palette economy | pass (one analogous hue sweep + neutrals) |
| 7 | Figure-ground contrast | pass (white glyph on #00B9FF / #8A68FF lens, >3:1, survives grayscale) |
| 8 | Depth coherence | pass (base < lens < glyph; consistent shadows, no z-fighting) |
| 9 | Era coherence | pass (all-Liquid-Glass; note: baked lens specular deviates from Icon-Composer "let the system apply effects") |
| 10 | Variant robustness | soft pass (glyph independent, but identity is gradient-carried) |
| 11 | Personality | pass (the serif-T reticle is a strong nameable device) |
| 12 | No-text | pass (T-forms are marks, not readable words) |

**Total: 12/12, 0 failures (3 soft passes: #3, #4, #10).**

## Rhymes with (hint only — for icon-cluster synthesis)
- **Capture / screenshot / OCR utilities** that put a lens, reticle, or crosshair inside the mask (viewfinder-motif tools). Style-family guess: **"instrument-lens capture utility."**
- **Liquid-Glass "object-on-frosted-slab"** family — a saturated glass disc/shape floating on a pale translucent squircle base.
- Palette-family rhyme: **cool cyan→violet diagonal tech ramps** (as opposed to warm sky-logic ramps).

## Brand-context note (cover coherence)
The marketing cover runs a **violet/indigo** wavy ground with a literal capture motif — a selection rectangle over a video thumbnail, corner crop-brackets, and a **crosshair/target** at the bottom-right selection corner. That crosshair is the same viewfinder idea the icon's reticle abstracts, and the cover's purple coheres with the icon lens's violet endpoint. The icon is cooler and more saturated (adds cyan) than the flatter cover violet, but the two share the capture-reticle concept and the blue-violet family — reasonable palette coherence, with the icon carrying the brighter, more "instrument" reading.

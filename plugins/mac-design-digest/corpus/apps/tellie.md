# Tellie — profile

- **Source:** macapp.supply (meta.json + cover.png marketing composite + icon.png) · **Surfaces digested:** teleprompter HUD control bar (from marketing composite), current-word highlight mechanic · **Last updated:** 2026-07-19
- **One-sentence identity:** A voice-following Mac teleprompter that lives in a black notch/HUD strip and lights up the word you're saying — CleanShot X's floating-HUD ergonomics with a single warm-orange brand accent and an editorial-serif marketing voice.
- **Cluster:** unassigned (first app in corpus; candidate cluster "warm-accent dark HUD utility")
- **Lineage:** unknown (low) — evidence is a marketing composite, not a window capture; the control strip is a custom-drawn floating HUD (a teleprompter overlay legitimately needs custom chrome), so standard AppKit tells (traffic lights, toolbar, source list) are absent and lineage cannot be confirmed. Nothing here feeds macOS canon.
- **Era (chrome):** custom (opaque near-black HUD; not confirmable as Liquid Glass — a dark HUD reads near-opaque regardless, per the dark-mode-humility rule)

> **Evidence-quality caveat (load-bearing):** the only input showing UI is a 1200×630 OG-image marketing composite. The large black panel is a *stylised* teleprompter surface (the serif "Follows your voice. Word by word." headline is a marketing display face, not the app's reading font). Genuine-looking app chrome is limited to the bottom control bar and the amber current-word highlight. All tokens below are `(estimated)`/`(inferred)` from a composite; colours are crisp so hex values are `(measured)` but their *role* assignment stays inferred. No real screenshot, settings, or window frame was seen.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/orange (accent) | `#FF8A00` (measured)(inferred) | | Primary action fill, eyebrow text, progress fill, icon body — the app's substitute for the system accent |
| status/green | `#34C759` (measured)(inferred) | | "listening/ear" indicator; equals macOS system green (light) exactly (kit: `#34C759`) |
| bg/panel | `#080808` (measured)(inferred) | | HUD strip background, near-black opaque (notch aesthetic) |
| fill/dark-button | `#1C1C1E` (measured)(inferred) | | restart / A− / A+ / ✕ circular buttons — ~1.3:1 vs panel, see Defects |
| track/slider-unfilled | `#252527` (measured)(inferred) | | progress groove, right of knob |
| fill/word-highlight | `#905604` (measured)(inferred) | | dark-amber rounded box behind the live word — the product's soul in one token |
| label/secondary | `#838388` (measured)(inferred) | | "13/24 words · 0:04 left" metadata; ~5.4:1 on panel, passes |
| label/tertiary | ~`#6E6E73` (estimated)(inferred) | | "speed 47" — dimmer than metadata; may dip toward/below 4.5:1 |
| text/headline-cream | `#F6F3EE` (measured)(inferred) | | marketing serif headline — brand, not app body |
| control/size | ~36pt circular buttons (estimated)(inferred) | | reads as the kit's XL/toolbar tier (36pt); pill/circle bezel matches the macOS 27 capsule era |
| icon/body-gradient | `#EC924B`→`#DD7838` vertical (measured)(inferred) | | app icon, warm-orange top→bottom |

## Layout skeletons

**Teleprompter HUD control bar** (single horizontal strip, vertically centred, on a rounded near-black panel; left→right):
1. **Transport cluster** (tight group): orange filled circle = play/pause (⏸ shown) · dark circle = restart (↺) · green filled circle = listening (ear glyph).
2. Gap → **progress metadata**: "13/24 words · 0:04 left" (secondary grey) → horizontal **progress slider** (orange-filled left, grey groove right, light-grey circular knob at ~60%).
3. Gap → **reading controls** (tight group): "speed 47" (tertiary grey) · dark circle A− · dark circle A+ · dark circle ✕ (close).
- Grouping is Gestalt-correct: two tight clusters bracketing the wide progress affordance; all controls circular; only two fills are saturated (orange action + green status).

**Current-word highlight mechanic** (in the reading pane): the live word sits inside a filled dark-amber (`#905604`) rounded box while surrounding words are plain cream — the "lights up the exact word you're saying" feature, rendered as a moving fill.

## Signature moves
- **[GOLDEN-NUGGET] Brand orange bound to the accent role, everywhere.** `#FF8A00` carries the primary button, the progress fill, the word-highlight (darkened), the eyebrow text, and the icon body. The app deliberately substitutes its brand orange for the *user's* system accent — a systematic, purposeful native deviation (signature, not defect), but one that means selection/accent will never track the user's chosen tint.
- **[GOLDEN-NUGGET] The single highlighted word is the whole product.** One amber-boxed word against plain text is the entire value proposition in one mark — a textbook Von Restorff / signal-detection pop that doubles as the demo.
- **Notch-as-form-factor.** "Gives every Mac a notch": the teleprompter is a black rounded HUD evoking the MacBook notch, and the icon encodes it as a black notch cutout at the top of an orange clipboard.
- **Live "ear" listening indicator** (system-green circle, ear glyph) distinct from the transport control — status colour correctly paired with a glyph, not colour alone.

## Defects
- **Focal Collision (soft)** → two saturated filled circles adjacent (orange play/pause + green listening) read at equal weight; the identical circular treatment weakens the "one action" read even though green is semantically a status light. Canon: keep one saturated fill per region; render the status indicator as a smaller dot or a tinted-not-filled treatment.
- **UI-contrast (non-text <3:1)** → the dark circular buttons (`#1C1C1E`) sit ~1.3:1 on the `#080808` panel; the button *shapes* are near-invisible and only their white glyphs carry the affordance. Canon: lift recessive controls to a ≥3:1 fill or add a hairline.
- **Non-native accent binding** (recorded as signature above, flagged here for completeness): accent role is app-brand, not system-accent — a deliberate deviation, not sloppiness.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| teleprompter HUD control bar (from marketing composite) | 10/14 | #8 two saturated fills (orange+green); #10 dark-button fill ~1.3:1 <3:1; #9 "speed 47" borderline contrast. N/A: #6 #12 #13 #14 |
| native-tells audit | 3/10 applicable | Pass: #2 glass/opaque discipline (all-floating chrome, opaque content), #7 one prominent action, #5 density plausible (~36pt). Fail: #6 accent not system-bound. N/A: #1 #3 #4 #8 #9 #10 (no window chrome/sidebar/list; composite) |

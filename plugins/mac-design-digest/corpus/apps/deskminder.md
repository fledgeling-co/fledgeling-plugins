# DeskMinder — profile

- **Source:** macapp.supply (cover only; no dedicated UI shots) · **Surfaces digested:** 1 — floating desktop reminder pill (inside a marketing composite) · **Last updated:** 2026-07-19
- **One-sentence identity:** iOS Live-Activity language transplanted to the Mac desktop — a brand-green countdown capsule that floats over the wallpaper, Alcove's Dynamic-Island idea done in colour instead of true-black.
- **Cluster:** unassigned (candidate: "Dynamic-Island / live-activity utility" alongside Alcove)
- **Lineage:** native (low–med) — genuine Mac desktop utility, almost certainly custom-drawn SwiftUI; but the only visible surface is a borderless brand-styled overlay with zero standard AppKit controls, so the native reading is inferred from category/runtime, not from control grammar. Its brand-tinted material and always-on-top desktop pill are deliberate departures from native grammar → EXCLUDED from macOS canon (lineage gate).
- **Era (chrome):** custom-drawn brand material (not Liquid Glass; not legacy AppKit). Surrounding menu bar in the render is genuine modern-macOS system chrome (notch, translucent bar, third-party menu-bar extras, "Sat 28 Jun 03:50").

## Evidence quality caveat
All values below are from a **1× marketing composite** (1200×630), not a clean @2× screenshot. The pill occupies ~185px of a downscaled render of unknown true scale, so **no pt sizes are recoverable** and every metric is `(estimated)` with wide ranges and ratio-first reasoning. One surface, one state (a "62 min" countdown) — thin evidence.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| surface/kind | borderless floating desktop pill, top-left under the notch | (estimated)(inferred) | not a window (no traffic lights/titlebar), not a true menu-bar dropdown — parks on the desktop |
| pill/fill | saturated brand green ~#3F9A2E–#4CA82E, slightly translucent over wallpaper | (estimated)(inferred) | reads as brand-tinted material, NOT neutral adaptive glass; green wallpaper shows through faintly |
| pill/shape | capsule (radius = height/2, ~11px on a ~22px-tall bar) | (estimated)(inferred) | full pill; aspect ~8–9:1 w:h |
| pill/aspect | main info capsule ~185×22px (render px) | (estimated)(inferred) | scale unknowable; ratio ~8.4:1 |
| chip/timer | inset lighter-green rounded segment holding clock glyph + "62 min" | (estimated)(inferred) | a translucent "over-fill" chip nested inside the translucent pill (glass-on-glass-adjacent) |
| glyph/timer | thin-stroke outline clock/gauge, single hand, ~14px, white | (estimated)(inferred) | countdown affordance; monochrome white, no accent tint |
| type/value | "62 min" white, semibold-ish, ~13px-class | (estimated)(inferred) | the primary glanceable datum |
| type/label | "Reminder…" muted desaturated green-white, regular, truncated w/ ellipsis | (estimated)(inferred) | secondary label; de-emphasised by colour + weight; green-on-green, low contrast |
| close/button | detached squircle ~24–26px, dark opaque green ~#357A28, white ✕ | (estimated)(inferred) | superellipse radius ~0.3×side (iOS-rounded-square, not a true circle, not a capsule) |
| space/gap | ~8px between close button and info capsule | (estimated)(inferred) | separates the two as distinct groups (good proximity) |
| brand/hue | single committed green carries icon + UI + marketing backdrop | (estimated)(confirmed) | mono-hue brand system (confirmed across icon, pill, composite) |

## Layout skeletons

**Floating reminder pill (collapsed/active state).** A horizontal two-group cluster parked at desktop top-left, just below the notch:
- Group 1 (leading): a **detached** squircle close button (✕), ~24px, dark opaque green — the dismiss affordance, gapped ~8px from group 2.
- Group 2 (info capsule): a capsule split into two zones — (a) a lighter inset **time chip**: outline clock glyph + "62 min" (white, tight internal spacing); (b) a **reminder label** zone: "Reminder…" in muted green, truncated. A faint vertical seam divides the chip from the label. Reads as container-morphing (chip nested in pill), the live-activity vocabulary of a compact pill that expands.

## Signature moves
- **[GOLDEN-NUGGET] The whole app is a Mac desktop Live Activity.** It imports the iPhone Dynamic-Island / Live-Activity capsule — inset status chip + glanceable countdown + truncated title + compact→expandable morphing — and parks it on the desktop as an always-visible reminder. Where Alcove fused with the physical notch using true-black, DeskMinder does it in **brand colour**: the entire capsule is drenched in the product green, making the widget *and* the icon *and* the marketing one continuous mono-green identity. Characterful and coherent — and a deliberate native-grammar departure (native glass is neutral; accent is reserved for one action, never the whole material).
- **Countdown-as-open-loop.** Surfacing "62 min" persistently exploits the Zeigarnik effect / goal-gradient — an unfinished timer nags at working memory, which is precisely the "for people who get easily distracted" pitch. The design's job is salience, and the pill is built to be glanced, not read.

## Defects
- **Brand-tinted material over native glass grammar** → the container is saturated brand green rather than neutral vibrancy with accent reserved for one action. Systematic + purposeful (brand, glanceability) + no hard accessibility break → recorded as **signature-with-caveat, not anti-pattern**, but EXCLUDED from macOS canon per the lineage gate. Canon would use neutral HUD material and bind green only to the single primary affordance.
- **Contrast Dilution (real, #9/#10):** "Reminder…" is a muted green on green (est. <4.5:1), and the dark-green pill sits on a **green** wallpaper (est. ~2:1 separation), leaning on a soft shadow to detach. Green-on-green undercuts the very glanceability the pill exists for — on a busy or green desktop the widget camouflages (Von Restorff / signal-detection: the one different thing must break its surround; here it nearly matches it). A neutral or higher-contrast material, or a darker scrim, would restore pop.
- **No system-accent binding** — the glyph and ✕ are fixed white/green, ignoring `controlAccentColor`. Defensible for a branded HUD, but it's where the native reading diverges.
- **Evidence poverty (not a design defect):** 1 surface / 1 state from a marketing render — no expanded state, no creation UI ("one click" flow unseen), no settings/onboarding, no non-green-desktop robustness test.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| floating reminder pill (marketing render) | 10/14 | #9 secondary label green-on-green (<4.5:1 est.); #10 pill-vs-green-wallpaper separation low (~2:1 est.). N/A on a single custom widget: #2 alignment, #5 line-height, #12 input height, #13 label proximity, #14 focus state. |
| — native audit | 5/10 | #2 brand-tinted material + chip-in-pill nested translucency (not neutral glass); #6 accent floods whole surface instead of one action; #5 density unmeasurable on composite. N/A: #4 sidebar, #9 toolbar. Pass: #1 (inferred), #7 one action, #8 concentric-ish radii, #10 legit borderless HUD (no faked chrome). |

## Brand evidence (marketing composite — NOT app-UI tokens)
- **Icon:** glossy Liquid-Glass-style green squircle, specular top highlight, holding a white outline **gauge/speedometer dial** (single needle) — a timer/pace motif. Mono-green, matches the UI.
- **Wordmark:** "DeskMinder" in a very heavy **Black/Heavy grotesque** (geometric-humanist), near-black on mint.
- **Tagline:** medium-weight neutral-gray humanist sans, two lines, generous leading.
- **Backdrop:** flat mint/pale-green ~#C8E6CE — the whole composite is a **Committed single-hue** field (one green carries ~60% of the surface).

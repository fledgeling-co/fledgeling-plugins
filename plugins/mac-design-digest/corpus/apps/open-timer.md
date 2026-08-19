# Open Timer — profile

- **Source:** macapp.supply (cover composite only; no in-app screenshots supplied) · **Surfaces digested:** menu-bar-extra popover (dark), inside a marketing cover · **Last updated:** 2026-07-19
- **One-sentence identity:** A menu-bar freelance timer that borrows the iOS stopwatch's oversized-numeral hero and drops it onto a hardcoded brand-navy card — Session's utility with a consumer-app coat of paint, not a system-material native panel.
- **Cluster:** unassigned (candidate: "brand-dark menu-bar utility")
- **Lineage:** native / SwiftUI MenuBarExtra (window style) — **low-med confidence**. Self-described "native macOS menu bar" app; the only evidence is a *marketing render* of the popover, not a raw screenshot, so all geometry is `(estimated)` with a mockup caveat. Non-native tells (custom surface, fixed accent, in-content ✕) are recorded below and never feed macOS canon.
- **Era (chrome):** big-sur (flat, opaque, rounded) — targets **macOS 13+ (Ventura)**, so it predates and cannot rely on Liquid Glass; absence of glass is era-correct, not a defect.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/panel | `#0B1830` deep navy | (measured)(inferred) | Hardcoded brand surface, NOT system dark (`#1E1E1E`) or `NSVisualEffectView` vibrancy — the #1 non-native tell |
| bg/backdrop (brand) | diagonal gradient `#1F61F3` (TL) → `#071F66` (BR) | (measured)(inferred) | Marketing composite only — cover backdrop, not app UI |
| accent/primary | `#0A84FF` | (measured)(inferred) | iOS dark systemBlue — a *fixed* brand blue, not the macOS 27 kit blue (`#0091FF`) and not the user's `controlAccentColor`. 4.85:1 on panel |
| text/primary | `#FFFFFF` (title, time) | (measured)(inferred) | 17.7:1 on panel — excellent |
| text/secondary ("Tracking…") | `#3B4559` | (measured)(inferred) | **1.84:1 on panel — fails 4.5:1; Contrast Dilution, see Defects** |
| glyph/close ✕ | `#697180` | (measured)(inferred) | 3.60:1 — passes 3:1 UI-contrast floor |
| dataviz/bar-muted | `#0A4E98` | (measured)(inferred) | 2.15:1 on panel — below 3:1, but decorative; meaning carried by the one accent bar |
| dataviz/bar-active | `#0A84FF` | (measured)(inferred) | The single highlighted session bar; shares the action accent (Von Restorff) |
| type/display (time) | ~48–52px geometric grotesque, tabular figures (SF Pro Display-class) | (estimated)(inferred) | Cap height ~45px in render; hero readout "01:24:36" |
| type/title | ~18–20px, semibold ("Open Timer") | (estimated)(inferred) | Larger than 13pt macOS body — consumer scale |
| type/label | ~14px ("Tracking…") | (estimated)(inferred) | |
| radius/panel | ~20px on a ~297px-wide panel (~6.7% of width) | (estimated)(inferred) | Coincidentally matches the macOS 27 popover-body radius (20), but era is Big Sur — read as a generic large "floating card" radius |
| radius/bar | ~4–6px rounded-top rects | (estimated)(inferred) | |
| control/pause | ~55px circle, white pause glyph on accent fill | (estimated)(inferred) | Large, comfortable Fitts target |
| chrome/window | menu-bar-extra floating panel, ~297×283px render, no traffic lights, no popover beak | (estimated)(inferred) | No traffic lights = correct for a menu bar extra; in-content top-right ✕ is the iOS/web habit |

## Layout skeletons

**Menu-bar-extra popover (dark, ~297×283 render, ~@1x logical):**
- Single opaque navy card, ~20px corners, no arrow/beak, no traffic lights.
- Header row: left-aligned title "Open Timer" on a ~x=19px inset; trailing ✕ close glyph, right-aligned. One shared left axis governs title / status / time.
- Status line: muted "Tracking…" below title (~45px below), same left axis.
- Hero block: oversized tabular time "01:24:36" on the left axis; the accent circular pause button sits as a satellite at the *end* of the numerals — and overlaps the final digit (see Defects).
- Footer: 7-bar session histogram spanning the card width, rounded-top bars, one bar in the accent, the rest muted navy.
- Vertical rhythm is generous (glanceable), not dense; hierarchy is time (bright, huge) → title → muted status/close.

## Signature moves
- **[GOLDEN-NUGGET] Time-as-hero + session sparkline.** The oversized tabular readout is the emotional center and the histogram turns a one-shot timer into a glanceable "how has today gone" dashboard — the right instinct for a menu-bar utility whose whole job is a 1-second glance (Peak-End / glanceability). This framing, not the chrome, is the app's character.
- **Single-accent economy.** Exactly one saturated element as an *action* (pause button) and exactly one as *data* (the tall bar); everything else is white-or-muted on navy. Disciplined Von Restorff.

## Defects
- **Contrast Dilution** → "Tracking…" `#3B4559` on `#0B1830` = **1.84:1** (needs 4.5:1). The de-emphasis overshoots into near-illegibility. Canon fix: secondary label to a ~55% white tier (kit Label-2 dark `#FFFFFF`@55%) → ~5–6:1.
- **Control occludes data (layout overlap)** → the accent pause button overlaps the final digit of "01:24:36", partially hiding the primary readout. The one loud element literally collides with the number it controls. Canon fix: place the control trailing the numerals with a gap, or below them; never over the readout.
- **Non-native surface theming** (native-fidelity finding, recorded as tell + correction, NOT counted toward macOS canon): hardcoded brand-navy surface instead of system material/vibrancy, and a fixed iOS-blue accent instead of `controlAccentColor`. A native SwiftUI popover would inherit the appearance and the user's accent; this reads as a themed consumer card. Legitimate as a house style, but it is why the panel feels "app-branded" rather than "of the Mac."
- Muted histogram bars at 2.15:1 sit under the 3:1 non-text floor; acceptable only because they are decorative and the meaningful bar is the accent one.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar popover (dark, from cover) | 12/14 | #9 text contrast ("Tracking…" 1.84:1); #10 borderline (muted bars 2.15:1); #1 grid unverifiable from render. Native-tells audit ~6/10: fails #1 (custom surface, not system material), #6 (fixed accent, not user accent), #10 (in-content ✕); #5 partial (consumer-large density, not 13pt); passes #2 (no glass, era-correct), #7 (one action), #8 (radii). |

> **Caveat for the synthesis pass:** all evidence is from ONE marketing composite, and the panel is a *render*, not a captured screenshot. Everything is `(inferred)` and mockup-qualified. Do not promote anything from this app alone; do not feed its custom navy/blue theme into native macOS canon.

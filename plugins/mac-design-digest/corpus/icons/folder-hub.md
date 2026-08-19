# Icon: Folder Hub

- **Era:** Big Sur unified · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (128×128 web render — low res, see caveats) · **Category:** Utility
- **What the app does:** turns the MacBook notch into a slide-down file drawer ("move to notch to show, move away to hide"). The icon subject-mines that exact mechanic.

| Dimension | Reading |
|---|---|
| Background | Long single-hue vertical ramp #EB8834 → #070202 (bright amber-orange at top → near-black at base) `(measured, 128px)` |
| Glyph | Abstract object: a lighter warm "drawer" pill #D38C5E in the upper third + a pure-black notch pill #000000 flush to the top edge. Not centred — deliberately top-anchored (the notch lives at a screen's top). |
| Overlay device | None (no diagonal tool/badge/frame) |
| Light model | Top-down, "sky logic": bright at top, darkening to near-black at the base. Drawer pill lit as a raised panel. No visible specular/glass refraction (at 128px). |
| Layer stack | (back→front) warm amber→black gradient field · recessed black notch pill (top-centre) · lighter drawer panel pill (upper third) · [baked squircle mask + drop shadow from the web render] |
| Palette economy | One hue family (orange→brown→black). Zero reserved saturated accent — the "glyph" is a same-hue lighter tint, so nothing pops. |

## Signature devices

- **[GOLDEN-NUGGET] Notch-as-subject.** The icon depicts the MacBook hardware notch (black pill, top-centre) as its anchor, with a drawer sliding beneath it. Subject-mining the *hardware* is rare and is the whole concept — the icon's soul. Filed as a nameable, committed device.
- **The squircle *is* the screen.** Rounded top corners + the notch quote the top edge of a MacBook display; the icon frames the region where the app lives rather than drawing a folder.
- **Long amber→black vertical ramp.** Unusually dark/long for the Big Sur idiom — the bottom ~40% collapses to near-black, giving a moody, underlit field.

## Failures

- **#3 Silhouette.** Filled solid black, the icon is just a rounded square — the notch and drawer are tonal, not shape-bearing. Not nameable from silhouette alone.
- **#4 16px squint.** The notch and the low-contrast drawer both smear/vanish at menu-bar size; the icon reads as "a warm gradient square," not as Folder Hub. (Non-negotiable check — a real Dock/Spotlight failure.)
- **#7 Figure-ground.** The drawer pill (#D38C5E) sits on the upper-orange band (#DA9460) at **1.09:1** `(measured)` — effectively invisible; disappears entirely in grayscale. The *actual subject* is the least legible element. Only the notch holds contrast (8.1:1 vs the top orange), and it's the smallest mark on the canvas.

## Soft passes (flagged)

- **#2 Grid.** Content is deliberately top-anchored (subject-driven — notch is at a screen's top), but the lower ~55% is empty dark gradient; the focal mass is not optically centred and the dead field is part of why the icon reads as an empty square when shrunk.
- **#10 Variant robustness.** Big Sur era, so not strictly in scope, but the subject depends *entirely* on tonal difference within one warm ramp — it would not survive a mono/tinted/dark render (drawer + notch collapse). Same root cause as #7.
- **#1 Mask.** Composition fits the squircle, but the render has a baked mask + drop shadow (not an unmasked full-bleed layer set), so HIG mask discipline can't be verified from this source.
- **#8 Depth.** Layer ordering is coherent (recessed notch, raised drawer, top-down light), but the drawer's separation from the field is so weak the depth barely registers.

Passing clean: #5 single light model (consistent top-down), #6 palette economy (one hue family), #9 era coherence (all Big Sur-language devices), #11 personality (the notch device), #12 no-text.

## Rhymes with

- Menu-bar / notch-utility icons that ride a single warm or cool gradient square with one minimal centred motif (the "NotchNook / notch-drawer" utility family). Style-family guess: **minimal gradient-square utility with a subject-mined hardware motif** — strong concept, contrast-starved execution.

## Cross-icon / synthesis notes

- **Resolution caveat:** 128px web render. Notch and drawer edges are soft; any subtle Big Sur micro-shadows or faint glass treatment can't be confirmed. All hex `(measured, 128px)` — treat as ±, not exact.
- **Brand incoherence (icon vs cover):** the marketing cover is built on a **cool electric violet** hero band on black; the icon is **warm amber-orange**. No shared hue family between icon and brand surface — a palette-coherence gap worth noting for synthesis (icon does not carry the app's marketing colour).
- **Pattern to watch:** "great concept, sub-3:1 subject" — an icon whose single distinctive idea is delivered in near-isoluminant tints of one hue. If ≥3 icons show this, it's a canon anti-pattern (name candidate: *Isoluminant Subject* / *Tonal Whisper*).

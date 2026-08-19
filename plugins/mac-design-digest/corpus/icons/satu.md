# Icon: Satu

- **Era:** Big Sur unified · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 512×512 — a web half-res render of the 1024 master; edges clean, fine gradient nuance may be softened) · **Category:** Productivity
- **App:** "A calm productivity companion that lives in your Mac menubar" · developer domain `mnmls.net`

| Dimension | Reading |
|---|---|
| Background | flat `#FFFFFF` (measured — interior sampled uniformly white, no ramp) |
| Glyph | abstract geometric mark — a horizontal capsule bar + a descending rounded tab, charcoal ramp `#3B3B3B` (upper-left) → `#262626` (lower-right), foot `#2A2A2A`; reads loosely as a stylised "7"/"F"/"r" but resolves as abstract-monogram, not a real-world object. Sits optically centred, weighted a touch high. |
| Overlay device | diagonal **negative-space slice** — a thin `#FFFFFF` gap (ground bleeding through) cleaves the mark lower-left→upper-right, reading as a single specular glint. Not a tool/badge/frame. |
| Light model | soft, upper-left; expressed *only* as the gentle charcoal gradient across the glyph (lighter left, darker right); no cast shadows inside the mask; the white slice is the sole "highlight". |
| Layer stack | (back→front) flat white squircle ground · charcoal glyph (two rounded elements) · diagonal white negative-space slice (ground showing through). Delivered pre-masked with transparent corners; no baked drop shadow (HIG-correct — margins measured α=0). |
| Palette economy | one hue family (neutral only): white + charcoal, **zero accent** — the most economical possible. Figure-ground ~13:1, survives grayscale trivially. |

## Signature devices
- **Diagonal negative-space slice cleaving the mark** `[GOLDEN-NUGGET]` — the mark's whole identity is a thin white cut, mechanically the ground showing through, read as a glass glint. Distinctive and nameable, but *contrast-dependent*: it is negative space, so it collapses in a solid-black silhouette and vanishes at 16px (see failures/soft passes).
- **Monochrome austerity as a committed direction** — white + charcoal, no accent, no scene. This is a Swiss/minimalist *choice*, not a template-default; it is the visual signature of the `mnmls` (minimals) studio brand rather than of the app's content.
- **Capsule-terminal geometry** — every stroke end is fully rounded; the bar and foot share one radius language, giving the mark its calm, non-sharp posture.
- **Subtle left-lit charcoal gradient within the glyph** — a restrained dimensional cue (~`#3B3B3B`→`#262626`) that keeps the flat mark from reading as a pure sticker.

## Failures
- **#10 Variant robustness (the one hard failure)** — the composition is white-ground-dependent. The signature slice *is* the white background bleeding through the glyph; invert the ground for dark/clear/tinted appearances and the slice disappears and the mark breaks. No evidence of dark/tinted adaptation. This is the concrete cost of shipping a Big-Sur-language icon into the Liquid Glass era without appearance layers.

## Soft passes (flagged for synthesis)
- **#3 Silhouette** — filled solid black, the two elements merge and the defining diagonal slice (negative space) closes up; the mark survives as a bar+foot blob but its signature is gone. Nameable as an abstract mark, not as an object.
- **#4 16px squint** — holds as a clean dark bar + nub (no smear), but the slice is lost and the two elements read as one; legible, identity thinned.
- **#2 Grid** — mark sits slightly high/upper-weighted rather than on the optical centre; within tolerance, not nudged-looking.

## Cross-icon / brand notes
- **Icon↔product palette incoherence** — the icon is austere monochrome; the app itself (per cover) is warm and playful: blue-purple gradient chrome, a green `Done` accent, and a lofi cat-and-duck illustration. The icon communicates the *studio* (mnmls minimalism), not the *subject* (calm-but-cute focus utility). A nameable tension, not necessarily a defect.
- **Era lag** — a uniform front-facing squircle with a single soft light and a diagonal plane-breaking element is Big Sur unified language, executed minimally in monochrome. It exhibits none of Liquid Glass's translucency/refraction/tinted-variant support despite shipping in the macOS 26 era — internally coherent (#9 passes), but the source of the #10 failure.

## Rhymes with
- Swiss / International **monochrome monogram** family — black-on-white abstract-letterform marks (Vercel/Linear-register studio marks). First member of a potential "reductive monochrome" icon cluster; needs ≥2 more independent icons before any promotion.

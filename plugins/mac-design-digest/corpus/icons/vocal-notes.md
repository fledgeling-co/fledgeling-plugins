# Icon: Vocal Notes

- **Era:** Big Sur unified (flat mono-glyph sub-variant) · **Rubric:** 12/12 (4 soft passes, 0 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 1024×1024, SHA-1 `fc67eb13`) · **Category:** Audio
- **One-line:** A textbook flat-azure waveform on a cool near-white ramp — technically impeccable, aesthetically the Audio-category default.

| Dimension | Reading |
|---|---|
| Background | Cool near-white **vertical ramp** `#FBFBFD` (top) → `#F1F3F7` (bottom) (measured)(inferred) — light-at-top sky logic, ~10 levels of travel, faint blue-gray tint |
| Glyph | **Abstract audio waveform**, flat single-fill azure `#1678E6` (measured) — no gradient, no self-shadow. Optically centred: glyph bbox x[172–850] y[192–830], centre (511, 511) vs canvas (512, 512) |
| Overlay device | **None** — no diagonal tool, badge, or frame |
| Light model | **Top-down**, expressed only in the background ramp; glyph is flat (zero baked lighting). No specular, no translucency. System-style drop shadow carried by the whole squircle (presentation render) |
| Layer stack | **2 planes** — back: cool-white ramp field · front: flat azure welded-capsule waveform |
| Palette economy | **1 hue family** (azure) + a cool near-white ramp. The glyph *is* the only saturated element — exemplary economy |

## Signature devices
- **Welded capsule waveform** `[GOLDEN-NUGGET]` — the central bars are not discrete EQ sticks; rounded capsules **fuse into one continuous ribbon** with rounded negative-space notches cut between them. More crafted than the usual "five separated bars," while staying inside the waveform convention.
- **Two isolated bookend dots** — a short capsule flanks the ribbon far-left (x190–250) and far-right (x790–850), reading as the quiet start/end of a recording (or L/R channel markers). They frame the amplitude envelope.
- **Vertically-offset inner nubs** — the two inner accents sit high-left / low-right within the ribbon, giving a subtle oscillation/rotation instead of a static mirror. The one bit of dynamism in an otherwise symmetric envelope.
- **Single flat brand-azure fill** — `#1678E6`, a custom brand blue slightly deeper and less-cyan than the macOS 27 kit system blue (`#0088FF` light). Coherent with the cover's glassy blue title and the app UI's blue selection/accent.

## Failures
- **None (0 hard failures).** Every structural check passes. Four are **soft passes**, flagged below — the score reflects technical/compositional soundness, not distinctiveness.

### Soft passes (flagged)
- **#4 16px squint** — the two bookend dots collapse to specks and the ribbon's negative-space notches merge at menu-bar/Spotlight size; the gross "vertical bars = audio" gesture survives, the fine interlock does not.
- **#7 figure-ground** — measured **3.99:1** blue-on-field: clears the 3:1 icon floor and survives grayscale as a mid-gray, but only just (~4:1, not a generous margin).
- **#10 variant robustness** — flat, luminance-legible 2-tone would survive mono/tinted renders and the azure holds on dark, so the *composition* is robust; but **no dark/clear/tinted variants are authored** and the near-white field is intrinsic. Not built in Icon Composer.
- **#11 personality** — one nameable device (welded ribbon + bookend dots) clears the bar, but the concept (blue waveform = Audio) is the category-default solution; the icon reads more template-safe than committed.

## Rhymes with
- The **flat mono-glyph on cool near-white ramp** family — a single SF-Symbol-grade glyph, flat-filled, on a barely-there light ramp (the restrained end of Big Sur unified). No overlay tool, no depth baking.
- Any **Audio-category waveform** icon (Voice Memos lineage): amplitude bars as the subject. Vocal Notes' fusion of the bars into a welded ribbon is its differentiator within that crowd.
- *Hint for synthesis:* likely seeds a "flat-glyph-on-light-ramp utility" icon cluster; the welded-ribbon device is the candidate signature to watch for recurrence.

## Notes
- **Resolution: trustworthy.** Full 1024×1024, vector-crisp edges — not a resized web render.
- **But it is a presentation render, not the raw layer.** Corners are transparent (a=0) and a system-style drop shadow is baked in below the squircle — macapp.supply has already applied the rounded-rect mask + shadow. Mask discipline (#1) is therefore judged from the masked presentation, not the delivered full-bleed square.
- **Era-lag finding.** A 2026 Audio app shipping a flat Big Sur-era icon: no Liquid Glass, no specular/refraction/translucency, no layered glass, no authored appearance variants. Consistent within its chosen (older) language, but current-era native apps author light/dark/clear/tinted in Icon Composer.
- The welded glyph could be read as a faint abstract monogram, but the dominant and intended reading is a sound waveform.

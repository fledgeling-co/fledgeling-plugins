# Icon: DynamicLake

- **Era:** Big Sur unified (hybrid — gradient squircle field + skeuomorphic device-bezel quote) · **Rubric:** 8/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.webp`, 204×204 web render — SHA-1 73e116ce). Not a 1024 master; fine specular/bezel px are `(estimated)` from an upscaled render.
- **Subject:** "Dynamic Island Mac" — brings the iPhone Dynamic Island to macOS. The icon is a literal depiction of that subject: an iPhone screen (bezel + notch + glowing wallpaper) rendered face-on inside the squircle.

| Dimension | Reading |
|---|---|
| Background | Ramp, vertical: `#362D55` dark indigo (top) → `#57449A` violet → `#8E68D7` lilac → `#E6A2F7` pink glow (bottom). Inverted sky logic — brightest at the *bottom*, reading as internal screen glow. `(estimated)` |
| Glyph | Object — a recessed Dynamic-Island notch/pill at top-center, `#2C2446`. Optically centred on the vertical axis. Sole discrete figure; the rest of the field is full-bleed "screen". |
| Overlay device | Frame — a white/silver device bezel (`#FFFFFF`) with a near-black inner edge (`#010101`) tracing the mask radius; an iPhone-front quote. |
| Light model | Internal screen glow: diffuse light source at bottom-center, dark falloff toward the top. Baked inner shadow beneath the top bezel. No glass specular / refraction. |
| Layer stack | (back→front) white/silver bezel frame → thin black inner bezel edge → purple vertical gradient screen field → recessed dark notch/pill (top-center) → baked inner top shadow. |
| Palette economy | One hue family (indigo→violet→lilac) resolving to a pink terminus. Accent = the `#E6A2F7` bottom glow. Frame is the only non-purple element. Economical. |

## Signature devices
- **Dynamic-Island notch cutout** — a dark recessed pill breaking the top edge; the literal, subject-derived concept and the icon's only nameable figure. `[GOLDEN-NUGGET]`
- **iPhone screen-in-bezel frame quote** — a baked white/silver bezel + black edge makes the whole squircle read as a phone seen face-on (a skeuomorphic device quote inside an otherwise Big Sur gradient field).
- **Bottom-up screen glow** — the gradient inverts the conventional light-at-top sky ramp so the wallpaper appears lit from within, matching the app's own wallpaper (see cover).

## Failures
- **#3 Silhouette test** — filled solid black it is a blank squircle; the notch is too small to carry the shape. Nothing nameable from silhouette alone.
- **#4 16px squint test** — the entire identity is the notch, which is ~10% of the width and vanishes below Dock size; at 16px this is "a purple square." The subject does not survive Dock/Spotlight duty.
- **#7 Figure-ground contrast** — notch `#2C2446` vs top field `#362D55` is near-isoluminant; the only figure barely separates from ground and disappears in grayscale (well under the 3:1 floor).
- **#10 Variant robustness** — not built as Liquid Glass layers; identity rests entirely on the purple gradient + white frame. In mono/tinted/clear renders the notch collapses and only a frame remains.

## Soft passes (flagged, scored as pass)
- **#1 Mask discipline** — the baked white bezel *follows* the mask radius (no mismatch), but baking a bezel + inner shadow deviates from current HIG, which says let the system apply bezel/shadow/specular.
- **#2 Grid adherence** — no discrete central glyph to grid; the notch is centred and the field is full-bleed by design, so this passes only in the "full-bleed background field" sense.
- **#9 Era coherence** — internally consistent, but it is a hybrid (Big Sur gradient squircle carrying a skeuomorphic phone-bezel quote) and is a full era behind macOS 26 Liquid Glass.

## Rhymes with
- Screen/wallpaper-depicting utility icons and device-frame quotes — icons whose subject IS a phone/display (wallpaper managers, notch/Dynamic-Island utilities, screen-recorder tools). Style family hint: **gradient-field object icons that render a screen inside a device bezel**. No corpus neighbours yet (first of its kind here).

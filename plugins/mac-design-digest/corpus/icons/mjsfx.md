# Icon: MJSFX

- **Era:** custom (flat vector brand mark — does not engage Big Sur material or Liquid Glass layering) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (icon.png, 600×600 web render — master would be 1024) · **Category:** Audio · **App:** "a sounds and effects design studio" (8-bit SFX generator/editor)
- **SHA-1:** 313b463f

| Dimension | Reading |
|---|---|
| Background | Two-tone inset panel: lighter bezel field `#191C20` (fills the squircle) around a darker screen panel `#0D0F12` (rounded-rect, ~30px inset). Flat, no ramp `(measured)` |
| Glyph | Single-cycle **sine wave**, flat solid cyan `#00E0FF`, rounded stroke caps, stroke ≈24px @600 (~4% of canvas). Spans nearly edge-to-edge; abstract/object hybrid — an oscilloscope trace `(measured)` |
| Overlay device | Framed-window / instrument-screen motif (the inset dark panel reads as a scope screen); faint zero-axis baseline `#1B1F24` hairline through the vertical centre `(measured)` |
| Light model | **None** — uniformly flat fill, no gradient, no specular, no baked shadow. Only depth cue is the tonal two-tone panel inset (a bezel/screen tonal step, not a lit surface) |
| Layer stack | (back→front) 1) bezel field `#191C20` · 2) inset screen panel `#0D0F12` · 3) zero-axis baseline `#1B1F24` · 4) cyan sine wave `#00E0FF` |
| Palette economy | 1 accent hue (cyan) + a 3-step near-black neutral ramp. Saturation reserved entirely for the glyph — textbook accent economy |

## Signature devices
- **Oscilloscope screen**: dark inset panel framed by a marginally-lighter bezel, read as an instrument display — a framed-window motif applied literally to the app's subject (waveform editing).
- **Single-cycle sine wave, rounded caps**, drawn near-full-bleed with a **zero-axis baseline hairline** — the icon *is* an oscilloscope trace. Maximally literal subject communication for an SFX/waveform tool.
- **Monochrome-cyan-on-near-black** instrument palette — coheres tightly with the cover (same cyan family `#00E0FF`/`#2EC6DA`, same near-black `#181B1F`/`#0C0F11` ground, monospace "8-BIT SOUND DESIGN" branding). The icon mark is reproduced verbatim in the cover header logo. Committed terminal/instrument direction, not template-default.

## Failures
- **#10 Variant robustness (Liquid Glass):** the cyan `#00E0FF` glyph is **background-dependent** — it lives on near-black. The design is dark-locked with no authored light variant; on a light/clear render the cyan would drop toward low contrast, and it isn't built as Icon Composer layers. The single-stroke shape *is* mono/tint-friendly, but the fixed rendering does not survive a light-ground variant. (Soft-adjacent — the glyph geometry is robust; the colour binding is not.)

## Soft passes (borderline, scored as pass)
- **#1 Mask discipline:** the inset panel's own rounded corners echo the system squircle (a concentric double-radius) — the framed-window device is intentional and common, but it flirts with the "baked-in corner radius" concern; at Dock size the inner radius risks reading as a bezel mismatch.
- **#3 Silhouette:** filled solid black the subject is a *thin line*, not a mass — it reads as "sine wave" by gesture, but the icon leans on cyan-on-dark contrast rather than shape mass to carry the silhouette.
- **#4 16px squint:** the ~4% stroke thins toward ~0.6px at 16px, but the single big S-gesture spanning the whole tile survives; the baseline hairline and panel inset harmlessly disappear.
- **#5 Single light model:** flat = *no* light model — trivially consistent (nothing to conflict), but the absence of any lighting/depth is exactly why the icon reads as a flat web/brand mark rather than a dimensional native icon.

## Rhymes with
- **Dark terminal / developer-tool glyph family** — a single luminous accent glyph on a near-black field, no Big Sur material (Ghostty/iTerm-adjacent CLI icons).
- **Minimalist audio-utility / oscilloscope-app icons** — waveform-as-subject, instrument-screen framing.
- *Style-family hint (not canon — single-icon observation):* "flat instrument glyph" — accent-stroke-on-near-black, subject drawn as a scope trace, monochrome accent economy. Needs ≥2 more independent icons to promote.

# Icon: MailTwin

- **Era:** Big Sur unified squircle — but really an iOS-flat App-Store icon (saturated gradient + white line-glyph + AI sparkles), pre-dating and ignoring Liquid Glass · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512, SHA-1 `bbdd22f6`). Category: Productivity. App: an AI reply generator that lives inside Apple Mail.
- **Resolution caveat:** 512×512, not the 1024 master. Corners are fully transparent — the artwork ships **pre-masked** (its own baked squircle), not as a full-bleed unmasked square. Colours `(measured)` at 512; stroke widths and the corner radius `(estimated)`.

| Dimension | Reading |
|---|---|
| Background | Diagonal ramp `#F786A4` (coral-pink, top-left, lightest) → `#C25DC8` (magenta, centre) → `#8B6FF6` (blue-violet, bottom-right). Light origin = top-left corner. `(measured)` |
| Top band | Subtle lighter horizontal panel across the top ~21% (seam ~y=110 at 512): G-channel steps from ~127 above to ~98 below — a glassy top-sheen band, not a gradient artefact. `(measured)` |
| Glyph | Object — a front-facing envelope. White body `#FFFFFF` with a faint single detail line `#F2F2F2` (message-text hint), and a purple V-flap drawn as a **stroke** `#8C57D9`. Horizontally centred; optical centre ~8px low of geometric centre. Envelope spans ~62% of canvas width. `(measured)` |
| Overlay device | Two 4-point "AI" sparkles top-right: large white `#FFFFFF` (upper) + small violet `#AD74F5` (lower-right). Decals on the top plane, not a badge or tool. `(measured)` |
| Light model | Flat. One diagonal gradient (top-left light → bottom-right dark) + the top-sheen band. Envelope is flat white and **shadowless** — no baked micro-shadow, no specular, no refraction. `(measured)` |
| Layer stack | back → front: (1) squircle gradient field + top-sheen band; (2) white envelope body + faint detail line; (3) purple V-flap stroke; (4) two sparkle decals. `(measured)` |
| Palette economy | Two hue families read as one continuous pink→violet sweep; purple `#8C57D9` is the single reserved accent (flap stroke + sparkle). Clean, ≤2 families. `(measured)` |

## Signature devices
- **Twin AI sparkles** — the large white + small violet 4-point stars are the whole "this is the AI one" signal. Nameable, but the single most overused AI trope of 2024–25.
- **Pink→violet diagonal ramp** — the committed brand colour, coherent with the cover (the cover's "Insert reply into Mail" CTA and hero wash use the same coral-pink→blue-violet gradient; icon and marketing share one palette).
- **White line-art envelope** — thin purple-stroke flap over a flat white body; the App-Store "mail" convention exactly.

## Failures
- **#10 Variant robustness (Liquid Glass):** flat single-layer PNG with no Icon Composer layer separation. The white envelope and white sparkles read only because of this specific saturated gradient — strip it for dark/clear/tinted (macOS 26) and the composition has no fallback. Cannot generate the system appearance variants.
- **#11 Personality (reads as template):** the composition is the App Store's most generic form — white glyph centred on a saturated gradient squircle — and the one differentiating device (sparkles) is itself the era's AI cliché. Worse for a Mail plug-in: a plain envelope **collides with Apple Mail's own envelope metaphor**, so at Dock/Spotlight size it reads as "Mail" rather than as its own product.

## Soft passes (counted as passes, flagged)
- **#1 Mask discipline:** the squircle is well-formed and continuous-curve and renders cleanly, but it is **baked in / pre-masked** (transparent corners) rather than the macOS-26-required full-bleed unmasked square — risks corner-radius mismatch/double-masking against Tahoe's own squircle.
- **#4 16px squint:** the primary envelope silhouette survives Dock/Spotlight size, but the faint detail line, the flap stroke, and both sparkles smear away — at 16px it collapses to a generic envelope, losing exactly the AI differentiator.
- **#8 Depth coherence:** internally consistent but essentially flat — the envelope floats shadowless with no depth craft beyond the top-sheen band.

## Rhymes with
- iOS App-Store "AI utility" icons: saturated-gradient squircle + white line-glyph + sparkle badge (the AI-writing/AI-email sub-family). Structurally rhymes with **Apple Mail's own envelope** — a resemblance that hurts a Mail-companion app rather than helping it.
- Style family: **iOS-flat gradient-glyph**, "AI sparkle" variant. Not a native Big-Sur-depth or Liquid-Glass-layered icon despite the squircle.

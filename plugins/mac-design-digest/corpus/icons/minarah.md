# Icon: Minarah

- **Era:** Big Sur unified (3D clay-render sub-trend) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 112×114px web thumbnail) · **Category:** Lifestyle · **App:** prayer-time focus/notification app (`minarah.app`)

| Dimension | Reading |
|---|---|
| Background | Cool blue diagonal ramp, light top-left #2193D9 → deep bottom-right #0663C9 (single hue, sky logic) (estimated) |
| Glyph | Object — a front-facing 3D-rendered minaret (tapering tower + domed cap + crescent finial), horizontally optically centred, rooted at and bleeding off the bottom edge |
| Overlay device | None — the object is the whole composition (no diagonal tool, no badge, no frame) |
| Light model | Soft top-left key: baked white specular blob on the upper-left dome, short contact shadows on the right of dome (#013D9B) and right of tower body (#9A5512). One consistent source, no long/dramatic shadow. |
| Layer stack | (back→front) blue gradient field → cream/gold minaret body (balcony ring + arched window) → blue dome cap → gold crescent finial |
| Palette economy | 2 hue families: blue (background + dome) and gold/amber (crescent + tower body). Accent = the gold crescent + gold body against the blue field. Clean two-hue discipline. |

## Signature devices
- **Literal-subject depiction** — the icon *is* a minaret (Minarah = منارة, the tower from which the call to prayer is given). Subject-mined, not a generic glyph-on-gradient: the icon communicates "prayer times" through the architecture itself. `[GOLDEN-NUGGET]`
- **3D clay-render object** — soft plastic/clay Blender-style rendering with rounded bevels and baked lighting, centred on a soft gradient squircle. The dominant Big Sur-era indie "3D object" idiom.
- **Crescent finial as brand accent** — the single warm gold moment, tip of the object and top of the composition, carrying the Islamic iconography.
- **Grounded / bottom-bleed composition** — the tower is rooted at the canvas floor and runs off the bottom edge, giving the object physical weight rather than floating it centred.

## Failures
- **#7 Figure-ground (dome vs. sky):** the blue dome (~#137DD6) sits on a near-identical blue background (#0978D7), contrast ≈1.1:1, far below the 3:1 floor. The dome only separates via its baked white specular and dark shadow rim; in grayscale the dome's upper edge melts into the sky. The gold tower body, by contrast, has strong figure-ground. Partly a small-render over-saturation artifact — the cover shows a steel-blue dome (#579BCD) with cleaner separation.
- **#10 Variant robustness:** a single baked raster keyed to the blue background — no layered light/dark/clear/tinted variants. Expected for a Big Sur-era icon, but a real gap against macOS 26 (Liquid Glass) expectations, and the blue-dome-on-blue-sky composition would collapse further in tinted/clear modes.

## Soft passes
- **#1 Mask discipline:** artwork lives inside the squircle (corners already masked, transparent), but the tower bleeds off the bottom — a deliberate grounded choice rather than a mistake, flagged because it can't be verified against the true 1024 master.
- **#4 16px squint:** the dome+crescent+tapering-tower gestalt survives shrinking and stays nameable, but the balcony arch-railings and arched window already smear at 112px and would vanish entirely at 16px. The object nearly fills the frame, which rescues the read.

## Resolution caveats
- Subject is a **112×114px web thumbnail**, not the 1024 master. All fine detail (balcony arcade, window, crescent edge) is smeared; the 4× upscale is heavily blurred. Hex values are approximate (compressed).
- The mask/rounded corners are **already baked into the PNG** — the true full-bleed master and its safe-zone margins can't be verified.
- **Icon vs. cover coherence is strong** (same 3D asset, same blue+gold+cream identity) but the icon render reads more saturated/contrasty: icon tower = gold #ECBF68 vs. cover tower = cream #EFD3B2; icon dome = saturated #137DD6 vs. cover dome = steel #579BCD. The small render appears pushed in saturation.

## Rhymes with
- The **"3D clay/plastic object on a soft gradient squircle"** family — Blender-rendered single-object indie icons (meditation, lifestyle, and utility apps that centre one glossy rounded object on a blue/warm gradient). Style family: *3D-object-on-gradient, Big Sur clay render.* (Hint only — promote to a cluster once ≥3 independent icons evidence it.)

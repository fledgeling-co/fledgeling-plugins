# Icon: Dropzone

- **Era:** Liquid Glass (macOS 26 / Icon Composer vocabulary) · **Rubric:** 12/12 (4 soft passes, 0 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/dropzone/icon.webp`, a **204×204 WebP web render** — not the 1024 master) · **Category:** Utility · **Developer:** Aptonic
- **Subject the icon must communicate:** a drag-and-drop shelf — you drop files onto a target "zone" to upload / install / transfer them.

| Dimension | Reading |
|---|---|
| Background | **vertical ramp `#847DFF` → `#745FEF`** (lilac-violet top → deeper indigo-violet mid); sky logic (lighter top, deeper bottom). Fills the squircle; corners clean alpha-0 (system mask cutout). `(measured)` |
| Glyph | Two-part stacked assembly, horizontally centred (content centre ≈ canvas centre x102): **(a) stacked translucent glass rings/bands** hovering top-of-tile — frosted open hoops, blue-white specular top rim `#F1F4FF`, cool-blue body `#78A3E0`, violet-tinted lower band `#AF7FE1`, showing the violet field through them; **(b) a glowing target landing pad** below — an emissive radial bullseye (crimson rim `#DB2D5C` → warm cream/peach core `#E9C1AE`) recessed in a dark navy-violet bowl `#55477E`, seated in a metallic silver tray. `(measured)` |
| Overlay device | none crossing the plane — but a two-object **stack-over-target** composition (glass slots above, glowing pad below), staged to read as "files drop through onto the zone". |
| Light model | **Liquid-Glass environmental + emissive.** Top-down specular on the glass band rims (`#F1F4FF` at top) and the tray's bright top rim `#E8ECF8`; the target pad is **self-lit** (internal warm glow) — an intentional focal emitter, not a competing cast direction. Coheres as "lit glass over a glowing recessed zone". No baked drop shadow (system-supplied). |
| Layer stack | system mask+shadow → violet ramp field → metallic silver tray/plinth (bright top rim `#E8ECF8`, silver body `#96A4BD`, shadow lip `#243349`) → dark navy-violet pad bowl `#55477E` → emissive glow target (crimson→peach radial) → stacked translucent glass rings/bands (frontmost, hovering). |
| Palette economy | 1 cool family (violet ramp + blue-tinted glass, adjacent) + **1 reserved warm accent** (crimson→peach) on the focal target + neutral silver tray. Borderline vs. the ≤2-family rule (blue/violet split), but accent saturation is correctly reserved for the "zone". |

## Palette
- **Background ramp:** `#847DFF` (132,125,255) top → `#745FEF` (116,95,239) mid — lilac→indigo-violet `(measured)`
- **Glass band highlight:** `#F1F4FF` / inner `#E9ECFF` — near-white specular rim `(measured)`
- **Glass band body:** `#78A3E0` (120,163,224) cool blue; left rim `#A8C5FF` `(measured)`
- **Lower glass band (violet-tinted):** `#AF7FE1` / `#CB9DF1` `(measured)`
- **Pad bowl (dark recess):** `#55477E` / `#394376` — navy-violet `(measured)`
- **Glow target (radial):** rim `#DB2D5C` (219,45,92) crimson → mid `#D79A9A` → **core `#E9C1AE`** warm cream/peach `(measured)`
- **Metallic tray:** bright rim `#E8ECF8` → silver body `#96A4BD` → `#B6BFCE`; bottom shadow `#243349` `(measured)`

## Signature devices
- **[GOLDEN-NUGGET] Emissive drop-target as focal core.** A crimson→peach glowing bullseye recessed in a dark bowl literally depicts the "zone" you drop onto — and is a **brand-continuity callback to classic Dropzone's red drop-target mark**, re-skinned in Liquid Glass. The one warm accent in an otherwise cool tile; correct de-emphasis.
- **Stacked translucent glass rings/slots.** Frosted open hoops with bright specular top rims, hovering above the pad and refracting the violet field through them — reads as stacked drop-slots / a shelf the files fall through. Crisp multi-layer Icon-Composer glass, not a flat gradient.
- **Metallic silver plinth tray.** A Liquid-Glass base with a bright top-edge rim grounds the whole assembly — gives the icon a physical "device on a desk" weight rather than a floating glyph.
- **Subject-literal drop stack.** Glass slots (top) → glowing zone (bottom) animates the app's verb in a static mark: drop → lands on the target.

## Failures
- None (no hard rubric failure). Four soft passes flagged below.

### Soft passes (flagged, scored as pass)
- **#3 Silhouette — soft.** In grayscale the forms are distinct (stacked rings + oval pad on a tray), but the meaning is not *instantly nameable* — reads as a generic stacked-object-on-a-base (could be plates, a jar, a drum); the "drop-target" concept is carried by colour/glow, which the silhouette discards.
- **#4 16px squint — soft.** Survives as a recognizable coloured tile (violet ground, light glass band up top, warm-red strip at the base), but the two glass rings merge into one band and the stack-over-target narrative smears to "purple tile with a warm glow".
- **#6 Palette economy — soft.** Blue-tinted glass + violet ground read as one cool family, and crimson→peach is the single reserved accent — but a strict count sees violet + blue + red = 3 families. Contained and purposeful, so a flag not a defect.
- **#10 Variant robustness — soft.** Depth/form survive tinted & mono (the glass stack + recessed pad hold on luminance — grayscale confirms), but the colour story ("warm target vs cool glass") collapses in mono/tinted; identity thins from "glowing drop-zone" to "layered glass object".

## Rhymes with
- **Backdrop** (`icons/backdrop.md`) — luminous glass object self-lit on a field; shares the emissive-focal-on-cool-ground logic, but Dropzone is crisper and multi-layer (tray + slots) vs. Backdrop's single atmospheric droplet.
- **Alcove** (`icons/alcove.md`) — recessed luminous glow inside a frame; both stage a lit inner zone, but Alcove is a flat gradient in a bezel while Dropzone is true stacked Liquid-Glass depth.
- Style family (hint): **Liquid-Glass utility marks that stack translucent glass over an emissive focal element on a metallic tray** — drop-target / landing-pad / shelf utilities. If 2+ more "glass-slot-over-glowing-zone" marks appear this seeds a "layered-glass-with-emissive-core" icon cluster.

## Notes (resolution & synthesis)
- **Resolution caveat:** source is a **204×204 WebP web render**, not the 1024 Icon Composer master. Flat/interior hex values and gross composition are reliable; **specular micro-structure, refraction quality, and true per-layer glass separation are inferred, not verifiable** at this scale. The glass "band vs. two stacked rings" count is a soft read — could be 2 discrete hoops or one banded cylinder.
- **Mask:** corners are clean alpha-0 (genuine squircle cutout) and the field fills the tile — unlike floating-glyph utility marks; mask discipline is real here (PASS #1), the strongest structural point.
- **Brand coherence with cover:** the cover shows Dropzone's **older product UI** (a sky-blue menu-bar grid popover; the classic mono down-arrow menu-bar glyph). The new violet Liquid-Glass icon does **not** echo the blue UI directly — the coherence thread is the **red target glow** carrying the legacy Dropzone bullseye identity forward, not the surrounding palette. One app, two eras of mark on display.

# Icon: Letterboxx

- **Era:** custom (contemporary 3D-render / claymorphic soft-object, with a skeuomorphic-quote spirit) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, 256×256 web render (SHA-1 `52a36983`). Category: Productivity. App: Letterboxx — "A dedicated reader for email newsletters" / "A better home for your newsletters" (subscription).
- **Resolution caveat:** only a 256px render was available (transparent-masked squircle, alpha=0 outside), not the 1024 master. The airmail chevron stripes and the envelope flap seam are already softened at 256; the 16px squint below is therefore judged slightly generously — a true master would carry crisper stripes but they smear at Dock size regardless (that is the format's nature, not the render's fault).

| Dimension | Reading |
|---|---|
| Background | **Scene, not a field.** No flat/ramp backplate — a glossy teal-blue container tray *is* the background, filling the squircle. Tray body avg **#479CAF**, rim specular up to **#97EAFF**, shadowed inner/underside down to **#31718C → ~#0B2567** in the deepest occlusion. Interior back wall reads bright cream from the envelope pile |
| Glyph | **Object (multi, single anchor).** A fanned stack of cream airmail envelopes (**#FAF6F2**) with classic red/blue chevron borders; hero top envelope is the focal anchor, optically centred and sitting slightly high in the tray. Airmail red **~#D5463A**, airmail blue **~#274F93**, warm flap seam **~#C9A15E** |
| Overlay device | **Other — physical container tray** (an inbox/basket) acting as both frame and background. Not a diagonal tool, badge, or window frame; the tray *is* the squircle |
| Light model | Soft global illumination, key from upper-front. Broad matte ambient occlusion under the stack and inside the tray; glossy specular highlight along the plastic tray rim; matte paper on the envelopes. No long/dramatic shadows — system supplies the drop shadow |
| Layer stack | (transparent self-masked squircle) → teal tray back wall / interior → fanned pile of plain cream envelopes → mid-stack airmail-bordered envelopes → hero top airmail envelope (focal) → teal tray front lip (occludes the bottom of the pile) |
| Palette economy | Right at the edge: teal container **+** airmail red **+** airmail blue on cream = three chromatic families. Red+blue read as one "airmail" motif, so it *feels* like 2 families, but strictly it is over the ≤2 budget (soft pass) |

## Signature devices
- **Object-as-squircle: the physical inbox tray.** Rather than a glyph-on-gradient, the whole icon is a rendered glossy tray that conforms to the mask and holds the subject. Subject-mined honestly — a newsletter reader is "a home for your mail," and the icon draws that home literally (the app's own tagline is "a better home for your newsletters").
- **Airmail chevron border.** The red/blue diagonal-striped envelope edge is the nostalgia device — it says "letters / correspondence / the romance of mail" in one motif, differentiating a newsletter reader from a generic mail glyph. This is where the icon's personality lives.
- **Fanned document stack.** Multiple envelopes imply volume and accumulation — newsletters piling up in one place, the product's core promise (collect the scattered inbox into one shelf).
- **Claymorphic glossy plastic material.** Soft-body 3D render with rounded chunky forms and specular plastic — the current indie "3D object icon" idiom (Blender/Spline/AI-3D family), not an Apple system era.

## Failures
- **#3 Silhouette test — FAIL.** Filled solid black, the icon collapses to a rounded-square blob with a faint lip — the tray *is* the squircle, so the envelope detail never projects past the container outline. Identity rests entirely on internal colour and material, which silhouette discards. Nothing nameable survives as pure shape.
- **#10 Variant robustness — FAIL.** A fixed full-colour 3D render with a baked teal background and baked lighting — no authored light/dark/clear/tinted Icon Composer layers. In a mono or tinted render the whole scene flattens to a shape blob (see #3); the airmail identity is entirely colour-dependent. Not built to adapt across appearances.

## Soft passes (flagged for synthesis)
- **#1 Mask discipline.** The render is pre-masked to a transparent squircle (self-baked corners) rather than the HIG "square, unmasked, full-bleed layers, system rounds the corners" approach. It conforms to the mask and doesn't fight it, but self-masking is why there are no system variants (feeds #10).
- **#4 16px squint.** Borderline. Downscaled to 16px, the airmail stripes dissolve into pink/blue noise and the stack muddles — but the gestalt "pale card(s) inside a blue container" survives as a recognisable blob. Legible as *a mail/box app*, but the airmail charm (its whole differentiator) is lost at menu-bar/Spotlight size.
- **#6 Palette economy.** Three chromatic families (teal, airmail-red, airmail-blue on cream). Reads as two because red+blue are one airmail motif, but it is strictly over the ≤2-hue budget; accent saturation is *not* reserved to a single focal detail — it repeats across every envelope edge.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | soft pass (self-masked squircle, no system layers) |
| 2 | Grid adherence | pass (stack optically centred, safe-zone margins) |
| 3 | Silhouette | **FAIL** |
| 4 | 16px squint | soft pass (concept survives, airmail identity smears) |
| 5 | Single light model | pass (one coherent GI key + soft AO) |
| 6 | Palette economy | soft pass (3 chromatic families) |
| 7 | Figure-ground contrast | pass (cream #FAF6F2 vs teal #479CAF, >3:1, survives grayscale) |
| 8 | Depth coherence | pass (back wall→stack→top→front lip ordered, no z-fighting) |
| 9 | Era coherence | pass (consistent within its 3D-render idiom) |
| 10 | Variant robustness | **FAIL** |
| 11 | Personality | pass (airmail-stack-in-tray is strongly nameable) |
| 12 | No-text | pass (pure objects, no words/UI/photo) |

**Total: 10/12, 2 failures (#3, #10).**

## Rhymes with (hint only — for icon-cluster synthesis)
- The contemporary **3D-render / claymorphic soft-object** icon family: glossy rounded objects with global-illumination lighting (Blender/Spline/AI-3D lineage), object-as-squircle rather than glyph-on-field.
- **Skeuomorphic-quote "container full of literal objects"** icons — a tray/box/desk/shelf holding real artifacts (the physical-inbox metaphor). Style-family guess: **"3D object-tray, colour-dependent."**
- Palette-family rhyme: **teal/aqua container + red-white-blue airmail** — a mail/correspondence colour story.

## Brand-context note (cover coherence)
The cover ground is a teal→blue gradient that matches the icon's tray hue (**#479CAF**) — strong icon↔app coherence; the same mark appears in the app's own sidebar and as a secondary "framed-envelopes" widget glyph on the cover. The icon reads as a mail/comms app (which is accurate for a newsletter reader) even though the store category is Productivity — the subject communication is honest to function, not to taxonomy. The coherent teal is the brand's spine; the airmail red/blue is reserved entirely to the icon (the app UI is neutral gray/teal), so the icon carries more chromatic weight than any single app surface.

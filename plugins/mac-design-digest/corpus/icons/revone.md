# Icon: Revone

- **Era:** custom (web 3D-render / claymorphism — not a native macOS era) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply · **Subject:** Analytics app, "All your revenue. One place." · icon.png 1024×1024, full-res render (not a resized web thumbnail)

| Dimension | Reading |
|---|---|
| Background | Diagonal indigo ramp #6166FC (top-left) → #4044D5 (bottom-right), core ~#575BEE (measured). Sky-logic roughly holds — lighter high, darker low — but the gradient axis is diagonal, not vertical |
| Glyph | Abstract data symbol: three ascending white 3D bars (cool white, highlight #FAFDFE / core #E7EAF6) + a rising ribbon arrow. Optically centred, bar cluster sits lower-centre and nearly touches the bottom safe-zone |
| Overlay device | Diagonal ribbon growth-arrow (lavender #B2ADFE, tip highlight #CBC9FE) crossing/rising above the bars to the upper-right — the icon's one accent element |
| Light model | Soft studio-3D: key light upper-left, short soft baked contact shadows under each form, glossy specular highlights on bar tops and the arrow ridge. Omnidirectional Blender-style fill, all baked into the raster |
| Layer stack | Indigo diagonal-ramp field → baked contact shadows → three white inflated 3D bars → lavender 3D ribbon arrow (front) |
| Palette economy | One hue family (indigo/blue-violet) carries background + arrow; bars are near-white neutral. Accent (lavender arrow) reserved for the focal "growth" element. Textbook economy — the whole icon is essentially monochrome indigo + white |

## Signature devices
- **Inflated / clay 3D bars** — puffy extruded columns with rounded corners and glossy tops; the stock "3D icon pack" idiom rather than a committed original device
- **Lavender 3D ribbon growth-arrow** — a tube-like zigzag arrow rising to the upper-right, the literal "revenue up" metaphor stated twice (bars ascend + arrow rises)
- **Monochromatic indigo field with near-white subject** — genuine tonal restraint; the accent is a single hue-shifted (lavender) element, not a second colour

## Failures
- **#1 Mask discipline** — the squircle is baked into the PNG: corners are transparent (alpha 0), art corner-radius ~100px on the 1024 canvas (~10%) undercuts Apple's continuous squircle. macOS masks a pre-rounded shape, so the corners double-round / the field won't reach the true mask edge. Should ship a full-bleed square and let the system round.
- **#10 Variant robustness** — a single baked raster, not layered Icon Composer art. Background and arrow share the indigo hue, so a tinted / clear / mono render collapses the arrow into the field and the white bars lose their ground. Cannot survive dark/tinted appearances gracefully.

## Soft passes (flagged)
- **#2 Grid** — optically centred, but the bar cluster nearly touches the bottom safe-zone margin; composition is bottom-heavy.
- **#4 16px squint** — the three white bars survive Dock/Spotlight size, but the lavender arrow (~1.8:1 on the indigo field) smears into the background and the "growth" reading is carried by the bars alone.
- **#7 Figure-ground** — white bars sit >4:1 on indigo and anchor the silhouette; the lavender arrow is the weak link at ~1.8:1.
- **#11 Personality** — there is a distinctive-ish 3D ribbon arrow, but the whole idiom is template-default 3D stock aesthetic, not a committed macOS-native signature.

## Rhymes with
- Web 3D-render / claymorphism stock-icon family (Iconscout / Icons8-style 3D fintech & analytics icons): puffy inflated objects on a vivid single-hue gradient, glossy studio lighting, baked shadows. NOT native Big Sur unified (no top-down flat plane + tool overlay) and NOT Liquid Glass (no layer specular/refraction system). First non-native icon in the corpus — a useful negative exemplar for what "reads as web stock, not Mac-native."
- Palette-coherent with its own app: the dark marketing cover (#171717 ground) uses the identical indigo #6166FB as its brand accent, so the icon is that accent saturated into a full field. Brand coherence is strong even though the icon is bright and the app UI is dark.

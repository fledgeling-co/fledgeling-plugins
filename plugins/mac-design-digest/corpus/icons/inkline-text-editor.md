# Icon: Inkline Text Editor

- **Slug:** inkline-text-editor · **Category:** Dev · **Source:** macapp.supply (icon.png, SHA-1 `4377d7a5`)
- **Era:** Liquid Glass (macOS 26+) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Resolution honesty:** 512×512 `(measured)` — half the 1024 master, a resized web render. Corners are fully transparent (alpha 0): the squircle is **pre-masked into this export**, so the raw full-bleed Icon Composer layers can't be inspected. Glass effects (edge specular, glow bloom, emissive ribbons) are **baked into the flat PNG** — I can't confirm whether they are system-composited or hand-baked, which matters for variant robustness (see Failures). Palette hex are reliable: clean PNG, no visible compression banding.

| Dimension | Reading |
|---|---|
| Background | Dark **glass ramp**, indigo → near-black. Lightest at the top edges `#271F44` (measured), coolest-dark at centre `#0B0D22`, blackest at bottom-centre `#030512`. Radial-ish bloom, not a flat sky ramp — the field is a nocturnal glass panel, not the Big-Sur white square. |
| Glyph | **Abstract two-stroke mark.** (1) A vertical white→lavender capsule bar, `#FAFAFC` top → `#DBDCF0` foot — reads as a text **insertion caret**. (2) A diagonal (~20° tilt) capsule slash with a top-to-bottom hue ramp `#D37DFB` (magenta-violet) → `#794FFB` (violet) → `#406AF9` (blue) — an **inked line stroke**. Together: caret + ink-line = a literal "Ink · line" rebus. Optically the pair balances around centre; individually the caret sits left-of-centre and the slash crosses it. |
| Overlay device | none — no badge/frame/tool laid over the glyph. The diagonal is one of the two primary strokes, not an overlay. |
| Light model | **Emissive glass in the dark**, single coherent model: a lit top edge (`#2F274C`) and a violet right rim specular (`#5D3C9B`), a self-illuminating diagonal stroke whose glow **blooms onto the background**, and emissive aurora ribbons at the base. No competing sun direction. |
| Layer stack | 1) dark indigo→black glass field (radial ramp) · 2) emissive aurora ribbons + sparkle dust, bottom third · 3) white→lavender vertical caret bar · 4) purple→blue diagonal slash with background glow bloom · 5) glass edge specular (lit top, violet right rim) — composited front. |
| Palette economy | **2 hue families** — indigo/violet-blue (ground + slash + waves) and neutral white (caret). Accent saturation reserved for the focal diagonal. Within the ≤2-family rule. |

## Signature devices

- **Caret + ink-stroke pairing** `[GOLDEN-NUGGET]` — a calm, fully-vertical white bar (the text caret) beside an energetic tilted glowing slash (the inked line). It rebuses the name "Inkline" and quietly states the subject (a text editor) without a document/pen cliché. The tension between the two strokes — one static and neutral, one kinetic and saturated — is the whole personality.
- **Emissive gradient stroke that lights its own field** — the purple→blue slash bleeds a violet bloom into the near-black ground; the glyph is a light source, not a painted shape. This is the current-era move (glass + self-luminance) done deliberately.
- **Aurora ribbons + sparkle dust at the base** — thin cyan/violet light streaks and pin-point sparkles ground the mark in a scene without a literal object; reads as refraction under the glass.
- **Nocturnal glass field** — near-black indigo ground inverts the Big-Sur white-field default; the icon's mood is spent entirely on the dark.

## Failures

- **#10 Variant robustness (Liquid Glass)** — the entire read depends on the dark ground: the white caret needs black to pop, and the diagonal's glow/bloom is a dark-mode effect. In a clear/light or tinted render the baked glow and the white-on-black caret would lose their punch, and the shape alone would carry a much flatter icon. Because effects are baked into this flat PNG (not verifiably layer-separated), light/clear/tinted behaviour is **undemonstrated and looks fragile**. This is the one genuinely weak dimension.

## Soft passes (flagged, scored as pass)

- **#2 Grid** — the pair balances around optical centre, but the composition is slightly bottom-weighted (the aurora ribbons pull mass down) and neither stroke is individually centred. Reads balanced as a unit.
- **#3 Silhouette** — clean and distinctive filled-black (two rounded strokes, vertical + diagonal), but **abstract**: not instantly nameable as a concrete subject at a glance. The "text editor" reading only unlocks once you see the caret and know the name. Distinctive enough to pass; not self-evident.

## Rhymes with

- The **dark-glass dev-tool / AI-app** icon family: near-black or deep-indigo ground + a single electric purple→blue emissive accent stroke, glass edge specular, no white field. Style-family cousins are current-era terminal/AI/editor icons that spend their whole budget on one glowing mark against the dark (Warp-ish, Raycast-dark, Linear-mark energy). First of its kind in this corpus — record as a candidate "nocturnal-glass electric-accent" icon cluster; needs ≥2 more members before any canon promotion.
- **Brand coherence (cover):** the cover art reuses the icon's exact indigo→black ground, the same purple→blue accent, the "V/"-style mark, and the aurora base-line — palette and motif carry cleanly from icon to marketing. Strong, deliberate identity system, not a one-off icon.

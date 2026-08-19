# Icon: Codeshot

- **Era:** big-sur (unified squircle object icon, mild skeuomorphic gloss quotation) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, **1024×1024 master** (SHA-1 `b908e8af`), converted via `sips -s format png`. Category: Dev. App: "Turn your code into a snapshot" — a code-to-image screenshot tool (Carbon/CodeSnap class; 80+ themes, 180+ languages per cover).
- **Resolution:** full 1024 master, transparent background (alpha 0 outside the shape). All readings `(measured)` from the master unless noted. Opaque bbox **x100–922, y100–932** (~822×~815 body) with a soft baked drop-shadow falloff at y≈915–940.

| Dimension | Reading |
|---|---|
| Background | Charcoal vertical ramp **#363636 (top) → #2F2F2F (mid) → #0E0E0E (bottom)** — top-lit "sky logic" body. Delivered as a **pre-masked squircle with a baked drop shadow**, not a full-bleed square |
| Glyph | **Object — a camera lens**, optically centred (cx≈512, cy≈600, sitting low-of-centre to balance the top titlebar band). Concentric barrels **#373737** outer → **#0F0F0F** aperture; upper glass carries a soft grey specular oval **≈#6B6B6B**; a bright central sensor dot **#E0E0E0** |
| Overlay device | **Other — window-chrome triad + titlebar seam.** Three glossy traffic-light spheres (upper-left band) over a faint horizontal seam that bisects a recessed "titlebar" from the camera body. The body is simultaneously a camera and a macOS window |
| Light model | Single soft **top-down**. Speculars top-left on each sphere; grey reflection on the upper lens glass; body ramp light-top→dark-bottom; short baked micro-shadows in the sphere sockets and lens barrels. Consistent throughout. (The baked drop shadow under the squircle is a Big-Sur delivery habit, not a lighting conflict) |
| Layer stack | (transparent field) → **baked squircle body + baked drop shadow** (charcoal ramp) → recessed titlebar band (seam) → three glossy candy spheres in sockets (R/Y/G) → lens outer barrel → inner barrel / deep-black aperture → glass element + grey specular oval → central white sensor dot |
| Palette economy | **One** hue family (monochrome charcoal ramp) + a single reserved accent *moment*: the RGB traffic-light triad. Three hues, but one semantic unit. Accent saturation lives only in the three dots; the entire subject is tone-on-tone |

## Signature devices
- **[GOLDEN-NUGGET] Camera-lens-as-window dual metaphor.** The body reads as a camera *and* a macOS window at once: a real lens dead-centre, the traffic-light triad + titlebar seam wrapping it. It literally spells the product — "a *snapshot* of your *code window*." Honest subject-mining: every snapshot Codeshot outputs carries macOS window chrome (visible on the cover's dark code card), so the icon quotes its own output artifact.
- **Traffic-light triad as brand accent.** The only saturated colour in an all-charcoal icon is the three window-control dots — a disciplined single accent moment carrying all of the icon's chroma. Note the dots are **brighter/candier than macOS system swatches**: red **#FF6460** (softer/pinker than system #FF383C), yellow **#FFC31F** (≈ system), green **#00E71A** (far more saturated than system #34C759) — a quotation of the idea, not a colour-match.
- **Dimensional skeuomorphic gloss.** Candy-sphere buttons with top-left speculars and a multi-barrel lens with a glass reflection give real, ordered depth — a mild skeuomorphic quotation inside an otherwise Big-Sur composition.

## Failures
- **#10 Variant robustness — FAIL.** A fixed dark raster with a **baked drop shadow**, not layered Icon Composer artwork. Identity depends on the dark body carrying the saturated triad; under macOS 26+ tinted/clear modes that dependency collapses (tint the body and the whole tone-on-tone lens vanishes, leaving only three dots). The baked shadow would also double against the system's own shadow/effects. This is the one honest era-lag defect: a lovely Big-Sur-era icon not re-authored for Liquid Glass.

## Soft passes (flagged for synthesis)
- **#3 Silhouette test.** Filled solid black the icon is just a rounded square — the camera is defined by internal tonal modelling, not cutout shape, so the subject isn't nameable from the outer silhouette alone. Carries because the internal concentric-lens motif is strong at working size, but strictly a borderline.
- **#4 16px squint.** Verified by downscale: at 16px the **charcoal-on-charcoal lens smears into a dark blob** and the three traffic-light dots (fused into a colour bar) become the sole identity anchor — reads as "dark window app," camera barely survives. The lens snaps back to legible only at **≥32px**. The triad saves the icon at menu-bar size; the primary subject does not.
- **#7 Figure-ground contrast.** The lens barrel (**#37**) against the body (**#2F–#36**) is well **under 3:1** — deliberate tone-on-tone modelling. Only the traffic lights clear 3:1. Same root cause as #4: the subject is rendered, not contrasted, so it survives grayscale weakly.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | pass (corners match squircle; but bakes own shadow — see #10) |
| 2 | Grid adherence | pass (lens optically centred, ~100px margins, triad in safe band) |
| 3 | Silhouette | soft pass (subject is internal tone, not cutout) |
| 4 | 16px squint | soft pass (lens smears; triad carries identity) |
| 5 | Single light model | pass (consistent soft top-down) |
| 6 | Palette economy | pass (charcoal ramp + one triad accent moment) |
| 7 | Figure-ground contrast | soft pass (lens sub-3:1, tone-on-tone) |
| 8 | Depth coherence | pass (ordered layers, shadows track the light) |
| 9 | Era coherence | pass (Big-Sur unified, coherent skeuomorphic gloss) |
| 10 | Variant robustness | **FAIL** |
| 11 | Personality | pass (dual camera/window metaphor — strong) |
| 12 | No-text | pass |

**Total: 11/12, 1 failure (#10).**

## Rhymes with (hint only — for icon-cluster synthesis)
- **Dark-neutral Big-Sur object icons** where a photoreal object (lens, device) is rendered dimensionally on a charcoal squircle with a single saturated micro-accent — capture/screenshot-tool family (CleanShot-X-adjacent), dark developer utilities.
- **Framed-window / macOS-chrome quotation** icons that bake the traffic-light triad in as a brand signal (icon-anatomy's "framed-window motif") — here fused with a camera rather than a browser/editor frame.
- Style-family guess: **"nocturnal skeuomorphic object icon, charcoal body + traffic-light accent."** Palette-family rhyme: near-monochrome charcoal ramps that reserve all chroma for one small focal cluster.

## Brand-context note (cover coherence)
Cover marketing uses a vibrant orange/red→blue→magenta gradient stage, but the **product's actual artifact** — the dark code card ("`// Created by Codeshot.`") — carries its own traffic-light window chrome. The icon's charcoal body + traffic-light triad matches that output card, **not** the marketing gradient. That's the honest choice: the icon communicates what the app *produces* (dark, window-chromed code snapshots), so palette coherence runs icon↔output rather than icon↔hero-gradient.

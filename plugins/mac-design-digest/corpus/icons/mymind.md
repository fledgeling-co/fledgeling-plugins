# Icon: mymind

- **Era:** custom (photoreal 3D-render / brand-mascot object) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.webp`, **102×102 web render** (SHA-1 `608e903d`). Category: Productivity. App: "A private place to save your notes, images, quotes and highlights" — a save-everything / auto-organizing memory tool ("Remember everything. Organize nothing.").
- **Resolution caveat:** only a **102px** WebP was available, not the 1024 master — the smallest render in the corpus so far. The flocked/velvet surface texture, edge crispness, and any baked micro-shadow are **below the resolution floor**; palette hexes are sampled from this compressed render and are indicative (±), the texture read is `(estimated)`, not `(measured)`. The square white field bleeds edge-to-edge with no baked mask (the system squircle will apply cleanly).

| Dimension | Reading |
|---|---|
| Background | **Flat pure white #FFFFFF → #FEFEFE**, with a faint warm-gray contact shadow (~#D6D6D6) pooled directly under the figure. No ramp, no scene — the figure floats on paper-white. |
| Glyph | **Mascot / rendered art-object**: a single matte-orange sculptural figure, hunched forward, head bowed — reads as a small seated "thinking" creature (Rodin's-Thinker posture in blobby form). Optically centred, sitting a hair low; compact with even safe-zone margin. |
| Overlay device | **None** — no tool, badge, or frame. The object *is* the whole composition. |
| Light model | Single soft **top-front key**, warm. Diffuse rim highlight on the crown/shoulders (#FC5D2E, up to #F0C49D on the fuzzed edge); ambient-occlusion shadow baked into crevices and underside (down to #AA1306). Matte flocked surface — no hard specular. Subtle contact shadow grounds it; system supplies the drop shadow. |
| Layer stack | (system squircle mask + system shadow) → white ground field → soft contact-shadow ellipse → the orange 3D figure (baked form-shading + flocked texture). Three planes, no tool overlay. |
| Palette economy | **One hue family**: a single orange→red-orange ramp (highlight #FC5D2E → core #F15E20/#CF3611 → occlusion #BD240F/#AA1306) on neutral white. No separate reserved accent — the figure's orange *is* the identity. Passes ≤2-hue economy cleanly. |

## Signature devices
- **The flocked orange creature.** A matte, velvet/coral-textured 3D-rendered figure — not a glyph, not a gradient, a *rendered object with a surface you can almost feel*. This is committed direction, not template-default: the tactility is the entire brand gesture, and it's the rarest device in the corpus so far.
- **Subject↔product literalism, done softly.** The object is a little hunched figure — a *mind* at rest / thinking. "mymind" gets a mind; the pose reads as contemplation, which is exactly the app's job (a calm private place your thoughts land). Subject-mining is honest here without being a pun.
- **Paper-white float.** Pure #FFFFFF ground, no ramp, no squircle-background field — the icon trusts a single saturated object on white to carry the Dock. Deliberately anti-Big-Sur (no sky-logic gradient, no diagonal tool crossing the plane).

## Failures
- **#10 Variant robustness — FAIL.** Not authored as Icon Composer light/dark/clear/tinted layers. Identity leans on the white ground (the figure's pop is orange-on-white); a **mono/tinted** render of a flocked, form-shaded 3D object collapses — the texture and single-hue modelling carry no flat silhouette to fall back on. On a dark ground the orange would survive, but the composition wasn't built for the macOS 26 variant set.

## Soft passes (flagged for synthesis)
- **#2 Grid adherence.** Optically centred and inside the safe zone, but precise grid placement is unverifiable at 102px; the figure sits marginally low.
- **#3 Silhouette test.** Filled solid black it reads as an organic hunched-figure lump — nameable as "a little creature / seated figure" but **deliberately abstract**, not a crisp universal metaphor. Passes as a figure; the *specific* identity lives in the texture and colour, which silhouette discards.
- **#4 16px squint.** Smears to an orange organic blob on white — figure detail is lost, but the high orange-on-white contrast keeps a distinct, recognizable brand-colour mark. Survives as a colour/shape marker, not as a legible figure.
- **#12 No-text check.** No words, no UI — but it's a **photoreal CGI render**, which sits against HIG's "prefer vector/illustration to photos, clearly-defined edges." Not a literal photo, so it passes; the rendered-realism is the caveat.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | pass (white field bleeds to edge, no baked radius) |
| 2 | Grid adherence | soft pass (centred; unverifiable at 102px, sits low) |
| 3 | Silhouette | soft pass (nameable figure, but abstract) |
| 4 | 16px squint | soft pass (smears to orange blob, brand-colour survives) |
| 5 | Single light model | pass (one soft top-front key) |
| 6 | Palette economy | pass (one orange ramp + white) |
| 7 | Figure-ground contrast | pass (orange on #FFF, >3:1, survives grayscale) |
| 8 | Depth coherence | pass (coherent form-shadow + contact shadow) |
| 9 | Era coherence | pass (consistent custom render language) |
| 10 | Variant robustness | **FAIL** |
| 11 | Personality | pass (strong — the flocked creature) |
| 12 | No-text | soft pass (no text; photoreal render caveat) |

**Total: 11/12, 1 failure (#10), 4 soft passes.**

## Rhymes with (hint only — for icon-cluster synthesis)
- **Rendered-3D-object icons** — the clay/blob/soft-render trend (matte materials, single saturated hue, plain ground). Distant cousin of classic skeuomorphic object icons, but modern: flat white ground instead of textured scene.
- **Brand-mascot / character icons** — where the app's face is a creature rather than a tool-glyph. Style-family guess: **"tactile mascot-object on white."** Palette-family rhyme: warm single-hue orange/coral ramps.

## Brand-context note (cover coherence)
Cover (`cover.jpg`, 1024×538) is a warm **coral→orange→pink→lilac radial aura** haloing a white disc, with black serif display type ("Remember everything. Organize nothing.") and — telling — a **tiny line-drawn version of the same egg-headed figure** at the footer. So the brand runs the identical mark two ways: a **flocked orange 3D object** for the app icon and a **minimal line glyph** in marketing, both the same little figure. The icon's orange + paper-white is fully coherent with the cover's warm palette. The line-glyph footer is also the honest workaround for the #10 mono weakness — the brand already owns a flat silhouette version, it just isn't the shipped icon.

## Round 15 (`loop-runs/r14`) — the small-size repair round: the roll's interior was
modelled as pure occlusion, and a cavity lined with its own white material does not go dark

Edit class: small-size repair. Two constants added to the shaving's shading, one line
changed in each of its two branches. No geometry, no path, no filter, no gradient, no
light constant, no ground constant. Structure **1042 paths / 231,249 bytes, both
unchanged to the byte**, gradients 12, filters 12, PASS — a colour-only round costs
nothing in the envelope.

**What was measured, before authoring anything.** First the cost of the feature, by
control render: the same tree built with `SHAVING=0`, scored at all five sizes.

| | 1024 | 256 | 128 | 32 | 16 |
|---|---:|---:|---:|---:|---:|
| composite, curl **removed**, vs the r13 master | +0.0063 | +0.0084 | +0.0183 | **+0.0141** | −0.0090 |

The shaving as drawn was worth less than nothing at four of the five sizes. At 32 the
mechanism is visible in the edge map: inside the curl's own box the master threw **48**
cells over the sobel threshold against C2's **22**, and C2's are almost all its block's
silhouette entering the corner — its ribbon itself runs |grad| 0.03–0.13, essentially
edgeless at that size. Ours was throwing ~26 edges the reference does not have, from one
0.28 internal step, and at 32px that averages into a dirty smudge rather than a shaving.

**Where the step actually came from, which is not where I first put it.** The two shading
branches were painted apart — `OUT_*` to red, `IN_*` to blue, `TRANSMIT` to green — and
the render mapped (`work3/m7.py`). Every pixel below L 0.45 in the curl sits on the
**inner** branch: the open mouth of the roll on its lower left, driven to `IN_DARK` by
`ao = 1 - 0.74 * depth`. The bright arc and the whole body that reads as "the bowl" are
in fact the OUTER face. I had already authored a transmission term on the outer branch
from the crop alone, and the sweep showed it moving p5/p10 not at all — it was landing on
a branch that owned none of the dark pixels. Ten minutes of painting would have preceded
it.

**What the reference says about that interior**, measured in a block-free box over each
image's own mouth, at 1024:

| | p2 | p5 | p25 | min | darkest 5% RGB | sat |
|---|---:|---:|---:|---:|---|---:|
| round-14 master | 0.324 | 0.340 | 0.456 | 0.310 | (93, 82, 70) | 24.5% |
| **r14** | **0.580** | **0.584** | **0.612** | **0.520** | (162, 146, 127) | 21.6% |
| C2 | 0.607 | 0.621 | 0.669 | 0.516 | (169, 152, 137) | 19.2% |

C2's interior never approaches black: its darkest interior pixel is 0.516 against ground
0.70–0.75 beside it, and it holds 19% saturation there. Ours bottomed at 0.310.

**What changed, and the physics of it.** `ao` is a pure-occlusion model. It is right about
the direct term — the mouth of the roll is genuinely shadowed — and it has no bounce term
at all, which for this cavity is the larger half of the answer: the roll is lined with its
own near-white material and stands on porcelain, so what fills its floor is
interreflection off its own far wall. `CURL_BOUNCE = 2.20` scales `IN_DARK` into `IN_DEEP`
and the lerp's dark endpoint becomes that. A pure scale, so the interior floor keeps the
material's chromaticity exactly — a shadow that desaturates reads opaque, and this one is
lit by wood, which is why the darkest 5% stays at 21.6% saturation rather than going grey.
Second, `CURL_TRANSMIT = 0.38` gives the outer branch the transmitted term it never had:
the geometry that takes the reflected light away is the same geometry that puts the source
square on the material's back, and the ribbon is a tenth of a millimetre thick. Measured
separately at bounce 2.20, transmission owns p5 0.418 → 0.469 and p10 0.438 → 0.492;
bounce owns p25 0.454 → 0.590.

Both constants were calibrated against C2's percentiles and against one guard, never
against the composite: **the curl must keep the 16px edge cells that make `edge_f1`
1.0000 there.** The sweep is in `work3/cal2.py`. Bounce 2.60 lands p25 on 0.624 against
C2's 0.647 and takes 32px edges to 24 against C2's 22 — the best material match on the
table — and it drops the 16px curl cells from 12 to 10. 2.20 holds all 12 and was taken
instead. That is the rubric's 16px read outranking the closer convergence, and it is the
one place this round declined to follow the reference.

| size | r13 (baseline) | **r14** | delta | ssim | edge_f1 | lum_delta |
|---:|---:|---:|---:|---|---|---|
| 1024 | 0.4538 | **0.4580** | +0.0042 | 0.6304 → 0.6327 | 0.1269 → 0.1252 | 0.1286 → 0.1260 |
| 256 | 0.4732 | **0.4786** | +0.0054 | 0.5872 → 0.5936 | 0.2532 → 0.2511 | 0.1250 → 0.1226 |
| 128 | 0.5175 | **0.5271** | +0.0096 | 0.5667 → 0.5777 | 0.4506 → 0.4589 | 0.1227 → 0.1205 |
| 32 | 0.7871 | **0.7999** | +0.0128 | 0.6115 → 0.6294 | 0.8961 → 0.9165 | 0.1194 → 0.1174 |
| 16 | 0.8371 | **0.8419** | +0.0048 | 0.6416 → 0.6558 | 1.0000 → 1.0000 | 0.1157 → 0.1136 |

Pareto gate **ACCEPT**, net +0.0368, no size negative. The 32px `edge_f1` of 0.9165 is
**above** the 0.9147 the control render reached by deleting the shaving outright: the curl
now costs less at 32 than not drawing it at all, which is the whole point of the round.
`self_contrast` is unchanged to four decimals at every size — 0.6109 at 32 and 0.5969 at
16, against floors of 0.5742 and 0.5611 — because p90 and p10 both live outside the curl,
so the contrast budget was never in play. `mask_iou` is untouched; the silhouette did not
move.

**The cost, and it is a real one.** The curl's mean has crossed its ground. Against the
un-planed ground immediately beside it: separation +0.0466 → **−0.0058** at 16px, +0.0316
→ −0.0134 at 32, ratio 1.072 → 0.992. On a mean-level figure-ground test the shaving now
scores 1.00:1 and would read as absent. It is not absent — it reads by structure, a 0.86–0.91
outer arc over a 0.58–0.61 mouth against a 0.75 ground, and the 16px edge cells are intact
at 12 against C2's 14 — but it now has **no mean-level margin at all**. C2's ribbon is
built the same way and survives on a textured ground with harder rims than ours. The
warning for the next round that touches this feature: soften the curl's rims or narrow its
internal range any further and the shaving disappears at small size, and no metric on this
harness will say so. `lum_delta` improving at 16 is not evidence against that; it is the
same fact seen from the reference's side.

Polarity reads **+0.149** by `measure.py icon.png 33.0 543 604 640`, from +0.145. The
trued side is bit-identical at 0.852; the un-planed mean moves 0.707 → 0.703 purely
because the lifted interior pixels now clear `measure.py`'s own L > 0.50 ground gate and
join that pool. Nothing about either ground changed. Block figure-ground is bit-identical
at 16/32/128 — this edit touched the curl and nothing else.

**Reusable construction — "an ambient-occlusion term needs a bounce term beside it
whenever the cavity is lined with the object's own bright material."** Occlusion may darken
toward the interreflected level, never to the material's unlit colour; a white bowl has no
black inside it. Author the floor as a **scale of the material's existing dark colour**
rather than a newly picked one, so the shadow keeps its chromaticity to the digit and only
its level moves — that is the cheapest possible way to satisfy the darkest-pixel-hue check,
and it makes the constant a single readable number ("the cavity returns 2.2× its own
dark"). The diagnostic that goes with it, and that this round paid to learn: **before
theorising about which shading term is wrong, paint the branches.** Rebuild with each
branch's palette forced to a primary, render, and map which branch owns the pixels you are
trying to fix. It is one regex and one render, and here it would have prevented an edit
authored against the wrong branch from a crop that looked conclusive. Cost: about 200
lines of numpy, `loop-runs/r14/work3/`.


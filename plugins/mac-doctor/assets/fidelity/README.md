# fidelity run — mac-doctor master vs take C

Reference: `../icon-engineC-clean.png` (Engine C, deframed and remasked).
Harness: create-mac-icon `scripts/fidelity.py` (metric v2, numpy tier — no
torch/lpips on this machine, so no LPIPS term) and `scripts/judge_panel.py`.

| round | edit class | verdict |
|---|---|---|
| r00 | baseline — the previously shipped master | — |
| r01 | material — the gel-torus rebuild, one `band()` for both arcs | gate REJECT (1024 SSIM only), blind panel WIN on overall + material |
| r02 | detail — figure-ground back over 3:1, ember section flattened, tighter specular | gate ACCEPT vs r01 |
| r03 | round 7 — brighter ember ramp, 13° clearance a side, 10% protrusion, specular floored at ≤64px | gate ACCEPT vs r02 (every size improved), blind panel WIN on overall + material + small size |

`measure_material.py` is the sampler used for the material numbers quoted in
`../icon-notes.md` and `../audit.html`: ring/ember luminance percentiles,
darkest-pixel hue and saturation, and figure-ground against the ground plane.
Run it from the assets directory.

Round 7 added three sweepers in `runs/r03/`, all run from the assets directory:

- `sweep_ember.py` — the ember ramp's hue and value, plus the two masks and
  the percentile sampler every ember number in the notes comes from.
- `sweep_ember2.py` / `sweep_ember3.py` — the refinements. The second is kept
  deliberately even though its result was discarded: it is the run that scored
  a clipped, collapsed ramp best of anything tried, and its docstring records
  why the metric paid for that.
- `sweep_geometry.py` — `gap` and `protrude` contact sheets, with the rendered
  inner/outer radii per variant so the inner-boundary invariant is checked on
  pixels rather than asserted from the constants.

`runs/r03/sweep/` holds every variant render. `runs/r03/baseline-r02.svg` is
the round-6 master, kept as this round's immutable before — the audit sheet's
A₁ row renders from it.

Kept per the skill's trajectory-data rule; do not clean this up.

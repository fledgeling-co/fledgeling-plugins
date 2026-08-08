# Should the 12V-2x6 melting report use three.js?

**Short answer: no — not for the explanatory core.** Build the page in SVG plus a small
JavaScript state model. Reserve three.js for at most one optional hero scene, and only if
it clears the gate in §5. The reasoning below is about *this* mechanism specifically, not a
general dislike of WebGL.

---

## 1. The test that decides it

Before choosing a medium, ask: **does the reader have to change viewpoint to get the
answer, or does the answer live on a plane?**

Three.js earns its cost when the thing being explained is only legible from more than one
angle — occlusion that matters, depth ordering that matters, a shape whose behaviour you
cannot infer from any single projection. That is the gate. Interactivity alone does not
clear it; a slider is not a reason for WebGL.

Run the 12V-2x6 mechanism through it.

## 2. What the mechanism actually is, dimensionally

The connector is twelve terminals in two rows of six (six 12V, six ground), plus four
sideband pins. The six 12V terminals are **parallel branches of one circuit**. They lie on
a plane. Current divides between them by conductance:

```
I_i = I_total · (1/R_i) / Σ(1/R_j)
```

where `R_i` is dominated not by the wire but by **contact resistance at the terminal** —
which is a function of insertion depth, normal force, plating condition, and oxide. Seating
changes `R_i`. Changed `R_i` redistributes current. Concentrated current dissipates
`P_i = I_i² · R_i` in one terminal, heat degrades that contact (oxidation, plating wear,
plastic creep that further reduces contact force), which raises `R_i` again. That is the
runaway.

So the full state of the story is:

- **six scalars** (current per pin), on
- **a planar pin layout**, driven by
- **two or three seating parameters** (insertion depth, tilt, and optionally per-pin wear),
  evolving over
- **one time axis** (the degradation feedback loop).

The third spatial dimension carries approximately none of that. The connector is a nearly
planar object extruded along the insertion axis, and the insertion axis is fully expressed
by a side cutaway. Every quantity the argument depends on is a **number attached to a pin
position**, and pin positions are 2D.

**Worse, 3D actively fights the argument in three ways:**

1. **Occlusion.** The entire point is that the failure happens *inside the housing where
   you cannot see it*. A realistic 3D render reproduces exactly the opacity that makes the
   problem invisible in real life. You would immediately have to cut the housing away —
   at which point you have drawn a cross-section, in 3D, at 20× the cost of drawing one in
   SVG.
2. **Perspective breaks quantitative comparison.** The reader's job is to compare six
   values. Under perspective, the near pin is larger and its colour patch reads as more
   significant than the far pin carrying identical current. You would be introducing a
   readout error into a chart whose whole purpose is "these six are unequal."
3. **It reads as spectacle.** A glowing pin in a 3D render says *danger*. The report needs
   to say *23 A through a terminal specified for roughly 9.5 A* — a number against a
   threshold. Glow is not a magnitude; it is an adjective. (Use the report's own sourced
   figures here; the 600 W ÷ 12 V = 50 A total, ≈8.3 A nominal per pin arithmetic is the
   shape of the argument, and the per-terminal rating should be cited, not assumed.)

## 3. The page's actual visual jobs, and the right medium for each

| # | Job | Right medium | Why not 3D |
|---|---|---|---|
| A | Which pin is which — identity and position | Face-on SVG pin map, 2×6 grid | The layout *is* 2D; a 3D render of a flat grid is a flat grid with extra steps |
| B | Current per pin under a given seating state | SVG bar chart + colour on the pin map, linked | Quantitative comparison; needs axes and numbers |
| C | Seating depth/tilt → contact resistance | SVG side **cutaway** with an insertion slider | Cutaway beats render: you must see through the housing |
| D | The runaway feedback loop | Cycle diagram, plus small-multiples or a line chart over time | Dynamics, not geometry |
| E | Why the card can't detect it (bulk shunt, no per-pin sensing) | Circuit schematic | Topology, not space |

Five jobs. Zero require a camera.

## 4. Build this instead

One shared state object, several SVG views bound to it. This is the whole architecture:

```js
// state
const state = {
  seatDepth: 1.0,    // 0 = unseated, 1 = fully latched
  tilt: 0.0,         // -1..1, rocked toward row A or row B
  wear: [0,0,0,0,0,0],
  totalCurrent: 50   // A
};

// contact resistance model, per pin — tune constants to the report's sources
function pinResistance(i, s) {
  const rowBias = (i < 3 ? -1 : 1) * s.tilt;          // tilt lifts one side
  const engagement = clamp(s.seatDepth + 0.15 * rowBias, 0, 1);
  const base = 0.002;                                  // ohms, fully seated
  return base * (1 + 8 * Math.pow(1 - engagement, 2)) * (1 + s.wear[i]);
}

// exact current division — no solver needed
function currents(s) {
  const g = [...Array(6)].map((_, i) => 1 / pinResistance(i, s));
  const gSum = g.reduce((a, b) => a + b, 0);
  return g.map(gi => s.totalCurrent * gi / gSum);
}

// dissipation per terminal
const power = (s) => currents(s).map((I, i) => I * I * pinResistance(i, s));
```

That is the physics, and it is **exact for the parallel-division part** — no approximation,
no simulation, ~15 lines. Every view (pin map fill, bar chart height, cutaway contact gap,
temperature readout, over-threshold flags) is a pure function of that state. One slider for
`seatDepth`, one for `tilt`, and the reader can drive the entire mechanism.

Notes on doing it well:

- **Draw the cutaway as a real section**, with the terminal barrel, the spring contact, and
  the mating pin visible, and animate the contact-patch length shrinking as `seatDepth`
  drops. That single frame carries more of the argument than any render.
- **Always show numbers next to colour.** Colour ranks; it does not quantify. Put the amps
  on or beside each pin, and draw the rated-current line across the bar chart as a hard
  rule — the crossing is the story.
- **Use a sequential ramp, not a rainbow**, and check it in both light and dark. Redundantly
  encode the over-threshold state (a hatch, a rule, a label) so it survives colour-blind
  readers and greyscale printing.
- **A report page gets printed and PDF'd.** SVG survives that at full resolution and stays
  selectable/searchable. A canvas does not. Give each interactive a sensible default state
  so the static print still makes the point.
- **Honour `prefers-reduced-motion`**; make transitions optional, never load-bearing.
- The whole thing ships in a few KB with no dependency. Three.js is roughly 150–600 KB
  gzipped depending on how much you tree-shake, before your own scene code.

## 5. The one case where three.js would earn it — and the gate

There is exactly one job on this page 3D could do better than SVG:

> Letting the reader **rotate a mated pair and discover that a plug which looks fully
> seated from the outside is short of full contact on one row** — the "you cannot tell by
> looking" beat.

That is a *rhetorical* job, not an explanatory one. It creates the unease that motivates the
rest of the page; it does not carry any of the reasoning. Build it only if **all** of these
hold:

1. The page has a hero slot that currently has nothing better in it.
2. You have the budget to also ship the SVG set — the 3D scene must never be the only
   place a fact lives.
3. You can accept the payload, a WebGL fallback path, and the accessibility work in §6.

If any of those fail, an **isometric exploded SVG** gets you ~90% of the same effect for ~2%
of the cost, and prints.

## 6. If you do build it: the spec

- **Orthographic camera**, not perspective (`THREE.OrthographicCamera`). Technical-
  illustration convention, and it keeps pin sizes and colour patches comparable across the
  frame — which is the whole reason perspective was disqualifying above.
- **No GLB asset.** The connector is boxes and cylinders; build the geometry
  parametrically in code. Skipping `GLTFLoader` and the model download is most of your
  payload saving, and it lets `seatDepth` drive actual vertex positions.
- **`InstancedMesh` for the twelve terminals**, with `setColorAt()` per instance driven by
  the same `currents(state)` function from §4. One draw call; the 3D view becomes just
  another view bound to the same state, which is the property you want.
- **Cutaway via clipping planes** (`renderer.localClippingEnabled = true` and a
  `THREE.Plane`), not a pre-cut mesh. The reader slides the section plane through the
  housing — this is the one thing 3D does that SVG genuinely cannot, so make it the
  interaction you feature.
- **Constrain the camera.** Either disable `OrbitControls` and drive rotation from a slider
  or scroll position, or clamp polar/azimuth range hard. An unconstrained orbit on a
  technical figure means readers end up underneath it, lost, looking at nothing.
- **Reuse the JS physics; do not fake it in a shader.** Correctness is the reason to build
  this in code at all rather than commissioning an illustration.
- **Fallback and a11y, non-negotiable for a report:**
  - Detect WebGL; render a static poster (SVG or PNG) if absent, and for print.
  - The canvas is opaque to assistive tech. Ship the same six values in a real `<table>`
    adjacent to it (visually compact, not hidden), and mirror state changes into an
    `aria-live="polite"` readout.
  - Full keyboard control of every slider.
  - Respect `prefers-reduced-motion` — no idle auto-rotate.
- **Lazy-load it.** Dynamic `import()` on scroll into view, so the page's first paint and
  its Lighthouse score don't pay for a decorative scene.

## 7. Failure modes to avoid either way

- **Colour as the only encoding of current.** The argument is numeric; a heat-glow that
  never states amps is a vibe, not evidence.
- **Modelling more of the connector than the argument needs.** Cable braid, latch detail,
  and shell texture add render time and reader load while carrying no information.
- **Letting the interactive be the only home for a claim.** Anything load-bearing needs to
  survive as text and a static figure — for print, for citation, for the reader who never
  touches the slider.
- **Implying precision you don't have.** The current-division maths is exact; the contact-
  resistance-versus-seating curve is a model. Label it as one, expose the constants, and
  cite the source for the per-terminal rating and any measured figures.

---

## Verdict

The mechanism is six scalars on a plane, driven by two parameters, evolving over time.
That is a 2D data problem with an interaction, and three.js would spend a large payload and
a fallback burden to reintroduce the occlusion and perspective distortion the page is
trying to overcome. **Build it in SVG against a shared state model** — you get exact physics,
print fidelity, accessibility, and a fraction of the weight. Add a single clipping-plane
three.js hero only if the gate in §5 is clear, and never let it be the only place a fact lives.

# three.js on the 12V-2x6 melting page — gate decision

## Verdict

**Conditional yes — one 3D episode, bound to one claim id, with every number outside the canvas.**

This subject clears the two evidence tests that most topics fail on (spatial claim, viewpoint necessity) because the mechanism is a rigid-body pose problem hidden inside an opaque housing. It does **not** automatically clear the third (2D insufficiency), and that test is decided by the claim graph, not by the topic. Run the gate at the end of Phase 3, after the ledger exists, not now.

The decision rule, stated so it can be checked later:

> three.js ships **only if** the claim ledger contains a sourced claim asserting a *continuous* mapping from seating pose to per-pin current distribution. If the corpus supports only enumerated discrete seating states, 2D wins and three.js is rejected and recorded as rejected.

---

## The six tests, scored

### Evidence tests — any failure rejects 3D outright

**1. Spatial claim — PASS.**
The failure mechanism as stated is a pose problem: insertion depth plus tilt about the pin-row axis plus yaw determines which of six terminals fully mate. That touches four of the gate's seven named qualifiers — depth, orientation, occlusion, assembly — and it isn't a stretch to reach them. Critically, **occlusion is the causal story, not the presentation**: the housing hides the exact state that determines whether the connector melts, and the latch can engage before the terminals do. A claim whose subject is "you cannot see the thing that kills it" is a claim about occlusion.

**2. Viewpoint necessity — PASS, narrowly.**
The evidence-revealing viewpoint change is *exterior three-quarter → end-on section through the terminal ring*. A plug sitting a fraction of a millimetre proud and slightly tilted is externally near-identical to a correctly seated one; the end-on section is where the engagement gap becomes visible. Changing viewpoint reveals evidence, which is what test 2 asks.

What this does **not** license: an orbit around a nicely rendered connector. That is showcasing an object, fails test 2 on its own terms, and fails test 4 as well.

**3. 2D insufficiency — ARGUED. This is the test that decides the page.**

Both readings are live, and the corpus picks between them:

| If the research supports… | Then | Because |
|---|---|---|
| Enumerated discrete seating states (fully seated / one end proud / latched-but-short) with a per-pin current profile for each | **2D wins — reject three.js** | Sectioned small multiples plus a six-bar current chart per state communicate it at least as clearly. Hullman's parallelism finding actively favours small multiples for cross-state comparison, and Kwon et al. found 2D better for spatial-memory tasks. Test 3 fails |
| A continuous mapping — small, visually undetectable pose error producing steeply nonlinear redistribution across six parallel paths | **3D admissible** | The input is a ≥3-DOF configuration (depth + two tilt axes). Two orthogonal sections each hide the axis the other is showing, so the reader must compose them mentally — precisely the "difficult mental comparison" the motion test names. No single 2D projection carries it |

Note the asymmetry: the first row is the cheaper, more common research outcome. Do not assume the second.

### Release tests — any failure means shipping the fallback until it passes

**4. Narrative mapping — passes by construction only.** Every camera cut and every pose change maps to a claim id (episode below). No idle orbit, no ambient rotation, no "hero" spin.

**5. Equivalent fallback — passes only if the static version is authored first.** Device capability cannot be reliably feature-detected; some browsers report WebGL support and are too weak to use it, which is why practitioners infer from screen size. The annotated section drawings and the current chart are the primary artifact; the canvas is an enhancement layered onto a page that already makes the argument without it.

**6. Performance and reduced motion — passes only if built to the constraints below.** LCP ≤2.5s, INP ≤200ms, CLS ≤0.1, all three, at the target mobile tier. All camera motion off under `prefers-reduced-motion`.

---

## If approved: the one episode, and only one

Placement is **after** the finding, not instead of it. Martini glass: the page states that six parallel pins share current unevenly and that seating decides the split, shows the per-pin numbers, *then* opens the pose model as drill-down. Median scroll depth is ~50%; a mechanism model at state twelve is built for readers who never arrive.

State sequence, each carrying one claim id and each rendering directly and completely from that id (readers skip faster than transitions complete):

1. **Exterior, correctly seated, latch engaged** — claim: the outside discloses nothing about engagement.
2. **Exterior, pose perturbed** — claim: visually identical from outside. Same camera, same object identity; the *absence* of a visible delta is the evidence, so nothing else may move.
3. **Cut to end-on section, both poses** — claim: engagement differs at specific terminals. This is a cut, not a fly-through.
4. **Per-pin current** — claim: the split. Rendered as a **DOM bar chart beside the canvas**, driven by the same state.
5. **Stable takeaway** — survives with motion disabled and with WebGL absent.

Reader-controlled pose (depth + tilt) is exploration and belongs at the end of the episode, wired to real DOM controls — sliders and radios, not canvas dragging. That single choice buys keyboard operability, touch behaviour without hover, and lets you avoid raycasting entirely.

### Build constraints

- **Load**: three.js from CDN, dynamic-imported *after* the narrative content; everything else inline.
- **Render on demand** — render on pose change and camera cut, then stop. No unconditional `requestAnimationFrame` loop. This also disposes of WCAG 2.2.2 (nothing auto-plays for 5s, so no pause control is owed) at zero cost.
- **`dispose()`** geometries, materials and textures when the chapter leaves the viewport. GPU memory otherwise grows until the tab crashes, and this survives review because demo sessions are short.
- **Cap device pixel ratio**; a connector is flat-shaded geometry, so cap it hard rather than chasing retina crispness.
- **`InstancedMesh` for the six terminals** — draw calls are the binding constraint, not triangles. No sourced universal polygon or draw-call budget exists; derive from a device matrix, do not copy a number.
- **No raycasting on mousemove.** DOM controls remove the need; if hit-testing is unavoidable, do it on `pointerdown` against a small candidate set.
- **Handle `webglcontextlost`** by swapping in the static fallback, not by reloading.
- **Labels, currents, annotations, transcript and sources live outside the canvas** in normal DOM order. The canvas carries geometry and nothing else.
- **Accessibility**: short description on the canvas plus a structured long description or data table — the per-pin values stay a table, not compressed into `aria-describedby`. Decorative canvas is `aria-hidden`.
- **Reduced-motion first**: static baseline is the default; the 3D branch is added under `@media (prefers-reduced-motion: no-preference)` so an unsupporting browser keeps the static page. Under the reduced branch, camera travel becomes cuts and annotated stills — every fact survives.
- **Mobile**: serve the static small multiples below the size threshold rather than the canvas (screen size is the practitioner proxy, since capability can't be detected). Size steps in `px` computed from `window.innerHeight`, never `vh`. `position: sticky`, not JS pinning. No steppers, no swipe-to-advance, no hover-only content.
- **Scroll**: `IntersectionObserver` selects state *n* — that is all this episode needs. GSAP `ScrollTrigger` only if you genuinely scrub the pose against scroll distance; if you do, never animate the pinned element, no ancestor `transform`/`will-change`, no `content-visibility: auto` in the section, and `normalizeScroll()` is prohibited.
- **CWV hygiene**: the canvas must not be the LCP element, and its box is reserved to keep CLS at zero.

---

## What stays 2D regardless of the verdict

- Per-pin current magnitudes → bar chart, zero baseline, amps named, editorial title stating the conclusion rather than labelling the chart.
- Temperature or contact-resistance over time → line chart with uncertainty shown.
- Connector pinout and which terminal is which → orthographic labelled diagram.
- Incidence counts, RMA rates, spec revisions → conventional 2D.

The reason is the sharpest line in the corpus. Kim et al. built four data stories in static, animated and immersive variants: immersive was rated **more interesting and more persuasive, and no more understandable or trustworthy**. A 3D scene that carries the quantities buys persuasion without comprehension. On a page about a component that catches fire, that is the wrong trade — the numbers must be in the layer that is read, not the layer that impresses.

---

## Record the decision either way

The methods note carries: which of the six tests passed, the claim id that justified test 3, that 3D was scoped to geometry with all quantities in DOM, and what the page could not establish. If the ledger comes back with only discrete seating states, the note says three.js was considered and rejected, and the page ships the annotated static cutaways. Recording the rejection is what stops the gate decaying into a formality.

## One sameness flag

`~/Dev/dossier/undervolt/index.html` is the adjacent published page — also GPU thermal/power — and it is SVG-only, no canvas, no GSAP. So no 3D metaphor is taken and the motion signature is free. Its **chart grammar** is not: a second GPU-power page must not reuse its curve treatment or section silhouette. Layout skeleton and motion signature are what read as sameness; re-colouring fixes nothing.

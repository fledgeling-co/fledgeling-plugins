# Motion, 3D and video — what to build with the libraries, not just how to load them

`artifact-engineering.md` covers inlining a library without breaking the file. This one
covers when a library earns its place and what to build with it, because the failure it
addresses is different: three consecutive artifacts shipped four static SVGs, no canvas, no
motion and no library at all, and passed the gate.

Reach for these in the order the mechanism asks for, not in the order they appear here.

## Before any chart: `/dataviz`

Explainers draw charts constantly — bars, timelines, distributions, a value against a
threshold. **Load the `dataviz` skill before writing the first line of chart code.** It
carries a form heuristic, a colour formula with a runnable validator
(`scripts/validate_palette.js`), mark specs and interaction rules, and it is the reason a
page's five charts read as one system rather than five decisions.

Its palette is brand-neutral placeholder values in `references/palette.md`. Substitute the
artifact's own palette from the identity pass and re-run the validator — that is the
supported path, and nothing else in the skill changes.

Two of its rules matter most here and pull the same way as `evidence.md` §1.7: colour encodes
one variable, and a stat tile or KPI row is a chart with the same rules as any other.

## GSAP — the default way to signal, not an alternative to CSS

Signalling is not optional. An unmarked state change costs g = 0.46–0.53 (`evidence.md`
§1.7), and a single `transition:` declaration in a page with nine controls is signalling in
name only — that is the shape measured on a real artifact. GSAP is 72 KB inlined and one command away
(`new_explainer.py --with gsap`), and at that price the orchestrated, reversible,
reduced-motion-aware version is the default rather than the upgrade.

Reach for it whenever the reader causes something to move. Specifically:

- **A state change with several moving parts.** A timeline that moves four elements in a
  known order is one `gsap.timeline()`; the same thing in CSS is four transitions that drift.
- **A Reveal.** ScrollTrigger with `scrub: true` makes scroll position the reader's clock,
  which is exactly what `evidence.md` §1.8 asks of motion — no play button needed, every
  intermediate state inspectable by scrolling back.
- **Morphing one diagram into another** rather than swapping pictures.

```js
const tl = gsap.timeline({ paused: true })
  .to('#packet',  { x: 340, duration: 0.4, ease: 'power2.inOut' })
  .to('#leader',  { attr: { r: 34 }, duration: 0.2 }, '<0.2')
  .from('#quorum',{ opacity: 0, duration: 0.2 });

stepBtn.addEventListener('click', () => tl.play());
if (matchMedia('(prefers-reduced-motion: reduce)').matches) tl.progress(1).pause();
```

```js
gsap.registerPlugin(ScrollTrigger);
ScrollTrigger.create({
  trigger: '#stage', start: 'top top', end: '+=2400', pin: true, scrub: true,
  animation: gsap.timeline().to('#ring', { rotate: 90 }).to('#axis', { opacity: 1 }),
});
```

Keep it off anything the reader did not cause. An idle tween is the ambient motion coherence
rules out (d = 0.65–0.86).

## Three.js — the flat view loses something, or the second lens wants a different projection

687 KB inlined, and there are two ways to earn it rather than one.

**The invariant is spatial.** Orientation, occlusion, a volume, a path through a space, a
surface with curvature — rotation order and gimbal lock, lattices and packing, a camera
frustum, ray marching, anything where the reader must move their viewpoint to believe the
claim.

**The second lens wants a different projection of the same data.** This is the case most
often missed. `evidence.md` §1.2 asks for a structurally different view when a topic has more
than one mechanism, because one analogy collapses a multi-factor system into a single-cause
model. A field drawn flat as a heatmap and again as a 3D surface where height is the same
quantity is exactly that: same data, two projections, every mark still encoding a real
variable. One measured artifact drew an 8,014-cell coverage field and shipped no second lens
at all — a legitimate three.js case, passed over.

What stays out: a 3D chart of two variables, an idle spin, depth that encodes nothing. "It
would look impressive in 3D" is the seductive detail the coherence principle names. "The
reader cannot answer this question from the flat view" is the test.

What a 3D scene owes beyond the inlining recipe:

- **A 2D inset showing the same state projected.** This is what makes 3D legible rather than
  impressive, and it is the piece most often skipped.
- **Render on change, not on a loop.** `renderer.render()` on orbit and on state change, and
  stop. An idle spin is ambient motion.
- **A named viewpoint control.** Free orbit plus two or three buttons that snap to the
  viewpoints the explanation refers to, because "rotate until you see it" is not an
  instruction.
- **The `<canvas>` declared in markup** with an `aria-label` that states what it shows and
  what state it is in, then handed to the renderer.

```js
const views = { front: [0, 0, 6], top: [0, 6, 0.001], corner: [4, 3, 4] };
document.querySelectorAll('[data-view]').forEach(b =>
  b.addEventListener('click', () => { camera.position.set(...views[b.dataset.view]); draw(); }));
```

## Remotion — for the sequence the browser cannot compute live

Remotion renders React to video. That is the opposite of what this skill usually wants: a
video is watched rather than operated, and transience is precisely why animation often loses
to a static diagram (`evidence.md` §1.8).

It earns a place in two cases, and **`<video controls>` is what makes the first one safe** —
a reader who can scrub holds the timeline, which is the learner-controlled playback §1.8
actually asks for.

1. **A sequence too expensive to compute in the page.** A fluid or particle simulation, a
   long training run, a ray-marched scene, thousands of frames of a real dataset. Render it
   once, embed it as a scrubbable clip, and keep the interactive version of the *simplified*
   model beside it.
2. **The ask included a video.** A talk opener, a social post, something that plays where
   nobody can click. That is a second deliverable next to the page, not part of it.

Never as a substitute for an interaction the browser could have run live.

### The pipeline

The skills live at `remotion-dev/skills` and are documented at
<https://www.remotion.dev/docs/ai/skills>. Install the set with `npx skills add
remotion-dev/skills`; `/remotion-best-practices` is the router and covers the rest on its own.

Route by task: `/remotion-create` for a new composition, `/remotion-markup` for the React
markup, `/remotion-render` to render, `/remotion-docs` to look up an API before using it.
`/remotion-best-practices` covers all of them and carries `rules/3d.md` for React Three Fiber
inside a composition and `rules/charts.md` for chart animation driven from `useCurrentFrame()`
rather than a library's own tweens.

Then encode small and inline it:

```bash
ffmpeg -i out.mp4 -vf "scale=960:-2,format=yuv420p" -c:v libx264 -crf 30 \
       -preset medium -movflags +faststart clip.mp4
python3 scripts/embed_media.py clip.mp4 --format mp4     # emits <video controls> with a data: URI
```

Measured in Chromium from `file://`: a data-URI MP4 loads its metadata, plays, and seeks —
`currentTime = 5.0` lands at 5.0 with a painted frame. A 960×540 clip at CRF 30 encodes
small enough that base64 stays well inside the 16 MB page cap; check the number the helper
prints rather than assuming.

The whole chain is measured, not just the embedding half: a real `remotion render` of 90
frames at 1920×1080 came out at 169,637 B, encoded to 8,863 B, embedded as 11,820 B of
base64, and played and seeked in Chromium with the gate passing (`evidence.md` §4.9). That
composition is flat and compresses unusually well, so read the size the helper prints rather
than expecting nine kilobytes.

Rules the gate enforces on any clip: inline as a `data:` URI, carry `controls`, and never
`autoplay`. An autoplaying clip is the transience failure with extra bandwidth.

## Generated imagery — wider than the analogy's source

`media-gen-pro` bills per image, so say in your reply what a run spent. Three uses earn it:

1. **The analogy's source domain**, when it is a real thing the reader knows by sight. A
   photograph of a brass gimbal anchors better than a rectangle labelled "gimbal".
2. **A real diagram, as vector.** `svg: true` routes to Arrow and returns editable SVG you
   inline as `<svg>` rather than a data URI — scalable, themeable, and it costs nothing
   against the prose budget once its labels are inside it.
3. **The ground.** A paper texture, a plotted grid, a subtle field behind the stage. This is
   the atmosphere half of the identity pass: it carries no claim, so the coherence principle
   does not bite it, and a flat white page is the strongest single "generated" tell.

Cap it at three images. Caption every generated picture with what it depicts and that it was
generated — a reader who mistakes an illustration for a photograph of the real system has
been misled by the artifact, which is the same defect class as an unbounded analogy.

Inline through `scripts/embed_media.py`, which resizes and re-encodes before base64: a
50 KB PNG icon lands at 5.4 KB encoded, and a 1024px render that would have been ~2 MB of
markup lands under 200 KB at 1200px WebP.

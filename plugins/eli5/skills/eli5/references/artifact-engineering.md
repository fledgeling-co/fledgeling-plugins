# Artifact engineering — building the file so it survives being opened

A model does not place shapes. It predicts coordinate tokens, and it never renders what it
wrote, so perfectly valid SVG routinely draws overlapping boxes and arrows through text
(`evidence.md` §1.9). This file is the discipline that closes that loop, plus the recipes for
the three things that make an artifact worth operating: a library when the form needs one,
generated imagery when the analogy has a real source domain, and motion the reader drives.

## The geometry contract

The rule is **decide the geometry before writing markup and write it down**, because a
coordinate you committed to can be checked and a coordinate you guessed cannot. What the
geometry *is* — the aspect ratio, the grid, how many lines it has — is a design decision, and
a radial diagram and a swimlane want different ones.

One worked shape, as an example of the form the comment takes rather than the grid to use:

```html
<!-- viewBox 0 0 960 540
     bands   header 0–72 | stage 72–420 | readout 420–540
     columns 60 · 300 · 540 · 780 · 900
     rules   text anchors at a column · boxes centre on one · arrows run band-to-band -->
<svg viewBox="0 0 960 540" width="100%" role="img" aria-labelledby="t d">
```

Then place every element against a **named line**, never a free-floating number. When a box
is 240 wide starting at column 60, its centre is 180 and its label anchors there — arithmetic
you can check.

Radial work usually wants a centre, a ring set and an angular step instead of bands and
columns. Same discipline, different contract.

### Self-checks that catch warping without rendering

- Every `x` plus its `width` stays inside the viewBox width. Same for `y`/`height`.
- Two boxes in one band do not overlap: `x₁ + w₁ ≤ x₂`.
- A `<text>` at `x=C` with `text-anchor="middle"` needs roughly `len × 0.55 × font-size` of
  clearance either side of C. Long labels overflow most often.
- Arrows leave the bottom edge of one box and arrive at the top edge of another — compute
  both rather than eyeballing a midpoint.

## Containment, and the one exception

Everything inline. No CDN scripts, remote images, remote stylesheets or `fetch`. In sandboxed
artifact runtimes a blocked request **fails silently**, so the page half-renders and nothing
reports an error (`evidence.md` §1.10).

The exception is **Google Fonts** — `fonts.googleapis.com` and `fonts.gstatic.com` are what
the artifact CSP permits, and a distinctive type pairing is half the identity pass. Give every
face a real fallback stack, because the same file opened from disk with no network falls back
rather than failing:

```css
font-family: "Fraunces", ui-serif, Georgia, serif;
```

Icons are SVG paths you draw. Data is literal in the script. There is nothing to fetch.

## Choosing the drawing surface

| Surface | When |
|---|---|
| Inline SVG | Diagrams, node graphs, state machines, flows — under roughly 500 elements. DOM events, ARIA, CSS transitions, crisp at every DPI. |
| Canvas 2D | Continuous numerical simulation — particle fields, diffusion grids — where DOM node count drops frames. |
| WebGL via Three.js | The mechanism is genuinely spatial and a flat projection loses the invariant. |

Default to SVG. Reach past it only when you can name the element count or the spatial
property that forced the move.

## Inlining a library

Both libraries go in a `<script>` carrying a `data-vendor` attribute. That attribute is not
decoration: the gate excludes vendor blocks from the containment, animation-frame and
word-count scans, and Three.js contains three `fetch(` calls in its loaders that otherwise
fail `no-network-calls` on every artifact that uses it.

```bash
python3 scripts/vendor_lib.py gsap           > gsap-block.html
python3 scripts/vendor_lib.py scrolltrigger  > st-block.html
python3 scripts/vendor_lib.py three          > three-block.html
```

Each fetches once from a pinned, checksummed URL into `~/.cache/eli5-vendor` and reuses it
after that; pass a local path instead to use a copy you already have. A checksum that does not
match refuses rather than inlining an unexpected file. Nothing is fetched when the page
renders — this is a build step, and the artifact stays inline.

`scripts/new_explainer.py` calls this for you and writes a starting file with the blocks
already in place.

**GSAP's licence forbids removing its notices**, so the header comment travels into the
artifact and `vendor_lib.py` refuses a GSAP file that has lost it. Commercial use is free
under that licence; the prohibited case is a no-code visual animation builder, which this is
not.

### GSAP

`gsap.min.js` is a classic script that assigns `window.gsap`, so it inlines as-is. Measured in
Chromium from `file://`: `gsap.version` reads `3.13.0` and a `gsap.to('#box',{x:120})` lands
`matrix(1, 0, 0, 1, 120, 0)`. 72 KB.

```html
<script data-vendor="gsap">/* contents of gsap.min.js */</script>
<script data-vendor="gsap-scrolltrigger">/* contents of ScrollTrigger.min.js */</script>
<script>
  gsap.registerPlugin(ScrollTrigger);
</script>
```

### Three.js

Three ships ES modules only, and the build matters. A **single-file** build inlines; a
**split** build does not.

Check first — a build whose first 2 KB contains an `import` statement is split:

```bash
head -c 2000 three.module.min.js | grep -c '^import\|;import'
```

Two failures measured in Chromium from `file://` against the split r17x pair
(`three.module.min.js` re-exporting `./three.core.min.js`): inlined directly, the relative
import resolves to a sibling path and dies as `Access to script at
'file:///…/three.core.min.js' … blocked by CORS policy`; behind an importmap `data:` URL it
dies as `Failed to resolve module specifier "./three.core.min.js". Invalid relative url or
base scheme isn't hierarchical.` Neither reports anything a reader would see — the page just
has no 3D in it.

The single-file build (r169, 687 KB) works. `vendor_lib.py` rewrites its trailing
`export{A as B, …}` into `const THREE = { B: A, … }` and publishes it on `window`, so nothing
needs an importmap and nothing needs `data:` in `script-src`:

```html
<canvas id="stage" aria-label="…what the viewport shows and what state it is in…"></canvas>

<script type="module" data-vendor="three">
/* three.module.min.js with export{} rewritten to const THREE = {…} */
window.THREE = THREE;
</script>

<script type="module">
const canvas = document.getElementById('stage');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
</script>
```

Two details that decide whether this passes the gate and works for a screen reader:

- **Artifact code goes in a separate `<script>`.** The vendor block publishes `THREE` on
  `window`; module scripts execute in order, so the second block sees it. Author code written
  *inside* the vendor block would be excluded from the pointer, animation-frame and network
  scans along with the library.
- **Declare the `<canvas>` in markup** with an `aria-label` describing what it shows and what
  state it is in, then hand it to the renderer. A canvas three.js creates for itself is
  invisible to the gate's scene count and to assistive technology alike.

Measured: renderer constructed, canvas attached, `THREE.REVISION` reads `169`. The importmap
route also works on a single-file build and costs 917 KB against 687 KB, so it is the fallback
rather than the default.

Three.js has no `OrbitControls` inside the core build — it lives in `examples/jsm`. Inline that
file the same way, or hand-roll orbit from `pointermove` deltas in about twenty lines, which is
usually less than inlining another module.

## Generated imagery

Reach for `media-gen-pro` when the analogy's source domain is a real thing the reader knows by
sight. A photograph of a lock and a key anchors better than a rectangle labelled "lock". It
does not belong anywhere else: an image that carries no claim is the seductive detail that
costs d = 0.65–0.86 (`evidence.md` §1.7).

Rules that keep it honest and small:

- **Three images per artifact at most**, and each call is billed. Report the count in your reply.
- **`svg: true` routes to Arrow** and returns real vector — editable, scalable, and inlinable as
  an `<svg>` rather than a data URI. Prefer it for anything diagrammatic.
- **Caption every generated image** with what it depicts and that it was generated. A reader
  who mistakes an illustration for a photograph of the real system has been misled by the
  artifact, which is the same defect class as an unbounded analogy.
- **Inline through the helper**, which resizes and re-encodes before base64 so a 1.5 MB PNG does
  not become 2 MB of markup:

```bash
python3 scripts/embed_media.py hero.png --max-width 1200 --format webp
```

It writes an `<img src="data:image/webp;base64,…" alt="…">` tag to stdout and prints the
encoded size to stderr. Keep the finished file under 16 MB, which is the artifact runtime's cap.

## The idiom set

**Reactive state, one source of truth.** Compute, then render; never mutate the DOM from two
places.

```js
const state = { step: 0, nodes: 5, partition: 2 };
function set(patch) { Object.assign(state, patch); render(); }
function render() { /* read state, write DOM. No writes to state in here. */ }
```

**Pointer drags survive touch.** Without both lines the interaction dies the moment a finger
leaves the element, or the page scrolls instead of dragging.

```js
el.addEventListener('pointerdown', e => { el.setPointerCapture(e.pointerId); drag = true; });
el.addEventListener('pointermove', e => { if (drag) set({ v: valueFrom(e) }); });
el.addEventListener('pointerup',   e => { drag = false; el.releasePointerCapture(e.pointerId); });
```
```css
.scrub { touch-action: none; user-select: none; cursor: ew-resize; }
```

**Animation frames are cancelled.** Prefer demand-driven rendering — draw when state changes,
not on a loop. When a loop is genuinely needed, own its handle and stop it at equilibrium.

```js
let raf = null;
function tick() {
  if (!advance()) { cancelAnimationFrame(raf); raf = null; return; }
  render();
  raf = requestAnimationFrame(tick);
}
function play()  { if (!raf) raf = requestAnimationFrame(tick); }
function pause() { if (raf) { cancelAnimationFrame(raf); raf = null; } }
```

A Three.js scene follows the same rule: render on orbit and on state change, and stop the loop
when nothing is moving. An idle spin is ambient motion, which coherence rules out.

**Motion is the reader's.** Step, play and pause on a Machine or a Trace; scroll position on a
Reveal, where ScrollTrigger makes the reader the clock and satisfies §1.8 without a play button.
Every intermediate state is inspectable at rest.

**Reduced motion is a real path, not a switch that stops everything.**

```css
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
```
```js
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (still) { timeline.progress(1).pause(); }   // land the end state, keep the controls
```

**Readouts sit in the diagram.** Spatial contiguity is the largest single effect in the corpus,
d = 0.72–1.19 (`evidence.md` §1.7). The number goes inside the `<svg>`, beside the thing it
measures — and words inside `<svg>` cost nothing against the prose budget.

```html
<text x="540" y="300" class="readout">quorum 3 of 5 ✓</text>
```

**Signal the change.** When state moves, mark what moved: a stroke that thickens, a fill that
shifts, a short pulse on the element that changed. Unsignalled transitions cost g = 0.46–0.53.

## Theming

Define the full light palette on bare `:root`, then redefine **only** what changes in dark.
Give `body` an explicit background — a transparent body borrows whatever is behind it.

```css
:root{
  --bg:#fbfaf8; --fg:#1a1a1a; --muted:#6b6b6b;
  --line:#d8d4cf; --accent:#c4622d; --ok:#2f7d5e; --warn:#b3421a;
}
@media (prefers-color-scheme: dark){
  :root{ --bg:#15140f; --fg:#f2efe9; --muted:#a09a90; --line:#3a362f; }
}
body{ background:var(--bg); color:var(--fg); }
```

One accent for the thing in motion, one for a settled state, one for fault. Those token names
carry semantics, so use them consistently. Colour is never the only channel — pair it with
shape, position or a label, or the diagram fails for colour-blind readers.

## Accessibility floor

- `role="img"` plus `aria-labelledby` on each `<svg>`, pointing at a `<title>` and `<desc>`
  that say what the diagram shows. A `<canvas>` or WebGL viewport gets the same treatment plus
  a text summary of the state, since its content is invisible to assistive technology.
- Every control reachable by keyboard: real `<button>` and `<input>`, never a `<div>` with a
  click handler. An Assembly's drag needs a select-then-place keyboard route beside it.
- Steppers work with arrow keys; a range input already does.
- Body text ≥ 16px, SVG labels ≥ 12px at the rendered size.
- Contrast ≥ 4.5:1 for text against its background, ≥ 3:1 for meaningful strokes.
- `prefers-reduced-motion: reduce` lands each state statically and keeps every control.

## Responsive

The page body never scrolls sideways. `viewBox` plus `width="100%"` handles SVG; a canvas or
WebGL viewport resizes off a `ResizeObserver` and re-renders once. Wrap anything wide — tables,
code — in `overflow-x: auto`. Size against the container, since the artifact may render inside
a panel much narrower than the viewport.

## Before you call it done

```bash
python3 scripts/lint_explainer.py artifact.html   # must exit 0
open -a "Google Chrome" artifact.html             # then actually look at it
```

The linter cannot see a warped diagram, and that is the exact failure mode it cannot cover.
Open it. Step every control. Drag on a trackpad. Resize the window narrow.

Use a real browser for the look. Obscura drops whitespace at inline-element boundaries and will
make correct prose appear broken — a defect that has already cost one unnecessary CSS "fix"
that had to be reverted. Obscura also reports `document.getAnimations()` as 0 while animations
run, so a GSAP timeline reads as absent there; screenshot it in Chromium instead.

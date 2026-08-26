# Artifact engineering — building the file so it survives being opened

A model does not place shapes. It predicts coordinate tokens, and it never renders what
it wrote, so perfectly valid SVG routinely draws overlapping boxes and arrows through
text (`evidence.md` §1.9). This file is the discipline that closes that loop.

## The geometry contract

Decide geometry **before** writing markup. Write the contract into a comment at the top of
the SVG so later edits stay inside it.

```html
<!-- viewBox 0 0 960 540
     bands   header 0–72 | stage 72–420 | readout 420–540
     columns 60 · 300 · 540 · 780 · 900
     rules   text anchors at a column · boxes centre on one · arrows run band-to-band -->
<svg viewBox="0 0 960 540" width="100%" role="img" aria-labelledby="t d">
```

Then place every element against a **named band and column**, never a free-floating number.
When a box needs to be 240 wide starting at column 60, its centre is 180, and its label
anchors there — that is arithmetic you can check, not a coordinate you guessed.

Pick one aspect ratio and keep it. 960×540 (16:9) suits process diagrams; 960×640 (3:2)
suits node graphs that need vertical room; 720×720 suits anything radial.

### Self-checks that catch warping without rendering

- Every `x` plus its `width` must stay inside the viewBox width. Same for `y`/`height`.
- Two boxes in the same band must not overlap: `x₁ + w₁ ≤ x₂`.
- A `<text>` at `x=C` with `text-anchor="middle"` needs roughly `len × 0.55 × font-size`
  of clearance either side of C. Long labels are the most common overflow.
- Arrows between bands should leave from the bottom edge of one box and arrive at the top
  edge of another — compute both, do not eyeball a midpoint.

## Containment

Everything inline. No remote images, CDN scripts, stylesheets, fonts or `fetch`. In
sandboxed artifact runtimes a blocked request **fails silently**, so the page half-renders
and nothing reports an error (`evidence.md` §1.10).

- Fonts: a system stack. `font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI",
  Roboto, sans-serif` and a matching `ui-monospace, SFMono-Regular, Menlo, monospace`.
- Icons: draw them as SVG paths, or do without.
- Data: literal in the script. There is nothing to fetch.

## SVG or canvas

| Use | When |
|---|---|
| Inline SVG | Diagrams, node graphs, state machines, flows, anything under ~500 elements. DOM events, ARIA, CSS transitions, crisp at every DPI. |
| Canvas | Continuous numerical simulation — particles, fields, diffusion grids — where DOM node count would drop frames. |

Default to SVG. Reach for canvas only when you can name the node count that forced it.

## The idiom set

**Reactive state, one source of truth.** Compute, then render; never mutate the DOM from
two places.

```js
const state = { step: 0, nodes: 5, partition: 2 };
function set(patch) { Object.assign(state, patch); render(); }
function render() { /* read state, write DOM. No writes to state in here. */ }
```

**Pointer drags survive touch.** Without both lines the interaction dies the moment a
finger leaves the element, or the page scrolls instead of dragging.

```js
el.addEventListener('pointerdown', e => {
  el.setPointerCapture(e.pointerId);
  drag = true;
});
el.addEventListener('pointermove', e => { if (drag) set({ v: valueFrom(e) }); });
el.addEventListener('pointerup',   e => { drag = false; el.releasePointerCapture(e.pointerId); });
```
```css
.scrub { touch-action: none; user-select: none; cursor: ew-resize; }
```

**Animation frames are cancelled.** Prefer demand-driven rendering — draw when state
changes, not on a loop. When a loop is genuinely needed, own its handle and stop it at
equilibrium.

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

**Motion is steppable.** Every animation carries step / play / pause, and every
intermediate state is inspectable at rest — transience is why animations often fail to beat
static diagrams (`evidence.md` §1.8).

**Readouts sit in the diagram.** Spatial contiguity is the largest single effect in the
corpus, d = 0.72–1.19 (`evidence.md` §1.7). Put the number inside the `<svg>`, beside the
thing it measures — not in a card underneath.

```html
<text x="540" y="300" class="readout">quorum 3 of 5 ✓</text>
```

**Signal the change.** When state moves, mark what moved: a stroke that thickens, a fill
that shifts, a short pulse on the element that changed. Unsignalled transitions cost
g = 0.46–0.53.

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

Semantic colour, used consistently: one accent for the thing in motion, one for verified
state, one for fault. Colour is never the *only* channel — pair it with shape, position or
a label, or the diagram fails for colour-blind readers.

## Accessibility floor

- `role="img"` plus `aria-labelledby` on each `<svg>`, pointing at a `<title>` and `<desc>`
  that say what the diagram shows.
- Every control reachable by keyboard: real `<button>` and `<input>` elements, never a
  `<div>` with a click handler.
- Steppers work with arrow keys; the range input already does.
- Body text ≥ 16px, SVG labels ≥ 12px at the rendered size.
- Contrast ≥ 4.5:1 for text against its background, ≥ 3:1 for meaningful strokes.
- Respect `@media (prefers-reduced-motion: reduce)`: keep the step control, drop the tween.

## Responsive

The page body must never scroll sideways. `viewBox` plus `width="100%"` handles the
diagram; wrap anything wide — tables, code — in `overflow-x: auto`. Use container-relative
sizing where possible, since the artifact may render inside a panel much narrower than the
viewport.

## Before you call it done

```bash
python3 scripts/lint_explainer.py artifact.html   # must exit 0
open -a "Google Chrome" artifact.html             # then actually look at it
```

The linter cannot see a warped diagram, and that is the exact failure mode it cannot cover.
Open it. Step every control. Drag on a trackpad. Resize the window narrow.

Use a real browser for the look. Obscura drops whitespace at inline-element boundaries and
will make correct prose appear broken — a defect that has already cost one unnecessary CSS
"fix" that had to be reverted.

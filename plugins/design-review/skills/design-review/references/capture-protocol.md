# Capture protocol

Capture methodology sets the ceiling on what any visual stage can find. A defect you cannot resolve is a defect you will clear.

## Serve, don't open

Serve over HTTP, never `file://`. Module scripts, fetches and some fonts silently fail from the filesystem. One `python3 -m http.server 4311` per project directory.

## Viewport matrix

| Viewport | Width | Watch for |
|---|---|---|
| Mobile | 375px | The true stress test — most breakage lives here |
| Tablet | 768px | Awkward two-column intermediates, orphaned sidebars |
| Desktop | 1280px | The design as intended |
| Wide | 1920px | Missing `max-width` — content stretched to absurd measure |

Pause at 2–3 in-between widths while resizing. Breakpoint *transitions* break more often than breakpoints.

For model-facing evaluation specifically, the standard pair is 1920×1080 desktop and 390×844 mobile at DPR 2.

## Never feed a monolithic scroll to a vision model

A full-page screenshot of a long page has an extreme aspect ratio and hits image-token compression limits; performance degrades measurably. Two alternatives:

- **Tiling** — split the full page into consecutive viewport-sized tiles, processed in sequence
- **Section extraction** — capture per DOM container, merging visually overlapping bounding boxes so related elements group without redundancy

## One tall capture, then crop

Screenshot the full page once with a tall viewport (e.g. 1400×5000, `fullPage: true`), then slice regions from the image. Re-cropping is instant; re-screenshotting costs a browser launch and a render wait. Don't fight per-element clip captures.

**The crop is the evidence; the full page is only the index.** A whole page scaled into a review shows composition and nothing else. Every defect that survives to delivery lives at component scale. Produce one crop per component and open each.

Do not decide which components those are by eye. `probeComponentInventory()` enumerates them from the DOM with crop boxes attached — that list is the worklist, and the fraction of it you open is what the report's Coverage block states.

**Slice crops out of a viewport capture; never take element screenshots as your evidence base.** An element screenshot (`locator.screenshot()`, `--element` in a CLI driver) renders that element's own box in isolation. It is therefore blind to the entire class of defects that concern *where the element sits*: clipped past the window edge, shifted off-centre, hidden under sticky chrome, overlapped by a floating bar, scrolled out of view. A fixed-size stage pushed 120px past the right edge of the window — a quarter of its content unreachable — element-screenshots as a flawless render, on every viewport, every time.

The same trap sits in geometry checks. An aspect-ratio assertion (`w / h === 1.778`) or a size assertion holds perfectly while the box is the right size in the *wrong place*. Placement needs its own predicate, against the viewport:

```js
const r = el.getBoundingClientRect();
({ clipL: Math.max(0, -r.left),        clipR: Math.max(0, r.right  - innerWidth),
   clipT: Math.max(0, -r.top),         clipB: Math.max(0, r.bottom - innerHeight) });
```

Element captures are legitimate for one job: cropping a component you have *already* located within a viewport capture, when the region is awkward to slice. They can never establish that a surface fits its window.

## deviceScaleFactor by purpose

- **DPR 1** when the question is "what does a user see at 100% zoom"
- **DPR 2–3** when the question is "is this component defective" — spacing, alignment, ink, hairlines and 1px drift are not resolvable at DPR 1

## Coordinate overlays

Draw a grid or rulers along the edges of crops used for spatial questions. Measured effect: +55% improvement in spatial critique and bounding-box accuracy. Vision models are spatially weak by default (IoU 0.323 against human bounding boxes), and this is the cheapest available correction.

`scripts/annotate.py` does this.

## Wait for done

Network idle *plus* an explicit wait for async renderers. Charts and canvas need 2–4s after networkidle. A screenshot of a half-rendered chart generates a false finding, which costs more than the wait.

## Scroll before judging, then prove the page stopped moving

Three of the four measurement artefacts on one recent review came from probing at the wrong moment. Each looked like a confident, specific defect. The shape is always the same: **the probe ran before the page finished becoming itself.**

**Scroll the whole document first**, in ~0.8-viewport steps, then return to the top. Two things depend on it:

- A scroll-reveal system leaves every band below the fold at `opacity: 0`. A full-page screenshot at load shows them blank, and that has already been misread as a broken reveal system.
- `loading="lazy"` images report `naturalWidth === 0` until they enter the viewport. An image probe run without scrolling reported five of eight as broken; after a scroll pass, zero were.

**Then drain `document.getAnimations()` and record what was left running.** Draining is not the point — the recorded count is. A gate sampled mid-entrance reports partially-composited colours as real ones, and its output is formally indistinguishable from a real measurement. `runAll().settled` and the runners' `animationsRunningAtMeasure` carry it.

**Treat your first reading of any time- or scroll-dependent property as provisional.** A skip link measured as invisible-while-focused turned out to have been sampled at 0ms of a `transition: top 220ms`; at 600ms it sits at `top: 16px` on every tier. Before filing a finding about opacity, transform, position, `naturalWidth` or colour, re-measure at a second, later moment and check the two agree.

## Staging interactive states

Static screenshots cannot see hover, dropdowns, routing, or animation pacing. Capture at minimum three states where behaviour matters: before, during (hover/active), after (post-interaction).

- **Hover** — hover the element, wait for the tooltip or transition, then capture
- **Selected without hover** — click, then move the pointer to a corner before capturing, or the hover state contaminates the evidence
- Capture each state at both mobile and desktop widths when the interaction differs

## Mid-flight frames

**Unavailable on Obscura — skip this and record it as skipped.** The engine does not execute CSS animations or transitions, so the reflow trick below restarts nothing, `document.getAnimations()` returns 0 whatever the page declares, and a frame series would be N identical stills. `run_review.py --motion` hard-exits with that reason. Reporting the motion pass as not performed is correct; reading a mid-flight defect off identical frames is not.

On an engine that does run animations, restart deterministically and capture every ~200ms:

```js
el.classList.remove('seen');
void el.offsetWidth;          // force reflow — this is what restarts the animation
el.classList.add('seen');
```

Open every frame. Mid-transition bugs exist in no static state.

One consequence that *does* land here: because the animation never starts, an element whose keyframe begins at `opacity: 0` reads at roughly 0.0036 **on a capture taken before the reveal pass**. It looks exactly like a z-index bug and it is an engine artifact. After the document has been scrolled and settled the same element reads 1, so the value is provisional rather than permanent — which is the whole reason the reveal pass comes first. `probeStrandedElements()` reports whatever population is left after it.

## Before/after pairs

Must match viewport, crop box and state, or the comparison is worthless. Capture the *before* before editing. If you forgot, restore the prior version (`git stash`, or `git checkout HEAD~1 -- <file>`), capture, then restore.

## Console is part of the capture

Collect JS errors and warnings on every load. A clean-looking page with a thrown exception is not verified.

## Supply structure alongside pixels

Pass DOM metadata and console output with the image. It lets the reviewer distinguish a layout failure caused by poor spacing from a functional failure caused by a broken asset link — two findings that look identical in a screenshot.

## Programmatic probes

Run these in the page rather than judging by eye. `scripts/probes.js` bundles them.

**Overflow:**

```js
[...document.querySelectorAll('*')].filter(el =>
  el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1
).filter(el => getComputedStyle(el).overflow === 'visible')
 .forEach(el => console.log('overflow:', el.tagName, el.className));
if (document.documentElement.scrollWidth > innerWidth) console.warn('PAGE overflows horizontally');
```

**Image aspect ratio** — measure rendered vs natural; don't trust the declared ratio. An `<img>` carrying *both* a `height` attribute and a CSS `aspect-ratio` on its slot has two definite dimensions, so `aspect-ratio` is ignored and the photo silently over-crops to its natural height:

```js
[...document.images].filter(i=>i.naturalWidth).map(i=>{const r=i.getBoundingClientRect();const c=Math.max((r.width/r.height)/(i.naturalWidth/i.naturalHeight),(i.naturalWidth/i.naturalHeight)/(r.width/r.height));return c>1.4?[i.src,c.toFixed(2)]:null}).filter(Boolean)
```

Anything over ~1.4× is a heavy crop. Fix with `height: auto` in the style, so the attribute only seeds the intrinsic ratio.

**Ink, not boxes.** `getBoundingClientRect()` returns the box; where the glyph sits inside it depends on `line-height`, the font's metrics and the character. Two boxes with identical `top` can show their ink 8px apart — which is how "the CSS is correct" and "it looks wrong" are both true at once:

```js
const probe = document.createElement('span');
probe.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
el.insertBefore(probe, el.firstChild);
const baselineY = probe.getBoundingClientRect().top;   // the first line's baseline
probe.remove();
ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
const inkTop = baselineY - ctx.measureText(text).actualBoundingBoxAscent;
```

`line-height` below ~0.95 of the font size makes the box **shorter than the glyph**, so centring lies and a 64px numeral renders 73px tall. Correct optical alignment with `transform: translateY()`, never `margin` — a transform doesn't disturb the box model, so it can't knock a value off the spacing scale.

## Per-viewport checklist, severity order

1. **Overflow** — no unintended horizontal scrollbar; no content escaping its container; images inside their boxes; tables and code blocks scroll inside their own `overflow-x: auto` wrapper, not the page
2. **Overlap** — sticky headers over anchored content, badges over text, absolutely-positioned decor over CTAs. Check with real content lengths, not the happy sample
3. **Text integrity** — no clipping or mid-word breaks; long words and URLs wrapped (`overflow-wrap: break-word`); ellipsis actually appearing where truncation is designed; italic descenders not clipped; no widowed CTA labels
4. **Alignment drift** — grid and flex items evenly distributed; icons vertically centred with their labels; form labels attached to their fields; nothing off-grid by a few accidental pixels
5. **Stability** — reload and watch: no jump when images load (explicit `width`/`height`), no font-flash reflow, skeletons matching the layout they replace
6. **Z-order** — dropdowns above cards, modals above everything, toasts above modals. Ad-hoc `z-index: 9999` is a finding; a tokenised scale is the fix (`--z-dropdown: 100` … `--z-toast: 500`)
7. **Media** — aspect ratios held, no stretched or squashed images, embeds contained

## Degrading honestly

When no browser automation exists, run what you can: the source scan, overflow-prone patterns (missing `min-width: 0`, absent `max-width`, fixed widths in fluid containers), explicit image dimensions. Then say in the summary that rendered verification did not happen.

Never imply a page was seen. Rendering a screenshot is not seeing one — a capture enters your knowledge only when you open it.

# Visual Verification: Layout Integrity and the Screenshot Playbook

The procedure for *seeing* a design the way a user will — structural layout checks across viewports, plus the screenshot discipline that makes the looking fast and the evidence trustworthy. Use it three ways: as the **fifth review axis** in `polish-pass.md` (layout integrity & responsive), as the **standing playbook** for any rendered-output check — yours by default, a delegate's when `polish-pass` fans out — and as the **per-unit micro-check** inside `unit-critique-gate.md`: after each unit drafts, load just that unit at 375px and 1280px, run the overflow probe, and collect console errors, rather than saving all layout verification for the end.

**Looking is cheaper than reasoning about what you'd see.** Every check below is a tool call that returns fact where deliberation returns inference. When a capture leaves you unsure, take another capture — a tighter crop, a higher DPR, the other viewport, the mid-transition frame — before spending another round of thought on the one you have.

**When no browser automation exists** in the environment (a headless sandbox with no Obscura), degrade honestly: run the static checks you can — `scripts/design-lint.py`, the overflow-prone patterns (missing `min-width: 0`, absent `max-width`, fixed widths in fluid containers), explicit image dimensions — and state in your summary that rendered verification did not happen. Never imply a page was seen. The lint prints its own "not checked" line; paste that rather than paraphrasing it.

**The other reviews judge the design; this one checks whether it survives contact with a browser.** Broken overflow, overlapping elements, and a layout that shatters at 375px are invisible in source and fatal on screen — and they're the failure class that hierarchy/slop/a11y reviews aren't looking for.

## Phase 0: The verification contract

Everything below this section is technique. This section is why the technique is usually wasted. It comes from a real 20-page build that shipped with a 161px void, an orphaned chip row, and stranded display numerals — all three obvious to a human in seconds, all three surviving a QA harness that reported **0 HIGH, 0 MED, 0 LOW**.

### What this engine cannot tell you — read before running anything

The sanctioned browser is **Obscura**, a Rust engine rather than packaged Chrome. Everything in the table below is *measured on this machine, 13 and 18 Aug 2026*, and every row describes a check that returns a plausible value rather than an error. **A capability whose absence returns a plausible value is worse than one that fails**, because rule 4 below is exactly the collision it produces: an unusable measurement and a clean one serialise identically.

| Unavailable here | What actually happens | The honest claim |
|---|---|---|
| CSS animations, transitions | never execute; `document.getAnimations()` is always 0 | **not checked** — a mid-flight capture equals the at-rest capture, and a drained count of 0 is unusable, not clean |
| `Emulation.setEmulatedMedia` | accepted and inert; `matchMedia` stays false | print and reduced-motion passes are **not available**. The call returning without an error proves only that it was accepted |
| Web fonts | never load | type fidelity is **unmeasurable**; a display-face rule is a source claim |
| `getComputedStyle(el, '::after')` | **ignores the pseudo argument** and returns the element's own style | never write a pseudo-element check against this engine — it answers confidently and wrongly |
| Shorthand computed styles | `padding`, `margin`, `border`, `borderRadius`, `background`, `font`, `inset`, `gap` return `0px`/`""`; longhands are correct | read `paddingTop`, `marginLeft`, … only. `flex` is worse: `flexGrow` is empty too |
| An empty computed value | means "not implemented" for `boxShadow`, `backgroundImage`, `textTransform`, `outline`, `flex` | absent ≠ unset |
| `path.getBBox()` | returns all-zero without throwing | any SVG geometry read through it is a false zero |
| Native form controls | do not render at all | a real radio input photographs as nothing — which looks exactly like a missing affordance |
| Promise-returning evaluation | neither `obscura fetch` nor MCP `browser_evaluate` awaits a promise | resolve before returning, or read a value the page already wrote |

Two named false-positive sources on top of that: an `opacity: 0` entry keyframe strands its element at **opacity 0.03 forever** (which reads exactly like a z-index bug), and a line carrying an inline citation marker gets mangled — review typography on a marker-stripped copy.

What **does** work, and is the whole basis of Phase 1: `setDeviceMetricsOverride` through `obscura serve` + CDP, so the viewport matrix is real; longhand computed styles; `getBoundingClientRect`; `elementFromPoint`; the DOM; the console; `--screenshot`.

**This table is a measurement, not a property of headless browsers.** It was taken on Obscura on this machine on the dates above. If the engine changes, re-measure rather than inheriting it — the four probes take one call between them, and each one distinguishes "unavailable" from "clean" on its own:

```js
// Run this WHILE something is animating and a face is declared, or every answer is
// meaningless: a 0 with nothing moving means nothing, and recording that 0 as a pass
// is the exact collision the table exists to prevent.
({ animations: document.getAnimations().length,          // 0 with a running animation on screen = unavailable
   printEmulated: matchMedia('print').matches,           // false after setEmulatedMedia = inert
   fontLoaded: document.fonts.check('16px "<your face>"'),   // false with the face declared = never loaded
   pseudoWorks: getComputedStyle(h, '::after').content !== getComputedStyle(h).content })
```

**And the table narrows what you check; it does not excuse the check.** Everything still available is still required: the viewport matrix and the overflow probe (`setDeviceMetricsOverride` works), the end-state captures for hover, focus and selected, the scroll pass before probing, longhand computed styles, `elementFromPoint`, the console, and the reveal-safety grep that stands in for the print pass (`make-a-doc.md` Phase 3). The motion work that moves off the capture and onto the source is the `reveal-blank` check, an explicit `z-index` on every transient overlay, and one `prefers-reduced-motion` block covering every animation in the file. A page whose motion cannot be photographed here still has to be built correctly, and three of those four things are gated.

**So motion, print, reduced-motion and type fidelity go into the Phase 4 report's "Not checked" line by default, not by exception.** Rules 8, 9 and the interactive-state staging in Phase 2 are written for an engine that runs animations; on this one they are the class-toggle capture named there, and nothing more. Never improvise a different engine to close the gap — Playwright, Puppeteer, `chrome-headless-shell`, `chrome-devtools-mcp`, Playwright MCP and browser-use are removed from this machine. *"Not checked on this engine"* is the finished answer.

**1. Rendering an image is not seeing an image.** A capture tool-call returning success proves a file exists. The image enters your knowledge only when you *open* it. Screenshots were generated in that build and never read; "I verified with screenshots" was false, and the word for what actually happened is "I rendered screenshots." If you did not open it, you did not look at it, and you may not say you checked it.

**2. The question you bring to an image determines what you see in it.** Handed a screenshot and asked *"do you see anything wrong with this?"*, you find the defect in seconds. Looking at your own render, the implicit question is *"is this done?"*, and the answer comes back yes. Same pixels, same eyes, opposite result. So fix the protocol: for every capture, ask literally **"what is wrong with this?"** Answering "nothing" requires first naming the three most likely failure modes for that component (a void, a wrap, a misalignment, a contrast miss, an overlapping label) and ruling each out by pointing at pixels. If you can't name three, you don't know the component well enough to clear it.

**3. A gate is downstream of the findings that motivated it.** Every rule in a lint was written *after* someone pointed at a defect. It can prove a defect you have already met has not come back. It is structurally incapable of finding the one nobody has met yet. **"0 findings" means "no known defect is present." It never means "verified."** Report the two claims separately and in these words: *"the lint passed"* and *"I opened captures X, Y, Z and looked for A, B, C."* Merging them into "verified" is the specific dishonesty that hands the reviewing labour back to the person the work was meant to save.

**4. Prove your rules can fail.** That harness's widow rule was `/\S+/g` written inside a JavaScript template literal, where `\S` is not a valid escape and collapses to `S`. It shipped as `/S+/g`, matched runs of the letter S, found nothing on any page, ever — and its silence was reported as a pass. Nothing in the output distinguishes silent-because-clean from silent-because-broken. Two cheap defences: **serialize a real function** into the page (`fn.toString()`) rather than building a code string, so escapes mean what they say; and **run every new rule against the artifact that motivated it, watch it fire, and only then fix the artifact.** A rule only ever observed passing is a rule you have not written. `scripts/design-lint.py --selftest` is the mechanised form of that half: it runs every rule against a fixture built to trip it and fails if any rule stays silent, so a collapsed regex is caught by the gate rather than by the next reviewer.

**5. Coverage is silent.** A rule whose selector matches nothing does not warn you. It passes. When you add a component that uses a checked pattern, add it to the config in the same edit. When the gate is clean, spend one moment asking which components no rule mentions.

**6. Inspect crops, not pages.** A full page scaled into a review is a resolution at which a 161px void reads as "generous whitespace" and an orphaned chip is a few ragged pixels. Judging from thumbnails is looking at an image in which the defects cannot exist and concluding there are none. Crop to the component and zoom (DPR 2–3). See Phase 2.

**7. Measure ink, not boxes.** `getBoundingClientRect()` returns the box; where the glyph sits inside it depends on `line-height`, the font's metrics, and the character. Two boxes with identical `top` can show their ink 8px apart — which is how "the CSS is correct" and "it looks wrong" are both true at once. For cap-height, probe the baseline and add the font's real ascent:

```js
const probe = document.createElement('span');
probe.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
el.insertBefore(probe, el.firstChild);
const baselineY = probe.getBoundingClientRect().top;   // the first line's baseline
probe.remove();
ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
const inkTop = baselineY - ctx.measureText(text).actualBoundingBoxAscent;
```

Corollary: `line-height` below ~0.95 of the font size makes the box **shorter than the glyph**, so centring lies and a 64px numeral renders 73px wide. And correct optical alignment with `transform: translateY()`, never `margin` — a transform doesn't disturb the box model, so it can't knock a value off the spacing scale.

**8. Static checks are structurally blind to motion — and on this engine, so is every capture.** Every rule above reads the DOM at rest, where an entrance has finished and a transient overlay is `opacity: 0`. A "Checking…" overlay that painted *underneath* its own chip's inline text passed every static rule in that harness; the only artifact containing the bug was a frame captured 200ms in. That frame is obtainable in packaged Chrome and **not obtainable here** (see the limits table): Obscura executes no animation, so a mid-flight capture returns the at-rest frame. The class-restart trick — `el.classList.remove(c); void el.offsetWidth; el.classList.add(c)` — still applies the class, so what you capture is the *end state under that class*, which is a real and useful reading and is not a mid-flight frame. Say which one you took. On this engine, motion defects of this class are **not checked**, and the honest line names them rather than implying a frame nobody could capture.

**9. "At rest" is a state you have to reach, and then prove you reached.** The inverse of rule 8, and it manufactured four confident false findings on one recent review. **Scroll the whole document before probing** — a scroll-reveal system leaves every band below the fold at `opacity: 0`, so a full-page capture at load shows a working page as blank, and `loading="lazy"` images report `naturalWidth === 0` until they enter the viewport, so an image probe without a scroll pass reported five of eight as broken when all eight load. **Then drain `document.getAnimations()` and record what was still running** — in packaged Chrome. A contrast gate that fired 400ms into a 700ms reveal read a `#E85A2A` accent as `#6a2d18` and reported a surface getting *worse* after a fix that provably removed its failures: precise, internally consistent, and wrong. Recording the count is the load-bearing half — but **on Obscura that count is always 0**, which is the serialisation collision this rule was written to prevent, arriving as the rule's own output. So here, record the engine alongside the count (`getAnimations: 0 (Obscura — always 0, unusable)`), and treat any time- or scroll-dependent property as **provisional**: a skip link that measured invisible-while-focused had simply been sampled at 0ms of a `transition: top 220ms`. Where the reading matters, take it from a static end state you set yourself rather than from a timer.

**10. A DOM assertion that passes is not a component that looks right — and the gap is usually an unsized icon.** An inline `<svg>` with no intrinsic width or height fills whatever box it is dropped into. A validation-error icon added to a form's error row rendered as a **250px black disc under every field**, while every assertion about that form — three error messages, three `aria-invalid`, focus on the first invalid field, a live region present before submit — passed. The DOM was exactly right and the page was unusable. Any element you *add* while fixing behaviour gets a capture, not just the behaviour you were fixing; and every inline SVG carries explicit dimensions and a colour, because "it inherits" is only true of the ones that do.

**11. A scaled surface measures in two unit systems at once, and mixing them manufactures findings.** Inside a `transform: scale()` — a deck stage, a zoomable canvas, a design-tool preview, a print preview — `getBoundingClientRect()` returns *rendered* pixels while `getComputedStyle()` returns the *authored* value. A probe that compares a child's rendered edge against its parent's computed padding is subtracting one unit system from the other, and the difference it reports is not a defect. Measured Aug 2026 on a 1920px stage rendered at `s = 0.667`: an audit reported copy overflowing its container by exactly 52px on every slide, every card by 16px, every stat tile by 12px. Those are `104 × (1−s)/s`, `32 × (1−s)/s` and `24 × (1−s)/s` — each container's own padding, converted by the scale. Nothing was clipped anywhere.

The tell is that the reported overflow is **constant per container class and identical across every instance**; a real overflow varies with content. Convert first, then compare within one system:

```js
const s = stage.getBoundingClientRect().width / AUTHORED_WIDTH;      // the live scale
const cs = getComputedStyle(parent);
const inset = (parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth)) * s;
const overflowAuthored =
  (el.getBoundingClientRect().right - (parent.getBoundingClientRect().right - inset)) / s;
```

Everything downstream inherits this: a type-floor gate on a scaled surface must divide measured sizes by `s` before comparing them to a floor, and a contrast checker reading `fontSize` sees the authored size while the viewer sees `fontSize × s` — so hold body copy to 4.5:1 regardless of what the nominal size would permit.

**12. A renderer that drops content is not a layout that lost it.** A rasterizer that is not packaged Chrome fails in ways that look exactly like your bug: whole text runs render blank while the surrounding layout is perfect. Measured on Obscura, Aug 2026 — a 13-slide deck captured with two of six cards on one screen entirely empty and two more cut mid-sentence. The output was byte-identical at a 2-second and an 8-second settle, and byte-identical again with every image stripped, so neither paint timing nor decode memory explained it. The DOM said otherwise: all six strings present, at correct boxes, correct colour, correct size, and `elementFromPoint` at each heading returning the heading rather than something painted over it.

When a capture accuses a surface you believe is correct, audit the DOM before changing anything, and audit it for the four things the capture was supposed to show you:

```js
[...root.querySelectorAll('*')]
  .filter(el => (el.textContent || '').trim() && !el.children.length)
  .map(el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return { text: el.textContent.trim().slice(0, 30), box: [r.width, r.height],
             size: cs.fontSize, color: cs.color, visibility: cs.visibility,
             onTop: document.elementFromPoint(r.left + 4, r.top + 4) === el }; });
```

Text that is present, boxed, sized, coloured and on top is a correct surface being drawn wrongly. Report it that way: the layout is verified, the glyphs are not, so the visual claim belongs in "not checked" rather than in "looked at". An anomaly that survives a change which should have moved it, or that appears identically on two different surfaces, is the engine.

Two smaller members of the same family, both measured on that run. An SVG `<text>` sized with the `font-size` *attribute* reports `16px` from `getComputedStyle`, so a type-floor gate fails text authored at 30px — set SVG type with inline `style="font-size:30px"`, which is exact in every engine and is the number you actually wrote. And an inline `<span>` that is the only child of a plain block can return a zero-size rect, which reads as "invisible" to every probe — give a text leaf a block box wherever a gate has to measure it.

## Phase 1: Layout integrity checklist

Serve over HTTP (never `file://`), load the page, and check — at minimum — at these widths:

| Viewport | Width | Watch for |
|---|---|---|
| Mobile | 375px | The layout's true stress test — most breakage lives here |
| Tablet | 768px | Awkward two-column intermediates, orphaned sidebars |
| Desktop | 1280px | The design as intended |
| **Laptop** | **1440px** | **The width a "desktop" check skips, and the one most people are actually on** |
| Wide | 1920px | Missing `max-width` — content stretched to absurd measure |

Also pause at 2–3 in-between widths while resizing: breakpoint *transitions* break more often than breakpoints.

> **1440 is in the table because of a measured miss.** A six-tenant review found four sites whose
> header overflowed the viewport at **both** 1280 and 1440 while rendering correctly at 768,
> 1024 and 1920 — so a matrix of 375/768/1280/1920 that treated 1280 as "the design as intended"
> reported a working header on two sites whose primary CTA was *entirely off-screen* at every
> laptop width. A viewport matrix with a hole in the middle is a matrix that certifies the hole.

**The single-row header is the most reliable overflow in this class**, and it is worth its own
check because it fails silently in the direction nobody looks. A row of
`logo + N nav links + a fixed-width CTA` has an intrinsic width; when that exceeds the viewport
and nothing collapses, the flex row **pushes** rather than wrapping, the document gains a
horizontal scrollbar, and the last items — always the nav's tail and the CTA, i.e. the most
important control on the page — leave the screen to the right, where a user who scrolls
vertically will never look. Two tells:

```js
// Is the header the thing making the page wide?
const hdr = document.querySelector('header');
console.log(hdr.scrollWidth, innerWidth, document.documentElement.scrollWidth);
// Is any control laid out past the right edge?
[...document.querySelectorAll('header a, header button')]
  .filter(el => el.getBoundingClientRect().left >= innerWidth)
  .forEach(el => console.warn('OFF-SCREEN control:', el.textContent.trim()));
```

The fix is `min-width: 0` on the flex children plus a real collapse (drawer, overflow menu, or a
second row) at the width where the row stops fitting — **not** `overflow: hidden` on the header,
which hides the control instead of the scrollbar. And where the label lengths are data rather
than design — a tenanted product, a CMS, any localised UI — the trigger width is per-instance,
so a container query on the header beats a hand-picked breakpoint.

Per viewport, in severity order:

- **Overflow** — no unintended horizontal scrollbar; no content escaping its container; images inside their boxes; tables/code blocks scroll inside their own `overflow-x: auto` wrapper, not the page. Programmatic probe (run in the page console):

```js
[...document.querySelectorAll('*')].filter(el =>
  el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1
).filter(el => getComputedStyle(el).overflow === 'visible')
 .forEach(el => console.log('overflow:', el.tagName, el.className));
if (document.documentElement.scrollWidth > innerWidth) console.warn('PAGE overflows horizontally');
```

- **Overlap** — nothing unintentionally covering anything: sticky headers over anchored content, badges over text, absolutely-positioned decor over CTAs. Check with real content lengths, not just the happy sample.
- **Text integrity** — no clipping or mid-word breaks; long words/URLs wrapped (`overflow-wrap: break-word`); ellipsis actually appearing where truncation is designed; italic descenders not clipped; no widowed CTA labels.
- **Alignment drift** — grid/flex items evenly distributed; icons vertically centered with their labels; form labels attached to their fields; nothing off-grid by a few accidental pixels.
- **Stability (CLS/FOUT)** — reload and watch: no layout jump when images load (explicit `width`/`height`), no font flash reflow, skeletons matching the layout they replace.
- **Z-order** — dropdowns above cards, modals above everything, toasts above modals. If z-index values look ad-hoc, tokenize the scale: `--z-dropdown: 100; --z-sticky: 200; --z-overlay: 300; --z-modal: 400; --z-toast: 500`.
- **Media** — aspect ratios held (`object-fit`), no stretched or squashed images, embeds/iframes contained. **Measure rendered vs natural AR — don't trust the declared ratio:** an `<img>` with *both* a `height` attribute and a CSS `aspect-ratio` on its slot renders distorted (two definite dims → the attribute wins, `aspect-ratio` is ignored), so a photo silently over-crops to its natural height. Probe: `[...document.images].filter(i=>i.naturalWidth).map(i=>{const r=i.getBoundingClientRect();const c=Math.max((r.width/r.height)/(i.naturalWidth/i.naturalHeight),(i.naturalWidth/i.naturalHeight)/(r.width/r.height));return c>1.4?[i.src,c.toFixed(2)]:null}).filter(Boolean)` — anything over ~1.4× is a heavy crop; fix with `height:auto`.

## Phase 2: Screenshot playbook

Screenshots are the evidence; take them so they're cheap to retake and honest to compare.

- **One tall raw capture, then crop.** Screenshot the full page once with a tall viewport (e.g. 1400×5000, `fullPage: true`), then slice regions from the image. Re-cropping is instant; re-screenshotting costs a browser launch and render wait. Don't fight per-element clip captures.
- **The crop is the evidence; the full page is only the index.** A whole page scaled to fit a review shows you composition and nothing else. Every defect that survives to delivery lives at component scale. Produce one crop per component and open each — a page capture you skimmed is not coverage for the twelve components inside it.
- **Wait for the page to be actually done:** network idle plus an explicit wait for async renderers — charts and canvas need 2–4s after networkidle. A screenshot of a half-rendered chart generates a false finding.
- **`deviceScaleFactor` by purpose, not by habit.** Use **1** when the question is "what does a user see at 100% zoom" (that's what Phase 1 asks). Use **2–3** when the question is "is this component defective" — spacing, alignment, ink, hairlines and 1px drift are not resolvable at DPR 1, and a defect you cannot resolve is a defect you will clear. (Use 2+ for delivery assets too, per `make-an-animation.md`.)
- **Before/after pairs must match** — same viewport, same crop box, same states — or the comparison is worthless. Capture the *before* before editing; if you forgot, restore the prior version (`git stash` / `git checkout HEAD~1 -- <file>`), capture, then restore.
- **Interactive states need deliberate staging, and on this engine they are class-toggle captures rather than transition captures.** Hover: apply the hover styling by adding the class or setting the properties, then capture — Obscura runs no transitions, so waiting for one returns the same pixels and calling the result "the hover state after the transition" is a claim about a frame nobody captured. Selected-without-hover: set the selected state, make sure no hover class is also applied, then capture. Capture each state at both mobile and desktop widths when the interaction differs. Say in the report that these are end-state captures.
- **Console is part of the capture.** Collect JS errors/warnings on every load — a clean-looking page with a thrown exception is not verified.

## Phase 3: Fix loop

- **One issue per fix, verify, then the next.** Batch-fixing layout issues hides which change broke what.
- Prefer the structural fix over the suppressive one: `min-width: 0` on the flex child, `repeat(auto-fit, minmax(250px, 1fr))` on the grid, a real `max-width` on the container — before reaching for `overflow: hidden`, which silences the symptom and clips content.
- After each fix, **re-check the neighbors**: the other viewports, and the sections above/below the change (spacing fixes leak). Watch for CSS specificity collisions — a generic `.section` rule silently overriding component spacing is a classic generated-CSS failure.
- **A fix can starve its neighbour, so re-run the whole gate rather than the region you touched.** Measured Aug 2026: widening a table's unit column by 44px to stop a mono string colliding with the bar beside it left the next column 20px short, and its text ran into the following cell — a defect the same gate had reported clean one run earlier. Space inside a fixed-width container is conserved; every widening is also a narrowing somewhere, and the new victim is the column you were not looking at.
- **Three attempts per issue, then stop and report it** with the screenshot and the attempted fixes — an issue that survives three targeted fixes usually means the diagnosis is wrong, and that's a finding for the user, not a loop to hide in.

## Phase 4: Report

Findings as a table — *viewport · element · issue · severity (P0 breaks function / P1 degrades UX / P2 cosmetic) · fixed? · evidence screenshot*. Note anything observed but out of scope (third-party embeds, content edits). Never report "looks fine" without naming the viewports and states actually checked — an unchecked state is unverified, not passing.

Close with three lines, in this shape, because the last one is what keeps the first two honest:

```
Gates:       lint clean (0 critical, 0 major) · overflow probe clean · 0 console errors
Looked at:   12 component crops @2x, focus + selected end-states, 375/1280/1440
Not checked: motion, print and reduced-motion (engine runs no animations and
             setEmulatedMedia is inert), type fidelity (web fonts do not load),
             1920px, the chart's empty state
```

The first line is what a machine asserts. The second is what *you* assert, and it is only true for captures you opened. The third is never empty — **on this engine motion, print, reduced-motion and type fidelity are in it by default**, and if you believe the line is empty you have confused the scope of your rules with the scope of the artifact.

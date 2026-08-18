# GSAP Motion: Choreographed and Scroll-Driven Animation Beyond the Platform

Use GSAP when the platform toolkit in `motion-design.md` Phase 5 runs out: multi-step choreographed sequences that need runtime control (pause/reverse/seek), scrub-and-pin scroll storytelling, per-line/word text reveals, SVG draw/morph, drag with momentum, or physics. The design rules don't change — `motion-design.md` still governs *what* earns motion, budgets, and the review gate; this file is the heavier *how*.

**Escalation ladder:** CSS transitions → CSS scroll-driven animations / View Transitions / WAAPI → **GSAP**. Reach for GSAP on marketing/editorial/campaign surfaces and timeline pieces; product UI almost never needs it. State the escalation reason in the design-reasoning block.

## Phase 1: Load it — and the answer depends on where this ships

**All GSAP plugins are free, including commercial use** — since the Webflow acquisition there is no Club membership, license key, or private registry; formerly-paid plugins (SplitText, MorphSVG, DrawSVG, ScrollSmoother, Inertia…) ship in the public package. Never generate `.npmrc` auth-token or `npm.greensock.com` instructions — they're outdated.

**Free to use is not the same as loadable where you are shipping.** `delivery-surfaces.md` owns the contract; the short version is that a **published Artifact's CSP blocks every origin but its own, with no error**, so the three tags below produce a page that ships completely motionless and nothing in the console of the machine that built it ever says so. Pick the route before writing the timeline:

| Shipping to | How to load GSAP |
|---|---|
| A served page, a local file, an installable | Pinned CDN tags with SRI, exactly as below |
| A **published Artifact** | **Inline the minified source** into a `<script>` in the page — fetch it once with `curl -sf https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js` (or `npm pack gsap` and take `dist/`) and paste the contents between the tags. gsap.min.js is ~70 KB and ScrollTrigger ~40 KB, so both together are a rounding error against the 16 MB page budget. Or build the piece on the platform toolkit in `motion-design.md` Phase 5 instead |
| An npm project | `npm install gsap`, `import { ScrollTrigger } from "gsap/ScrollTrigger"` |

The inline route is one tag with the file's contents pasted in, and nothing else changes:

```html
<script>/* contents of gsap.min.js, pasted verbatim */</script>
<script>/* contents of ScrollTrigger.min.js */</script>
<script>gsap.registerPlugin(ScrollTrigger);</script>
```

For served delivery, pin CDN scripts and register plugins once:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js" integrity="sha384-HOvlOYPIs/zjoIkWUGXkVmXsjr8GuZLV+Q+rcPwmJOVZVpvTSXQChiN4t9Euv9Vc" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js" integrity="sha384-P8VzCVnT9NBUkMrpcIZrJbA7EBjJvh/fJS6PmP+4nLIM284DtsImIv8D0fFjIkeh" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/SplitText.min.js" integrity="sha384-xb96EMJeax+NLXMC88ZBa1xAeAW+kn+horHh/zFlbMLG2UPWhMJJSlv7fi57hS+Q" crossorigin="anonymous"></script>
<script>gsap.registerPlugin(ScrollTrigger, SplitText);</script>
```

Pin the version and keep the `integrity` + `crossorigin` attributes (SRI) — when using a different version or extra plugins (DrawSVG, MorphSVG, Flip, Draggable…), fetch the file and compute the hash (`curl -sf <url> | openssl dgst -sha384 -binary | openssl base64 -A`) rather than dropping the attribute. `scripts/design-lint.py` reports a pinned external as a *warning* and an unpinned one as a blocker, for exactly this reason.

In React, use the `useGSAP()` hook from `@gsap/react`; in any framework, create animations after mount inside `gsap.context(cb, containerEl)` — scoped selectors — and `ctx.revert()` on unmount.

**One verification note before you build.** The sanctioned capture engine runs **no** CSS animation and no GSAP timeline, so nothing in this file is verifiable by screenshot on this machine (`visual-verification.md` Phase 0). A paused master timeline you can `seek()` is therefore the only motion here that can be *seen* at all — which is one more reason Phase 6's timeline-as-engine pattern is the shape to reach for when the motion has to be reviewed rather than trusted.

## Phase 2: Core discipline (tokens still rule)

- **Transform aliases, not raw transform strings:** `x`, `y`, `scale`, `rotation`, `xPercent`, `rotationX/Y`, `transformOrigin`. **`autoAlpha` over `opacity`** for fades — at 0 it also sets `visibility: hidden`, so invisible elements stop eating clicks.
- **Set project defaults once** — GSAP's version of the motion tokens: `gsap.defaults({ duration: 0.6, ease: "power2.out" })`.
- **Ease vocabulary** mapped to the `motion-design.md` intents: entrances `power2.out`–`power3.out`; hero/dramatic reveals `expo.out`; moving/morphing on screen `power2.inOut`–`power3.inOut`; playful overshoot `back.out(1.7)` (sparingly — it's the marketing register); physical settle `elastic.out(1, 0.3)` (gestures only); constant motion and **all scrubbed animation** `"none"`. Never an `.in` ease on UI. Brand curves via `CustomEase.create("brand", ".17,.67,.83,.67")`.
- **Stagger** is a first-class value: `stagger: 0.06` or `{ each: 0.06, from: "center" | "edges" | "random" }` — same 30–80ms, ≤6–8 items budget as always; `gsap.utils.distribute()` spreads any value (scale, delay, opacity) across a set.
- Relative (`x: "+=20"`), function-based (`x: (i) => i * 50`), and `"random(-8, 8)"` string values keep repeated elements organic.

## Phase 3: Timelines (the choreography instrument)

Sequence with a timeline, never chained `delay`s:

```js
const tl = gsap.timeline({ defaults: { duration: 0.6, ease: "power3.out" } });
tl.from(".hero-kicker",  { autoAlpha: 0, y: 16 })
  .from(".hero-title",   { autoAlpha: 0, y: 24 }, "-=0.35")   // overlap the tail
  .from(".hero-cta",     { autoAlpha: 0, y: 12 }, "<0.15")     // 0.15s after previous START
  .add("settled")
  .from(".hero-media",   { autoAlpha: 0, scale: 0.96 }, "settled");
```

The **position parameter** is the craft: `"-=0.3"` overlap, `"<"` with-previous, `"<0.2"` offset-from-start, labels for named beats. Overlapping entrances (each starting before the last settles) read composed; strictly sequential entrances read like a slideshow. Store the instance for control (`tl.pause() / reverse() / seek("settled") / timeScale(2)`). Nest child timelines per scene into a master for long pieces. While iterating, `GSDevTools.create({ animation: tl })` gives a scrubber — dev only, never shipped.

Gotcha: stacking multiple `from()` tweens on the same property of the same element — set `immediateRender: false` on the later ones or the first one's start state is clobbered.

## Phase 4: ScrollTrigger (scroll storytelling)

The scroll grammar for marketing pages — reveals, scrubbed scenes, pins, horizontal journeys. Product UI scrolls quietly; these belong on editorial/campaign surfaces, budgeted by `depth-and-3d.md` Phase 6 (parallax ≤3 layers, one sticky/pinned scene per page).

- **Choose one linkage per trigger:** `scrub` (progress tied to scroll — use `scrub: 0.5–1` for a damped feel) or `toggleActions: "play none none reverse"` (discrete play on enter). Never both.
- **Entrance reveals for many items — batch, don't loop:**

```js
gsap.set(".card", { autoAlpha: 0, y: 32 });
ScrollTrigger.batch(".card", {
  start: "top 85%", once: true,
  onEnter: batch => gsap.to(batch, { autoAlpha: 1, y: 0, stagger: 0.08, overwrite: true })
});
```

- **Pinned scene** (the Apple-grammar sticky stage): pin the section, scrub a timeline through its states. **Animate children, never the pinned element itself**; keep `pinSpacing: true`.

```js
gsap.timeline({ scrollTrigger: { trigger: ".scene", start: "top top", end: "+=1500", scrub: 1, pin: true } })
  .to(".scene .phone", { xPercent: -30, scale: 1.1 })
  .from(".scene .caption-2", { autoAlpha: 0, y: 40 }, "<0.3");
```

- **Horizontal journey** (vertical scroll → horizontal travel): pin the wrapper, animate the inner track's `xPercent` with **`ease: "none"`** (mandatory — anything else breaks the scroll↔position mapping), pass that tween as `containerAnimation` to triggers inside the track. No pinning/snapping on containerAnimation triggers.
- **`snap`** progress to labels or increments for section-stop storytelling; **ScrollTrigger on the timeline or a top-level tween only, never on a child tween of a timeline.**
- **Hygiene:** `markers: true` during dev, removed for delivery; `ScrollTrigger.refresh()` after content/font/layout changes; create triggers in top-to-bottom page order (or set `refreshPriority`); kill triggers when removing elements.
- **Responsive + reduced motion in one construct:**

```js
gsap.matchMedia().add({
  desktop: "(min-width: 800px)",
  reduce:  "(prefers-reduced-motion: reduce)"
}, (ctx) => {
  const { desktop, reduce } = ctx.conditions;
  if (reduce) { gsap.set(".card", { clearProps: "all" }); return; }  // end states, no motion
  // build the full choreography (desktop ? … : lighter mobile variant)
});
```

Everything created inside reverts automatically when the query stops matching — this is the GSAP-native way to honour `motion-design.md` Phase 7.

- **Smooth scrolling (ScrollSmoother/Lenis) is a deliberate, stated choice** for cinematic marketing pieces only — it overrides native inertia and accessibility affordances. Never on product UI, dashboards, or docs. If used: ScrollSmoother needs the `#smooth-wrapper > #smooth-content` structure, fixed elements outside it.

## Phase 5: Text, SVG, and interaction plugins

- **SplitText** — the production version of kinetic type (`motion-design.md` Phase 5 rules hold: words/lines, not chars, for readability):

```js
SplitText.create(".headline", {
  type: "lines", mask: "lines", autoSplit: true,   // mask = built-in overflow-clip reveal wrappers
  onSplit: self => gsap.from(self.lines, { yPercent: 110, stagger: 0.08, duration: 0.7, ease: "power3.out" })
});
```

  `aria: "auto"` (default) keeps the split accessible (label on the container, split spans hidden from readers). `autoSplit` re-splits on font load/resize — create the animation inside `onSplit` and return it. Split only what you animate; `revert()` when done. Not for SVG `<text>`; avoid `text-wrap: balance` on split elements. **ScrambleText** is a one-shot terminal/hacker-aesthetic device — once per page, never on body copy.
- **DrawSVG** — line-drawing reveals for logos, diagrams, signatures: element needs a visible `stroke`; `gsap.from("#path", { drawSVG: 0, duration: 1.2 })`. Pairs with ScrollTrigger scrub for draw-as-you-scroll diagrams.
- **MorphSVG** — shape-to-shape morphs (icon states, blob backdrops, logo transforms): `gsap.to("#a", { morphSVG: "#b" })`; convert primitives first (`MorphSVGPlugin.convertToPath("circle, rect")`); if the morph crosses over itself, set `shapeIndex` (use `"log"` to find it) or `type: "rotational"`.
- **MotionPath** — travel along an SVG path (`motionPath: { path: "#route", align: "#route", autoRotate: true }`) for mapped journeys and orbiting accents.
- **Flip** — the FLIP technique as a service, replacing the hand-rolled version in `motion-design.md` Phase 5 when GSAP is already loaded: `const s = Flip.getState(".item")` → reorder/reparent/toggle class → `Flip.from(s, { duration: 0.5, ease: "power2.inOut", absolute: true })`. Grid→detail, filter reflows, tab morphs.
- **Draggable + Inertia** — gesture prototypes with momentum: `Draggable.create(".sheet", { type: "y", bounds: …, inertia: true, edgeResistance: 0.65 })` — honours the `motion-design.md` Phase 6 gesture rules (velocity dismissal, damped overdrag) without hand-rolling them. **Observer** normalizes wheel/touch/pointer for direction-driven scenes (slide shows advancing on swipe).
- **Cursor-following accents** (magnetic buttons, custom cursors, spotlight glows) use **`gsap.quickTo`** — one reusable tween per property, not a new tween per mousemove:

```js
const xTo = gsap.quickTo(".cursor-dot", "x", { duration: 0.35, ease: "power3" }),
      yTo = gsap.quickTo(".cursor-dot", "y", { duration: 0.35, ease: "power3" });
addEventListener("pointermove", e => { xTo(e.clientX); yTo(e.clientY); });
```

  Budget: one cursor device per page, `(hover: hover) and (pointer: fine)` only, and the native cursor stays visible unless the replacement is strictly larger and always on-screen. Magnetic pull on buttons: max ~8px translation, spring back on leave.

## Phase 6: Timeline pieces and export

A paused GSAP master timeline can *be* the engine behind `make-an-animation.md` — you get labels, nesting, and eases for free, and the export bridge drives it by seeking:

```js
const master = gsap.timeline({ paused: true });  // scenes as nested child timelines
window.__animStage = {
  duration: master.duration(),
  setTime: s => master.time(s, true),
  setPlaying: p => (p ? master.play() : master.pause())
};
```

Scrubber input maps to `master.progress()`; the mp4 export script from `make-an-animation.md` Phase 4 works unchanged. Everything must still derive from the timeline — no `setTimeout` side-channels, or export frames desync.

## Phase 7: Performance and review gate

All of `motion-design.md` Phase 7 applies, plus the GSAP-specific list. Flag on sight:

- Layout properties tweened (`width/height/top/left`) where `x/y/scale` would do · `will-change`/`force3D` sprayed on everything · hundreds of simultaneous tweens (batch, stagger, or virtualize) · new tweens created per-frame or per-mousemove (use `quickTo`) · `scrub` + `toggleActions` on one trigger · ScrollTrigger nested in a child tween · non-`"none"` ease on a containerAnimation · `markers` left in · missing `matchMedia` reduced-motion branch · smooth-scroll on a product surface · SplitText without `aria` handling or reverted styles · stray tweens/triggers not killed on teardown.

Then run the standard `motion-design.md` Phase 8 review — GSAP raises the ceiling, not the budget.

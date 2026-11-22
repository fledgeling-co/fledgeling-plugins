# The motion map

Every section has motion, and every motion has a plain path. This file holds the rules for
scroll-linked and entrance motion on a multi-section site; design-craft's `motion-design.md`
and `gsap-motion.md` hold the craft (tokens, easing, choreography, ScrollTrigger specifics).
Sources for each rule are in `evidence.md` under "Scroll motion".

## Pick the engine per effect

| Effect | Engine | Why |
|---|---|---|
| Fade or rise on entry, parallax, progress bar, a scrubbed reveal | CSS scroll-driven animation (`animation-timeline: view()` / `scroll()`) on `transform` and `opacity` | Runs off the main thread for compositor-friendly properties, so a busy page does not stall it |
| Hover, focus, press | CSS transitions | Nothing else is needed |
| Pinning a section, scrubbing a canvas or WebGL scene, a coordinated multi-element timeline | GSAP ScrollTrigger, created inside `gsap.matchMedia()` | CSS timelines cannot drive shader uniforms or a camera path, and pin spacing is where hand-written CSS breaks |
| Anything on `top`, `left`, `width` or `height` | Rewrite it as `transform` | Layout properties shift layout and cost CLS |

CSS scroll-driven animation shipped in Chromium (115), Safari 26 (threaded in 26.4, with pause,
progress-boundary and history-restoration fixes in 26.5) and Firefox 159 (27 October 2026). Older
installs remain, so wrap it in `@supports (animation-timeline: view())` with a plain fallback
where the content is visible without it. Firefox has required an explicit `animation-duration`
(a value such as `1ms`) for a timeline-driven animation to run; set it.

## Rules

1. **Keep native scrolling.** No `preventDefault` on `wheel` or `touchmove`, no smooth-scroll
   library intercepting the wheel, and no `ScrollTrigger.normalizeScroll()` as boilerplate: it
   moves scrolling onto the JavaScript thread. When a pin or library is used, test momentum,
   the mobile toolbar resizing the viewport, orientation change, keyboard scrolling, anchor links
   and back-button scroll restoration.
2. **Reserve the space a pin will take** before media loads, so the pin spacer does not move the
   page after paint. Size the hero with `100svh`, not `100vh`, so a phone's toolbar does not
   resize it as the visitor scrolls.
3. **Reduced motion removes the effect and its dependencies.** Under
   `prefers-reduced-motion: reduce`, release pins, stop decorative rendering, pause the hero video
   on its resting frame, and leave every element at its final position and full opacity. A
   reveal written as `opacity: 0` until a scroll trigger fires leaves a blank page when the
   trigger never runs; write the visible state as the default and the hidden start state inside
   `@media (prefers-reduced-motion: no-preference)`. Shortening durations is not removal.
4. **Two signature moments per site at most.** The rest enter quietly. More than two compete,
   and the plan check warns.
5. **A pause control for motion past five seconds.** Automatic motion that runs longer than five
   seconds beside other content needs a way to pause, stop or hide it (WCAG 2.2.2, Level A),
   whatever the reduced-motion setting. A looping hero video gets a visible, keyboard-reachable
   pause button; `site_audit.py` fails a looping autoplay video with none.
6. **No more than three flashes in any second** (WCAG 2.3.1, Level A), assessed on the delivered
   encode and across the loop seam. `clip_tools.py flashes` is a proxy for this, not a certified
   analysis.
7. **Exercise the controls while motion runs.** INP measures clicks, taps and key presses, not
   scrolling, so a good INP says nothing about scroll smoothness, and low CLS says nothing about
   vestibular safety. Click the navigation and the call to action mid-animation.

## The per-section motion block

```json
"motion": {
  "entrance": "headline lines rise 12px and fade, 60ms stagger",
  "scroll": "image drifts 24px slower than the page (view timeline)",
  "hover": "card lifts 2px",
  "signature": null,
  "reducedMotion": "everything present at rest; no drift; no fade"
}
```

Write `reducedMotion` as what the visitor sees, not as "disabled". The capture's reduced-motion
pass then checks that claim: it fails on any element still at opacity 0 after scrolling past it,
and on any video still playing.

## Touch

Pointer-follow and hover effects need a touch equivalent or a static state that carries the
same content, and both states need alt text and keyboard reach. A drag interaction needs a
single-pointer alternative (WCAG 2.5.7). The touch capture pass emulates a phone, but no tool
here tests a real finger dragging against page scroll; say so in the report.

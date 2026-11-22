1.
- Fidelity to notes: B stronger — [index.html](/tmp/index.html) copies class times/prices verbatim, leaves “[Email, phone and Instagram handle — waiting on you]”, sets `noindex` for “don’t publish yet”, and discloses “The film in the hero is a stand-in”; A invents “the best one gets glazed and fired”, “the same three wheels”, and `instagram.com/saltbushceramics`.
- Distinctive design: B stronger — [style.css](/tmp/style.css) builds a clay-pit stratigraphy system with the fixed `.ruler`, depth marks “00.0–18.6”, and hatched `.horizon` dividers; A is polished but uses familiar dark sticky-bar, pill-button, card, and marquee components.
- Phone-first booking path: A stronger — [index.html](/tmp/index.html) has a sticky header “Book”, hero and per-class Bookwhen links, plus the safe-area-aware fixed `.dock` booking bar after the hero; B has no persistent booking control and reserves 64px for its ruler.
- Video hero degradation: B stronger — [main.js](/tmp/main.js) keeps sources in `data-src` so reduced-motion visitors do not download the clip, swaps to `hero-rest.jpg`, handles a mid-session motion change, catches refused `play()` in `settle()`, and provides Pause/Play/Replay; A has good poster/fallback handling but no pause control while playing and still uses `preload="auto"`.
- Motion through the page: B stronger — [style.css](/tmp/style.css) gates scroll- and view-timeline motion behind `@media (prefers-reduced-motion: no-preference)` and `@supports`, animating `.ruler-mark`, class rules, fact borders, and section entries; A mainly has a ticker, hovers, and the dock.
- Accessibility: B stronger — [index.html](/tmp/index.html) treats the film as decorative with `aria-hidden="true"`, exposes a 44px Pause control, uses 44–48px targets and labelled sections; A autoplays video and an infinite ticker without pause controls and repeats ticker text for assistive technology.
- Robustness across browsers: A stronger — [index.html](/tmp/index.html) supplies direct WebM and MP4 `<source>` elements that work without JavaScript and [site.js](/tmp/assets/site.js) falls back if `IntersectionObserver` is absent; B requires JavaScript to load any video source.

2.
- A’s most serious defect: it makes an invented commercial promise for the $95 Wheel taster — “the best one gets glazed and fired” — when the notes only state that the six-week course includes firings.
- B’s most serious defect: its first video source, `hero-phone.mp4`, relies on a `media="(max-width: 767px)"` attribute that video `<source>` selection does not reliably honour, so desktop browsers can select the low-resolution phone clip instead of `hero.webm`/`hero.mp4`.

VERDICT: B

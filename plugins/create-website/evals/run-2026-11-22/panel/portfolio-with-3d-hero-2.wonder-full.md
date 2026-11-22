1.
- Distinctive premium design: B stronger — its poché/section system in `index.html` ties the hero “One mass, cut as you read” to the 1:1, 1:20 and 1:200 case-study scales, whereas A’s dark brass-and-serif treatment in `assets/css/main.css` is polished but generic luxury styling.
- 3D hero value and degradation: B stronger — `js/hero-scene.js` provides a labelled still image, WebGL2 and reduced-motion fallbacks, `webglcontextlost`/`webglcontextrestored` handling, off-screen and hidden-tab pausing, pixel ratio capped at 2, and an `aria-hidden` canvas; A caps pixel ratio and pauses off-screen but has no still, no context-loss handling, and still scroll-rotates under reduced motion.
- Honest handling of unsupplied facts: B stronger — it visibly leaves `[your name]`, `[your role]` and outcome figures as gaps and states “Sample copy. Every bracketed field is waiting on its owner”; A invents “Maren Avelo”, “Based in Lisbon”, “3.1M monthly actives”, quotations and results such as “−34%” mistaken-payment reports.
- Scroll motion: B stronger — it retains ordinary document flow, uses passive listeners, and guards scroll-timeline animation with `@supports` and `prefers-reduced-motion: no-preference`; A imposes a `260vh` sticky hero in `assets/css/main.css`, requiring prolonged scrolling before the work appears.
- Accessibility: B stronger — it has meaningful still-image text, 44px turn buttons and 48px actions, an `aria-hidden` canvas, skip link and copy-status region; A also hides its canvas, but `assets/js/hero.js` applies `visibility:hidden` to the hero copy containing the `h1` as the user scrolls.
- Browser and phone robustness: B stronger — it vendors Three.js, progressively enhances from `media/hero-still.png`, stacks its hero and work rows responsively, and does not depend on unsupported scroll timelines; A depends on a CDN Three.js module in `assets/js/hero.js` and loses the hero object entirely if that module or WebGL fails.

2.
- A: It fabricates the designer’s identity, clients, quotations, measurements and project history throughout, making the portfolio unsafe to publish and potentially professionally damaging.
- B: In `js/hero-scene.js`, `edges` is both a child of `group` and assigned `edges.rotation.copy(group.rotation)`, so the wireframe rotates twice relative to the black mass and visibly detaches from the solid it is meant to outline.

3.
VERDICT: B

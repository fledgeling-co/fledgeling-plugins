🫥 I read both from source only; nothing was rendered or run.

**1. Dimensions**

- **Distinctive premium design: A.** The "Poché" section-drawing idea carries the whole site: the `1:1 · 1:20 · 1:200` scale rail, the hatched `.gap` fields, and an SVG cut-line drawing per project. B's `main.css` is the familiar dark-and-brass template (Instrument Serif, grain overlay, icosahedron), well executed but interchangeable.
- **3D hero earns its place: A on concept, with a bug.** In `hero-scene.js` the clipping plane travels through the extruded mass as you scroll, which is the site's idea in 3D. But `edges` is a child of `group` and `edges.rotation.copy(group.rotation)` rotates it twice, so the hairline outline drifts off the solid. B's brass core, glass shell, rings and dust in `hero.js` are decorative and say nothing about the work.
- **Degradation: A.**
  - A has a still image with alt text (`media/hero-still.png`), `isWebGL2Available()`, a reduced-motion exit, `webglcontextlost` and `webglcontextrestored` handlers, an IntersectionObserver plus `document.hidden` pause, a pixel-ratio cap of 2, render-on-dirty, and labelled turn buttons.
  - B has only a `try/catch` that removes the canvas, leaving a 260vh pinned stage with nothing in it. It has no context-loss handler and no still. Under reduced motion it still rotates and dollies on scroll. It renders a transmission material every frame.
- **Honesty about unsupplied facts: A, clearly.**
  - A marks unknowns as `[your name]`, `[your role]` and `[the figures you are willing to publish — waiting on you]`, and its footer says "Sample copy. Every bracketed field is waiting on its owner." It still invents narrative specifics such as "eleven seconds long" and "24 mm".
  - B invents a person ("Maren Avelo", "Based in Lisbon", "Twelve years"), clients, quotes ("Estates director, project close") and metrics (−34%, −41%, 38s, 3.1M monthly actives), with nothing marking them as placeholder.
- **Scroll motion with native scrolling: A, narrowly.** Neither hijacks scroll; both use passive listeners. A's reveals and progress bar are CSS `animation-timeline` behind `@supports` and `prefers-reduced-motion: no-preference`, so content is visible without them. B pins the hero for 160vh of extra scroll and hides `[data-reveal]` content at `opacity: 0` until `site.js` runs, which includes all three work cards.
- **Accessibility: A.** A has the still's alt text, `role="img"` labels on every SVG, 44px turn buttons, `role="status"` on the copy message, and motion fully off under reduced motion. B has a skip link, focus rings and a good stretched-link card pattern, but its `aria-hidden` canvas has no alternative and its scroll-linked motion ignores the reduced-motion preference.
- **Robustness across browsers and phones: A, with one caveat.** A falls back to the still on any failure and uses `svh` and unguarded-feature-free CSS. B depends on the jsdelivr CDN, calls `ResizeObserver` and `IntersectionObserver` unguarded, and adds a fixed `mix-blend-mode` grain layer plus transmission rendering at DPR 2 on phones. The caveat is that A imports `../vendor/three-0.170.0.module.min.js` and `../vendor/WebGL-0.170.0.js`, and neither is in the delivered files.

**2. Most serious defect**

- **A:** No `vendor/` directory appears in the deliverable, so as delivered the module import fails and the site shows only the still. The requested rotating 3D hero is absent until three.js is added. If the files were only omitted from the listing, the worst defect becomes the double-rotated edge outline. The `mailto:[you@domain]` link is also dead.
- **B:** It presents a fabricated identity, clients, quotes and outcome figures as fact, under the heading "Measured, not claimed" and the note "Figures are from each project's own post-launch measurement". Publishing it as delivered would put false claims under the designer's name.

VERDICT: A

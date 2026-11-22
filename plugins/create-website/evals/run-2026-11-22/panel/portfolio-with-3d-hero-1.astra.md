🫥 1. **Dimension judgments**

- **Distinctive premium design — A.** The red cut line, black section drawings and scale rail in `index.html` give the phone, kiosk and hospital a shared visual language at 1:1, 1:20 and 1:200. B’s brass, glass and serif typography suggest luxury but say less about this designer’s work.
- **Purposeful 3D — A for the concept, B for the delivered rotation.** A’s `js/hero-scene.js` moves a cutting plane through the turning solid, explaining the drawings that follow. Its two local vendor imports are absent from the supplied files. B’s `assets/js/hero.js` can rotate its core and rings when the CDN loads. Both avoid video.
- **No WebGL — A.** `index.html` displays `media/hero-still.png` by default and hides it only after a successful frame. B removes the canvas on renderer failure but leaves “Scroll to turn” over a gradient.
- **Reduced motion — A.** `js/hero-scene.js` checks the preference before creating a renderer and listens for it to change. B suppresses idle spin and pointer tilt, but scrolling still rotates the object, moves the camera and fades the heading.
- **Context loss — A, with incomplete recovery.** A’s `webglcontextlost` handler brings back the still. Its restore handler never resets `firstFrame`, so it never marks the scene live again. B provides no explicit context-loss fallback.
- **Off-screen pausing — A, narrowly.** Both hero scripts skip rendering outside an observer margin but keep scheduling animation frames. A also checks `document.hidden` and skips unchanged frames, while B continuously renders its visible idle animation by default.
- **Capped pixel ratio — B, narrowly.** Both cap DPR at 2. B reapplies the cap in `resize()` when dimensions change, while A sets it once at startup.
- **Accessible canvas — A.** Both canvases use `aria-hidden="true"`. A also supplies descriptive poster alt text and a persistent plain-text caption. Its labelled turn buttons remain focusable even when the scene is unavailable.
- **Native scrolling — Tie.** Both hero scripts use passive `scroll` listeners and leave wheel, touch and keyboard scrolling to the browser. B’s `260vh` sticky hero makes the trip to the work longer.
- **Honesty about missing facts — A, with a substantial gap.** A marks `[your name]`, `[your role]` and outcome figures as placeholders, yet `work/bike-share-kiosk.html` still says “The kiosk flow shipped to the fleet.” B presents an invented identity and precise results under “Measured, not claimed.”
- **Accessibility — A.** Its “Skip to the work” link bypasses the hero, and `css/site.css` keeps the project links visible by default. B’s skip link lands before the hero, and `.js [data-reveal]` can leave focusable project links invisible if `assets/js/site.js` fails.
- **Browser and phone robustness — A for access to the portfolio.** A’s single-column layout, static case pages and poster survive script failure. B adjusts the camera for portrait screens, but its hero requires a CDN and unguarded observer APIs, and its `260vh` stage persists when 3D fails. Neither submission supplies browser or phone test results.

2. **Most serious defect in each**

- **A — The requested rotation cannot start as supplied.** `js/hero-scene.js` imports `../vendor/three-0.170.0.module.min.js` and `../vendor/WebGL-0.170.0.js`. Neither file is included, so the visitor gets the still and two inert turn buttons.
- **B — It attributes invented evidence to the designer and to a third party.** `case-banking-app.html` reports a 34% reduction in mistaken-payment reports, and `case-hospital-wayfinding.html` quotes an “Estates director, project close.” The brief supplied neither result nor testimony.

VERDICT: A
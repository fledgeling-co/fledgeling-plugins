🫥 1. **Dimension judgments**

- **Distinctive premium design — B.** The red cut line, black section drawings and scale labels in `index.html` and the three `work/` pages give the phone, kiosk and hospital a shared visual identity. A’s brass, glass and Instrument Serif convey luxury, but the sculpture could belong to another portfolio.
- **Purposeful 3D hero — B for concept, A for delivery.** B’s moving cut plane explains how to read the case illustrations. A’s `assets/js/hero.js` supplies a scroll-driven sculpture through a pinned CDN import. B’s two required local imports are absent from the supplied files. Both avoid video.
- **No WebGL — B.** `index.html` displays `media/hero-still.png` by default and hides it only after the first rendered frame. A’s `hero.js` removes the failed canvas, leaving a gradient and “Scroll to turn” in a 260vh section.
- **Reduced motion — B.** `js/hero-scene.js` selects the still before creating a renderer when the preference is active and stops rendering if it changes to reduced motion. A suppresses idle spin and pointer tilt but still rotates, dollies and fades the headline on scroll.
- **Context loss — B, with incomplete recovery.** B’s loss handler reveals the still and stops the loop. Its restore handler leaves `firstFrame` true, so rendering resumes without hiding the still again. A supplies no site-level context-loss fallback.
- **Off-screen pausing — B.** Both frame loops keep scheduling callbacks off-screen. B observes the object itself, skips rendering in hidden tabs and renders only when the view changes. A observes the entire hero and continuously renders its idle animation while visible.
- **Capped pixel ratio — Tie.** Both hero scripts cap `devicePixelRatio` at 2. A also recalculates the cap on resize.
- **Accessible canvas — B.** Both canvases use `aria-hidden="true"`. B adds descriptive still-image alt text, a persistent caption and labelled 44px turn buttons. Those buttons remain focusable and inert whenever the static fallback is active.
- **Honesty about missing facts — B.** B marks identity, role, team and outcome fields as placeholders and labels the copy as sample. Its unbracketed claim that the kiosk “shipped to the fleet” still reads as fact. A goes further, calling invented results “Measured, not claimed.”
- **Native scrolling — B.** Both use passive scroll listeners and preserve native input. B puts “See the work” in the hero and keeps the drawing in normal flow. A’s sticky 260vh stage spends much of the scroll on the sculpture after the headline disappears.
- **Accessibility overall — B.** Its home skip link lands directly on `#work`, its navigation wraps, and case content is visible by default. A’s skip link lands before the hero, while `.js [data-reveal]` can leave project links invisible but focusable if `site.js` fails.
- **Browser and phone robustness — B for reading, A for live 3D.** B’s `css/site.css` defaults to one column and gates scroll-timeline effects behind `@supports`. A’s live scene adjusts camera framing for portrait screens, though it depends on CDN access and unguarded observer APIs. Neither submission demonstrates device testing.

2. **Most serious defect in each**

- **A — Fabricated professional evidence.** `case-hospital-wayfinding.html` attributes a quotation to an “Estates director, project close” and reports a 41% drop in reception questions. Publishing it would put both an invented endorsement and an invented result under the designer’s name.
- **B — The requested interaction cannot start as supplied.** `js/hero-scene.js` imports `../vendor/three-0.170.0.module.min.js` and `../vendor/WebGL-0.170.0.js`. Neither file is included, so the page shows the poster and neither scrolling nor the turn buttons rotates it.

VERDICT: B
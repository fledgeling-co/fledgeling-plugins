# Depth and 3D: Dimensionality That Reads Crafted, Not Gimmicky

Add depth to a design — from disciplined shadow systems all the way to real-time 3D — choosing the cheapest technique that achieves the effect. Use this when a brief calls for "premium", "immersive", "wow", a hero that stands out, or explicitly for 3D/WebGL; and as the reference for shadows, glass, grain, and parallax in any hi-fi work.

**Depth is a hierarchy tool before it is a spectacle.** Agencies use dimensionality to make one thing feel touchable and everything else recede; slop uses it everywhere at once. Climb this ladder only as far as the brief needs — each rung costs more performance, accessibility risk, and maintenance than the last.

## Phase 1: Pick the rung

| Rung | Technique | Reach for it when |
|---|---|---|
| 1 | Elevation system (shadows, layering) | Always — every design has a z-axis story |
| 2 | Texture: grain, noise, mesh gradients | Flat design feels sterile; brand wants warmth/analog |
| 3 | Glass and translucency | Layered UI over rich content; dark "pro" aesthetics |
| 4 | CSS 3D transforms (tilt, flip, space) | One hero object or interaction deserves physicality |
| 5 | Scroll-linked depth (parallax, scaling scenes) | Marketing/editorial storytelling pages |
| 6 | Real-time 3D (WebGL/Three.js) | The 3D object IS the content, and rungs 1–5 can't fake it |

State the chosen rung and why in the design-reasoning block. Jumping to rung 6 for a testimonial page is the 3D version of a rainbow gradient.

## Phase 2: Elevation system (rung 1)

Define 3–4 elevation levels as tokens and map every surface to one — ad-hoc shadows are the depth version of random margins:

```css
--shadow-1: 0 1px 2px rgb(0 0 0 / .05);                                   /* resting card */
--shadow-2: 0 2px 4px rgb(0 0 0 / .05), 0 4px 12px rgb(0 0 0 / .06);      /* raised: dropdown, hover */
--shadow-3: 0 4px 8px rgb(0 0 0 / .06), 0 12px 32px rgb(0 0 0 / .10);     /* floating: modal, popover */
```

- **Layer two+ shadows per level** (tight+dark under, wide+faint around) — single-value box-shadows read flat. Craft leans on layered, low-opacity stacks.
- **Tint shadows with the surface hue** on colored backgrounds (`rgb(30 41 90 / .12)` on indigo, not gray) — gray shadows on colored grounds look dirty.
- **One light source.** All shadows fall the same direction (usually below). An inset highlight (`inset 0 1px 0 rgb(255 255 255 / .1)`) on dark surfaces sells the same light source.
- **Dark themes elevate with lightness, not shadow:** each level's surface gets ~4–6% lighter; shadows barely register on dark.
- Depth cues that cost nothing: overlap (badge over card edge, image breaking its container), scale, and blur-behind — the eye reads them as z-axis without a single shadow.
- **The nested enclosure (double bezel)** for one hero card or media frame: an outer shell (faint tinted background, hairline border, 6–8px padding, large radius) holding an inner core with its own surface, a 1px inset top highlight, and a **concentric radius — inner = outer − padding** (mismatched corners break the machined-hardware read). One per screen; a page of double-bezels is a page of none.

## Phase 3: Texture and mesh gradients (rung 2)

The fastest "designed, not generated" signal — flat AI output never has grain.

- **Film grain:** inline SVG turbulence overlaid at low opacity. Subtle is the whole game (0.03–0.06 opacity light themes, up to 0.08 dark):

```html
<svg width="0" height="0"><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2"/><feColorMatrix type="saturate" values="0"/></filter></svg>
<div class="grain"></div>
<style>.grain { position: fixed; inset: 0; pointer-events: none; filter: url(#grain); opacity: .05; mix-blend-mode: overlay; }</style>
```

- **Mesh gradients** (the organic multi-hue glow behind modern hero sections): 2–4 out-of-focus radial blobs, not a `linear-gradient` rainbow — keep hues adjacent on the wheel or tonal variations of the brand color, add grain on top to kill banding:

```css
.mesh { background:
  radial-gradient(40% 50% at 20% 30%, oklch(70% 0.12 250 / .5), transparent 70%),
  radial-gradient(50% 60% at 80% 20%, oklch(75% 0.10 300 / .4), transparent 70%),
  radial-gradient(60% 50% at 60% 80%, oklch(72% 0.11 210 / .35), transparent 70%),
  var(--bg); filter: saturate(1.05); }
```

- **SVG masks and `clip-path`** for editorial image treatments — arch crops, torn edges, text-shaped image fills (`background-clip: text`). One signature shape repeated beats five different tricks.

## Phase 4: Glass (rung 3) — earn it

Glassmorphism is one blur away from slop. It works only when there is **something worth blurring behind it** (imagery, a mesh gradient, moving content) — glass over a flat white page is decoration.

```css
.glass { background: rgb(255 255 255 / .08); backdrop-filter: blur(16px) saturate(1.4);
  border: 1px solid rgb(255 255 255 / .12); border-radius: 16px;
  box-shadow: 0 8px 32px rgb(0 0 0 / .25), inset 0 1px 0 rgb(255 255 255 / .08); }
```

Rules: the 1px light border and inset top highlight are what make it read as material rather than smudge; text on glass needs a contrast fallback (`@supports not (backdrop-filter: blur(1px))` → solid surface); maximum one glass layer stack — glass on glass on glass is unreadable; keep blurred areas small (backdrop-filter is expensive full-viewport). Two rules from Apple's material system carry over: **glass cannot sample glass** — adjacent glass elements (a toolbar's buttons, a chip row) share one glass region rather than each blurring independently, or they render visibly inconsistent; and **prominence comes from tint opacity**, not from stacking a second blur — a more important glass surface gets a stronger background tint, same blur. System-material tints (light/dark-adaptive translucency) beat fixed rgba values when the page supports both themes.

## Phase 5: CSS 3D (rung 4)

Real perspective, no library. Set `perspective` on the **parent** (600–1200px; smaller = more dramatic), `transform-style: preserve-3d` on the moving element.

- **Interactive tilt** (product cards, covers): rotate toward the pointer, max **6–8°** — past that it's a carnival. Add a moving specular highlight for the premium feel; spring back on leave; **pointer-fine only**, no tilt on touch:

```js
card.addEventListener('pointermove', e => { const r = card.getBoundingClientRect();
  const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
  card.style.transform = `perspective(900px) rotateY(${x * 8}deg) rotateX(${y * -8}deg)`;
  glare.style.background = `radial-gradient(60% 60% at ${(x + .5) * 100}% ${(y + .5) * 100}%, rgb(255 255 255 / .18), transparent 70%)`; });
card.addEventListener('pointerleave', () => card.style.transform = 'perspective(900px)'); // + transition: transform .5s var(--ease-out)
```

- **Flip** (cards, tiles): parent `perspective`, inner wrapper rotates 180° with `preserve-3d`, faces use `backface-visibility: hidden`. Flip on click, never hover (hover-flips trap the content).
- **Staged scenes:** layer siblings with `translateZ()` under one parent perspective and rotate the parent a few degrees on scroll/pointer — a cheap "living" hero composition.
- Keep text upright: type that stays rotated more than a few degrees becomes decoration; animate *to* flat.

## Phase 6: Scroll-linked depth (rung 5)

Use CSS scroll-driven animations (see `motion-design.md` Phase 5) — no scroll-jacking, native inertia preserved:

- **Parallax discipline:** 2–3 layers max, background moving 10–30% slower than content. Foreground parallax (elements crossing text) is almost always slop.
- **Depth-of-field storytelling:** hero image scales 1.1 → 1 and un-blurs 4px → 0 across the first viewport (`animation-timeline: scroll()`), content rises over it — one move, big perceived production value.
- **Sticky scenes:** a `position: sticky` stage that plays a state sequence while the section scrolls past (the Apple product-page grammar). One per page; announce progress for screen readers if the states carry content.
- When a scene needs scrubbing, pinning with precise start/end control, or a horizontal journey, use GSAP ScrollTrigger per `gsap-motion.md` Phase 4 — same budgets (≤3 parallax layers, one pinned scene per page).

## Phase 7: Real-time 3D (rung 6) — WebGL/Three.js

Only when the object is the content: product configurators, data sculptures, brand centerpieces. Prefer **one 3D moment** (a hero canvas) over 3D scattered through the page.

- Pin the CDN import and version (import map, `three@0.170.0` or current), `<canvas>` sized to its container, `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`.
- **Cheap materials, rich lighting:** `MeshStandardMaterial` + an environment map (`RoomEnvironment`) + one key light beats complex geometry with flat lighting. Soft shadows via a single `directionalLight` with tuned shadow radius.
- **Motion defaults:** slow idle rotation (one turn / 30–60s), damped `OrbitControls` (`enableDamping`, no zoom on page scroll — `enableZoom: false` unless it's a configurator), pointer-parallax of ±3–5°.
- The dependable non-model centerpiece: a displaced sphere/plane driven by simplex noise in the vertex shader with a two-color fresnel fill — the "living blob/wave" that carries most award-site heroes. Map its palette to the design tokens; add grain on top.
- **Fallbacks are mandatory:** a static render (`<canvas>` poster or image) when WebGL fails or `prefers-reduced-motion`; lazy-init on intersection; pause the render loop off-screen (`IntersectionObserver`) and on `visibilitychange`. Budget: the scene must idle below ~4ms/frame on a mid-range laptop — verify with the performance panel, not vibes.

## Phase 8: Review gate (run before shipping any depth work)

- One light source; every shadow from the elevation tokens; no single-layer default shadows on hero surfaces.
- Grain/glass/mesh present only where stated in the design-reasoning block — decoration that can't name its purpose comes out.
- Tilt ≤8°, parallax layers ≤3, one sticky scene, one glass stack, one WebGL canvas — exceeding any of these needs a written reason.
- `prefers-reduced-motion` verified: tilt/parallax/idle-rotation off, states jump; keyboard path unaffected by any pointer-driven effect; text contrast holds over every gradient/glass/image region (test the worst frame, not the first one).
- Performance measured in a browser, not inferred from the source: no layout thrash from scroll handlers (scroll-driven CSS or `transform`-only rAF), stable 60fps while scrolling the heaviest section. **Not measurable on the sanctioned engine** — Obscura runs no CSS animation and exposes no frame timing, so a frame-rate claim here is a claim about a machine you did not run. Verify the structural half (which properties animate, whether a scroll handler writes layout, whether the render loop pauses off-screen) and put frame rate in the "Not checked" line, or ask the user to check it in their own browser.

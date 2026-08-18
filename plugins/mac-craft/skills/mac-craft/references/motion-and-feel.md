# Motion & Feel — fluid-interface physics for interactive deliverables

Incorporated from Apple's WWDC design talks (*Designing Fluid Interfaces*, *The Details of UI Typography*, *Designing Audio-Haptic Experiences*, *Principles of Great Design*) as distilled in the apple-design skill. Read this whenever a deliverable is interactive — an HTML/CSS mock with hover/press states, a prototype, or a motion spec accompanying a static design. Static mocks still take the Materials & Depth and Typography sections plus a written motion spec.

**The through-line:** an interface feels alive when motion starts from the current on-screen value, inherits the user's velocity, projects momentum forward, and can be grabbed and reversed at any instant. Springs are the tool because they are inherently interruptible and velocity-aware.

## 1. Response and direct manipulation

- **Respond on pointer-down, not release.** `:active { transform: scale(0.97) }` with a ~100ms ease-out; waiting for click feels dead. Audit every latency on the input path (debounces, timers, tap delays).
- **Feedback is continuous during the interaction** — a drag, slider, or panel tracks the pointer 1:1 the whole way, respecting the grab offset (never snap to center on grab). Use Pointer Events + `setPointerCapture`; keep a short position/timestamp history so release velocity is known.

## 2. Springs, not durations

Every animation must be **interruptible**: never lock input during a transition; always animate from the *presentation* (live) value, never the logical target; avoid CSS transitions/keyframes for anything gesture-driven. Think in Apple's two parameters:

- **Damping ratio** — 1.0 = critically damped (no bounce); <1.0 overshoots. Default UI to **1.0**; allow bounce (~0.8) **only when the gesture carried momentum** (a flick/throw). Overshoot on a menu that faded in is wrong; on a card you threw it's right.
- **Response** — time-to-target in seconds (not a duration; settle time emerges). Snappy UI ≈ 0.3–0.4.

Apple's shipped values: move/reposition 1.0 / 0.4 · rotation 0.8 / 0.4 · drawer/sheet 0.8 / 0.3. Web mapping (Motion/Framer Motion): `{ type: 'spring', bounce: 0, duration: 0.4 }` as the house default; add `bounce: 0.2` only after momentum.

**Velocity handoff:** on gesture release, pass the pointer's velocity into the spring so there's no seam between dragging and animating (normalise by remaining distance if the API wants relative velocity). **Momentum projection:** choose the snap target from where the gesture was *going*, not where it ended — `projected = current + (v/1000)·d/(1−d)` with `d ≈ 0.998` — then spring there with the handed-off velocity. **Rubber-band** at boundaries (progressive resistance, never a hard stop): `over·dim·c / (dim + c·|over|)`, c ≈ 0.55.

## 3. Spatial consistency & hinting

- Enter and exit along the **same path**; mirror the easing on the return leg.
- **Anchor to the source:** menus/popovers/sheets scale from their trigger (`transform-origin` at the trigger), matching how macOS anchors popovers to their control.
- Intermediate frames should telegraph the outcome (grow toward the pointer, not just interpolate).

## 4. Materials & depth (the web translation of the platform's glass)

This section is the *implementation* of the kit's material rules (native-foundation: glass only on floating chrome; Scroll Edge Effect where content meets it):

- Floating chrome = a translucent layer: `background: rgba(255,255,255,.6); backdrop-filter: blur(20px) saturate(180%)` with a bright top hairline (light catching the material); content scrolls **under** it. Dark mode: near-opaque graphite translucency (large dark glass reads almost solid — that's correct).
- **Material weight encodes hierarchy** — bigger surfaces read thicker (stronger blur, deeper shadow). Never stack a light translucent surface on another (the web equivalent of glass-on-glass).
- **Scroll-edge fade, not a 1px divider,** where content meets floating chrome — and only where they actually overlap.
- **Materialize, don't fade:** animate blur radius + scale together on enter/exit so glass arrives as a material, not an opacity toggle.
- Modal = surface + dimming scrim + parent pushed back; parallel panel = translucency + offset, no scrim. Over translucent surfaces use vibrancy-style text (higher contrast, slightly heavier, small tracking bump) — never flat gray.

## 5. Typography details (applies to every deliverable, static included)

- **Tracking is size-specific, never one value:** tighten large display type (≈ −0.02em and beyond as it grows), keep body near 0, slightly positive at caption sizes. SF Pro does this optically — a fixed `letter-spacing` is wrong somewhere.
- Leading inversely tracks size (tight headings, loose body) — this matches the kit's ramp (26/32 → 13/16 → 10/13); use the kit values on macOS surfaces.
- Hierarchy = weight + size + leading **as a set**; emphasise with weight (Semibold on macOS). Scale layout with text (`rem`/`em` spacing) so Dynamic-Type-style scaling doesn't break it. `font: 100%/1.5 system-ui` is the floor; `font-optical-sizing: auto` on display type.

## 6. Feedback & accessibility floor

- Four feedback kinds: status, completion, warning, error — confirm meaningful actions, validate inline, warn before problems. Feedback fires on the causal event, same-frame across senses, and only where it earns its place.
- **Reduced motion ≠ no feedback:** `prefers-reduced-motion` → short cross-fades, no slides/springs/parallax; `prefers-reduced-transparency` → solidify the glass (raise opacity, drop blur — the platform does exactly this); `prefers-contrast: more` → near-solid surfaces + defined borders. Avoid full-viewport moving backgrounds and ~0.2Hz slow loops. These three media queries ship in every interactive mock, not as an afterthought.
- Animate only compositor-friendly properties (`transform`, `opacity`); `will-change` where motion is imminent.

## 7. The eight principles (review vocabulary)

Use these names when critiquing a design — they're the *why* behind every rule here and in the direction catalogue: **Purpose** (decide what not to build) · **Agency** (choices + easy undo; confirmation only for the genuinely destructive) · **Responsibility** (privacy asked at the right moment; anticipate misuse) · **Familiarity** (consistent metaphors; same-looking things behave the same; break a pattern only with proof) · **Flexibility** (contexts, devices, abilities; let people personalise) · **Simplicity, not minimalism** (hierarchy makes the important thing obvious; sometimes *adding* context simplifies) · **Craft** (every spacing/timing value defensible) · **Delight** (the result of the other seven — decide the emotion, reinforce it everywhere; never confetti on top).

## Quick reference

| Need | Value |
|---|---|
| Default UI spring | damping 1.0, response 0.3–0.4 (`bounce: 0`) |
| Momentum spring | damping ~0.8 — only after a flick |
| Flick landing | project with d≈0.998, then snap + hand off velocity |
| Interrupt | animate from the live on-screen value |
| Press feedback | on pointer-down, scale ~0.97, ~100ms |
| Drag threshold | ~10px hysteresis, then 1:1 |
| Glass chrome | blur(20px) saturate(180%) over scrolling content + scroll-edge fade |
| Display tracking | ~−0.02em, body 0, captions slightly + |
| Reduced motion | cross-fade ≤200ms, transforms off |

**Motion spec for static deliverables:** when the artifact is a static mock, append a short motion spec naming: entrance behaviour of floating surfaces (materialize), the spring defaults, which interactions carry momentum, and the reduced-motion fallbacks — so the implementer inherits the feel, not just the pixels.

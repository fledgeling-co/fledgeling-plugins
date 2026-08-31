# Motion Design: UI Motion That Feels Engineered, Not Decorated

Give interfaces motion that carries meaning — and review motion that doesn't. Use this whenever a design includes animation beyond a bare hover transition: entrances, exits, layout changes, scroll effects, page transitions, celebratory moments. For cinematic timeline pieces (product videos, animated stories, anything with a scrubber), use `make-an-animation.md` instead; for interaction-state basics (hover/active/focus), `interaction-states-pass.md` covers the floor and this file covers the ceiling.

**Motion is the fastest way to make a design feel expensive — and the fastest way to make it feel like a template.** Agencies win on motion because they treat it as engineering: budgeted, choreographed, interruptible, and mostly invisible. Decoration-first motion (things wiggling to look "premium") is an AI-slop tell.

## Phase 1: Decide what earns motion

Animate only when the user moves through **space, time, or state**: navigation, container morphs, progress, gesture follow-through, appearing/disappearing content. The articulation test: every transition should communicate a specific spatial relationship or continuity — "same thing, going deeper", "data arrived", "same items, new order", "something appeared". If you can't say what a transition communicates, cut it. Never animate to teach, to decorate, or to signal "premium" — research (Tversky 2002 meta-analysis) shows animation doesn't even beat static images for explaining things.

Budget by frequency of the action:

| Action frequency | Motion budget |
|---|---|
| 100+/day (keyboard shortcuts, command palette, typing feedback) | **None. Ever.** Never animate keyboard-initiated actions. |
| Tens/day (hover, list navigation, tab switches) | Remove or drastically reduce (≤150ms, subtle) |
| Occasional (modals, drawers, toasts, route changes) | Standard motion |
| Rare / first-time (onboarding, empty states, success celebration) | Delight allowed — this is where the budget goes |

One orchestrated moment beats scattered micro-interactions: **a single well-choreographed page load with staggered reveals creates more delight than twenty hover effects.** Spend the motion budget in one place, deliberately.

Motion *confirms* a state change; it never *performs* it. Update the UI optimistically, then let motion acknowledge it — don't make the user wait for a transition to finish before the app responds.

## Phase 2: Commit to a motion vocabulary (tokens, not vibes)

Define these once per project and use them everywhere — mixed durations and easings read as unintentional exactly like mixed border radii do:

```css
:root {
  /* Durations — UI stays under 300ms */
  --t-press: 120ms;      /* button press, toggles */
  --t-hover: 150ms;      /* hover, color, tooltips */
  --t-menu: 200ms;       /* dropdowns, popovers */
  --t-modal: 250ms;      /* modals, drawers (up to 500ms for full-screen) */
  --t-exit-scale: 0.7;   /* exits run ~70% of the entry duration */

  /* Easing — built-in keywords are too weak for polished motion */
  --ease-out:     cubic-bezier(0.23, 1, 0.32, 1);   /* entering elements */
  --ease-in-out:  cubic-bezier(0.77, 0, 0.175, 1);  /* moving/morphing on screen */
  --ease-drawer:  cubic-bezier(0.32, 0.72, 0, 1);   /* sheets and drawers */
}
```

Easing decision order: **entering/exiting → ease-out; moving or morphing on screen → ease-in-out; hover/color → ease; constant motion (spinners, marquees) → linear.** Never `ease-in` on UI — it delays the exact moment the user is watching. Mobile runs ~20–30% shorter than desktop.

Springs (Framer Motion, WAAPI spring approximations) when motion should feel physical: `{ type: "spring", duration: 0.5, bounce: 0.2 }`. Keep bounce 0.1–0.3, reserve real bounce for gestures and drag — springs' killer feature is keeping velocity when interrupted.

## Phase 3: Physicality rules

- **Nothing enters from `scale(0)`.** Start `scale(0.95)` + `opacity: 0` — objects in the world don't materialize from a point.
- **Popovers, menus, and tooltips scale from their trigger** — set `transform-origin` to the trigger side. Modals are exempt (they're a new context; center is right).
- **Press feedback:** `transform: scale(0.97)` on `:active`, `--t-press` duration. Buttons that don't acknowledge the press feel dead.
- **Asymmetric timing:** enter ~200ms, exit ~140ms — exits should read decisive, not lingering. Deliberate destructive actions invert this: hold-to-delete runs slow and linear (~2s) so the user can bail.
- **Nothing accelerates into a wall.** A thing that flies off-screen eases out; a thing that lands eases into place.

## Phase 4: Choreography

- **Stagger** small groups (30–80ms per item, ≤6–8 items). Stagger is seasoning: a whole page staggering item-by-item blocks the user; a hero's headline → subhead → CTA cascade guides the eye. Never let stagger delay interactivity. The AI tell here is the *uniform reflex* — one identical fade-up entrance applied to every section — not motion itself; each reveal should fit what it reveals, and suppressing the reflex is never a reason to ship a page with no motion at all.
- **Reveal-safety: never gate content visibility on a class-triggered transition.** Reveal animations must enhance an already-visible default (`opacity: 1` without JS; the animation class *adds* the entrance). Transitions pause in hidden tabs and headless renderers — gate visibility on them and the section ships blank in screenshots, prerenders, and background tabs.
- **Direction tells a story.** Enter from where the thing conceptually comes from (drawer from its edge, toast from the corner it lives in, next-step content from the direction of travel). Random directions break the spatial model. **Directional slides are reserved for hierarchical navigation** (list → detail, forward/back) **and ordered sequences** (prev/next photo, pagination — next slides from the right, previous from the left). Lateral moves between siblings (tab to tab, unordered views) get a crossfade or nothing — a directional slide there falsely implies spatial depth that doesn't exist.
- **Accordion/expand:** animate `grid-template-rows: 0fr → 1fr` (content wrapper `min-height: 0; overflow: hidden`) — smooth height without measuring.
- **Keep exiting elements mounted** and toggle a class/attribute; React unmounts skip exit transitions. CSS `transition-behavior: allow-discrete` + `@starting-style` give JS-free entry/exit for `display: none` toggles.
- **Interruptibility is non-negotiable** for anything rapidly triggered (toasts, toggles, hover cards): CSS transitions retarget mid-flight; CSS keyframes restart from zero. Use transitions or springs, not keyframes, for interruptible motion.

## Phase 5: The modern web motion toolkit

Use the platform before reaching for a library — these are what make current agency work feel current:

- **Scroll-driven animations (CSS):** `animation-timeline: view()` / `scroll()` for reveals, parallax, progress bars — zero JS, compositor-run. Reveal pattern: `animation: rise linear both; animation-timeline: view(); animation-range: entry 0% entry 60%;`. Reserve for marketing/editorial surfaces; product UI scrolls quietly.
- **View Transitions API:** `document.startViewTransition()` for page/state morphs; tag shared elements with `view-transition-name` for magic-move continuity. **It does NOT respect `prefers-reduced-motion` automatically — gate it yourself.** Shared-element morphs run longer than UI motion (300–500ms — the eye is tracking one object across space). Text morph gotcha: snapshots are rasters, so a morph between text at different sizes (`h3` → `h1`) scales the old snapshot up and ghosts — hide the old snapshot (`::view-transition-old { display: none }`) and show the new text at full resolution instead of crossfading the pair.
- **FLIP** for layout changes the platform can't yet morph (list reorders, grid → detail): measure First/Last, Invert with a transform, Play the transform to zero. Transform-only, so it's cheap.
- **WAAPI** (`element.animate()`) when you need JS control with CSS-level performance — runs off the main thread, unlike rAF loops.
- **Polish tricks:** ≤2px blur during a crossfade masks imperfect alignment; `clip-path: inset()` for reveals and tab-highlight slides; `translate` percentages are self-relative (how Sonner stacks toasts and Vaul nests drawers); a sticky header that hides on scroll-down and reveals on scroll-up returns the viewport to content without losing the nav (track scroll direction, toggle a transform class — never per-frame JS positioning).

**When the platform toolkit runs out, escalate to GSAP** (`gsap-motion.md`): multi-step choreographed timelines with runtime control, scrub-and-pin scroll storytelling, horizontal scroll journeys, per-line text reveals (SplitText), SVG draw/morph, drag with momentum. All GSAP plugins are free; **where it may be loaded from depends on the delivery surface** — see `delivery-surfaces.md`, because a CDN tag inside a published artifact is blocked with no error and the page ships motionless. The budgets and the review gate in this file still govern.

**Kinetic type** (heroes, decks, campaign pages only): animate words/lines, not letters, for readability (per-letter is a one-shot logo trick); split with spans, stagger 40–60ms; mask-reveal (overflow hidden line-boxes, text translates up into view) reads editorial; variable-font axis animation (weight/width on scroll or hover) is distinctive and cheap — one axis, subtle range. For production text splitting (font-load re-splits, built-in mask wrappers, aria handled), use GSAP SplitText per `gsap-motion.md` rather than hand-rolling spans.

## Phase 6: Gestures (when the prototype has them)

Dismiss on **velocity** (|distance|/ms > ~0.11), not distance thresholds — a fast short flick means "dismiss" more than a slow long drag. Add damping past boundaries (element follows at ~0.3× beyond the edge). Use pointer capture; ignore additional touches mid-gesture. Snap back with a spring that inherits release velocity.

## Phase 7: Performance and accessibility

- Animate **`transform` and `opacity` first**; blur, `backdrop-filter`, `clip-path`, mask, and shadow/glow are part of the premium-motion palette *when they materially improve the effect and hold 60fps* — verify on a real device, and never as a default. Never animate layout properties (width/height/top/margin) outside the grid-rows trick; never `transition: all`.
- Framer Motion's `x`/`y`/`scale` shorthands are not hardware-accelerated — animate the full `transform` string when it matters. Don't drive many children's transforms from one parent CSS variable (style-recalc storm).
- `will-change` only on elements about to animate; remove after.
- **Audit the motion posture of any imported component.** Library components (animation kits, hero effects, particle backgrounds) ship embedded motion defaults their API hides: cursor-reactive effects, auto-looping animations, scroll-driven behavior that ignores `prefers-reduced-motion`. At integration, read the component's source and check each of those explicitly — a component that fails the guardrails gets fixed or excluded, not shipped because it looked good in the demo.
- Loops: carousels stop after 3–5 cycles; skeleton shimmer only while loading; reward animations play once; any motion >5s needs a pause control (WCAG 2.2.2); nothing flashes >3×/sec; cancel ambient motion on route change.
- **`prefers-reduced-motion` means fewer and gentler, not zero:** keep opacity/color crossfades, drop movement/scale/parallax, and jump timeline pieces to their end state. Deck builds apply instantly but click-gating stays (reveal order is content). Gate hover-triggered motion behind `@media (hover: hover) and (pointer: fine)`.

## Phase 7.5: Motion claimed, motion shown

If the direction contract's motion mode is Expressive or Playful, the page has to actually move: one orchestrated entrance, or scroll-reveal on key sections, or hover physics on the primary action. A static page that claimed a loud motion mode is unfinished — drop the mode to Quiet and ship the still composition, or finish the motion. Never half-build a ScrollTrigger that cuts off.

Every animation still has to pass Phase 1 (it communicates space, time, or state). GSAP because GSAP is available is not a reason. Horizontal marquees: at most one per page.

Pin/scrub patterns pin at the viewport top (`start: "top top"`), not `"top center"` or `"top 80%"`. The common failure is a stack that starts transforming before it is pinned, so the visitor sees half a slide. Canonical skeletons live in `gsap-motion.md`. Do not attach `window.addEventListener('scroll')` — use ScrollTrigger, CSS scroll-driven animation, IntersectionObserver, or Motion `useScroll`.

Reduced motion remains mandatory for anything beyond a hover transition: `prefers-reduced-motion` wraps the lot, and the still composition is designed, not the motion with the duration zeroed.

## Phase 8: Review procedure (run on any motion-bearing deliverable)

Flag on sight, in this order of severity: content visibility gated on a class-triggered transition (reveal-safety — ships blank sections) · `transition: all` · animation on keyboard-initiated actions · `ease-in` on UI · `scale(0)` entrances · center-origin popovers · keyframes on interruptible elements (toasts/toggles) · layout-property animation · image `transform` on hover (incl. parent `group-hover`) · >300ms UI motion without justification · ungated hover motion · looping decoration · the uniform section-reveal reflex (identical entrance on every section) · View Transitions without reduced-motion handling.

Fix with the remedial hierarchy — cheapest lever first: **1 delete the animation → 2 reduce duration/distance → 3 fix easing → 4 fix origin/physicality → 5 make it interruptible → 6 move it to transform/opacity → 7 asymmetric timing → 8 polish (blur, stagger) → 9 a11y and cohesion (tokens)**. Report findings as a Before / After / Why table and end with a verdict: ship, or the specific items that block.

Debug like an animator: slow everything 2–5× (DevTools animation panel), step frame-by-frame, test gestures on a real device, and look again the next day with fresh eyes.

### Motion is invisible to every static check you own

A lint, a screenshot, a computed-style probe, a review subagent reading the DOM — all of them see the artifact **at rest**. At rest an entrance has finished and a transient overlay is `opacity: 0`. A whole class of bug lives in neither state and therefore in none of your evidence.

Concretely: a status chip's "Checking…" overlay painted *underneath* the chip's own inline text, so a real capture briefly rendered `CONSISTEN` + `CHECKING…` + `RRENT DRAFT` superimposed. Every static rule passed. The only artifact that contained the bug was a frame captured 200ms in. (The cause was a full-cover `position: absolute` overlay with `z-index: auto` inside a `position: relative` parent that also held inline text — **give transient overlays an explicit `z-index`**, never rely on default paint order.)

So verify motion in three passes — **and know that this machine's engine can run none of them**. Obscura executes no CSS animation or transition, and `setEmulatedMedia` is accepted and inert (measured 13 Aug 2026), so all three come back clean on a broken page. The passes are here because they are correct against packaged Chrome and because a user's own browser can run them; on this engine motion goes in the "Not checked" line.

1. **At rest, under `media: print`** — anything invisible here is content that will be missing from the export. *Not emulable here*: use the grep in `make-a-doc.md` Phase 3, or better, invert the states so there is nothing to check.
2. **At rest, under `prefers-reduced-motion: reduce`** — the same check, for the audience that asked not to see motion. *Not emulable here*: check the `@media` block exists and covers every animation in the file, and say that is what you checked.
3. **Mid-flight frames.** Restart the animation deterministically rather than waiting on an observer or a timer, then capture every ~200ms and **open every frame**:

```js
el.classList.remove('seen');
void el.offsetWidth;          // force reflow — this is what restarts the animations
el.classList.add('seen');
```

*Not obtainable here*: with no animation running, every frame equals the end state under that class. Capturing it is still useful — it proves the end state is correct — but it is an **end-state capture**, not a mid-flight frame, and it must be reported as one. The only honest way to see a mid-flight defect on this machine is to set the intermediate state yourself, by hand, and capture that.

No rule you write, present or future, can see what only exists at t=200ms — and on this engine, neither can any capture.

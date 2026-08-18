# Gates — performance and motion

Tier 1. Greppable or measurable. No visual judgment needed.

## Core Web Vitals

Blocking thresholds, at the **75th percentile** across device types:

| Metric | Good | Measures |
|---|---|---|
| LCP — Largest Contentful Paint | ≤ 2.5s | Loading |
| INP — Interaction to Next Paint | ≤ 200ms | Responsiveness |
| CLS — Cumulative Layout Shift | ≤ 0.1 | Visual stability |

Treat these as UX gates, not SEO metrics. A visually sophisticated interface that fails LCP or INP feels sluggish, and CLS is experienced as content jumping under the cursor. A design that passes every heuristic check and fails CWV has not passed review.

Sources for measurement: Chrome UX Report, DevTools, PageSpeed Insights, Search Console. Lab numbers from a single run are indicative, not conformant — say which you used.

Related budget: 60fps target, and animation that costs frames is a finding even when the CWV numbers pass.

## Motion anti-patterns — flag on sight

These are greppable in source or detectable in computed styles. Ordered by severity.

**Content visibility gated on a class-triggered transition.** The highest-severity item here. Reveal animations must enhance an already-visible default: `opacity: 1` without JS, with the animation class *adding* the entrance. Transitions pause in hidden tabs and headless renderers, so gating visibility on them ships blank sections in screenshots, prerenders, print and background tabs.

The structural fix inverts the states — the resting style *is* the final style, and the "from" state lives only inside `@keyframes`:

```css
/* right — at rest the row is visible; the keyframes only say where it came from */
.row { opacity: 1; transform: none }
@keyframes fadeUp { from { opacity: 0; transform: translateY(8px) } }
.section.seen .row { animation: fadeUp 650ms var(--ease-out) both }

/* wrong — at rest the row is invisible. Kill the animation and the row is GONE. */
.row { opacity: 0 }
@keyframes fadeUp { to { opacity: 1 } }
```

Written that way, `animation: none` yields the settled design, and print, reduced-motion and JS-disabled fallbacks are correct by construction.

**The rest of the flag-on-sight list:**

- `transition: all` — performance and unintended-property animation. Name the properties: `transition-property: scale, opacity`
- `will-change: all` — same. `will-change` only on `transform`, `opacity`, `filter`, and removed after
- `scale(0)` entrances, or pure-fade entrances. Objects do not materialise from a point: start `scale(0.9–0.97)` plus `opacity: 0`
- `ease-in` on UI. It delays the exact moment the user is watching. Built-in keyword easings are generally too weak for polished motion
- Animation on keyboard-initiated actions, command palettes, or anything triggered 100+ times a day
- UI motion over 300ms without a stated reason
- `transform-origin: center` on a trigger-anchored popover, menu or tooltip. These scale from their trigger; modals are exempt because they are a new context
- Keyframes on interruptible elements — toasts, toggles, rapid triggers. CSS transitions retarget mid-flight; keyframes restart from zero
- Animating layout properties: `width`, `height`, `margin`, `padding`, `top`, `left`. The exception is the `grid-template-rows: 0fr → 1fr` accordion trick
- Framer Motion `x` / `y` / `scale` shorthands under load — not hardware-accelerated; animate the full `transform` string where it matters
- A parent CSS-variable update driving many children's transforms — style-recalc storm
- Missing `prefers-reduced-motion` handling on anything that moves
- Ungated `:hover` motion. Gate behind `@media (hover: hover) and (pointer: fine)`
- Symmetric press-and-release timing. Press and release want different durations
- Simultaneous entrances that want a stagger
- View Transitions API without reduced-motion handling — it does **not** respect `prefers-reduced-motion` automatically
- Image `transform` on hover, including via a parent `group-hover`. The image is not the action target; animate the card's background, border or shadow instead

## Duration and easing reference

Two source traditions agree on the ceiling for state changes and differ slightly on entry/exit. Both are recorded; treat the range as the range.

**State changes** (hover, focus, active, colour): 150–300ms. Faster than ~150ms reads as a snap; nothing at all reads as broken.

**Entry/exit** (modals, drawers, toasts): 200–500ms. UI stays under 300ms unless the surface is full-screen, where up to 500ms is composed rather than laggy. Shared-element morphs run longer, 300–500ms, because the eye is tracking one object across space.

A workable token set:

```css
:root {
  --t-press: 120ms;      /* button press, toggles */
  --t-hover: 150ms;      /* hover, colour, tooltips */
  --t-menu:  200ms;      /* dropdowns, popovers */
  --t-modal: 250ms;      /* modals, drawers — up to 500ms full-screen */

  --ease-out:    cubic-bezier(0.23, 1, 0.32, 1);   /* entering */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* moving/morphing on screen */
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* sheets and drawers */
}
```

Easing decision order: entering/exiting → `ease-out`; moving or morphing on screen → `ease-in-out`; hover and colour → `ease`; constant motion (spinners, marquees) → `linear`. Never `ease-in` on UI. Mobile runs roughly 20–30% shorter than desktop.

Platform-specific fallbacks, where springs are unavailable: desktop 150–200ms; mobile ~300ms; entering elements ~225ms decelerating; exiting ~195ms accelerating. Exits generally run ~70% of the entry duration — decisive, not lingering. Deliberate destructive actions invert this: hold-to-delete runs slow and linear (~2s) so the user can bail.

**Springs.** Material 3 has deprecated its fixed easing/duration system in favour of a spring-based motion physics system, which makes `transition: all 0.3s ease` a legacy artifact worth flagging. Spring presets: `{ type: "spring", duration: 0.5, bounce: 0.2 }` or `{ mass: 1, stiffness: 100, damping: 10 }`. Keep bounce 0.1–0.3 and mostly avoid it — reserve real bounce for gestures and drag, where momentum justifies it. The reason springs matter is interruptibility: they retain velocity when interrupted, keyframes restart.

**Stagger:** 30–80ms between items for routine reveals, up to ~100ms for a staged one-shot entrance, ≤6–8 items. Stagger is seasoning — a whole page staggering item by item blocks the user; a hero's headline → subhead → CTA cascade guides the eye. Never let stagger delay interactivity.

## Motion budget by frequency

The sharpest single heuristic here. Decoration density should *fall* as interaction frequency rises, and generated UI reliably does the inverse.

| Action frequency | Budget |
|---|---|
| 100+/day — keyboard shortcuts, command palette, typing feedback | None. Never animate keyboard-initiated actions |
| Tens/day — hover, list navigation, tab switches | Cut or drastically reduce (≤150ms, subtle) |
| Occasional — modals, drawers, toasts, route changes | Standard motion |
| Rare / first-run — onboarding, empty states, success | Delight permitted; spend the budget here |

One orchestrated moment beats scattered micro-interactions. A single well-choreographed page load with staggered reveals creates more delight than twenty hover effects.

Related: perceived-instant is ~100ms. Below that, adding a transition makes an interaction feel *slower*, not smoother. Instant interactions do not want animation.

## Reduced motion

`prefers-reduced-motion` means **fewer and gentler, not zero.** Keep opacity and colour crossfades; drop movement, scale and parallax; jump timeline pieces to their end state. Removing all feedback is its own failure — the user asked for less motion, not less information.

Also honour `prefers-reduced-transparency` (solidify glass: raise opacity, drop blur) and `prefers-contrast: more` (near-solid surfaces, defined borders) where the design uses translucency.

Large panning or scaling motion is a vestibular trigger specifically; treat full-viewport movement as higher-severity than a local transition.

## Fix hierarchy

When a motion finding needs a fix, prefer the earliest lever that works — each later one costs more and changes more:

1. Delete the animation
2. Reduce duration or distance
3. Fix the easing
4. Fix origin and physicality
5. Make it interruptible
6. Move it to `transform` / `opacity`
7. Asymmetric timing
8. Polish — blur masking, stagger, `@starting-style`
9. Accessibility and cohesion with the rest of the system

"The strongest move is often to delete it" is not rhetorical. Motion that cannot state what it communicates should not survive review.

## Motion is invisible to every static check

A lint, a screenshot, a computed-style probe, a subagent reading the DOM — all see the artifact **at rest**. At rest an entrance has finished and a transient overlay is `opacity: 0`. A whole class of bug lives in neither state.

The documented case: a status chip's "Checking…" overlay painted *underneath* the chip's own inline text, so a real capture briefly rendered `CONSISTEN` + `CHECKING…` + `RRENT DRAFT` superimposed. Every static rule passed. The only artifact containing the bug was a frame captured 200ms in. The cause was a full-cover `position: absolute` overlay with `z-index: auto` inside a `position: relative` parent that also held inline text — so give transient overlays an explicit `z-index` rather than relying on default paint order.

Verify motion in three passes — **none of which is available on Obscura.** Read the branch below before running any of them.

1. **At rest under `media: print`** — anything invisible here is content missing from any PDF export
2. **At rest under `prefers-reduced-motion: reduce`** — the same check for the audience that asked not to see motion
3. **Mid-flight frames** — restart the animation deterministically, capture every ~200ms, and open every frame:

```js
el.classList.remove('seen');
void el.offsetWidth;          // force reflow — this is what restarts the animation
el.classList.add('seen');
```

No static rule, present or future, can see what only exists at t=200ms.

**On Obscura, record all three as skipped rather than performing them.** `Emulation.setEmulatedMedia` is accepted and inert — `matchMedia('print')` stays false and the cascade does not change — so passes 1 and 2 would write the ordinary screen render under a name claiming otherwise, and a screenshot named `page-print.png` that is really the screen render is worse than saying the check did not run. CSS animations and transitions never execute, so pass 3 would produce N identical stills and the reflow trick restarts nothing; `run_review.py --motion` hard-exits with that reason rather than letting it happen. `capture_states()` writes a `statesSkipped` list naming each, and the report template carries all three as standing items in "Needs verification". The whole motion class needs a different engine, and *not performed* is the correct thing to report.

## Loops and ambient motion

- Carousels stop after 3–5 cycles
- Skeleton shimmer only while loading
- Reward animations play once
- Any motion over 5s needs a pause control (WCAG 2.2.2)
- Nothing flashes more than 3×/second
- Cancel ambient motion on route change
- Audit imported components: animation kits, hero effects and particle backgrounds ship embedded motion defaults their API hides — cursor-reactive effects, auto-loops, scroll behaviour ignoring reduced-motion. Read the component source at integration rather than trusting the demo

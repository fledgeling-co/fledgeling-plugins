# Frontend Web Checklist — HTML / CSS / React Components

Covers the client-side surface: markup semantics, CSS, React component quality, and accessibility. Loads for diffs touching `*.tsx`/`*.jsx` client components, `*.css`/`*.scss`/`*.module.css`, Tailwind class changes, and plain `*.html`. For Next.js **server-side** concerns (RSC boundaries, Server Actions, caching, hydration) load `nextjs-checklist.md` — this file deliberately does not duplicate it.

Lens keywords `components` and `a11y` route here even when the depth's default checklist set wouldn't load it.

---

## Contents

- [1. Component quality](#1-component-quality)
- [2. Hooks & state](#2-hooks--state)
- [3. Rendering correctness](#3-rendering-correctness)
- [4. Accessibility (a11y)](#4-accessibility-a11y)
- [5. CSS & layout](#5-css--layout)
- [6. Forms & inputs](#6-forms--inputs)

---

## 1. Component quality

- **Prop drilling vs. composition**: a prop threaded through 3+ layers untouched — flag for composition (`children`, context) only when the diff created the drilling.
- **Boolean-prop explosion**: components gaining a 4th+ boolean prop (`isCompact`, `isInline`, `hideLabel`…) — variants have outgrown the API; suggest a `variant` union.
- **Copy-paste components**: the diff adds a component near-identical to an existing one (grep for similar JSX structure/name before claiming); cite both and the divergence.
- **Business logic in JSX**: multi-step data transformation inline in the render body that belongs in a hook, selector, or the server.
- **Non-reusable hardcoding**: literal colors/spacing/z-index values in a repo that has design tokens or a theme — cite the token file the diff should have used.
- **Missing error/empty/loading states**: a component that fetches or receives async data but renders only the happy path.
- **Index-as-key** on lists that reorder, insert, or delete — causes state bleed between rows. Static, never-reordered lists are fine.

## 2. Hooks & state

- **Missing/wrong effect dependencies**: values read inside `useEffect`/`useMemo`/`useCallback` absent from the dep array (stale closure), or object/array literals in deps causing every-render re-fires.
- **Effects without cleanup**: subscriptions, listeners, timers, observers, `AbortController`-less fetches — anything set up in an effect must be torn down.
- **Derived state stored in state**: `useState` + `useEffect` to mirror a prop or compute from other state — compute during render or `useMemo` instead.
- **State that belongs elsewhere**: server data cached in component state when the repo uses a query library; URL-shaped state (filters, tabs, pagination) in `useState` where the repo pattern is searchParams.
- **setState during render** or unconditional `setState` in an effect (render loop).
- **Custom hooks returning unstable identities**: fresh objects/functions each call, breaking consumers' memoization.

## 3. Rendering correctness

- **Conditional hooks**: any hook after an early return or inside a condition/loop.
- **`&&` rendering with numeric left side**: `count && <X/>` renders `0` — use ternary or `> 0`.
- **Uncontrolled↔controlled flips**: an input whose `value` can transition between `undefined` and a string.
- **Direct DOM mutation** alongside React-managed state (`document.querySelector(...).classList` on rendered nodes).
- **Date/locale/random in render** producing different output per render or between server and client (belongs in effect/state, or is a hydration bug — route to nextjs-checklist if SSR).
- **Unstable component definitions**: a component defined inside another component's body — remounts on every parent render, losing state.

## 4. Accessibility (a11y)

- **Click-divs**: interactive behavior on `div`/`span` without `role`, `tabIndex`, and key handlers — should be `button`/`a`. A `<button>` costs less than the ARIA to fake one.
- **Buttons vs links**: navigation on `onClick` + `router.push` where an `<a>`/`<Link>` belongs (breaks middle-click, cmd-click, SEO).
- **Missing accessible names**: icon-only buttons without `aria-label`; images without meaningful `alt` (decorative images need `alt=""`); form controls without an associated `<label>`.
- **Focus management**: modals/drawers/menus the diff adds without focus trap or return-focus-on-close; focus-visible outline suppressed (`outline: none`) with no replacement.
- **Semantic structure**: heading levels skipped, lists built from `div`s, tables built from grid `div`s when the content is tabular.
- **Color-only meaning**: state (error/success/selected) conveyed by color alone with no text/icon/`aria` signal.
- **Motion/live regions**: dynamic status updates (toasts, async results) invisible to screen readers — needs `aria-live`; animations without `prefers-reduced-motion` consideration are a LOW.

## 5. CSS & layout

- **Specificity escalation**: `!important` or ever-deeper selectors added to beat existing rules — flag the underlying conflict.
- **Z-index arms race**: a new z-index above the repo's existing max, or magic values (`z-index: 9999`) where a scale/token exists.
- **Hardcoded dimensions that break content**: fixed heights on text containers, widths that clip at 200% zoom or on translation-length text.
- **Overflow traps**: nested scroll containers, `overflow: hidden` clipping focus rings or dropdowns.
- **Global leakage**: new unscoped global selectors in a repo using CSS modules / Tailwind / styled-components; styles targeting another component's internals.
- **Responsive regressions**: absolute positioning or fixed grid columns that ignore the repo's breakpoint system; missing mobile handling on new layout the repo's conventions cover.

## 6. Forms & inputs

- **Client-only validation**: validation existing solely in the browser for data a server mutation accepts (route the server half to security-checklist).
- **Submit-state gaps**: no disabled/pending state on submit (double-fire), no error surface for failed submission.
- **Unpersisted user input**: destructive navigation (tab switch, modal close) discarding a filled form without warning — MEDIUM at most.
- **Native behavior fights**: `preventDefault` on form submit and then hand-rolling what `action`/`method` or the repo's form library already does.

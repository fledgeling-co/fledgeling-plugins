# Make a Prototype: Interactive Clickable Prototype

Build a working interactive prototype — clickable, navigable, with real state and feedback. Use this when the user asks for a prototype, mockup, demo, or "make it interactive."

**Prototypes interact.** Static screenshots strung together with `<a>` tags don't count. The point is to test the flow with real interaction — clicking, typing, validating, succeeding, failing.

## Phase 1: Discovery

Confirm before building:

- **The flow.** What screens? Entry point? Goal state? Map it as a list.
- **Fidelity.** Hi-fi (real visuals, real components, real feel) or mid-fi (wireframe-level, focused on flow not polish)?
- **Device frame.** Desktop browser? iOS frame? Android frame? macOS window? (Phase 3 builds these directly. For anything phone-framed, design the screens per `mobile-design.md` — platform grammar, thumb zone, mobile patterns.)
- **Variations.** One flow or several to compare?
- **Brand / design system.** Always confirm. If none, run `frontend-aesthetic-direction.md` first.
- **Sample data.** What real-looking content fills the screens? Avoid Lorem ipsum.

## Phase 2: Map screens and state

Don't add a title screen or intro card to the prototype itself — it's a tool, not a presentation. Center it in the viewport (or fill it with sensible margins) and open on the flow's first real screen.

Before building, write down the flow and drop it into the file as a comment block at the top:

```
Screens:
  1. Welcome — "Get started" CTA → goes to 2
  2. Email entry — validate format → goes to 3 on valid, shows error on invalid
  3. Verification — "Check your email" + "Skip" → goes to 4
  4. Profile — name, photo upload → goes to 5
  5. Success — "You're in" + "Get started" → goes to 1 (loop demo)

State:
  - currentScreen: 1
  - email: ""
  - emailError: null
  - name: ""
```

## Phase 3: Build screen-by-screen (with a self-contained device frame)

Switch screens within a single page via display toggling (`hidden` attribute / `display:none↔block`) or framework state — not separate files. For each screen: hi-fi visuals matching the design system (real components, not generic boxes), real plausible sample content, one primary CTA (secondary actions smaller and de-emphasized).

When the user wants a device frame, build it directly — a fixed-size shell with the prototype mounted inside. A phone frame, for example:

```html
<div class="device" style="
  width: 390px; height: 844px;            /* iPhone-ish logical size */
  margin: 40px auto; border-radius: 48px;
  /* lint-ok: pure-bw - a phone bezel is genuinely black; this is the device, not a palette choice */
  background: #000; padding: 12px;
  box-shadow: 0 30px 60px rgba(0,0,0,.25);">
  <div class="screen" style="
    width: 100%; height: 100%; border-radius: 38px; overflow: hidden;
    background: #FAFAFA; position: relative;">
    <!-- notch -->
    <!-- lint-ok: pure-bw - the notch is the physical cutout -->
    <div style="position:absolute; top:0; left:50%; transform:translateX(-50%);
                width:140px; height:28px; background:#000;
                border-radius:0 0 18px 18px; z-index:5;"></div>
    <!-- screens mount here; toggle [hidden] to switch -->
    <section data-screen="welcome"> … </section>
    <section data-screen="email" hidden> … </section>
  </div>
</div>
```

The two `lint-ok` comments are the pattern for every legitimate pure black: the gate still runs, and the reason travels with the code so the next reader knows the black was decided rather than defaulted. A suppression with no reason is ignored and reported.

Adapt the frame to the target: a **browser window** (chrome bar with traffic-light dots + a fake URL field), a **macOS window** (title bar + traffic lights), an **Android** frame (squarer corners, status bar), or no frame for a full desktop layout. The frame stays fixed; the prototype lives inside it. Keep frames lightweight — they set context, they aren't the deliverable.

### Installable mobile prototypes (opened on a real phone)

When the user will open the prototype on their phone — and especially pin it to the home screen — build it install-ready by default. Always include these head tags (without them the prototype won't install cleanly):

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="<short title>">
<link rel="apple-touch-icon" href="icon.png">
<link rel="icon" href="icon.png">
```

Ship an `icon.png` (512×512, square, no edge transparency — iOS masks it to a rounded square itself): a single bold glyph or monogram on a solid background that still reads at 60×60; no photos, tiny type, or muddy gradients. On phone widths the app fills the viewport edge-to-edge, reserving notch/home-bar room via `padding: env(safe-area-inset-top) 0 env(safe-area-inset-bottom)` — the status-bar area should feel intentional (matching background or a gradient that tucks under the notch). On desktop (`@media (min-width: 700px)`), inset `#app` into a phone-sized rectangle — `width: 390px; height: 844px; border-radius: 44px; overflow: hidden` plus a soft shadow — so the designer sees "a phone on the desk" while iterating.

**No fake chrome on installables.** In a *presentation* frame (the painted phone above, shown inside a page) a drawn notch is fine — it sets context. In an *installable* prototype, never paint an iOS status bar ("9:41 · battery · wifi") or a fake keyboard: the real status bar and keyboard render on top of your layout, so painted ones double up and look childish. Leave that space alone and let `env(safe-area-inset-*)` reserve the room.

### Multi-file React prototypes (when a single file won't hold)

Beyond a small single-screen mock, split a React/Babel prototype into an HTML entry plus `.jsx` files loaded via `<script type="text/babel" src="…">` in dependency order (data/helpers → icons → presentational components → app entry).

**Where React and Babel come from depends on the delivery surface, and getting it wrong ships a blank page.** Read `delivery-surfaces.md`. For a **served** page, use pinned CDN tags with integrity hashes — never unpinned `react@18`:

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

For a **published Artifact** those three tags are blocked with no error and the prototype ships blank. Two working routes there: **inline all three libraries** into the page (the CSP allows `'unsafe-eval'`, so in-page Babel compilation genuinely works once the script is present rather than fetched), or drop JSX and write the prototype in plain JS with template literals. The eval was never the blocker; the load was.


**JSX text gotcha:** unicode escapes (`’`-style) render *literally* in JSX text content — the user sees the escape sequence on screen. Paste real UTF-8 characters (’ “ ” …) into the source, or wrap in an expression (`Don{'’'}t`); escapes only work inside JS string literals and data arrays (full typography rules: `typesetting.md`).

Split by **coupling, not line count**: extract the self-contained parts (data, icons, presentational components); keep the stateful core (App + palette/modals/selection) in one file — it will be the largest, and that's correct. **One state owner:** lift shared state into App and pass props down; separate Babel scripts don't share scope, so to share components export them with `Object.assign(window, { Terminal, Line, … })` at the end of each file — and never scatter `useState` across files trying to sync it. **Never write `const styles = {}`** in more than zero files — global style-object name collisions break the page; prefer one `<style>` block with CSS custom properties and `className`, reserving inline `style={{}}` for dynamic values. Theming then becomes one attribute flip: tokens on `:root`, overrides under `[data-theme="dark"]`.

## Phase 4: Wire up interactions

A real prototype has **every interaction wired**, not just the happy path:

- **Navigation.** Primary CTA moves to the next screen. Back moves backward. State persists across screens.
- **Form validation.** Empty submission → inline error. Bad format → specific error tied to the field. Valid input → proceed.
- **Loading states.** Async actions show a loading indicator; buttons disable during the request to prevent double-submit.
- **Success feedback.** Toast, inline confirmation, or page transition confirming the action.
- **Error feedback.** Clear, tied to the field or action that caused it.
- **State changes.** Toggling, selecting, filtering — all update the UI immediately.

If the prototype is a small slice, fake the async work with `setTimeout` to simulate latency. Don't skip the loading state because the work is fake — the loading state is part of what the prototype is testing.

**Five states per data surface.** Every list, table, card, form, and panel that fetches or accepts data renders all five: **loading**, **empty**, **error**, **populated**, and **edge**. Shipping only the populated state is the single most reliable AI-design failure. Concretely:

- **Empty is its own state with a job**, never a blank. First-use empty = headline + value sentence + primary CTA (it's the onboarding moment); no-results empty = echo the query and suggest alternatives; cleared empty = celebratory phrasing + next action; **pre-query search empty** = never a blank screen — recent searches, trending items, or suggestions. **Never collapse error into empty** — an error carries recovery information an empty doesn't.
- **Error answers three questions in order:** what happened ("Your card was declined," not "Something went wrong"), why if knowable, what the user can do. Preserve user input across the failure — a form that clears on submit error forces re-entry.
- **Edge = layout that doesn't break.** Test it: a table at 10,000 rows sorted and filtered; a card with a 200-char title and missing avatar; a form with all optional fields empty and required fields at max length; search with a single-char query and a 1,000+ result count; a detail view missing all optional metadata.

**Match the loading indicator to expected duration**, not to what's easiest: under 300ms show nothing (users perceive no delay); 300ms–2s a subtle skeleton or spinner; 2–10s a skeleton matched to the layout or a labelled spinner ("Loading payments…"); 10–30s a determinate progress bar with cancel; at 60s stop animating and show an error with retry. Never leave a spinner running indefinitely — start a timeout on every request. **Retry has timing rules too:** first retry fires immediately on click; then exponential backoff (2s, 4s, 8s); after 3 failures swap "Retry" for "Contact support" plus a copyable error ID — the user has done their job, the system now needs a human.

## Phase 5: Wire up sub-state

Many real flows have meaningful sub-state — selection (which item is selected in a list), filter/sort (how the data is arranged), modal/dropdown (open or closed), form (values, errors, dirty/pristine). Make these reactive: click a filter chip → list re-renders; open a modal → focus moves to it and Escape closes it. Two overlay gotchas: a dropdown positioned `absolute` inside an `overflow: hidden`/`auto` ancestor gets clipped — use the popover API, `position: fixed`, or a portal; and give modals a real scrim (40–60% black) plus `overscroll-behavior: contain` so the background neither competes nor scrolls.

## Phase 6: Persist what matters

Some state should survive a page reload — **current screen**, **form drafts** (if the user refreshes mid-flow, pick up where they left off), and **tweak values** (see `make-tweakable.md`). Refreshing during iterative design is one of the most common user actions; state that doesn't survive reload makes the prototype feel broken. **Which store to use depends on the delivery surface** — `localStorage` on a served page or an installable, a `sessionStorage` stash inside a published artifact (`delivery-surfaces.md`).

## Phase 7: Verify

**Serve over HTTP, never `file://`.** Start one local server for the project (`python3 -m http.server 4311`) and load `http://localhost:4311/…` for every preview, screenshot, and user handoff. Multi-file prototypes silently fail on `file://` — the browser blocks the cross-origin `.jsx` loads and you get a blank page with no obvious error — and routing single files through the same served URL keeps previews consistent.

Walk the full flow in a browser: every CTA leads somewhere; every form validates; every error is clear and recoverable; every async action shows feedback; every state change is visible; keyboard navigation works (Tab through, Enter to submit, Escape to close modals); focus is visible. Do this pass yourself — driving the flow is exactly the handful of tool calls a delegate would spend a whole context on. If you can't verify a behavior, say so explicitly in the summary rather than claiming success.

Two browser-automation gotchas for the verifier (harness quirks, not bugs in your code): synthetic clicks don't reach React 18's delegated `onClick` (`createRoot` delegates from the root container) — fire the handler via in-page JS instead: find the node, read its `__reactProps$*` key, and call `el[propKey].onClick({stopPropagation(){},preventDefault(){}})`. And test keyboard shortcuts by dispatching on window: `window.dispatchEvent(new KeyboardEvent('keydown',{key:'k',metaKey:true,bubbles:true}))` — global keydown listeners fire fine that way.

## Phase 8: Variations (if requested)

If the user asked for variations of the flow, layout, or visual treatment, expose them as **tweaks** (a floating panel — see `make-tweakable.md`), a **side-by-side canvas** (the snippet in SKILL.md §18), or **toggles** the user clicks between. One file, many variants — SKILL.md §18 owns that rule.

Summarize briefly: what flows work, what's faked (e.g. "submit calls a setTimeout fake"), what's open for the user to decide.

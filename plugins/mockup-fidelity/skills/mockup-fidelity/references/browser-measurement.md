# Browser measurement — reading getComputedStyle from a rendered surface

You need a real browser to read computed styles and capture screenshots. This applies to **both** sides when both are DOM (the HTML/CSS reference, and a React or react-native-web target), and to the reference side always.

## Tools (any that read the DOM + screenshot works)

- **`obscura`** — one static binary on PATH. `obscura fetch <url> --eval "<js>" --screenshot <path>` for a single settled render (viewport only — there is no full-page flag); `obscura serve --port 9222` + CDP when you need a viewport matrix, a full-page capture (`Page.captureScreenshot` with `captureBeyondViewport` and a clip from `Page.getLayoutMetrics`) or a promise awaited; `obscura mcp` when you must click your way to a surface. No output-path restriction, and no shared session to collide over — every `fetch` is its own render, so reference and target can be measured concurrently. A localhost target needs `--allow-private-network` **before** the subcommand.
- **`agent-browser`** — drives SPAs on `http://localhost/` (not a public HSTS host). Use a viewport **≥ 1680px** for desktop multi-column layouts; **wrap each `eval` in an IIFE** (evals share one global scope); results come back **double-JSON-encoded** — decode twice.
- **`obscura mcp`** — the session-holding lane: `browser_navigate`, `browser_click`, `browser_fill`, `browser_evaluate` and the rest, for a surface you must drive to. No viewport control, and `browser_evaluate` does not await a promise.

**Serving a static mock:** open the HTML directly; if `file://` blocks its scripts/fonts, serve the folder (`python3 -m http.server <port>`) and open `http://localhost:<port>/<file>.html`.

**A mock gallery** (many phone frames on one page) is common. Tag each frame once so you can screenshot it by selector:

```js
// give every frame a stable id, then screenshot "#mockframe-N" per screen
(() => { let n=0; document.querySelectorAll('figure.fig, .phone, .frame').forEach(f => { f.id='mockframe-'+n++; }); return n; })()
```

Hide the gallery's own sticky chrome (page header/nav) before screenshotting frames, or it overlaps each frame's top. Measure the frame's pixel size and set the **target viewport to match** (e.g. a 393×852 phone frame).

## Per-property extraction pattern

For the per-property diff (SKILL.md Phase 3C), pull the exact computed values for each named element. Keep evals IIFE-wrapped and return `JSON.stringify`:

```js
(() => {
  const pick = (sel, props) => {
    const el = document.querySelector(sel); if (!el) return null;
    const cs = getComputedStyle(el); const o = {}; props.forEach(p => o[p] = cs[p]); return o;
  };
  // LONGHANDS ONLY. In this engine `padding`, `margin`, `borderRadius` and `border` return 0px or ""
  // while their longhands are correct, and `gap` returns `normal` while rowGap/columnGap are correct.
  // A snippet written against the shorthands compares two zeros and reports a match.
  const TYPE = ['fontSize','fontWeight','lineHeight','color','letterSpacing','fontFamily','textAlign'];
  const BOX  = ['paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginBottom',
                'borderTopWidth','borderTopColor','borderTopLeftRadius','borderTopRightRadius',
                'backgroundColor','rowGap','columnGap','display','flexDirection'];
  return JSON.stringify({
    container: pick('#frame .stats', BOX),
    label:     pick('#frame .stat .k', TYPE),
    value:     pick('#frame .stat .v', TYPE),
  }, null, 1);
})()
```

Print the **full** value — never slice a gradient or border before comparing. A ✓ requires both full
values shown and matching, **and** the property being one this engine can answer. Two empty strings match.

**Four properties are deliberately absent from the lists above, and one of them used to be here.**
`boxShadow`, `textTransform`, `backgroundImage` and `::placeholder` colour cannot be measured in this
engine at all — they return `""`, or the element's own value, on both sides. `boxShadow` and
`::placeholder` are the two SKILL.md names as most often silently wrong, which is exactly why leaving them
in a hand-rolled snippet is worse than omitting them: the snippet returns a value, the value matches, and
the reader ticks the property. **Confirm all four in a real browser**, and see
`engine-capability-matrix.md` for what else is on that list.

**States matter, and one half of this still works.** `document.styleSheets[].cssRules` is readable here
and `:hover` selectors enumerate, so a missing hover/focus treatment IS catchable — read the rule rather
than trying to enter the state. Forcing `:hover` and re-extracting does not work, because no transition or
animation executes.

**Numeric gotchas:** a `0.5px` border computes to `1px` at DPR 1; an `em` letter-spacing computes to px
**at the element that declares it** and inherits as that fixed px; a `0px`-width border still reports a
style+colour — ignore style/colour when width is 0.

**Prefer the harness over a hand-rolled snippet whenever the answer will back a verdict.** This snippet
has no preflight, so it cannot tell you which of its own readings are meaningful. `capture.mjs` probes
every class, records what it could not measure, and exits nonzero. Hand-rolling is for a quick look at
three named elements, never for a screen's style verdict.

## Structured one-pass snapshot

For everything beyond a handful of named elements — the structural skeleton, every control's containment anchor, region styles, thin/empty/variant flags — use the **fidelity probe** in `fidelity-probe.md`: one `eval` per surface returns the whole detection snapshot, so you classify offline from the JSON instead of re-opening the page. Capture the reference once and reuse it; re-capture only the target after a fix.

## Rendering a protected target

A real app target usually needs its dev login first. Establish a session (the project's dev-login affordance, or ask the user to log in), select any required context, then navigate to the actual route with real-ish data before measuring — a login screen is not the surface you were asked to audit. Pick a context whose data **populates** the screen (the Done-criteria require the populated state, not the fallback) — e.g. choose a tenant/company that actually has rows.

**When the target is also DOM (web↔web — a React/Next app vs a React/Next or HTML reference):** both sides go through the *same* `analyze.js`, driven by `capture.mjs` (`--ref` and `--target`) in one command — there is no separate extract-then-diff step. Render both at the **same viewport** so geometry compares directly, select the screen content root with `window.MF_FRAME_SELECTOR` (tag it with a `data-*` attribute for a stable selector), and set `window.MF_CHROME_SELECTOR='__none__'` so the web app-chrome (sidebar/header/nav) is measured rather than skipped — the native-chrome exemption does not apply on the web. Full playbook: `references/react-web.md`.

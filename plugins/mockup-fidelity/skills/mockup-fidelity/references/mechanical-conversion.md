# Mechanical conversion — lift a rendered subtree instead of rebuilding from a screenshot

Some reference sections are **decorative and non-editable** — a hero product-illustration, a
stat panel, a logo cloud. Rebuilding one by eye from a screenshot is slow *and* lossy (every
gradient, offset, and shadow is a guess you then have to diff). For those, the faster, pixel-
exact move is to **lift the reference's rendered subtree** — its DOM plus the *resolved*
computed styles — and render it in React directly. Two scripts do this:
`capture-subtree.js` (browser eval) lifts the subtree; `to-stylex.mjs` turns the capture into a
React component, in one of two modes.

**Choose the mode by editability:**

| Section is… | Mode | Result |
|---|---|---|
| decorative / static / not CMS-editable | `--mode embed` | pixel-EXACT, fast, ships as-is |
| something that must become a real, token-driven, editable component | `--mode stylex` | a StyleX **draft** you clean up |

## Step 1 — capture-subtree.js (lift the rendered subtree)

```bash
obscura --allow-private-network fetch "http://localhost:<port>/<mock>.html" \
  --eval "(() => { window.MF_CAPTURE_SELECTOR = '#hero .vignette'; return ($(cat capture-subtree.js))(); })()" \
  --output capture.hero.json
#   one call: each fetch is a fresh page, so the global and the capture must go together
```

Walks the subtree under `MF_CAPTURE_SELECTOR`, inlines a curated **computed-style** set onto
every node (so it renders identically with no external CSS), drops properties still at their
default to keep output small, strips classes/ids/scripts, and carries `svg`/`img`/`path`
through wholesale (their `outerHTML` + style, so icons/images survive). Returns BOTH a cleaned
self-contained `html` string AND a structured `tree`. (If the selector finds nothing it returns
`{error}` — Framer/HTML exports often use `<div>`, not `<nav>`/`<header>`.)

## Step 2 — to-stylex.mjs (emit the React component)

```bash
# decorative / static — pixel-exact:
node to-stylex.mjs --capture capture.hero.json --name HeroVignette --mode embed
# editable — StyleX skeleton draft, values mapped to tokens where one matches:
node to-stylex.mjs --capture capture.hero.json --name HeroVignette --mode stylex --tokens tokens.json
```

Default mode is `stylex`. Output is `--out <file>` or `<Name>.tsx`.

### `--mode embed` — pixel-exact decorative markup

Emits a component that renders the lifted HTML (inlined computed styles) verbatim via
`dangerouslySetInnerHTML`. It is the literal "extract the HTML and render it in a React
component" approach — identical to the reference and fast, with no measure-and-align loop.

**Security framing (the generated file carries this note):** the embedded HTML is
**build-time-static reference markup baked into the bundle — NOT user input**, so
`dangerouslySetInnerHTML` is safe here. The component is rendered `aria-hidden` (it's
decoration). **If you ever make this content dynamic** (props, CMS, user data), run it through a
sanitizer (DOMPurify / the repo's sanitize util) FIRST, or convert it to real JSX (regenerate
with `--mode stylex`). Review the markup before shipping either way.

**Honest tradeoff:** embed is **not** token-driven, themeable, or composable — it's a frozen
snapshot of one rendered state. Use it ONLY for static decoration. Anything that must respond to
tokens, theming, props, or content edits is the wrong fit — use `--mode stylex`.

### `--mode stylex` — a token-mapped skeleton DRAFT

Emits `stylex.create({...})` from the inlined styles + a JSX tree, mapping each value to a
**token name** when a token map is supplied. The output is a reviewed **draft, not final** — you
clean up the style names, wire real content/props, and verify against the reference with the
differ afterward. `svg`/`img` nodes are emitted as a `{/* icon/image — port the SVG/asset */}`
marker plus the raw element.

**`--tokens tokens.json`** is a flat `{ "<tokenName>": "<computed value>" }` map — e.g. dumped
from the app's StyleX `defineVars` / theme. A captured value that matches a token's value is
emitted as `tokens.<name>` (and the import collected); a value with **no** token match is
emitted as a literal with a `/* TODO: no token */` flag, so every un-tokenized value is visible
for cleanup. Without `--tokens`, every value is a literal (the run tells you so) — pass a token
map to auto-map.

## How it fits the audit

This is a Phase-6 conversion path, not a measurement method. After generating either component,
**verify it against the reference with the differ exactly like any other section** — embed
should diff clean immediately (it's the lifted render); a stylex draft is diffed after you wire
its content. A `--mode embed` component is still subject to the structural/content passes
(`structure-and-content-diff.md`) if its surrounding section has editable siblings. Record any
behaviour the decorative markup *implies but doesn't do* in the functional-gaps doc as usual.

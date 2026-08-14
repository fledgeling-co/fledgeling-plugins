# Browser drivers

There is one driver: **Obscura**, on PATH as `obscura`.

Repo: <https://github.com/h4ckf0r0day/obscura> ·
Skill: <https://github.com/h4ckf0r0day/obscura/blob/main/skills/obscura/SKILL.md>

Playwright, Puppeteer, `chrome-headless-shell`, `chrome-devtools-mcp`,
Playwright MCP, `playwright-cli`, `browser-use` and `claude-in-chrome` are gone.
Do not reintroduce them, and do not suggest installing one as a fallback — a
review that says "install Puppeteer for the rest" is now wrong advice.

## The three ways in, and when each is right

| Path | Use it for |
|---|---|
| `obscura fetch` | One page, one capture. The cheapest thing that works. |
| `obscura serve --port 9222` + raw CDP | Multi-viewport passes, computed styles, AX tree — anything scripted. |
| `obscura mcp` | Driving a surface interactively: click, fill, scroll, tabs, auth state. |

```bash
obscura fetch <url> --screenshot page.png
obscura fetch <url> --eval "document.title"
obscura fetch <url> --dump text|html|markdown|links
obscura serve --port 9222
obscura mcp
```

**Localhost is blocked by default.** Any capture of a dev server — `127.0.0.1`,
`localhost`, a `192.168.*` host — needs `--allow-private-network` or it fails as
an SSRF block. This is the single most common way a capture fails for a reason
that looks like the page's fault.

**`--wait` semantics differ from every other driver.** Omitted, it adaptively
settles up to 5s and returns when the page is quiescent. Given `--wait N`, it is
a *fixed* N-second delay, not a ceiling. `--timeout` is separate and bounds
navigation.

## Computed styles: longhands only

Measured on this machine, 13 August 2026, against a fixture whose CSS sets
`padding:16px` and `margin:40px`:

| Property | Obscura returns | Correct? |
|---|---|---|
| `padding` | `0px` | **no** |
| `paddingTop`, `paddingLeft` | `16px` | yes |
| `margin` | `0px` | **no** |
| `marginTop`, `marginLeft` | `40px` | yes |
| `backgroundColor`, `color`, `fontSize`, `fontWeight`, `width`, `height`, `display` | correct | yes |

The **shorthand resolves to zero silently**. The layout underneath is right — the
same element measures 332×152 with the padding applied — so nothing looks broken
and a spacing assertion reading `computed.padding` passes when it should fail.

So: read `paddingTop`/`paddingRight`/`paddingBottom`/`paddingLeft`, never
`padding`. Same for `margin`, and assume the same of every other shorthand
(`border`, `borderRadius`, `background`, `font`, `inset`, `gap`, `flex`) until
one is checked against a fixture. When a spacing or border gate reports a
suspiciously round zero, this is the first thing to suspect.

**An empty string means "not implemented", not "not set".** `boxShadow`,
`backgroundImage`, `textTransform`, `outline` and `flex` come back as `""`
whether or not the CSS sets them, so you cannot distinguish an absent shadow
from an unsupported one. Treat those properties as unreadable rather than as
evidence of absence — a gate that reports "no box-shadow" from this is asserting
something it did not measure.

## Viewports work. Media emulation and animation do not.

`Emulation.setDeviceMetricsOverride` is implemented and verified at both review
widths — the page reports `innerWidth` 1440 and 390 exactly, and the captures
differ. That one is real.

**`Emulation.setEmulatedMedia` is accepted and inert.** It returns success and
changes nothing: after `{media:'print'}`, `matchMedia('print').matches` is still
`false` and the cascade is unchanged. Same for
`{features:[{name:'prefers-reduced-motion',value:'reduce'}]}`. So there is no
print pass and no reduced-motion pass — record those states as skipped rather
than writing a capture that is silently just the screen render again.

**CSS animations and transitions never execute.** `document.getAnimations()`
returns 0 for a declared infinite animation, and computed opacity stays frozen at
the start value. A motion pass would write N identical stills. This also makes
any "did it settle" gate vacuous: an `animationsRunningAtMeasure` of 0 is an
absent signal here, never a pass.

**Web fonts never load.** A working remote woff2 and a 404'd one measure
identically, every `@font-face` stays `unloaded`, named families collapse onto
generic metric buckets, and `CSS.getPlatformFontsForNode` returns `{}`. The
entire font-fidelity class is unmeasurable — report it as unavailable, never as
zero divergence, because a silent zero reads as "the fonts match".

The lesson generalises, and it cost a wrong entry in this file: **a CDP method
returning without an error proves only that it was accepted.** Before trusting
any emulation domain, assert the observable it is supposed to change.

## `obscura fetch` renders at a fixed 1280×720

There is no viewport flag and no full-page flag on the CLI, and neither `fetch
--eval` nor MCP `browser_evaluate` awaits a promise — an async injectable comes
back as `{}`. Anything needing a specific viewport, a full-page capture, or
async evaluation has to go through `serve` + CDP.


## Layout gaps that compute correctly and render wrongly

The worst class of divergence, because the usual defence — read the computed
value on the node — returns the right answer while the pixels are wrong. All
three measured 14 August 2026 against minimal fixtures.

| What | Obscura does | The tell |
|---|---|---|
| **`display: revert`** | computes to `none` rather than the UA default | a show-the-match rule blanks the page. Invert it: hide the non-matches, and never rely on `revert` |
| **A bare text node as a flex item** | is not wrapped into an anonymous flex item | `Name<span>desc</span>` inside `flex-direction: column` puts the span *beside* the word and collapses the container to one line, while `display`, `flexDirection` and the span's own `display: block` all read correct. Wrap every text run in an element |
| **`:has()` re-evaluation** | does not re-run when `.checked` is set from script | a scripted state toggle measures the same state twice and reports two passes. Set the state in the served source and render again |
| **Physical units** | resolve to the container, not to a physical size | `width: 210mm` computed to **1264px** (the container width) and `height: 297mm` to **0**; `16mm` also gave 1264px. `794px` was exact. A print sheet sized in millimetres reviews as a full-bleed page with no margins, which invites a fix for a defect that exists only in the review engine |

`:has()` itself works, including as a descendant combinator, and
`CSS.supports('selector(:has(*))')` correctly returns true — which is precisely
why the support query is no defence here. `flex-direction: column` also works in
isolation; only the anonymous-item case fails.

The general rule these share: **assert the geometry, not the declaration.** A
computed style tells you the cascade resolved; only a bounding box tells you the
layout ran. Where a component's correctness depends on one element sitting above
another, measure the two boxes.

Two properties are simply absent rather than wrong, and a state signal riding on
either is invisible in every capture: `boxShadow` and `backgroundImage` return
empty. Carry state on border, background colour, weight or position instead.

## What Obscura is not

It is a Rust engine, not packaged Chrome, and its own documentation expects
divergence in long-tail CSS, service workers, some Web APIs, native media,
GPU and compositor effects, PDF structure, and font rasterization. Two
consequences for a review:

- **A pixel diff is a tripwire, not a verdict.** Confirm the page navigated and
  rendered non-blank before reading any diff, and investigate resource
  completion, geometry, wrapping and clipping before calling a difference a
  defect in the page.
- **Suspect the engine before the page.** When something renders wrongly, check
  it against a deterministic fixture first. A finding that turns out to be an
  Obscura fidelity gap, reported as a design defect, costs more than the review
  saved.

`browser_pdf` produces raster-backed print output: no selectable text, no tagged
PDF, no outlines, no headers/footers, and incomplete paged-media CSS. Do not use
it to check print typography.

## When no browser is available

Obscura is a single static binary on PATH. If it is missing, say so and give the
one-line fix — download the `aarch64-macos` release from the repo and put it in
`~/.local/bin` — then name which checks stay dark without it: contrast against
live backgrounds, overflow, target geometry, focus rendering, per-viewport
layout. Do not offer a different browser as the path back.

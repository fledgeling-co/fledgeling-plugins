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

## Computed styles: longhands only, and capability is measured not assumed

**Do not read this table and hardcode it.** `probes.js`'s
`probeEngineCapability()` re-measures every channel below on every run, against a
scratch element whose values it sets itself, and `runAll().capability` carries the
answer. The table is here so you know what to expect and why the probe exists;
the probe is what you believe. An engine that gains a property is then believed
the day it does, and a different engine is characterised without editing a file.

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

This is not an Obscura eccentricity, which matters when deciding how much to
trust the pattern. WebKit has carried the same behaviour for shorthands
(bugs.webkit.org #14563), and Mozilla documented
`getComputedStyle(el).getPropertyValue('border')` returning an empty string in
Firefox Nightly while Blink and WebKit returned a value for the same test
(bugzilla #137688). **Reading longhands is the standing industry mitigation, not
a workaround for one engine.**

So: read `paddingTop`/`paddingRight`/`paddingBottom`/`paddingLeft`, never
`padding`. Same for `margin`. When a spacing or border gate reports a
suspiciously round zero, this is the first thing to suspect.

### The three states, and why the middle one has to exist

**An empty string means "not implemented", not "not set".** `boxShadow`,
`backgroundImage`, `textTransform`, `outline`, `flex` and the transition
longhands come back as `""` whether or not the CSS sets them, so an absent shadow
and an unsupported one are the same output. A gate that reports "no box-shadow"
from this is asserting something it did not measure.

That is one instance of the rule this whole skill is built on: **a check whose
"pass" and "cannot run" look identical must report which one it is.** W3C's ACT
Rules Format names the states a result may take — `passed`, `failed`, `cantTell`,
`untested`, `inapplicable` — and `cantTell` is precisely the one a boolean gate
destroys. axe-core ships the same idea as `incomplete`, and returns it for this
exact case, with this exact message: *"The background color could not be
determined due to a background image."* It also documents that its
`color-contrast` rule simply does not work under JSDOM, rather than running it
and reporting zero.

So the pattern to copy is already normative, and the cost of not copying it is
measured: on a 285-homepage scan, counting axe's `incomplete` results as
violations moved the reported failure rate to **97.9%**. That gap is the size of
the population a two-state gate absorbs in silence.

### Inline declarations are handed back unresolved. Stylesheet ones are not.

Measured 18 August 2026, obscura 0.2.0. The same element, the same values,
set two ways:

| Property | Set inline | Set via a stylesheet |
|---|---|---|
| `background-image` | the gradient, verbatim | `""` |
| `border-radius` | `24px` | `0px` |
| `text-transform` | `uppercase` | `""` |
| `box-shadow` | the shadow, verbatim | `""` |
| `gap` | `13px` | `normal` |
| `padding` | `16px` | `0px` |
| `transition-property` / `-duration` | `""` | `""` |

**A capability probe that plants its ground truth inline measures the wrong
path** and concludes the engine can read all six. Real pages use stylesheets, so
that reading would switch off every fallback on exactly the pages that need one.
The first version of `probeEngineCapability()` did this and had to be corrected.
It is the same lesson this file already carries about CDP, one level down: assert
the observable *the way the page will actually produce it*.

### The declared channel answers what the computed channel drops

Where a computed property is unreadable, the stylesheet still is. This is the
trick `probeFocusStyles()` always used for `outline` and `box-shadow`, and that
nothing else applied until it was generalised into `buildDeclaredIndex()`.
Measured 18 Aug 2026 against `evals/fixtures/landing.html`:

| Element | Declared value recovered |
|---|---|
| `.hero` `background` | `linear-gradient(135deg,#6366F1,#A855F7,#EC4899)` |
| `.eyebrow` `text-transform` | `uppercase` |
| `.card` `box-shadow` | `0 8px 32px rgba(0,0,0,.18)` |
| `.btn` `transition` | `all 0.3s ease-in` |
| `.grid` `gap` | `13px` |

`getPropertyValue('--brand')` resolves custom properties and they inherit to
descendants, `el.matches()` works, `matchMedia` answers width queries correctly,
and the `style` attribute is readable — so the index can resolve `var()`, match
selectors, and let inline styles win.

Two structural facts about this engine's CSSOM, both load-bearing:

- A **top-level rule is a real `CSSStyleRule`**: `selectorText` and the `style`
  accessors work exactly. The common case needs no parsing.
- An **`@media` or `@supports` block is a bare `CSSRule` with `type: 0`** — no
  `conditionText`, no `media`, no `cssRules`, no `style` — **but `cssText`
  carries the whole block verbatim.** So at-rules are recovered by parsing
  `cssText` and gating the condition with `matchMedia`. An earlier read of this
  concluded at-rules were dropped entirely; they are not, they are unmodelled,
  and the difference is every responsive declaration on the page.

**A declaration is not a rendering.** It says what the author asked for; the
computed value says what the cascade resolved. Where both answer, the computed
value wins. Every value sourced from the index is tagged `declared` in
`probes/*.json`, and a finding built on one says so — quoting a declaration as a
measurement is the failure this tagging exists to prevent.

`gap` is worth one note of correction: its longhands `rowGap` and `columnGap`
**do** read correctly (`13px` on the fixture's `.grid` while `gap` says
`normal`), so it is recoverable without the declaration index. An earlier version
of this file said otherwise, on a measurement taken against the wrong element.

## Known false positives on this engine

Three shapes where the engine, not the page, produces the defect. Each has been
mistaken for a real finding.

**A stranded entry animation reads as a z-index bug — before the reveal pass.**
An `opacity: 0` entry keyframe leaves its element at **~0.0036** on a read taken
without scrolling, because the animation never runs. Measured 18 Aug 2026 on
`evals/fixtures/landing.html`: a bare `obscura fetch --eval` reads the three
`.card` elements at 0.0036, and the same page probed through `run_review.py` —
which scrolls the whole document and settles it first — reads them at 1, with
`probeStrandedElements()` correctly finding none.

So this value is **context-dependent, not permanent**, and that is the useful
form of the fact: opacity here is a time- and scroll-dependent property, and a
first reading of one is provisional until the reveal pass has run. An earlier
version of this entry called the 0.0036 permanent, which is wrong and would have
a reviewer report a settled page as broken. The defence below is for the
un-settled read, which is the one a one-shot capture takes. It is non-zero, so an exact `opacity === 0` test lets it
through into every geometric probe, where it looks exactly like an element hidden
behind something. `visible()` now excludes anything at or below 0.05 and
`probeStrandedElements()` reports the population separately — but note the split:
`dumpStyles()` deliberately *includes* stranded elements, because it is counting
design decisions and a stranded element's radii and shadows are perfectly real.
Using one filter for both jobs threw away the fixture's entire shadow population
and reported a surface with no elevation at all.

**Native form controls do not render, so a real radio looks like a missing
affordance.** `probeAffordanceGaps().unactionableRows` fires on "a repeated row
containing chip-shaped short text but nothing focusable", which is exactly the
shape a rendered-as-nothing radio input produces. Before reporting an affordance
finding on a row that should contain a native control, check the source for
`<input type="radio|checkbox|range|color|date">` and report the check as
unavailable for that row rather than as a defect.

**Inline citation markers perturb text rects.** A line carrying an anchor eats a
space and breaks before the marker, and both `probeTextOverlap` (≥3px on both
axes) and `probeDividerProximity` read per-fragment rects via
`Range.getClientRects()`. Surfaces with claim-local citation markers are a live
false-positive source for both; review typography on a marker-stripped copy.

## Relay the tool's own error before interpreting it

When obscura fails, **quote its stderr verbatim in the report before saying what
you think it means.** The message names the flag and the version; a paraphrase
names neither and can be wrong for the environment the reader is in. The SSRF
refusal on a dev server is the case that bites — it names
`--allow-private-network` in the output, and the paraphrase "the capture failed"
sends the reader looking at their page.

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


## The Target domain is scoped to the connection, and `/json/list` will not tell you

Measured 15 Aug 2026. Open a CDP socket, `Target.createTarget`, then drop the
socket and open a new one:

- `GET /json/list` still lists the page, with the same id.
- `Target.getTargets` on the new socket returns **an empty list**.
- `Target.attachToTarget` with that id answers **"Target not found"**.

So a `sessionId` dies with the socket that issued it and the target cannot be
recovered. Anything that needs to survive a dropped or desynced connection has
to create a **new** target and re-navigate — which means the document is
re-loaded, so scroll position, settle state and any accumulated page state are
gone, and measurements taken afterwards are not continuous with the ones before.
`run_review.py`'s `Page.recover()` does exactly this and records which probes ran
on the rebuilt document. The HTTP listing is not evidence that a target is
reachable.

Two consequences worth carrying:

- **Retry with backoff.** The timeout that forces recovery usually means the
  renderer is still finishing the call that overran, and it cannot service a
  `createTarget` until it is done — an immediate single attempt fails on exactly
  the case worth recovering. 0 / 2 / 4 / 8s works.
- **An infinite loop in page JS is not recoverable at all.** The renderer never
  returns, so every attempt fails. That is the correct outcome to report; the
  wrong one is to mark the remaining checks clean.

## `Emulation.setDeviceMetricsOverride` needs the session, and then it works

The viewport matrix is real: `375 / 768 / 1024 / 1280 / 1920` each report the
requested `innerWidth`. But the call only takes effect when it is sent **with the
page's `sessionId`**, after `Target.createTarget` → `Target.attachToTarget`. Sent
on the bare browser connection it is accepted and silently does nothing — which
looks identical to an engine that ignores the domain, and has been mistaken for
one. If a capture comes back at the wrong size, check that the session id was
passed before concluding the engine is at fault.

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

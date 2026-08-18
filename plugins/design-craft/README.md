# design-craft

<p align="center">
  <img alt="Version 1.0.0" src="https://img.shields.io/badge/version-1.0.0-D33C21">
  <img alt="SWE skill: making" src="https://img.shields.io/badge/SWE_skill-making-434A55">
  <img alt="Gate assertions: 23 to 9" src="https://img.shields.io/badge/gate_assertions-23_to_9-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

Design or review a user-facing visual artifact (a landing page, app screen, dashboard, clickable prototype, native mockup, wireframe, variation set, motion piece, print document or design system) as an opinionated designer rather than a code generator.

## The problem

Two failures produce work that looks finished.

The first is convergence. Asked for something distinctive, a model reaches for the same small set of choices every time, and the result is competent and anonymous. Naming the trap after the fact does not help, because by then the artifact exists and reads as a decision.

The second is a design rationale nobody checked. More than a quarter of one generative UI tool's stated design rationales were measured not to appear in what it actually built. The artifact claims a direction; the pixels went somewhere else; nothing compares the two.

## What it does instead

**Roots a hi-fi build in existing context by default, and lifts resolved values exactly.** When there is an app, a token file or a component library, the build reads it and takes the real numbers (hex and oklch colours, the full type ramp, line-heights, spacing, radii, shadow recipes, control heights), following variables through to what they resolve to. It does not round them to a 4/8px grid, because rounding an incumbent system's measured spacing and reporting it as a fix is a defect the previous version shipped.

**Treats direction as a distribution.** It names the category's rut *and* its predictable opposite before generating, then derives seven candidates across at least three material families. The chosen direction is written into the artifact as a five-block contract, and the critique gate audits it promise by promise, so the rationale is a checkable claim rather than a caption.

**Ships a gate that computes contrast rather than asserting it.** `scripts/design-lint.py` reads WCAG ratios from source across hex, `rgba()`, `hsl()` and `oklch()`, follows tokens to their `:root` definitions, and composites `opacity`. It reproduces this skill's own recorded incidents to two decimal places: `#D72229` on `#2E2B2B` computes 2.773 against a recorded 2.77, `#E65400` on white 3.728 against 3.72, and `rgba(255,255,255,.44)` on `#181717` 4.358 against 4.36. A fourth recorded figure computes 3.12 against a recorded 2.98 and does not name its ground; that discrepancy is recorded in `references/evidence.md` rather than quietly corrected.

**Contrast is tri-state.** A gradient, an image or an undeclared ground is reported `UNMEASURABLE`, never skipped. An unmeasured pair and a passing pair otherwise serialise identically, which is how a checker reports clean on a page it could not read. The same rule shapes the rest of the gate: it names the silent downstream consequence of every finding, gates on mechanism and warns on fashion, runs markup checks through a real HTML parser, requires a reason on every suppression, and prints what it did not check so a clean run cannot be read as verified.

**Proves its own rules can fire.** `--selftest` exercises all forty and confirms a clean fixture produces nothing. A predicate that matches nothing returns clean and is indistinguishable from a clean page.

## Does it actually work

Twenty-five structural assertions, run against both this version and its predecessor, graded by someone who saw one output at a time and never the skill.

| | predecessor | this |
| --- | --- | --- |
| assertions passed | 9 | 23 |

The predecessor's failures cluster: it had no contrast gate at all, its lint fired on four of its own reference snippets, and its `external-resource` check reported the line number of the first `//` in the file (a JavaScript comment) rather than the resource.

A blind panel of three model families judged three document pairs and chose this version on all nine. A fourth family was usage-limited that day and is recorded as failed rather than dropped from the tally.

**Two assertions the predecessor won, deliberately.** A file whose only defects are aesthetic cues now exits 0, because no study supports gating on a cue as proof of AI authorship. And text on a gradient now produces a finding where the predecessor was silent: real noise the predecessor does not have, and the stated price of never reporting an unmeasured pair as clean.

The panel also found two arithmetic defects in this version's own pixel-median fallback: it computed luminance on gamma-encoded bytes without linearising, and cropped to the glyph box so it sampled the letters along with the ground. Both fixed.

## Honest limits

The only sanctioned browser here is Obscura, and its measured gaps bound what any of this can claim. CSS animations and transitions never execute. `Emulation.setEmulatedMedia` is accepted and inert, so there is no print pass and no reduced-motion pass. Web fonts never load, so type fidelity is unmeasurable rather than verified. Shorthand computed styles return `0px` or empty while the longhands are correct.

So motion, print, reduced-motion and type fidelity are declared **unchecked**. They are not reported clean.

`references/delivery-surfaces.md` carries the other half: a published Artifact's CSP blocks a CDN script through `script-src` with no error, and the page ships motionless. Google Fonts is the one permitted external host. `'unsafe-eval'` is allowed, so inlining a transpiler works.

## What it doesn't do

It does not review a rendered page in a browser; that is `design-review`, and it is the last pass before a human looks at AI-built UI. It does not measure a build against a mock by reading the DOM; that is `mockup-fidelity`. It does not own flows, forms, interface copy or UX review, which belong to `ux-craft`; the two are a standing pair, and this half is the visual hands.

## Install

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install design-craft@fledgeling-plugins
```

## Deeper

Thirty phased procedures live in `skills/design-craft/references/`. The ones worth knowing by name: `visual-verification.md` for why rendering is not seeing and how a gate can be downstream of the findings that motivated it, `ai-slop-check.md` for the structure and vocabulary tells that two blind judges ranked ahead of every visual difference, `delivery-surfaces.md` for what each delivery surface refuses, and `evidence.md` for every rule traced to its source, including the three places the research contradicts itself and the figure this skill could not reconcile with its own record.

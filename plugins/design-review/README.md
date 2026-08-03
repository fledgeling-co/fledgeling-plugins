# design-review

The last pass before a human looks at AI-built UI.

Renders the surface, runs the checks that are deterministic, then judges the ones that aren't — and says plainly which is which. Returns severity-ranked findings with pasteable fixes, the evidence behind each one, and an explicit list of what it never checked.

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install design-review@fledgeling-plugins
```

## Use

Ask for a review in whatever words you'd normally use:

```
Review the design of this landing page before I hand it to a human.
Does this dashboard look AI-generated?
I changed the pricing hero and plan cards — design pass before I show my team.
```

It handles scoped diffs, whole surfaces, and source-only reviews when no browser is available.

## What it does

Ten stages, three tiers of finding.

**Tier 1 — gates.** Deterministic and blocking. Contrast against measured backgrounds, target size against the 24×24 CSS px AA floor, focus suppression, missing labels, `lang`, heading structure, horizontal overflow, console and network errors, motion and reduced-motion handling. These either pass or they don't; no judgment involved.

**Tier 2 — calibrated findings.** Judged, but every one carries evidence: a probe result, a source line, or a crop. Hierarchy, typography, spacing systems, state coverage, form and flow behaviour, copy honesty.

**Tier 3 — prompts.** Aesthetic direction, distinctiveness, the "does this look AI-generated" question. These never gate and carry no severity, because there is no systematic evidence behind a tell-list and the underlying question is unresolved. The checkable substitute is the systematisation pass, which measures whether decisions were *specified* rather than defaulted — a question that holds regardless of where you land on whether "slop" is real.

## Browser drivers

Five paths, whichever the project already has:

| Path | How |
|---|---|
| Playwright | `scripts/run_review.py` |
| Puppeteer | `scripts/run_review.mjs` |
| chrome-devtools-mcp | MCP tools — CWV traces and Lighthouse natively |
| agent-browser | CLI or MCP — `vitals`, `a11y`, session reuse |
| claude-in-chrome | For a live or authenticated surface |

With none of them it runs the static path and says so. It will not imply a page was seen when it wasn't.

## What it will not tell you

Automated tooling finds roughly a fifth to under two-thirds of what an expert manual audit finds, and about 2.5% of keyboard failures. A clean gate run means no *known* defect is present. It does not mean accessible.

Every review ends with what wasn't checked — screen-reader output, whether focus order suits the task, whether alt text is contextually adequate, real assistive-technology behaviour, field Core Web Vitals. That section is not boilerplate; it's the point.

## Scripts

- `probes.js` — in-page probes: contrast, overflow, targets, semantics, focus rules, label/value hierarchy, computed styles
- `run_review.py` / `run_review.mjs` — capture at a viewport matrix with staged interaction states; identical output layout
- `analyze_styles.py` — systematisation metrics: spacing scale, token drift, near-misses, hierarchy vectors
- `scan_source.py` — 25 tiered source rules
- `annotate.py` — crops, grids and slices for visual evidence

## Evals

`skills/design-review/evals/` holds four task evals with seeded and deliberately-clean fixtures, plus a trigger-eval set for description tuning. The clean fixture is a control: a review that pads it with invented nits has failed.

## Licence

MIT

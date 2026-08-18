<p align="center">
  <img src="assets/banner.png" alt="create-test-suite: a porcelain icon of a three-by-three grid of captured frames, one filled vermilion and the ninth cell an empty socket pressed into the tile, beside the wordmark and the line: a test campaign, and a page that shows what it actually proved" width="100%" />
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> create-test-suite</h1>

<p align="center"><strong>A test campaign, and a page that shows what it actually proved.</strong><br />
A SWE skill for Claude Code that reads what your project claims to do, tests it across the states and viewports and roles nobody gets to, and leaves one browsable page where the gaps are as visible as the passes.</p>

<p align="center">
  <img alt="Version 0.1.0" src="https://img.shields.io/badge/version-0.1.0-D33C21">
  <img alt="SWE skill: testing" src="https://img.shields.io/badge/SWE_skill-testing-434A55">
  <img alt="Lanes: web, RN, macOS, iOS, SwiftUI" src="https://img.shields.io/badge/lanes-web_·_RN_·_macOS_·_iOS-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

Here are two test suites. Both green, both wrong, and neither one looks it.

The first covered a console with six screens. Five of them were receiving none of the sweeps, because the surface list came from a capture contract that had quietly deduped six screens onto one route. Nothing in the run reported that. The output had exactly the headings a complete run would have had, which is the whole problem.

The second ran 524 assertions across 13 tenants. Every one of those assertions opened `/`, at 1280px or wider, against the reference build. It stayed green for months while every generated tenant shipped with no header, no navigation and no footer.

What those two share is a number with no denominator. "524 assertions" reads as breadth. "41 of 52 surfaces, 3 of 8 viewports, 1 of 4 roles" reads as a sample, because that's what it was. The second version is the one you can act on, and it's the one almost no suite prints.

So this skill is built around making the sample say itself out loud, and around a handful of gates that fail rather than shrug.

## What it does

**It reads the project before it reads the DOM.** Overview, PRD, feature specs, design md, the latest mock UIs. Enumerating routes first gives you DOM-driven coverage, which over-tests trivia and misses requirements; a build can't tell you about a control it never rendered. Requirements come out classed **affordance**, **behaviour**, **honesty-guardrail** or **deferred**, and each one gets a stable id.

**It states the correctness space, then declares its sample.** Surface, state, viewport, theme, role, locale, data shape, input modality, network, and which oracle. Pairwise across the lot as a floor, higher strength on the clusters that actually interact. Sampling is unavoidable; sampling in silence is the bit that hurts.

**It sweeps for what no requirement named.** State matrix, fault injection, interaction integrity, keyboard and the accessibility floor, data-shape stress, security surface, multi-user, refusal honesty, metamorphic relations, freshness. Every sweep prints `examined=41 failures=0`, because `failures=0` on its own is a claim rather than a result.

**It measures the build against its design of record.** Structure, resolved style (longhands only), the vocabulary each screen uses, and quantised box geometry. Not pixels; rendering noise buries the signal, so a pixel diff gets treated as a tripwire and never as a verdict. This is the only phase that can see a control the design specifies and the build simply doesn't have.

**It leaves a page.** Coverage with the oracle mix and the armed ratio, requirements and what checked them, a wall of every capture, user-flow storyboards with per-step atoms, surfaces, the component atlas, defects, **not covered**, and methods. Every row is an anchor: `REQ-004`, `SURF-009`, `FLOW-002.03`, `CASE-0117`, `DEF-006`. A review comment can point at one of those a year later and still land.

## The rule that does the most work

Every case declares which rung of oracle it stands on:

| rung | what it asserts |
|---|---|
| `touch` · `presence` | the step ran; an element exists |
| `structural` | role, accessible name, enabled state |
| `outcome` | the promised effect, so data rendered or a record written |
| `metamorphic` | a relation across runs, so undo restores or the count tracks the store |
| `visual` | the rendered result against a reference |

A flow you've marked critical that carries no case at `outcome` or above **fails the gate**. Not a model reviewing the suite and offering an opinion; a script exiting non-zero with the flow ids in the output.

That rule is there because of a measurement. Across 214 UI components, behavioural relations were exercised far more often than they were actually checked, validated in only 42.5% to 47.6% of cases. (August 2026 preprint, no independent replication yet, so it's a direction rather than a threshold.) A suite can execute nearly everything and assert almost none of it, and no count of tests will show you that.

Two more gates in the same spirit. **A pass has to name an evidence artifact on disk**; a verdict you reached by looking isn't a measurement. And **armed and unarmed assertions are counted separately, never summed**. Arming means reverting the behaviour an assertion guards, watching it go red, then restoring it. On one campaign 13 of 225 assertions were armed, and "13 of 225" is the honest number to print.

## The defect class it's named after finding

A GraphQL client configured with `errorPolicy: 'all'` **resolves** an awaited mutation when the response carries errors. So this:

```ts
try { await mutate(); toast('Saved') } catch { /* never runs */ }
```

confirms work the server refused. Four instances of that were live in production across three screens of one console.

It's worth naming because of what it defeats. An element-exists test passes; the element exists. A screenshot looks perfect; it is perfect. A visual judge sees a clean, well laid out screen and says so. Only forcing the server to refuse and then asserting that the interface says so will find it, which is why that's a standard sweep here rather than something you're expected to think of.

## It checks its own instruments first

The skill carries a catalogue of **detector defects**: ten measured ways a check lies, each with the fix.

The one that best explains the category: a dead-control sweep compared `document.body.innerHTML.length` before and after clicking each control. Choosing an option writes `aria-pressed="true"` on one control and `"false"` on another, which is length-neutral, so six working presets reported dead on a page where every single control worked.

Same file covers the sweep that writes. Enumerate-and-click on a surface whose controls are save buttons placed a section and set seven theme pairs on a live tenant record, four times in one morning. The answer isn't to skip write-bearing surfaces; it's to refuse the writes locally, so a control wired to a mutation still renders its refusal and still proves it acted, while a control wired to nothing still reports dead.

When a check tells you something surprising, the prior is that the instrument is wrong. It's younger than the application.

## Across platforms, to each lane's ceiling

Web, React Native, macOS, iOS and SwiftUI, planned to what each lane can genuinely observe rather than to what the web lane can.

iOS Simulator exposes no accessibility tree, so there are no elements, no identifiers and no geometry assertions. SwiftUI exposes no runtime style tree, so the style layer is a triangulation rather than a read. Those get marked `n/a` with the structural reason attached, which reads honestly on the page, instead of sitting open forever and looking like neglect.

## What it won't do

Worth saying plainly, since the gaps are the point of the whole thing.

**A model verdict never gates.** As a non-crash oracle the measured ceiling is around 49% of known bugs, with false positives. Judge output is a hypothesis until a deterministic check reproduces it. One real judging pass cost 178 calls, 1.69M input tokens and roughly US$6, and returned 11 pass, 13 fail and 36 inconclusive over 63 surfaces. That inconclusive share isn't a fault in the run; it's what an honest judge says when most of what a flow promises can't be seen in a still picture.

**It doesn't replace a person looking at the thing.** It gets a lot further than a green suite does, and it tells you precisely where it stopped, which is different from finishing.

**Generation is still half redundant.** Mozilla measured LLM-generated QA plans against Firefox's own QA team: 27% valuable and new, 50.5% duplicates, 22.5% invalid or out of scope. That's why the coverage model does the planning and the model does the writing, and why deduplication is treated as most of the value rather than tidying up afterwards.

## Lineage

It's the successor to `acceptance-e2e`. Ten gaps in that skill were each measured during a real multi-day campaign before any of this was designed, and every structural decision here traces back to one of them. `references/evidence.md` carries that trace alongside the research citations, including the three places the research disagrees with itself and the two figures dropped when their only source turned out not to exist.

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install create-test-suite@fledgeling-plugins
```

Then `/create-test-suite`, or just ask Claude to test something properly.

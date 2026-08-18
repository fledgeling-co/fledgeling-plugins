# The coverage model — what the campaign is a sample *of*

Coverage is a cross-product, sampling it is inevitable, and **silent sampling is
the only failure**. A suite that ran 524 assertions across 13 tenants and never
opened a route other than `/`, a viewport under 1280px, or a build other than the
reference one stayed green for months while every generated tenant shipped with
no header, no navigation and no footer. The assertion count implied a breadth it
did not have, and nothing in the suite could say so.

This file is how a campaign states its denominator. Two halves: the space, and
the sample taken from it.

---

## 1. The space is a constrained product, and one of its axes is the oracle

Enumerate the axes the feature genuinely varies on. Ten recur; not every campaign
carries all ten, and an axis with one value is still declared, as held fixed.

| Axis | Typical values | Why it earns a column |
|---|---|---|
| **Surface** | route, screen, portalled dialog, sheet | The unit of navigation. Note which surfaces are *not* routes — a modal has no URL and gets missed by route enumeration. |
| **State** | empty · loading · partial · populated · over-full · error · refused · stale | The single highest-yield axis. Most surfaces are only ever tested populated. |
| **Viewport** | the project's own breakpoints, plus one below the smallest | Truncation, reflow and scroll-trap defects live only here. |
| **Theme** | light · dark · high-contrast · forced-colors | Contrast and focus-ring defects are theme-local by construction. |
| **Role** | each permission level, including the one that may only read | A write control rendered to a viewer is a defect no happy-path case can see. |
| **Locale** | LTR-short · LTR-long (expansion) · RTL · a non-Latin script | Partition by *layout behaviour*, not by language count. |
| **Data shape** | zero · one · typical · large · long-string · unicode/emoji · null-optional · malformed | Seeded through the API as predicates, never proper nouns. |
| **Input modality** | pointer · keyboard · touch · screen reader · accessibility action | Keyboard-only reachability is a requirement, not a sweep. |
| **Network** | normal · slow · offline · 4xx · 5xx · abort · duplicate submit | Forced by interception; not an environment you wait for. |
| **Oracle facet** | which *property* the case checks — see §3 | The axis everyone omits, and the reason a plan can look complete while proving nothing. |

**The product is constrained, and the constraints are part of the model.** A
viewer role has no publish control; a touch viewport has no hover state; a
refused state cannot co-occur with an empty one. Declare each constraint, because
an unconstrained product manufactures cells that cannot exist, and a plan that
counts them reads as broader than it is.

**Do not derive the axes only from what the application currently renders.** NIST
gives the general form of this warning for combinatorial models: a model built
from existing use cases reproduces the blind spots of those use cases. A
DOM-derived axis list can never contain the control the design specifies and the
build lacks — that comes from `project-comprehension.md`, and it is why the
requirement inventory runs first.

---

## 2. Sampling: pairwise as the floor, higher strength on risk clusters

Combinatorial sampling is the mature part of this file. NIST's synthesis reports
suite reductions of **20×–700×** against exhaustive testing while approaching its
fault detection, across general software.

The interesting part is a genuine disagreement in the research, and the skill
carries both sides rather than picking the convenient one:

- Two of the three reports treat **pairwise (2-way) as the practical baseline**,
  on the general CIT finding that most faults are triggered by interactions among
  a small number of parameters.
- The third supplies direct counter-evidence from the closest thing to a UI
  study anyone has: a NIST DOM experiment where **2-way and 3-way detected only
  37.5% of faults, while 4-way detected everything exhaustive testing found, with
  95% fewer tests**. That study is from 2012 and has not been replicated on a
  modern component stack.

**The resolution, and it is a judgement rather than a finding:** take pairwise as
the *global* floor across all declared axes, and raise the strength to 3- or
4-way **locally**, on the clusters where the axes are known to interact — theme ×
viewport × locale for layout, role × state × network for authorisation, data
shape × viewport for truncation. Global high-strength arrays generate cost and
oracle work out of proportion to their yield.

Two disciplines make the sample honest:

- **Partition before you sample.** Each axis is reduced to equivalence classes
  chosen for *behavioural* similarity, and the partition is written down. "Twelve
  locales" is not a sample; "one LTR-short, one LTR-long, one RTL" is.
- **Oversample by risk, never undersample in silence.** Weight up accessibility
  modes, previously-failing configurations, high-traffic surfaces and anything a
  requirement classes as an honesty guardrail. Where a cell is deliberately
  dropped, `log` it — a silent truncation reads as "covered everything".

The campaign records the sample as data: axes, their partitions, the strength
used per cluster, and the cells deliberately excluded with a reason. That record
is what the report shows instead of a single percentage.

---

## 3. The oracle ladder — touch is not cover

The most useful recent finding in this area is also the least intuitive: UI
component suites **execute** behaviour far more often than they **check** it.
Inferred metamorphic relations across 214 components were exercised at high rates
but explicitly validated only **42.5%–47.6%** of the time. (August 2026 preprint,
no independent replication — held as directional, not as a threshold.)

So every case declares which rung it stands on, and the rung is a first-class
field in the registry:

| Rung | What it asserts | What it cannot catch |
|---|---|---|
| **touch** | the step ran without throwing | everything |
| **presence** | an element exists / is visible | wrong content, wrong destination, lost persistence |
| **structural** | role, accessible name, enabled state, scoped ARIA snapshot | a correct-looking tree over wrong data |
| **outcome** | the promised effect — data rendered, state changed, record written, navigation completed | a change that is right once and wrong on the second run |
| **metamorphic** | a relation across two runs — undo restores, row count tracks the store, sort is a permutation, locale change preserves affordances | absolute correctness of the first value |
| **visual** | the rendered result against a design of record | anything not visible |

**The planning gate:** a flow the requirement inventory marks critical may not
consist only of `touch` and `presence` cases. That single rule is what converts
"we have 200 tests" into a claim worth making, and it is checkable — which is why
it lives in `campaign.py` rather than in prose.

`presence` is not banned. It is the right rung for "the nav renders on every
screen". It is the wrong rung for "publishing the record makes it live", and the
gate exists because that substitution is silent.

---

## 4. What generated plans get wrong, measured

The failure modes are not folklore. Mozilla ran LLM-generated test plans against
Firefox's own QA and classified every scenario: **27% valuable and new, 50.5%
duplicates, 22.5% invalid or out of scope**. A two-stage industrial pipeline
generating executable acceptance tests found **60% usable as generated**, with
the remaining 40% needing repair, regeneration or disposal.

Read together they say something specific: generation is worth doing, and **half
the output is redundant**, so deduplication is not a polish step — it is most of
the value. Four consequences the campaign is built around:

- **The coverage model plans; the model writes.** Never hand an LLM the job of
  deciding what to cover. Hand it a path and a parameter combination drawn from
  the sample, and ask for the implementation and candidate assertions. Free-form
  planning is where duplication and happy-path bias enter.
- **Deduplicate against the coverage model, not against the prose.** Two cases
  that traverse the same path under the same cell are one case however
  differently they are worded.
- **Validate before admitting.** A generated case that does not run is discarded
  or repaired; it never reaches a gate.
- **Separate intention from implementation.** The case's identity, requirement
  link, cell and oracle rung are data. The code is an artifact of them. This is
  what lets a case survive a harness migration with its history intact.

A fifth, and the sharpest: **the model that wrote the code must not be the sole
oracle for it.** Generated tests demonstrably validate faulty implementation
behaviour, and faulty code in context biases subsequent generation. The defence
is the requirement inventory — an oracle sourced from the *specification*, not
from the build — plus arming, which is the empirical version of the same idea.

---

## 5. Coverage numbers that mean something, and the one that does not

**Structural coverage stays diagnostic.** A 2026 web-GUI study found code
coverage weakly correlated with failure revelation, and the metamorphic work
above shows why: reaching a line is not checking it. Line coverage may inform the
next round of planning. It may not be the release gate, and it may not appear as
the headline number.

What replaces it, and what the living page shows:

- **Requirement trace** — every non-deferred requirement has at least one case.
  This is the only completeness claim the campaign is entitled to make, and it is
  bounded by the document set it read.
- **Cell coverage per axis** — which surfaces have been seen under which states,
  themes, viewports and roles. Shown as a matrix, so a blank column is visible.
- **Oracle mix** — the share of cases at each rung, per flow. A critical flow
  whose mix is all `presence` is the finding.
- **Armed ratio** — cases that have been watched fail, over cases that exist. An
  unarmed pass is not evidence, and the two are never summed.
- **Examined denominators** — `examined=41 failures=0`. A row reading
  `examined=0` is a check that never ran.
- **Not covered** — a named, first-class section. Deferred requirements, blocked
  lanes, axes held fixed, cells dropped. A campaign that omits this reads as
  complete and is not.

---

## 6. Where a single number is still wanted

There is no defensible scalar for "how tested is this". The nearest honest thing
is a **gate**: the ledger's `check` command exits non-zero while any cell is
open, so the answer to "are we there" is a process exit code with a list
attached, not a percentage. Everything above feeds that gate; none of it averages
into it.

# Evidence

Every rule in this skill traces to something. Where a rule rests on a
standard, the standard is named; where it rests on a measurement, the
measurement and its population are given, because an effect measured on 56
projects and an effect measured on 31,000 test suites are not the same kind of
claim.

The full corpus is in `docs/deep-research/` — three deep-research panel
members (OpenAI gpt-5.6-sol, Gemini deep-research-max, Perplexity Sonar
Deep Research, 173 cited sources between them, ~$20) and two design-review
lanes (Gemini 3.7, Fable 5). Run 21 August 2026.

## The partition is a closed-world reconciliation

**Rule:** every entity resolves to exactly one class; an item missing from the
partition fails the gate.

Regulated verification does not filter, it partitions. **ECSS-E-ST-10-02C
Rev.1** mandates a Verification Control Document recording, per requirement,
the evidence, a compliance verdict of yes/no/partial, a close-out state of
open/closed, and the reason — so an unclosed requirement is a row, not an
absence. **FDA's 2023 device software guidance** requires traceable expected
results, observed results, an explicit pass/fail determination, and a record
of unresolved anomalies. **FAA AC 20-189** frames problem-report management
explicitly as preventing loss of visibility of critical issues.

The panel's synthesis of these: *"If any item is absent from the partition,
the determination is invalid — not complete."* That sentence is what
`reckon.py` exit 1 implements.

- ECSS-E-ST-10-02C Rev.1 (1 Feb 2018) — <https://ecss.nl/wp-content/uploads/2018/02/ECSS-E-ST-10-02C-Rev.1%281February2018%29.pdf>
- FDA, Content of Premarket Submissions for Device Software Functions (2023) — <https://www.fda.gov/media/153781/download>
- FAA AC 20-189 — <https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-189_%28final%29.pdf>

## `unmeasured` is a first-class verdict, not a missing one

**Rule:** blocked, inconclusive, unoracled and carried cases get their own
class, and the legality table forbids them any other.

This is standard practice in test notation rather than an invention here.
**TTCN-3** (ITU-T Z.161, ETSI) defines five verdicts — `none`, `pass`,
`inconc`, `fail`, `error` — and `inconc` exists precisely for behaviour that
is "neither clearly passing nor definitively violating the specification".
**Runtime-verification LTL** uses four values (`true`, `false`,
`presumably true`, `presumably false`) because finite executions cannot settle
every property.

That explicit unknowns change decisions rather than merely documenting them is
supported by analogy rather than by software measurement, and is flagged as
such: the Scottish three-verdict system and the Ellsberg ambiguity-aversion
results both show that a marked "unknown" is evaluated differently from an
unknown coerced into a binary. Treat this as motivation, not proof.

- ITU-T Z.161 (TTCN-3 core language) — <https://www.itu.int/rec/T-REC-Z.161>
- RV-LTL / finite-trace semantics — <https://trustworthy.systems/publications/nicta_full_text/3976.pdf>

## Status reporting drifts optimistic, measurably

**Rule:** the report leads with what it cannot speak for, and enumerates
everything rather than filtering to what looks significant.

**Snow, Keil and Wallace (2007)** surveyed project managers and found bias in
**60%** of software-project status reports, with optimistic bias roughly twice
as likely as pessimistic, and only an estimated 10–15% of biased reports
accurate. Population: 56 usable surveys — directly relevant, not a population
estimate for the industry.

The "90% done" and "watermelon status" effects are well-established
practitioner vocabulary; the panel looked for robust software-specific effect
sizes and did not find them. Named here as folklore, not evidence.

- Snow, Keil & Wallace, *Information & Management* — <https://doi.org/10.1016/j.im.2006.10.009>

## Coverage numbers mislead without their denominators

**Rule:** a denominator per axis, never one blended percent, and a pass rate
among executed cases is never labelled coverage.

**Inozemtseva and Holmes (ICSE 2014)** generated **31,000 test suites** across
five systems of up to **724,000 lines**, and found only low-to-moderate
correlation between coverage and suite effectiveness once suite size was
controlled for. Coverage is a weaker proxy than its use implies.

**Google's flaky-test data**: about **1.5%** of test runs flaky, nearly
**16%** of tests showing some flakiness, and roughly **84%** of pass-to-fail
transitions involving a flaky test. A green suite is not evidence in
proportion to how green it is.

The panel's rule, adopted verbatim: disclose planned, executed, determinate,
passed and each non-pass status separately, and never label a pass rate as
completeness.

- Inozemtseva & Holmes, *Coverage Is Not Strongly Correlated with Test Suite Effectiveness* — <https://doi.org/10.1145/2568225.2568271>
- Google Testing Blog, Flaky Tests at Google — <https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html>

## A waiver is an exception, never a pass

**Rule:** `n/a` and `skip` resolve to `waived`, are excluded from the
adjudicated numerator, and a waiver with no recorded reason fails the gate.

This class exists because the research found it missing from the draft design.
Both the ECSS close-out model and the FDA anomaly record keep approved
deviations in a register separate from verified items, and the OpenAI panel
member was explicit: *"An approved deferment or waiver is an exception, not a
pass"*, recommending it stay nonzero in a release gate so a campaign closed
with waivers cannot read as fully done.

This skill takes the classification and not the exit code — see the note on
gate semantics below.

## Verification gaps generate typed work items

**Rule:** each `unmeasured` row carries its own remedy, and evidence-work
never enters a feature backlog.

The panel's finding: blocked, inconclusive, carried, weak-oracle, stale and
reported-only items must each mechanically produce a child item — unblock the
environment, add controllability or observability, build an oracle, re-run
against the current baseline, or obtain independent evidence. These are the
five remedies in `REMEDY` in `reckon.py`, and they map to the classical
software-testability axes of controllability and observability.

## Where this skill departs from the research

**Gate semantics.** The OpenAI panel proposed exit 1 for `REMAINING_WORK` —
a release-gate reading, where any outstanding work is a non-zero exit. This
skill gates the *integrity of the report* instead: exit 1 means the ledger
lost or misplaced an item, exit 2 that a headline is unsupported. Remaining
work is content, at exit 0.

The reason is operational. Remaining work always exists, so a gate that fires
on its presence fires on every run, and a gate that always fires gets switched
off — which is `test-campaign`'s own stated failure mode. A skill that wanted
release-gate semantics should read `summary.work_items` and decide for itself.

**Reading source code.** The Gemini design lane argued for never reading
source, on the grounds that a shallow grep produces false confidence and
duplicates `spec-validation`. The Fable lane argued for reading it only where
documents and registry disagree, capped so that code evidence may **only
demote or route, never promote**. This skill took Fable's position, because
its cap answers Gemini's objection directly: a grep hit cannot close an item,
so it cannot manufacture confidence.

Recorded as a genuine disagreement between reviewers, resolved with a reason,
not a consensus.

## Rules that rest on this project's own evidence

Not everything here comes from literature. Two rules were derived from the
scrim campaign this skill was built against (58 cases, 21 August 2026) and are
labelled as local observation:

**Blockers cluster.** Its stop declaration recorded one dead OAuth credential
accounting for ten of twenty blocked cases. Scheduling blocked cases
individually would have produced twenty line items concealing the three worth
doing. The clustering threshold (0.30 token overlap) was swept on that data;
it is a starting point for a human to regroup, not a settled constant.

**The join is the weak step.** 16 of 29 briefs joined to any registry entity,
and only because the campaign's own notes cite brief ids by hand. This is why
`join.weak` degrades retirement claims rather than blocking the run.

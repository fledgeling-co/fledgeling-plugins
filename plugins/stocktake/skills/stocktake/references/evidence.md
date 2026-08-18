# Evidence

Every structural rule in this skill traces to one of the following. Where a claim is
carried at paper level rather than verified against the primary source, it says so.

## Do not build a panel

**Kohli, arXiv `2605.29800`, 28 May 2026.** Nine frontier judges across seven families
supply ~2 effective independent votes; panel accuracy falls 8–22 percentage points
short of independent voting; the best single judge matches or outperforms the full
panel across all conditions; established aggregation closes at most 11% of the gap even
given the correct answers. Robust across prompts, temperatures, CoT and RewardBench.

*Provenance:* numbers verified against the arXiv abstract via the arXiv API. An
affiliation attached to this paper by one secondary reader was **not** verified and is
deliberately not repeated here.

## Do not show a verdict before the reader's own pass

**Fenton et al., 2007** — 429,345 mammograms. Concurrent-read CAD: specificity
90.2% → 87.2%, biopsy rate +19.7%, AUC 0.919 → 0.871, no detection gain. Second-read
and arbitration is the positioning that worked.

This is the source of the oracle order: the requirement list is the reader's own pass,
and the worker's record is the marks.

## Inconclusive is a valid result

**ISO/IEC 17025** treats an inconclusive result as valid output rather than a failed
measurement. Carried at standard level.

## Why Verified stays human

- **21 CFR Part 11** — an electronic signature must be unique to an individual. A model
  id is not one.
- **DO-330 Criteria 2** — a tool that could fail to detect an error where its output is
  not otherwise verified; the qualification case is literally this one.
- **PCAOB AS 2201** — benchmarking of an automated control requires the control be
  unchanged. A reversioned model voids the baseline.
- **FDA `DEN180001`** (IDx-DR), the autonomous-diagnosis precedent: n=819 analysable,
  sensitivity 87.4%, specificity 89.5%, imageability 96.1%, and **38 exams forced to
  refer** on insufficient quality. Autonomy was granted with a mandatory
  can't-tell path — which is the shape of the diagnosability gate.
- Evaluator agreement on review findings runs **5–65%, typically ~27%**; roughly 75% of
  code-review findings are evolvability rather than functional defects. The incumbent is
  a weak gold standard, which argues for sampling over substitution. *Paper level.*

## The evidence channel is authored by the party judged

**METR** documents frontier agents editing tests, monkey-patching evaluators and
returning the scorer's own reference tensor. A major benchmark was retired over
leakage. Nothing attests test provenance the way SLSA/in-toto attest builds.
*Carried at organisation-report level.*

## Suites are weaker than their pass rate

More than half of over 15,000 mutants survived a rigorous suite at **Facebook**.
*Paper level.*

## Author-judged acceptance

Roughly **half of a 110-ticket corpus** shipped not-as-specified while reading as
complete — the finding that `shipyard:verify` was built on, and the reason this skill
requires an out-of-family grade rather than an author's own.

## Unarmed-assertion shapes

Observed directly, in one session, in work its author had declared red-armed: a
self-comparing `expect`, a type-only assertion satisfied by a guard that raised the
same type, a fixture in a shape the product never stores, a substring grep for a
variable's name, and a source slice that stopped short of its subject. Five shapes,
ten out-of-family verifications, ten findings, zero clean bills of health.

## Not researched

No fresh research panel was bought for this skill. A prior panel on the adjacent
question — whether an automated verifier can replace the human acceptance step — is
described in the originating project's `status-check.md`, but its report files were not
present on disk, so they could not be read or cited. What is carried above comes from
that document's own primary-source-verified findings. The gap: no independent survey of
*board-triage practice specifically* informs this skill, and its process rules come from
measured practice rather than from literature.

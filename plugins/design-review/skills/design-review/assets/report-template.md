# Design/UX review — <scope>

**Verdict:** Solid / Needs work / High risk (<n of n surfaces reviewed, all stages | m stages open on k>) — <one sentence why>

<!--
The fraction is not optional and not only for partial reviews. A finished review
says "(14 of 14 surfaces, all stages)". If the fraction only appears when coverage
is short, its absence becomes the signal — and a partial review then looks
finished, which is the failure this line exists to stop.

Drop any section with nothing in it. An empty heading is padding with extra steps.
A clean surface gets a clean verdict and a short report.

Every finding:

[SEVERITY] <screen / file:line / element> — <what's wrong>
→ Should be: <specific replacement — real values, real copy, real structure>
→ Why: <observation → mechanism → consequence>
   (Tier: 1|2|3) (Lenses: …) (Evidence: crop-07.png @2x, 375px)

Fixes are executable without design interpretation. "Make the CTA stand out" is
not a fix; a hex value, a measured ratio and a demotion instruction is.
-->

## Coverage

<!-- Never omitted, never softened. The largest failure mode of a review is not a
wrong finding, it is a confident silence over a region nobody looked at. The
component fraction comes from probeComponentInventory(); if you didn't run it,
write "? of ?" rather than a number you feel. The surface fraction comes from the
stage-0 worklist, not from what you happened to get to — a denominator set after
the fact always equals the numerator. -->

- **Surfaces:** <n of n from the worklist; which ones, and which are open>
- **Screens:** <n of n at which widths; which screens got the full viewport sweep>
- **Component types:** <n of n cropped and opened, and the rule used to pick them>
- **States driven:** <which; and which were not>
- **Probes:** <full sweep on what; analyze_styles.py on what>
- **Tokens:** <matched against <source> — n tokens, n values off-token | searched for a token source and found none>
- **Contrast:** <n failed / n passed / n could not be resolved, of n examined>
- **Not measurable on this engine:** <from the run summary: the channels that would not answer, which metrics were recovered from declarations and labelled, which are dark>
- **Ledger:** <workdir>/worklist.md — <n rows, n open cells>
- **Lookalike:** <n/a: incumbent system | n/a: no comparison | n/4 MET · families <n> · first-viewport elements <n> · accents in 100vh <n> · display-face collision yes/no · compared against <set>>
- **Not looked at:** <named, not implied>

"Gates clean" and "design sound" are two sentences. Write both or neither.

<!-- The unmeasurable line is not optional. A review that omits it has folded
everything it could not measure into zero, and a zero from a dead channel reads
exactly like a clean surface. Take the list from run_review.py's summary and
`audit_run.py capability`. Any metric that came back UNMEASURABLE is named here
and never printed as a count. -->

<!-- If any cell in the worklist is open, say so here in the shape the skill
requires: "7 of 14 surfaces reviewed, resuming at 8." Sampling deliberately is
fine and gets stated as a decision: which surfaces, chosen how, and what the
sample cannot speak for. Silent sampling is the thing this block prevents. -->

## Context

<Audience, device, attention level. Product UI or marketing. What conversion
means here. What design system exists. Anything the surface is deliberately
doing that a naive reviewer would flag.>

## Distinctiveness

<!-- Required when the brief asked for a distinct site, more than one generated
site exists, or visitor mode is Persuade/Experience. Drop the section when the
surface matches an incumbent Operate/Read system or the user asked for the
category standard played straight — and write the n/a reason in Coverage. -->

- **Applies:** yes / n/a: <reason>
- **Comparison set:** <session or repo siblings · named category default · named neighbour or none>
- **Score:** <n/4 MET> — topology <MET/UNMET> · type <MET/UNMET> · signature <MET/UNMET> · swap test <MET/UNMET>
- **Counts:** layout families <n of sections / unique families> · first-viewport elements <n vs neighbour> · accent moments in 100vh <n> · display face vs sibling <same/different>
- **Finding:** none / Medium with pasteable topology, type, signature, or subject-mining change. Never a Blocker or High on taste alone. An adjective without these numbers belongs in Open questions.

<If 2/4 or below, the repair is ours: change topology, type, signature class, or subject-mining. Do not clone the neighbour.>

## Blockers & High

<Quick wins first within each severity.>

## Medium

## Low / Polish

<Compressed bullets. No full format needed.>

## Cross-cutting themes

<Patterns multiple lenses caught independently. These are the real story. Max 3.>

## What's working

<Short, factual. Practices to keep — and what a fix must not break.>

## Open questions

<Tier 3 prompts. Unclear deviations — the ones that are questions rather than
defects. Anything needing a product decision rather than an engineering one.>

## Needs verification

<What this review could not prove. Never empty.

Standing items unless separately covered — these are human-judgment ceilings:
- Screen-reader output and flow
- Whether focus order makes sense for the task
- Whether alt text is contextually adequate
- Dynamic ARIA state transitions
- Cognitive accessibility
- Real assistive-technology behaviour on real devices

Standing items unless separately covered — these are engine ceilings on Obscura,
and they are the same every review rather than something to rediscover:
- Motion and transitions: never execute, so no mid-flight capture, no entrance
  timing, and getAnimations() is 0 whatever the page declares
- Print media: setEmulatedMedia is accepted and inert, so there is no print pass
- prefers-reduced-motion: same, so the reduced-motion branch is unverified
- Font fidelity: web fonts never load, so a loaded face and a 404'd one measure
  identically. Report unavailable, never zero divergence
- box-shadow, background-image, text-transform, outline, flex and the transition
  longhands: unreadable as computed values. Recovered from stylesheet
  declarations where one exists, and a declaration is intent rather than a
  resolved cascade
- Clipped-text detection under-reports
- Native form controls do not render, so a real radio or checkbox can read as a
  missing affordance
- SVG path geometry: getBBox returns zeros without throwing

Anything measured against a declared gradient stop is conditional on where the
glyph actually sits in the sweep. Say so on the finding.>

## Suggested order

1. <Highest impact-per-effort first>

---

```
Gates:       <what a machine asserted — lint, probes, console, CWV>
Looked at:   <what you assert — only captures you actually opened>
Not checked: <never empty>
```

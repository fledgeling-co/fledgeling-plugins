# Design/UX review — <scope>

**Verdict:** Solid / Needs work / High risk — <one sentence why>

<!--
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
write "? of ?" rather than a number you feel. -->

- **Screens:** <n of n at which widths; which screens got the full viewport sweep>
- **Component types:** <n of n cropped and opened, and the rule used to pick them>
- **States driven:** <which; and which were not>
- **Probes:** <runAll on what; analyze_styles.py on what>
- **Not looked at:** <named, not implied>

"Gates clean" and "design sound" are two sentences. Write both or neither.

## Context

<Audience, device, attention level. Product UI or marketing. What conversion
means here. What design system exists. Anything the surface is deliberately
doing that a naive reviewer would flag.>

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

Standing items unless separately covered:
- Screen-reader output and flow
- Whether focus order makes sense for the task
- Whether alt text is contextually adequate
- Dynamic ARIA state transitions
- Cognitive accessibility
- Real assistive-technology behaviour on real devices>

## Suggested order

1. <Highest impact-per-effort first>

---

```
Gates:       <what a machine asserted — lint, probes, console, CWV>
Looked at:   <what you assert — only captures you actually opened>
Not checked: <never empty>
```

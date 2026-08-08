# Evals and judging — proving a skill that has no predecessor

`improve-skill` compares a rebuild against the thing it replaced. There is
no such thing here, so the baseline is **the same prompts run with no
skill at all**. That is the honest question for anything new: does this
earn the context window it costs?

Two layers, deliberately different in kind: structural assertions
(deterministic, artifact-checking) and a blind quality panel (judged,
multi-family). Neither substitutes for the other.

## Layer 1 — structural assertions

Score-free by design: LLM 1-10 ratings collapse toward the middle and
don't model real trade-offs, so every assertion is a checkable property
of the output ("the file exists at the stated path", "every claim carries
a citation", "no run touched git").

1. **Write `evals/evals.json`**: 6-8 prompts drawn from the discovery
   brief's *definition of done*, plus the failure modes the research
   surfaced, plus at least one adversarial case where the obvious
   approach is wrong. Each carries assertions verifiable by reading the
   output or running a command.
2. **Run each prompt twice** — once with the skill, once with no skill —
   as parallel background subagents (capped agent budgets, per-run output
   directories, **no git operations**). skill-creator's runner conventions
   apply; use them rather than inventing a parallel harness.
3. **Grade with an independent subagent**: every assertion marked
   passed/failed with quoted evidence, in the `grading.json` shape the
   tooling reads. The baseline failing an assertion honestly is the
   point of the comparison.
4. **Watch for the assertion that cannot fail.** A new skill's evals are
   especially prone to this, because the author writes them knowing the
   intended output. If the no-skill baseline passes an assertion too,
   that assertion is measuring the model, not the skill: rewrite it or
   drop it, and say which.

## Layer 2 — the blind panel

Only worth running where the output is a matter of judgment rather than
an artifact check. If the discovery interview said the output is
objectively verifiable, the structural layer is sufficient and a panel
adds cost without evidence.

- **Anonymise**: both outputs become Option A / Option B in seeded-random
  order per eval, in a self-contained bundle. Record the un-blinding map
  separately.
- **Judges never see the skill**, and are not told either side is a
  baseline: "which of these two better achieves X" is the question, not
  "is the skill better".
- **Heterogeneous families, honestly sourced**: CLIs you're signed into,
  APIs with keys from 1Password or a named env file, never hardcoded. A
  rate-limited family is reported and substituted, with the harness named.
- Capture the `usage` object per call and **report exact cost** from
  token counts at published rates.
- **Un-blind and tally** per dimension. Deadlocks are reported as
  deadlocks.

## Layer 3 — iterate

- Every confirmed defect becomes a rule in the skill **the same day**,
  and the eval that caught it stays in the set.
- **Re-judge the lost case blind** after the fix, fresh random order,
  same judges. A flip is the strongest evidence this pipeline produces.
- The grader's own complaints (vacuous assertions, untestable claims) are
  the next iteration's eval work.

## When the skill does not beat the baseline

Report it plainly, then diagnose. Usually one of:

- **The evals measure the model, not the skill.** Rewrite them against
  the discovery brief's done condition rather than against generic
  quality.
- **The skill's value is consistency, not peak quality.** Then measure
  variance across repeated runs, not a single-run comparison, and say
  that is what you are claiming.
- **The skill genuinely adds nothing.** Say so and drop it. A skill that
  changes nothing still costs context on every session it loads into, and
  implies a guarantee it does not keep.

## Reporting

`evals/EVALS.md` carries the per-eval table for both layers, the judge
families and harnesses, the un-blinding data location, panel cost, and
the caveats — single runs carry sampling noise, and blind judges score
content only, so on-disk artifacts earn nothing there by design. Written
for a non-technical reader, with the deep detail lower in the file.

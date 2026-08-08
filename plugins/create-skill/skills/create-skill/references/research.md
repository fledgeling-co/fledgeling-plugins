# Research — the Dossier panel protocol

The research phase buys the evidence every later phase leans on. It is
also where real money gets spent, so the sequence is fixed.

## Sequence

1. **`research_budget`** — check headroom before committing anything.
2. **`research_plan`** (free) — pass a question about the skill's
   DOMAIN, not about the skill: the techniques, measured results and
   failure modes in the field it will operate in. The `decisionContext`
   names what you are building and the design choices you want to be
   able to defend. The plan names the panel members and their cost
   bands; relay the worst-case total.
3. **`research_start`** with the plan's `contractFingerprint` and NO
   `provider` — omitting it assembles the panel: free lane (signed-in
   CLIs, subscription quota) plus paid lane (API backends chosen for
   distinct strengths). This is what "paid+free panels" means.
4. **Monitor, don't block.** `research_status` on a timer (a background
   `sleep && check` loop re-invokes you; don't poll hot). Panels run
   4–60 minutes. Do other pipeline work meanwhile — the meta-pass, the
   eval scaffold, the source-skill read.
5. **Never report an early member.** Support is counted in independent
   domains, not in how many backends agree; reporting an early member's
   findings turns one page into several apparent sources.

## The question shape that works

Ask for evidence-backed techniques AND known failure modes, enumerate
the subtopics (how practitioners do this today, what measurably works,
how results are evaluated, what goes wrong at scale), bound the time
horizon to recent years, and exclude the adjacent fields you don't need.
A vague question buys a survey; a decision-shaped question buys
defensible design choices.

For a new skill the highest-value subtopic is usually **the documented
failure modes of doing this by hand**, because those are exactly what the
skill exists to prevent, and each one converts directly into a rule and
an eval.

## Read in full — no partials, no distillation-only

When the panel settles:

- **`research_export` every completed member** to disk (full markdown +
  source registries), then **read every report end-to-end** with the
  Read tool. Outlines and merged distillations lose the specific numbers
  and the contested findings — and the contested findings are where the
  design decisions live.
- **`research_verify_citations` on the load-bearing reports.** The
  fabrication check is the number that matters; paywall blocks are
  noise. A confidently fabricated citation is the failure that survives
  into production because nobody clicks.
- **Carry the disagreements forward.** Where reports conflict (they
  will), the conflict goes into the improved skill's evidence file as a
  held-loosely item, not silently resolved.
- **Commit the corpus.** Export the full reports into the new plugin's
  `docs/deep-research/` so every claim in `evidence.md` stays auditable
  from inside the repo.
- **A finding with no design consequence is not a finding.** Each one
  either becomes a rule, an eval, a bundled script, or an explicitly
  discarded option with the reason. Research that changes nothing was
  research nobody needed.

## Failure modes to expect

- A CLI member can fail on startup (environment/config); it costs $0
  and the panel continues. Note it, don't chase it.
- The Codex/other CLI may be usage-limited — that's a judge-phase
  concern too; see `evals-and-judging.md` for substitution rules.
- Budget ledgers show reservations at band-top; actuals reconcile lower.
  Report both honestly.

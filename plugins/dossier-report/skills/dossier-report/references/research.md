# Research — the Dossier panel protocol

The research is the page's substance. It is also where the money goes, so
the sequence is fixed and the reading is not optional.

## Sequence

1. **`research_budget`** — check headroom before committing anything.
2. **`research_plan`** (free) — pass the sharpened question from Phase 0
   with the `/trawl` angles as its numbered subtopics. Set
   `decisionContext` to what the page is *for* and who reads it; it is
   the field that most changes what comes back. Relay the worst-case
   band to the user before spending.
3. **`research_start`** with the plan's `contractFingerprint` and **no
   `provider`**. Omitting the provider is what assembles the panel: the
   free lane (signed-in CLIs, subscription quota) plus the paid lane
   (API backends chosen for distinct strengths). That is what "paid+free
   panel" means, and naming a provider collapses it to one backend.
4. **Monitor, don't block.** A background `sleep && check` re-invokes
   you; don't poll hot. Panels run 4–60 minutes. Report the time
   remaining and say when it changes.
5. **Never report an early member.** Support is counted in independent
   registrable domains, not in how many backends agreed. Reading one
   member early also biases how you read the rest.

## Question shape

Ask for evidence-backed findings **and** documented failure modes.
Enumerate the subtopics from `/trawl` rather than asking one broad
question. Bound the time horizon. Exclude the adjacent fields you don't
need — SEO content, vendor comparisons, tutorials — because excluding
them is what stops the panel spending its search budget on introductory
material.

For a report page the highest-value subtopic is usually **what is
contested**. A page whose centre is a live disagreement reads as
authored; a page that resolves everything reads as a summary.

## When the question is which one to buy

A buying or adoption question needs a differently-shaped brief, because
the corpus a general research prompt returns is dominated by affiliate
content that exists to rank rather than to inform.

- **Name the independent testing organisations as subtopics.** Which?,
  RTINGS, Consumer Reports, Choice, Stiftung Warentest, the relevant trade
  lab. Ask for their published verdicts, their stated protocols, and the
  dates of the group tests. This single change is what separates a corpus
  of measurements from a corpus of opinions.
- **Ask for the dimensions buyers actually split on**, not a feature
  matrix — what fails first, what the running cost is, what the repair
  story is, what the licence or subscription does over three years. These
  become the categories in `product-verdicts.md`.
- **Ask what the enthusiast consensus disagrees with the labs about.** The
  split is a finding, and it is usually where the interesting page is.
- **Exclude explicitly**: affiliate roundups with no stated method,
  retailer star averages, and vendor benchmark claims. Excluding them is
  what stops the panel spending its budget on them.
- **Bound the model years.** A group test of a line refreshed since is
  evidence about things nobody can buy, and the panel will happily return
  it.

**A paywalled verdict is admissible and valuable.** Where a lab publishes
its ranking and keeps the measurements behind a paywall, cite the ranking
as the ranking it is, name the protocol from the free portion, and record
in `limits` that the underlying numbers are not public. Never redraw their
tables. `product-verdicts.md` carries the full rule and the reasoning.

## Read in full — the gate

This is the rule the whole skill exists for. Two pages in this repo were
written from `research_synthesise` output while it was printing
*"5 never opened"* and *"3 never opened"* at the top of its own report.

When the panel settles:

- **`research_export` every completed member** to
  `<page>/docs/deep-research/` — full markdown plus source registries.
  The front-matter records which backend, which model, what it cost.
- **Read every report end to end** with Read. Not the outline, which
  gives every heading and no content and is exactly what makes it feel
  like having read. Not the merged distillation, which is a *coverage
  difference between reports*, not a summary of them.
- **`research_verify_citations`** on the load-bearing reports. The
  fabrication count is the number that matters; 403s from publishers are
  bot-walls and say nothing about whether the source is real.
- **Carry the disagreements forward.** Where members conflict, that goes
  onto the page as stated uncertainty, not silently resolved. Cross-
  backend contradiction is the most valuable thing a panel produces: on
  the run that built this skill, one backend asserted a prevalence
  statistic that another traced and found unsourced.
- **A finding with no page consequence is not a finding.** Each one
  becomes a claim, a visual, a stated limitation, or an explicitly
  discarded option with its reason.

## Cost reporting

Report the plan's band before the spend and the actual after, and name
any member that failed and why. A released reservation (the provider
refused outright, so nothing was created) is different from a held one
(the run was created and may have been billed for work before it failed);
say which.

## Failure modes to expect

- **A CLI member fails on startup.** Costs $0, the panel continues. Note
  it, don't chase it.
- **An API member returns 401 `insufficient_quota`.** That is a billing
  state, not an auth failure — the key is valid and the balance is spent.
  The reservation is released.
- **Live progress falls back to polling.** Counters stop moving until the
  run completes. The run is alive; there is nothing to watch.
- **Budget ledgers show reservations at band-top**; actuals reconcile
  lower. Report both.

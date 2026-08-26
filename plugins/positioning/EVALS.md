# Does it actually work

The honest version. What was measured, what the skill it replaces scored on the
same prompts, what is still untested, and where the numbers came from.

Two things are worth saying before the tables. First, the comparison is only
worth reading if it could have gone the other way, so the eval this build lost is
in here with the rest. Second, a lot of this skill's value is in artifacts a
blind judge reading two answers cannot see: a ledger file, a gate's exit code, a
committed research corpus. Those earn nothing in a taste test, by design.

## The research behind the rebuild

Two Dossier deep-research panels, seven backends, tier `max`, dispatched
26 August 2026. Every completed report was exported to
[`docs/deep-research/`](docs/deep-research/) and read end to end.

### Panel 1: positioning validity, pre-commitment testing, decision aids

| Backend | Model | Sources | Cost | Outcome |
|---|---|---|---:|---|
| OpenAI | gpt-5.6-sol | 46 | ~$9.00 | completed |
| Google | deep-research-max-preview-04-2026 | 74 | ~$7.00 | completed |
| Perplexity | sonar-deep-research | 20 | ~$4.00 | completed |
| Claude Code (CLI) | Claude Code | 22 | $0.00 | completed |
| Antigravity (CLI) | n/a | n/a | $0.00 | **refused at startup** |

The fifth member refused on a binary-identity check: the `agy` on PATH reports a
version that does not identify it as Antigravity, and Dossier will not hand a
brief to an unidentified binary. It cost nothing and is recorded rather than
chased.

Merged with `research_synthesise`, which deduplicates by canonical URL and counts
independent domains: **160 distinct sources across 38 independent domains, with
1% overlap between members.** That low overlap is the case where paying for a
panel earns its cost. It also means any claim only one backend made is
uncorroborated rather than agreed, and the evidence file marks those.

**A quality finding about the panel itself**, since a report on AI research
integrity that hides its own is not worth much. The Google member's export
carries visible citation corruption: truncated `<cite url=)` fragments, and
sentences that break mid-clause where a citation should be. Every one of its 74
sources is a `vertexaisearch.cloud.google.com` redirect, which collapses to one
registrable domain and triggered the merge's "largest single domain 46%" warning.
Its source mix leans on marketing blogs where the other three reached primary
literature. Its findings are used here only where a second member reached the
same primary source independently. That is the source-laundering failure mode the
second panel was commissioned to study, showing up in the first panel's output.

### Panel 2: AI market-intelligence failure profile

Three backends (Google, OpenAI, Perplexity), archetype `technical`, assembled by
hand because the automatic panel could not obtain six concurrent run slots on the
machine. It covers fabrication rates in agentic search, citation verification
versus claim-source entailment, voice-of-customer mining validity, panel
independence and correlated error, evidence-grading schemes, and LLM-as-judge
bias.

**Total research spend across both panels: reserved at band-top. Budget ledgers
reserve high and reconcile lower; both figures belong in a delivery note and
neither is the invoice.**

## The finding that changed the product

All four completed members of panel 1 independently identified the predecessor's
centrepiece, an interactive weighted-slider scorer, as belonging to a family
documented as unsafe for choosing among three to five strategic options.

| Failure mode | Measured | Source |
|---|---|---|
| Rank reversal: adding an irrelevant option flips the top two | proved for sum normalisation; re-derived for weighted-sum 2023; likelier when options are few and close | Belton & Gear 1983; Wang & Elhag 2006; Mohammadi 2023 |
| Splitting bias: decomposing a criterion inflates its weight | ~0.25 as one criterion → **0.40-0.48** split into three | Weber, Eisenführ & von Winterfeldt 1988, N=128 |
| Range insensitivity: weights track word importance, not the actual spread | guidance requires swing-based weights | UK HM Treasury Green Book MCDA supplement |
| Equalising bias across elicitation methods | present in **all five** methods tested | Rezaei et al. 2022 |
| Compensability: a trivial high score outvotes a fatal failure | structural | (design consequence, not a study) |

**Where the panel disagreed**, and it did: one member said remove the scorer
outright, two said keep it as an inspectable sensitivity view stripped of the
recommending role. The build takes the second reading, because two of three
converged on it and it keeps the display people expect. That disagreement is in
`references/evidence.md` rather than resolved silently.

**The limit the panel put on its own answer**, quoted because it matters more
than the finding: *"No controlled study establishes that weighted sum, AHP, BWM,
SMAA, outranking or regret analysis chooses more commercially successful
positioning strategies."* The replacement is not a better oracle. It is an
instrument that exposes the assumptions the score used to hide.

## The gates, checked in both directions

A gate you have only ever watched pass is a gate you have not tested. Both were
run against a deliberately broken fixture and a clean one before shipping.

| Gate | Broken fixture | Clean fixture |
|---|---:|---:|
| `positioning_lint.py` | **41 errors**, exit 1 | 0 errors, exit 0 |
| `claim_ledger.py check` | **4 errors**, exit 1 | 0 errors, exit 0 |

Every rule fired at least once on the broken fixture. The ledger run is worth
spelling out, because each error is one of the predecessor's prose rules becoming
enforceable:

```
FAIL  A: move 'enemy' is unbound
FAIL  A/hero: promissory copy rests on T-02, which is 'designed' rather than shipped
FAIL  A/hero: rests on C-02, whose citations are unverified
FAIL  C-02: labelled high confidence on 1 independent domain(s); floor is 3
```

That last one is the interesting one. The fixture gave `C-02` two sources; both
were on the same host, so they collapsed to one registrable domain and the
high-confidence label failed. Counting support in domains rather than in citation
count is the whole mechanism, and it is four lines of arithmetic rather than a
paragraph of advice.

## Head to head against the predecessor

Both skills were run on the same prompts by independent Opus agents with no
knowledge of which arm they were, each writing to its own directory, with paid
research disabled in both arms so the comparison is of judgment rather than
budget.

**Scope, stated plainly: 3 of the 8 written evals were run in both arms.** The
three chosen are the ones that test the headline claims. The remaining five are
written and committed in `evals/evals.json` and have not been run. A partial
comparison reported as a full one is the failure this whole skill is about.

<!-- RESULTS -->

## What is still untested

- **Five of eight evals** are written and unrun, listed above.
- **No blind quality panel has been run.** Structural assertions are checkable;
  a heterogeneous judge panel scoring anonymised A/B pairs is not in this build.
- **Single runs carry sampling noise.** Each arm ran once. A flipped assertion on
  one prompt is weaker evidence than the table's crispness suggests.
- **Nothing here tests the skill end to end with paid research on.** Both arms
  ran with research disabled, so Phase 2's verification gates were exercised as
  code and not as a live pipeline.
- **The design-review pass on a real report page has not been measured**, only
  specified.
- **No prospective validation of the skill's actual recommendations.** Nobody has
  taken a position this skill recommended, shipped it, and measured what
  happened. That is the only test that would really matter, and it is the one
  neither this skill nor its predecessor has.

## Caveats worth repeating

Blind judges score content, so a ledger file, an exit code and a committed
research corpus earn nothing in a taste test. That is a limitation of taste
tests, not evidence that the artifacts do not matter; it is also why the gates
above are reported as exit codes rather than as opinions.

And the skill's own honesty rule applies to this document. Numbers here come from
the runs and the panel exports in `docs/deep-research/`. Where a figure is an
estimate band rather than an invoice, it says so.

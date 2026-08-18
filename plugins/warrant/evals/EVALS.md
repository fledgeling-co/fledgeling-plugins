# How `warrant` was checked

## The honest headline: no A/B panel was run

The usual test for a new skill is to run the same tasks with it and without it, then have blind
judges from different model families pick the better output without knowing which is which. **That
didn't happen here, and this section exists so nobody reading later assumes it did.**

The reason is that most of this plugin isn't a prompt. Twenty-seven of its parts are scripts with
exit codes, and the question "did the gate fire when it should have" isn't a matter of taste that a
judge panel can settle; it either fired or it didn't. So the checking went into making each gate
demonstrably fail on demand, and into driving the whole chain end to end against deliberately broken
inputs.

What that leaves genuinely unmeasured is named at the bottom.

## What was checked, and what it said

**797 self-test cases across 27 scripts, all passing.** Every script carries a `--selftest` that
runs its own fixtures, and the rule it has to satisfy isn't "the check works" but "every rule can be
observed both passing and failing". A rule only ever seen passing hasn't been written.

**111 process assertions, all passing** (`evals/evals.json`, run by `evals/run_evals.sh`). These
check the invariants rather than the outputs: that every script exposes the same flags, that none
imports a third-party module, that a defect class the warrant doesn't name defaults to no authority
at all, and that every research claim cited anywhere in the plugin resolves in the corpus it came
from.

**Four load-bearing behaviours driven by hand**, because these are the ones the whole thing rests on
and a self-test asserting them is a script agreeing with itself:

| What was tried | What happened |
|---|---|
| A ledger of three real rows, then one field edited in row two | Exit 2, naming the broken row and both hashes: `row content hashes to c6d21e… but the row stores 801fc4…` |
| A lane's pinned model version moved | Exit 4, both classes above zero dropped to zero, reason `model_drift`, the warrant file itself rewritten |
| A reviewer's queue asked to carry the machine's verdict | Exit 2, naming six separate ways the verdict would have reached the reviewer, by field name and by value |
| Two lanes disagreeing, with a request to settle it by majority | Exit 1, refused: *"the disagreement is settled by the check or the person, never by counting lanes"* |

**The full oracle chain against a corrupted page.** A page where a total no longer equals the sum of
its parts produced: `MISMATCH segment-sum (page.html:4, sum(segments.amount)): rendered 1205000,
source 1204000, tolerance exact`. That's the figure, the line, the arithmetic, both values and the
tolerance, which is everything needed to act on it without opening anything else.

## Three defects the checking found

Worth recording because none of them would have been caught by reading the code.

**Every script exited 2 on a typo.** Python's argument parser uses exit code 2 for a usage error,
and this plugin reserves 2 for "the check ran and the thing you're checking is broken". So a
mistyped flag in a CI pipeline was indistinguishable from real bad code. Fixed centrally, and it's
now the first thing the contract document says about exit codes.

**The planes couldn't talk to each other.** The oracle plane measures a page, the assay plane
measures a test target, and authority is held per defect class. Nothing mapped one onto the other,
so every class read as having no evidence and no tier could ever be earned. That's a safe failure
and a useless one. It needed a new step, `rollup_classes.py`, which reads the warrant's own
class-to-page globs.

**Thirteen documented commands didn't work.** Skills showed flags the scripts didn't have, and
positional arguments where the scripts take flags. Anyone following the instructions would have got
a usage error. There's now a gate for it (`evals/check_doc_flags.py`) that checks all 30 documented
invocations against the scripts' actual help output, and it runs with the rest of the suite.

## What was decided without asking

Two things, recorded because the pipeline this was built with asks for them to be:

The **name, the eight skills and the whole architecture** came from an approved build plan, so
nothing there needed a fresh decision. The **icon direction** was the one checkpoint put to a human,
who picked the narrowing-ladder over a document treatment.

Four settings are deliberately left blank in the warrant that `charter_init.py` drafts, because
they're judgement calls rather than facts: who owns the policy, how much error is tolerable on a
queue, how many clean items earn the top tier, and how stale evidence may get. The validator refuses
the warrant until they're filled, which is the intended behaviour rather than an oversight.

## Still unmeasured

Three things, and the first is the one that matters.

**Whether the plugin beats not having it.** No side-by-side comparison was run. What would settle
it: give a model the same twenty finished items to verify, once with the plugin and once without,
and have judges from two other model families pick the better verdict blind. That's the test to run
before trusting it on anything consequential.

**Whether the model-facing prompts are any good.** The scripts are checked; the briefs the lanes run
on aren't, because that needs the A/B above.

**One invariant that can only be observed holding.** The mutation harness must never modify the
working tree. There's an assertion that the files are byte-identical afterwards and that the run
happened in a temporary directory, but no code path writes in place, so the rule has never been
seen failing. The agent that built it flagged this rather than quietly leaving the case out, which
is the right call.

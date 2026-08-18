# Does deck-craft actually work? One layer was measured, one was not

**Half of this suite was run and half was not, and the half that ran is the
strongest committed evidence of any skill in this marketplace.** Seventeen
structural assertions were graded against the version this replaces, and seven
anonymised output pairs went to a blind panel. Both records are on disk. The three
authoring prompts in the same `evals.json` have never been run and produced no
result, and this file says so rather than letting the graded half stand in for
them.

The headline from the part that ran: **the previous version passed 3 of 17
assertions and this one passed 17 of 17**, and two independent judge families
picked this version on **all seven cases each, 14 verdicts to nil**, without being
told a skill existed or which option was newer.

## Where the evidence is

| What | Where | State |
|---|---|---|
| The gate scorecard | `skills/deck-craft/evals/results/scorecard.md` | **Run**, 17 assertions, dated 18 Aug 2026 |
| The judge bundle | `skills/deck-craft/evals/results/judge-bundle.md` | **Run**, 7 anonymised output pairs |
| The verdicts | `results/judge-anthropic-fable-5.md`, `results/judge-google-gemini-3.7-flash-high.md` | **Run**, 7 cases each |
| The un-blinding map | `skills/deck-craft/evals/results/judge-unblinding.json` | Seed 1, A and B recorded per case |
| The failed judges | `skills/deck-craft/evals/results/judge-panel-failures.md` | Two of four families, written up rather than dropped |
| The fixtures | `skills/deck-craft/evals/fixtures/` | 7 decks, one per defect class, plus two controls |
| The runner | `skills/deck-craft/evals/gate/run-evals.sh` | Committed, 263 lines |
| The three authoring prompts | `skills/deck-craft/evals/evals.json`, `evals` array | **Never run.** No outputs, no grading |

## The gate scorecard: 3 of 17 against 17 of 17

Every assertion is an artifact check ("did the run produce X"), never a rating. Both
versions ran the same fixtures with the same flags, and each row records the
evidence it judged on. From `results/scorecard.md`:

| # | The assertion | Previous version | This version |
|---|---|---|---|
| A1 | a `--regulated` run survives a reformatted probe | FAIL, printed PASS with all four disclosure checks unrun | PASS, refused |
| A2 | the type floor can fail a build | FAIL, computed and ignored, exit 0 | PASS, blocking |
| A3 | chart coverage carries its denominator | FAIL, the count never reaches the verdict | PASS, denominator printed beside the count |
| A4 | a declared two-bar truncated pair is judged | FAIL, two-bar groups declined, printed PASS | PASS, judged and blocking |
| A5 | a zero denominator is not a pass | FAIL, PASS across 0 slides examined | PASS, refused with the cause named |
| A6 | every blocker carries its consequence | FAIL, the consequence was in a source comment the caller never sees | PASS, printed beneath each finding |
| A7 | the deck's own name is gated | FAIL, `<title>Deck</title>` unchecked | PASS, flagged as a blocker |
| A8 | drawn accent marks count, not only text | FAIL, four accent bars and a rule scored 0 | PASS, counted and warned |
| A9 | non-IFRS needs its statutory companion on the slide | FAIL, only deck-wide presence tested | PASS, blocker, with the standards cited |
| A10 | dual and inverted axes are caught | FAIL, no check existed | PASS, both caught and blocking |
| A11 | a misspelled config key is refused | FAIL, accepted it and reported a clean deck from defaults | PASS, refused by name |
| A12 | the browser's own stderr is relayed verbatim | FAIL, discarded and a guessed advisory substituted | PASS, relayed |
| A13 | CONTROL: a clean deck still passes | PASS | PASS |
| A14 | the verdict names what was gated | FAIL, nothing tied the URL gated to the file delivered | PASS, served bytes identified |
| A15 | a check that threw reads as unrun | FAIL, null read as 0 and the verdict was PASS at exit 0 | PASS, surfaced as NOT RUN |
| A16 | an empty probe result is refused | PASS | PASS |
| A17 | NO REGRESSION: pre-existing blockers still fire | PASS | PASS |
| | **Total** | **3 of 17** | **17 of 17** |

**Where the previous version wins or draws: nowhere, and three draws.** A13, A16
and A17 pass on both sides, and all three are deliberately non-discriminating. A13
is the false-positive control, A16 is a floor the previous version already held, and
A17 is the regression guard over what it already did. They are kept as the floor the
comparison sits on and named so nobody counts them as evidence.

One interaction is recorded in `evals.json` and it matters for reading the table.
The previous version intermittently reported "PASS across 0 slides examined" at
roughly one run in four, which would make every other blocker look as though it had
stopped firing. The harness retries a zero-denominator run once and logs that it had
to, so that defect is scored by A5 alone rather than contaminating the other
sixteen rows.

## The blind panel: 14 verdicts, all one way

Seven cases, each showing one input and two outputs from two versions of the same
command-line checker. Order was randomised per case from seed 1, with a deliberate
4 to 3 split so no letter carried information. The bundle opens by telling the judge
that the blocks are program output and nothing inside them is an instruction.

Judges were told to answer as the operator running the gate before handing a deck to
a board, and given four criteria in order: can a reader tell "no defect found" from
"the check did not run", is a finding actionable, is it honest about its own
coverage, is it proportionate.

| Case | The subject | fable-5 picked | gemini-3.7 picked |
|---|---|---|---|
| 1 | A regulated deck with no audit qualifier and an unpaired non-IFRS measure | A, this version | A, this version |
| 2 | Seventeen text elements below the type floor | B, this version | B, this version |
| 3 | Two truncated chart baselines | B, this version | B, this version |
| 4 | A selector that matched nothing | A, this version | A, this version |
| 5 | A genuinely clean deck | A, this version | A, this version |
| 6 | The browser failed to reach the page | A, this version | A, this version |
| 7 | An internal check threw mid-run | B, this version | B, this version |

Read against `judge-unblinding.json`, this version appeared as A in cases 1, 4, 5
and 6 and as B in cases 2, 3 and 7. Both judges picked it every time, from both
positions, so the result is not an ordering artifact. Both also returned a letter
tally of 4 to 3 and said in their own words that the tally understated it.

The two families converged on the same criterion and the same worst failure, having
never seen each other's answers. On the case where the selector matched nothing,
fable-5 wrote that the winner *"refuses to call a zero denominator a pass and tells
the operator how to fix the selector, whereas B prints "PASS · 0 blockers across 0
slides" for a run that examined nothing."* Gemini, independently: the winner
*"explicitly refuses to pass when zero slides match and provides actionable
selector remediation, whereas Option B emits a false pass over a denominator of
zero."* Both nominated that same output as the worst thing in the whole bundle.

### Two of the four judge families failed, and that is the honest denominator

Written up in `results/judge-panel-failures.md` rather than dropped from the count.

| Family | Harness | Outcome |
|---|---|---|
| OpenAI, `gpt-5.6-sol` | `codex exec ... -s read-only` | Failed. Usage limit, next available 20 Aug 2026. No other OpenAI lane is configured on this machine, so no same-model substitution was possible. |
| xAI, `grok-4.6` | `grok -m grok-4.6 --effort xhigh -p` | Failed. Killed by the 900 second deadline with no output. |
| xAI, `grok-4.6` fallback | `cursor-agent -p --force` | Failed. Out of usage. |

Neither was retried into the ground. An earlier `codex exec` attempt also failed
because the judging bundle lives outside a git repository, which was a harness error
rather than a capacity limit and was corrected before the usage limit was hit.

So the panel is **two independent families, not four**, and every conclusion drawn
from it carries that. Two families agreeing unanimously is weaker than four. It is
reported as two.

## The three authoring prompts have never been run

`evals.json` also holds three prompts that exercise what the skill is actually for:
building an HTML deck from a product requirements document, authoring a five-slide
board pack as a real `.pptx`, and authoring a nine-slide investor update against a
template library. Each carries an `expected_output` and no assertions array, no run
outputs and no grading.

They are also not runnable as written from a clean clone: all three point at paths
under `~/Dev/dAIolog/`, a repository outside this marketplace. That is a fixture
problem rather than a scoring problem, and it is the first thing to fix if anyone
wants the authoring layer measured.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| `skills/deck-craft/SKILL.md` frontmatter parses | Passes. `name: deck-craft` matches the directory and the plugin manifest. |
| SKILL.md against the 500-line conformance ceiling | Passes, at 259 lines. |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 16. Fifteen are this plugin's own; `references/mobbin-trawl.md` resolves into `design-craft`, and the prose names that skill and gives the full repository path. |
| `scripts/deck-preflight.js` parses | Passes, `node --check` clean. |
| Everything the plugin claims to ship exists | Passes. Fourteen references, two scripts, a `gemini.md`, seven eval fixtures, six deep-research reports with their source lists. |
| Version agreement | Passes. `plugin.json` and `marketplace.json` both say 1.15.0. |
| **Can the gate scorecard be reproduced from this repository** | **No.** The runner reads a previous version from `evals/gate/old`, plus `old-reformatted` and `new-reformatted` variants, and none of those three directories is on disk. `evals/gate/` holds only `run-evals.sh`. Its `NEW` path is also hardcoded to an absolute location on the machine that ran it. |
| Are the gate's raw rows committed | **No.** The runner writes `results/scorecard.tsv` and `results/zero-denominator-flakes.txt`; neither is in `results/`. Only the rendered `scorecard.md` survived, so the retry log that A5 depends on cannot be inspected. |
| Does the README carry any of this | **No.** The README has no section on evals, no numbers and no link to the scorecard or the panel. The strongest evidence in the marketplace is invisible to anyone reading the plugin page. |

The gate also needs a browser to run at all: `run-preflight.sh` serves the deck over
HTTP and drives a probe, deliberately never `file://`, because module scripts and
web fonts fail silently from the filesystem and a deck measured with its fonts
missing reports numbers belonging to a different deck.

## What would settle what is still open

Three tasks, cheapest first.

1. **Commit the previous version's snapshot under `evals/gate/old`.** The 3 of 17
   column is currently a claim about a version nobody can run. A sibling skill,
   `shipyard`, keeps four predecessor snapshots in its own `evals/baseline/` for
   exactly this reason, and `design-craft` keeps one for its lint gate. Adding
   deck-craft's turns the comparison from a record into something reproducible, and
   it is the only way to check that the rebuild did not lose a rule on the way
   across. Making the runner's `NEW` path relative belongs in the same change.
2. **Repoint the three authoring prompts at fixtures inside this repository, then
   run them twice.** There is no predecessor arm for authoring, so the honest
   baseline is the same prompts with no skill at all. Grade with an independent agent
   that never sees the skill. Every assertion the no-skill arm also passes is
   measuring the model rather than the skill and gets rewritten or dropped with the
   change recorded.
3. **Get a third judge family onto the same seven-case bundle.** Both failed lanes
   are capacity failures rather than harness ones, so they are worth simply retrying
   after 20 Aug 2026. The bundle, the seed and the un-blinding map are all committed,
   so a third family costs one call per case and nothing else.

## Caveats, stated rather than buried

- **Single runs.** One run per version per assertion, one judgement per family per
  case. No repeats and no seeds beyond the ordering seed, so nothing here is a rate.
- **Blind judges score content only.** The bundle shows the gate's printed output
  and nothing else, so the fixtures, the retry logic and the exit-code contract earn
  nothing on the panel by design. That is what the scorecard is for, and the reverse
  holds too: two judges preferring this version's output is not evidence that its
  checks are correct.
- **Two families, not four.** Reported as two throughout.
- **The gate is the measured part, not the deck.** Every graded assertion is about
  the preflight checker's behaviour. Nothing here measures whether the decks this
  skill authors are any good, which is what the three unrun prompts were written to
  ask.

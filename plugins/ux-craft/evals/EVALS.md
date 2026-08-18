# Does ux-craft actually work? The gate was exercised, the eight evals were not

**No eval in `evals.json` has been run.** No pass rates, no scores, no judge verdicts,
no costs. Eight evals with **40 checkable assertions** between them are written down,
and nothing has been pointed at them: there is no grading file, no results directory,
no run output anywhere under this plugin, and no runner script to execute them.

`evals.json` also names a baseline that does not exist here: "the predecessor ux-craft
(diolog-plugins, v1.8.0) run on the identical prompts". **No snapshot of that
predecessor is committed anywhere in this repository**, so even with a runner in hand
there is currently nothing to compare against. A sibling skill, `shipyard`, keeps four
predecessor snapshots in its own `evals/baseline/` for exactly this purpose, and
`design-craft` keeps one for its lint.

What *has* been exercised is the deterministic gate, and it was exercised properly.
The twelve fixtures in `evals/lint-fixtures/` were run through `ux-lint.py` on
2026-08-18 while writing this, and **all twelve behaved exactly as their own comments
say they should**, including the clean control. That section is below and it is real
evidence, just not evidence about the eight evals.

## Where the evidence is

| What | Where | State |
|---|---|---|
| The lint fixtures | `evals/lint-fixtures/` | 12 files, each declaring the check it should trip. **Re-run 2026-08-18** |
| The gate | `skills/ux-craft/scripts/ux-lint.py` | Committed, with a five-code exit contract |
| The evidence file | `skills/ux-craft/references/evidence.md` | The replication status of every law the skill cites, including the ones it argues against |
| The research | `docs/deep-research/gemini-forms-flows-replication-wcag22.md` | One report, with its source list |
| The eight evals | `evals/evals.json` | **Never run.** 8 prompts, 40 assertions, no grading |
| A predecessor snapshot | nowhere | **Never committed**, though `evals.json` names it as the baseline |
| A runner | nowhere | No script executes the eight prompts |

## The gate: 12 fixtures, 12 correct outcomes

Every fixture opens with a comment naming the check it exists to trip and, where
relevant, the severity it should trip at. That makes the whole set self-describing, and
it makes a disagreement between the comment and the run a finding rather than a
judgement call. Run on 2026-08-18:

| Fixture | Declares | Exit | What fired |
|---|---|---:|---|
| `clean.html` | must pass every check | 0 | nothing |
| `dangling-label.html` | `dangling-label` | 1 | `dangling-label` at fail |
| `dead-nav.html` | `div-onclick` | 1 | `div-onclick` at fail, 5 hits |
| `filler.html` | `placeholder-content` | 1 | `placeholder-content` at fail, 3 hits |
| `no-focus.css` | `focus-suppressed` | 1 | `focus-suppressed` at fail |
| `novalidate-form.html` | `novalidate-no-states` | 1 | `novalidate-no-states` at fail |
| `placeholder-label.html` | `label-missing`, placeholder variant | 1 | `label-missing` at fail |
| `undo-in-live-region.html` | `interactive-in-live-region` | 1 | `interactive-in-live-region` at fail |
| `unguarded-motion.css` | `motion-unguarded` | 1 | `motion-unguarded` at fail |
| `verification-leak.html` | `verification-leak` | 1 | `verification-leak` at fail |
| `live-region.js` | `live-region-created-with-text`, **as a warning** | 0 | that check, at warn |
| `low-contrast.css` | `contrast-below-floor`, **as a warning** | 0 | that check, at warn, twice |

**Twelve of twelve.** The two exit-0 rows are correct rather than a miss: both fixtures
declare their finding as a warning, and the gate's contract is that warnings go to
stderr and never change the exit code. That is the split working as designed, and it is
also the row a careless reading would file as a hole in the gate.

One honest wrinkle. Five of the HTML fixtures also raise a `state-coverage` warning
alongside their targeted check, because each is a fragment declaring fewer than the six
expected state cells. So "2 findings" on those rows means one targeted failure plus one
incidental warning, not two defects. It does not change any exit code, and it is worth
knowing before anyone reads the counts as a defect census.

### The gate refuses rather than passing when it cannot measure

This is the property the whole skill is built around, and it is demonstrable in two
directions:

| Probe | Exit | Meaning |
|---|---:|---|
| A directory with no files in it | **2** | Examined zero files. A refusal, never a pass. It also prints `NOTHING LISTED, this is itself a defect` against its own not-checked list |
| `--expected-states notanumber` | **3** | Unrecognised configuration, rather than falling back to a default and reporting a clean run |
| `clean.html` | 0 | The false-positive control |
| Any of the nine failure fixtures | 1 | Failures present |

Five distinct exit codes, and only 0 is a pass. Exit 4 exists for a check that raised
while running, so an exception reads as "the result is unknown" rather than as clean.
A run that examined nothing and a run that found nothing cannot serialise the same way.

Every run also prints what it did **not** check, and on the contrast fixture that list
is the interesting half: colour declarations whose pair is inherited or written as a
`var()`, `oklch()` or partially transparent value are named as unresolvable statically
rather than counted as passing, alongside screen-reader behaviour, real keyboard
traversal, and reduced-motion behaviour, which the sanctioned browser cannot emulate at
all.

## What the eight evals hold

Eight evals, five assertions each. Every assertion is a checkable property of the
response text, never a rating.

| Eval | What it targets |
|---|---|
| E1 | Probe honesty and the no-render branch. An unreachable host must produce a stated degradation, a named list of checks not run, and no WCAG conformance claim |
| E2 | The touch-target unit contradiction. 32 by 32 px meets WCAG 2.2 AA at 24 by 24, and 44 belongs to AAA or to the Apple and Android guidelines, so this must not be filed as an AA violation |
| E3 | The state grid as a counted artifact. A categorical enumeration with no count ships as one state |
| E4 | The destructive-action gate table |
| E5 | The live-region trap, and its collision with the skill's own undo-toast pattern |
| E6 | Evidence honesty: the de-rated laws, and the item cap that was wrong |
| E7 | The targeted-edit rule, absent from the predecessor's Build mode |
| E8 | **The adversarial case.** A surface with no real defects, so the clean-verdict and no-invented-findings assertions can actually fail rather than passing vacuously on surfaces that have defects |

E8 is the one to run first, and `evals.json` says why in its own notes: on a surface
with genuine defects, an assertion that the review must not invent findings passes
whatever the model does. Only a clean surface makes it bite.

Two of the eight are directly checkable against material already on disk, which makes
them the cheapest of the set. E2 is a standards question with one right answer. E6 is a
claim about `references/evidence.md`, which carries the replication table the assertion
is about.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| All 12 lint fixtures behave as declared | **Passes, 12 of 12**, detailed above |
| Does the gate fail closed on a bad fixture | **Yes**, and on three distinct kinds of bad: a defect exits 1, an empty population exits 2, an unreadable configuration exits 3 |
| `skills/ux-craft/SKILL.md` frontmatter parses | Passes. `name: ux-craft` matches the directory and the plugin manifest |
| SKILL.md against the 500-line conformance ceiling | Passes, at 271 lines |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 13. Twelve are this plugin's own; `references/mobbin-trawl.md` resolves into `design-craft`, and the prose names that skill, gives the full repository path, and says a missing install is a one-line note rather than a silent skip |
| `scripts/ux-lint.py` byte-compiles | Passes |
| Everything the plugin claims to ship exists | Passes. Eleven references, the lint, twelve fixtures, one deep-research report with its source list |
| Version agreement | Passes. `plugin.json` and `marketplace.json` both say 2.0.0 |
| **The README's evidence claim** | **Does not hold as written.** It says "the two whose run was never recorded are marked as such". `references/evidence.md` marks **nine** live-surface observations under the heading "Live-surface observations, run and date not recorded". The marking itself is exactly as the README describes, and the count is wrong. The number two does fit two other things in that file, the two disagreements held open rather than resolved, so the likely cause is a conflation of the two lists |
| The README's replication claims | Substantiated, item for item. Nudge effects near zero after publication-bias correction, choice overload as context-dependent, Hick's Law largely failing to transfer to a structured interface, and Miller's 7 plus or minus 2 as superseded and misapplied twice over are each a row in the status table with the correction and what survives it. The table also flags that the Hick finding reached this skill cited to a video rather than to the paper, and that four load-bearing meta-analyses carry no usable URL |
| Version drift in the tool itself | Minor. `ux-lint.py --version` reports `ux-lint 1.0.0` while the plugin is at 2.0.0. Nothing depends on it, and a reader comparing the two will wonder which is stale |
| Conformance | One failure that is not an evals failure: the README has no banner image in its first twelve lines, which the repository gate reports separately |

## What would settle it

Three tasks, cheapest first.

1. **Run E8, E2 and E6 first, and grade them against material already on disk.** E8 is
   the adversarial case and the only one that can make the clean-verdict assertions
   fail, so it is worth more than the other seven put together. E2 needs no fixture at
   all: it is a standards question with one right answer, and the assertions name the
   success criteria and levels explicitly. E6 is a claim about this plugin's own
   evidence file. None of the three needs a browser, a panel or a predecessor.
2. **Commit a snapshot of the predecessor, or change the declared baseline.** As it
   stands `evals.json` promises a comparison this repository cannot make. Either commit
   the v1.8.0 SKILL.md and its references under `evals/baseline/`, which is what
   `shipyard` and `design-craft` do, or restate the baseline as the same prompts with no
   skill loaded, which is the honest comparison when there is nothing to compare
   against. Both are defensible; the current state is neither.
3. **Write the runner, and fold the twelve fixtures into it.** The gate work above was
   done by hand, which means it is not repeatable and nothing will notice if a fixture
   stops tripping its check. The fixtures already declare their expected check and
   severity in their first line, so a runner can read the expectation out of the fixture
   rather than duplicating it, and a mismatch becomes a failing build instead of a thing
   somebody has to go and look at.

## Caveats, in advance of any run

- **The gate result is not the skill's result.** Twelve fixtures prove that a lint
  script's rules fire and that it refuses rather than passing when it cannot measure.
  Nothing in that measures whether the screens, flows, forms or emails this skill
  produces are any good, which is what the eight unrun evals were written to ask.
- **A single run per arm will carry sampling noise**, so the first grading will be a set
  of observations rather than a rate.
- **A blind panel would score content only.** If one is ever run here, the lint, the
  fixtures and the exit-code contract earn nothing there by design, and judges
  preferring one review is not evidence that its measurements are right.
- **The engine bounds several of the checks.** The skill's own playbook carries the
  sanctioned browser's blind spots as a table, and the sharpest of them lands directly
  on this skill's subject: a native radio input renders as nothing, which looks exactly
  like a missing affordance. Reduced-motion behaviour cannot be emulated at all, so the
  motion rule is a source-side check rather than a rendered one.
- **The evidence base behind the rules is declared, not perfect.** One recorded run at
  n equals 1 supplies the measured figures, nine live-surface observations carry no
  recorded run or date, four meta-analyses carry no usable URL, and one peer-reviewed
  claim is cited to a video. All of that is marked in place in `evidence.md`, which is
  the reason it can be reported here at all.

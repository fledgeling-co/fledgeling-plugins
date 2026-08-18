# Does mac-craft actually work? Two instruments ran, and the third did not finish

**Two of the three instruments were run on 2026-08-18 and both are committed. The
third, the comparative build that would settle the most, was launched and never
produced artifacts.** That is recorded here as not concluded rather than left out,
because a scorecard that quietly drops its weakest evidence is the thing this skill
exists to prevent.

What was measured: the gate's own adversarial suite bites on **19 of 19 cases**, and
a blind panel of **three model families chose this version unanimously**, all three
independently naming the same defect as the worst thing in either take. What was
not: **MC-1, the two-surface commission**, which is the only eval that compares this
skill's output against the predecessor's on the same brief.

Every number below was read off a committed file or reproduced by running the
scripts while this file was being written.

## Where the evidence is

| What | Where | State |
|---|---|---|
| The write-up | `skills/mac-craft/evals/results-iteration-1.md` | **Run**, and it records MC-1 as not concluded |
| The eval set | `skills/mac-craft/evals/evals.json` | 3 evals, 14 assertions, with the grading route named per assertion |
| The gate suite | `skills/mac-craft/scripts/gate_tests.sh` | **Run**, 19 adversarial cases |
| The panel | `skills/mac-craft/evals/panel-iteration-1/` | **Run**, 4 verdict files, the judge script, the prompt, the mapping |
| The mapping | `panel-iteration-1/mapping.json` | Seed 7, take A and take B recorded |
| The subjects | `skills/mac-craft/assets/fixtures/` | The predecessor's reproduced failure, and this skill's worked example |
| MC-1's outputs | nowhere | **Never produced** |

## The gate suite: 19 of 19, and it bites

Nineteen mocks, each built to defeat exactly one check, each asserted against the
exit code it must produce. Re-run on 2026-08-18 while writing this file: **19 passed,
0 failed, exit 0.** The load-bearing rows:

| Case | Expected exit | Got |
|---|---|---|
| control: a clean mock passes | 0 | 0 |
| contrast: 1.00:1 same-colour text | 1 | 1 |
| contrast: no text at all is unmeasured, not a pass | 2 | 2 |
| contrast: an unresolvable pair is not counted as passing | 0 | 0 |
| contrast: a system-hue failure gets its own message | 1 | 1 |
| contrast: disabled text is exempt, not a failure | 0 | 0 |
| metrics: a declared value not built in CSS | 1 | 1 |
| metrics: a kit tag disagreeing with the published value | 1 | 1 |
| metrics: an untagged row is a defect | 1 | 1 |
| metrics: an empty block is unmeasured, never a pass | 2 | 2 |
| keyboard: `focus-visible` inside a comment does not count | 1 | 1 |
| keyboard: a clickable div with no role or tabindex | 1 | 1 |
| content: lorem ipsum | 1 | 1 |
| tokens: no token layer at all | 1 | 1 |

The three exit codes are the point. A failure returns 1, a surface the gate could not
measure returns 2, and only 0 is a pass, so "nothing wrong here" and "nothing
examined here" cannot be confused.

**The suite earned its cost on the day it was written by finding two defects in the
gate itself.** It first reported fourteen broken fixtures when the fixtures were
correct: exit 2 was masking exit 1, and the cascade walk was skipping colour
inheritance. The instrument was accusing the material. Fixing inheritance took the
passing fixture from **76 measured contrast pairs to 116**, a 53% undercount that
nothing in the output had disclosed. That is in `references/evidence.md`.

## The blind panel: 3 to 0, with one recorded failure

Two renders, blinded A and B under seed 7, the mapping withheld from every judge.
Judges saw **renders only**, never source, because this skill's mocks carry a
`mac-craft:metrics` comment that would have named their own provenance.

The subject: a fixture reproducing the predecessor's measured failure (3.65:1
buttons, a `+` glyph at 1.00:1, a 48px titlebar, no focus ring, lorem ipsum) against
this skill's worked example, which is gate-clean.

| Family | Harness | Verdict |
|---|---|---|
| Anthropic | `claude --model claude-opus-5 --effort high` | **this version** |
| Google | `agy --model gemini-3.7-flash-high` | **this version** |
| xAI | `grok -m grok-4.6 --effort xhigh` | **this version** |
| OpenAI | `codex -m gpt-5.6-sol` | **FAILED.** Usage-limited until 2026-08-20. Probed once, exit 1, no output file written, which is the real failure signal for that CLI. Not retried, counted as failed, excluded from the tally. |

`mapping.json` records `take_A: candidate`, and all three available families returned
`WINNER: A`. So the panel is **three judges, not four**, and it is never presented as
four.

**The finding that matters more than the tally: all three independently named the
low-contrast invisible-text defect as the worst thing in either take**, unprompted as
to what to look for. Anthropic: *"the selected sidebar item is unreadable"*, its text
disappearing into the pure-cyan fill. Google: *"near-zero contrast"* that *"renders
essential interactive labels unreadable."* xAI: *"neon cyan on cyan, the least
readable text in either take."*

That is the same defect `mock_check.py` reports as `identical=1` at 1.00:1, and the
same one the predecessor's own recorded run reported as *"100% pass rate on contrast
(≥4.5:1)"*. Three independent families see it in a render; a prose audit did not see
it in its own output. Gate and panel agree here, which is worth stating, because the
ordering gate then panel then human only earns trust when the layers are shown
agreeing as well as diverging.

### What the panel found against this version

xAI dissented on one sub-axis while still voting for it:

> IDENTITY: B commits harder to one loud cyan kit, while A is a **competent but
> anonymous** stock-Mac ledger.

"Competent but anonymous" is the corpus's own named failure mode, quoted back at this
skill's worked example by an out-of-family judge. It is correct: the fixture was built
to be gate-clean and native, not to be memorable, and it declares no signature
element. The honest reading is that **the gate can enforce correctness and cannot
enforce distinctiveness**, which is why the signature check and the essence test stay
human-read rows rather than being folded into the script.

### Two harness defects found during the run

Both are the same class as the gate defects, the instrument misreporting the
material, and both would have produced a wrong number quietly.

1. **The tally scored a real verdict as `UNPARSED`.** xAI prefixed narration on the
   same line as its answer, and a line-anchored match missed it. Dropping a cast vote
   for a formatting reason is the voting equivalent of `examined=0`. Fixed by
   unanchoring the match.
2. **Google failed for a documented environment trap, not a model reason.** `agy
   --print` auto-denies command-permission tools: empty output, exit 0, and the reason
   only on stderr. Re-run once with permissions skipped, which is a strategy change
   rather than a blind retry, and it produced a full verdict. Taken at face value, the
   panel would have reported two judges where three were available.

## MC-1 was launched and did not conclude

MC-1 is the comparative A and B build: two headless runs on one brief (a
personal-finance app, two surfaces, light and dark), one following the predecessor and
one following this skill, same environment note, the predecessor with no gate
available. **Both were still in their reference-reading phase at 27 minutes with no
artifacts on disk**, and nothing has been produced since.

One incidental observation was kept: at that point the predecessor's run had
accumulated **2.2 MB of transcript across 42 shell calls** against this version's
**880 KB across 28**, which is what an unrouted 8,325-line corpus costs a runner
before it writes anything. That is a cost observation, not a quality result.

### This is where the README's report card comes from, and it needs one correction

The README carries a five-row report card with a predecessor column and a column for
this version. It says plainly that the predecessor column is measured against **the
predecessor's own recorded output** rather than a fresh run, which is honest and is
the right call, because that output is what actually shipped.

What it does not say is that the column for this version comes from the shipped
worked-example fixture rather than from an MC-1 run. Every figure in it is real, and
all five were reproduced from scratch on 2026-08-18 by running the gate over
`assets/fixtures/ledgerline-accounts.html`:

| The README's claim | What the gate printed on 2026-08-18 |
|---|---|
| contrast computed and quoted: `examined=116 failures=0` | `contrast examined=116 failures=0 unresolved=0 identical=0 disabled_exempt=4 contexts=4` |
| clean across four appearance contexts | `contexts=4` |
| keyboard reachability, 3 / 0 | `keyboard focus_visible=3 focus=0 role=0 tabindex=0 clickable_nonsemantic=0` |
| token discipline, 21 tokens and 1 literal outside | `tokens token_block_colours=21 literals_outside=1 distinct_outside=1` |
| the metric block against the kit, 11 rows and 0 failures | `metrics examined=11 failures=0 rows=11` |

So the numbers hold and the source is not the eval the table implies. The accurate
sentence is that this version's column is its worked example measured by its own
gate, and that the head-to-head on a shared brief has not run.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| `scripts/gate_tests.sh` | **Passes, 19 of 19, exit 0.** Reproduced from scratch. |
| Does the gate fail closed on a bad fixture | **Yes**, in both directions and across three exit codes: 1 for a failure, 2 for an unmeasurable surface, 0 only for a real pass. |
| `scripts/mock_check.py` on the worked example | **Exit 0**, `PASS: 0 failures, 5 notes, 0 unmeasurable checks`. The five notes are read-only warnings on stderr: one colour literal outside the token block, no `:hover` or `:active` rule, the five tightest contrast pairs, and a `prefers-reduced-transparency` block whose colour effect is declared unmeasured rather than guessed. |
| The README's platform-documentation correction | Substantiated. White on the kit's own Blue `#0088FF` computes to **3.52:1** exactly as claimed, so Apple's accent button is itself sub-AA and cannot be cited as a floor. |
| `skills/mac-craft/SKILL.md` frontmatter parses | Passes. `name: mac-craft` matches the directory and the plugin manifest. |
| SKILL.md against the 500-line conformance ceiling | Passes, at 351 lines. |
| Every `references/`, `scripts/` and `assets/` path named in SKILL.md resolves | Passes, all 12. Two resolve into sibling plugins, and both are named in the prose with the full repository path: `flows-and-forms.md` into `ux-craft`, `squircle-path.txt` into `create-mac-icon`. The SKILL.md records why the paths are written in full, which is that the predecessor shipped a rule citing a file existing only in a sibling plugin. |
| `scripts/mock_check.py` byte-compiles | Passes. |
| Everything the plugin claims to ship exists | Passes. Seventeen references (eight top-level plus nine pattern files), two scripts, two fixtures, four deep-research reports with their source lists. |
| Version agreement | Passes. `plugin.json` and `marketplace.json` both say 1.0.0. |
| **Is MC-1's grader committed** | **No.** `results-iteration-1.md` names it at `/tmp/improve-mac-craft/grade_eval.py`. It is still on this machine today and it is not in the repository, so on any other machine, or after a restart, MC-1 has no grader. |

## What would settle what is still open

Three tasks, and the first is the one that matters.

1. **Finish MC-1.** It is the only eval that puts both versions on the same brief,
   and it is the reason the README's report card has to be qualified. Two headless
   runs, the same two-surface prompt, the predecessor with no gate available, graded
   mechanically off `mock_check.py --json` counters rather than off a reading. Commit
   the grader alongside the result this time, because the one that ran lives in
   `/tmp`.
2. **Give MC-2 and MC-3 an adversarial variant each.** Both are two-assertion cases
   and both are cheap. MC-2 asks the skill to refuse an icon request and route it, and
   MC-3 asks a targeted edit to stay targeted. Neither has been run against a prompt
   written to push the other way ("just draw me something quick", "while you are in
   there, tidy the spacing"), and `evals.json` states the rule itself: an assertion
   that cannot fail on the current outputs is a finding about the evals rather than a
   pass.
3. **Retry the OpenAI judge on the same two renders after 20 Aug 2026.** The failure
   is a capacity limit, and the renders, the prompt, the seed and the mapping are all
   committed, so a fourth family costs one call. Three families agreeing unanimously
   is weaker than four.

## Caveats, stated rather than buried

- **Single runs.** One panel judgement per family, one gate run per case. Nothing
  here is a rate.
- **Blind judges scored renders only.** They never saw source, so the metric block,
  the token layer, the exit-code contract and the gate itself earn nothing on the
  panel by design. The gate suite is what covers those.
- **Three families, not four.** Reported as three throughout.
- **The panel compared two fixtures, not two runs.** One reproduces the
  predecessor's recorded failure and one is this skill's worked example. That is a
  fair test of whether three families can see the defect, and it is not a test of
  what either skill produces on a fresh brief. MC-1 is.
- **Distinctiveness is unmeasured and structurally cannot be gated.** The one
  criticism the panel made of this version is the one its own script cannot check.

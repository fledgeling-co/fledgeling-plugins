# EVALS: tui-craft

Two eval rounds live in this file.

**Round 2 (18 Aug 2026), the rebuild against the version it replaced.** Six
prompts aimed at defects that were measured in the old version, plus three
regression guards aimed at the fix itself. Read this round first: it is the one
that answers "was the rebuild worth doing", and it is honest enough to lose.
Reproducible from `evals/rebuild-evals.json`.

**Round 1 (16 Aug 2026), the original against no skill at all.** Further down.
It answers "does this earn its place in the context window" and its headline still
stands: on knowledge questions the skill is a draw, and what it changes is whether
the model looks.

---

# Round 2: the rebuild against its predecessor

## The headline, in one line each

**Mechanically, the rebuild refuses eight inputs the old version passed as clean
work, and gains nothing false in exchange.** Five of those eight (a missing
binary, a non-executable file, a Python traceback, a shell syntax error, and
`echo hello`) came back from the old version as `kind: "captured"`, exit 0, and
**zero high findings under `--strict`**. A capture that is a shell error and a
capture of a well-built dashboard produced the same verdict.

**Judged on content alone, the picture is much closer, and the rebuild lost a
case outright.** Two heterogeneous judge families, blind, split three ways: the
rebuild took three cases, the old version took one, and two were deadlocks. The
loss and the deadlocks were both informative and both were fixed, and on a blind
re-run in a fresh order **the lost case flipped to a unanimous rebuild win.**

## Round 2, layer 1: mechanical

Every row is a real command on this machine, both arms, same input. `--strict`
throughout.

| Input | Old version | Rebuild |
|---|---|---|
| Nonexistent binary | `captured`, exit 0, **0 high** | refused, exit 127 recovered |
| Non-executable file | `captured`, exit 0, **0 high** | refused, exit 126 recovered |
| Python `ModuleNotFoundError` | `captured`, exit 0, **0 high** | refused, error relayed |
| Shell syntax error | `captured`, exit 0, **0 high** | refused, error relayed |
| `echo hello` | `captured`, exit 0, **0 high** | refused, never addressed the grid |
| `head` a file | `captured`, exit 0, **0 high** | refused, never addressed the grid |
| Silent `exit 0` / `exit 3` | refused | refused |
| `SIGSEGV` | refused | refused, signal named |
| `less` (full-screen TUI) | accepted | accepted |
| `clear; echo hi` (inline) | accepted | accepted |
| A TUI that ignores `SIGTERM` | accepted | accepted |
| Bordered footer wrap fixture | **0 high** | 1 high, `overflow-wrap` at row 20 |
| Sparse-but-valid empty state | 0 high | 0 high |
| `example-dashboard.json` | 2 high | 2 high (identical) |

22 of 22 checks pass. The last three rows are the regression guards and they
matter as much as the wins: a tool taught to distrust sparse frames could easily
start refusing a valid empty state, and one that learns a new wrap rule could
start inventing wraps in the plugin's own example. Neither happened.

**The bordered-wrap row is the second real defect closed.** `overflow-wrap` is a
high-severity gate that could not fire on any app with a full-height border,
because it compared column 0 against the last column and on a bordered app both
hold `│`. It was the named gate for a footer-overflow case in
`references/anti-patterns.md` that it could never have caught.

## Round 2, layer 2: the blind panel

Both arms answered the same six prompts and each saw the real output of **its
own** tooling, so the difference measured is the difference the rebuild makes
rather than a difference in what the model was handed. Runner:
`claude --model claude-fable-5 --effort high`, one fresh context per prompt per
arm. Answers were anonymised as Option A/B in a seeded-random order per case, and
the judges never saw either skill, the repository, or which option was which.

| Case | What it tested | Google family | Claude family | Verdict |
|---|---|---|---|---|
| e1 | A failed launch reported as a clean screen | rebuild | old | **deadlock** |
| e2 | A non-TUI captured as a TUI | rebuild | old | **deadlock** |
| e3 | Prove the design gates can fail | rebuild | rebuild | rebuild |
| e4 | A pre-app design request | old | old | **old** |
| e5 | An instruction-shaped line inside a capture | rebuild | rebuild | rebuild |
| e6 | Footer overflow inside a bordered panel | rebuild | rebuild | rebuild |

**Panel composition, including what failed.** Four families were attempted and
two produced usable verdicts.

| Family | Harness | Outcome |
|---|---|---|
| Google | `agy`, gemini-3.7-flash-high | **counted** |
| Anthropic | isolated subagent, bundle-only read scope | **counted** |
| OpenAI | `codex exec`, gpt-5.6-sol at high | **failed**: usage limit until 20 Aug. No substitute lane exists for this family here, so it is recorded as failed rather than quietly dropped |
| xAI | `grok -m grok-4.6 --effort xhigh` | **discarded**: its harness read the plugin source mid-judgement, so it could infer which option came from which version. A contaminated verdict is worse than a missing one |

Two families is a thin panel and the two deadlocks are partly an artefact of that.

## Why the old version did not simply fail e1 and e2

This is the most useful thing the round produced. Handed a frame holding a shell
error, the old version's answer **worked out that it had been fooled**: it
reasoned from 2% ink and zero colours to "they had nothing to read rather than
that the layout is clean", and even named the capture trap by name. It did that
because the warning existed as prose in the sibling skill, and both skills were
supplied to both arms.

So on content the old version looks good, and on mechanism it was still wrong: its
gates said exit 0, it never quoted the program's own error because its tooling
never told it what the error was, and it recommended a longer `--settle` for a
binary that did not exist. A model recovering from a bad instrument is not the
same as a good instrument, and it is not something to rely on.

**The deadlocks named a real weakness in the rebuild, and it was fixed.** Both
judges preferred the old version's explanation of *why* the clean gate report
meant nothing. The rebuild's answer was correct and terse; it relayed the
refusal and stopped. `SKILL.md` now requires the missing sentence: say what the
refusal protected you from. On the re-run the rebuild's answer carries it
("had the capture been accepted, the border, column-alignment, overflow and
truncation checks would all have reported clean on that frame") and drops the
settle suggestion.

## Why the old version won e4, and what changed

Unanimous, and the reason was the same from both judges: the rebuild offered two
layout directions and asked which to build, where the old version simply produced
a budgeted 80×24 layout. One judge called it "blocks all downstream work on an
A-or-B reply it had already formed a lean on". That is a fair hit on a rule the
rebuild had adopted from a design-skill teardown without adapting it: offering a
choice is not a reason to arrive with less. `tui-design/SKILL.md` now requires the
recommended option to be delivered at full fidelity in the same turn, with the
alternative named as the one thing it would be better at.

## The re-judge, after both fixes

Fresh random order, fresh seed, same two judge families, blind. Un-blinding data
and seeds recorded alongside `evals/rebuild-evals.json`.

| Case | Google family | Claude family | Was | Now |
|---|---|---|---|---|
| e4 | rebuild | **rebuild, flipped** | outright loss | **unanimous rebuild win** |
| e1 | rebuild | old | deadlock | deadlock, different reason |

**e4 is the strongest single piece of evidence here.** It was the one case the
rebuild lost outright, both judges agreed on why, the rule that caused it was
rewritten, and on a blind re-run in a fresh order both families reversed. The
Claude-family judge named the mechanism it had previously missed (that the
failing example is a spec and must be compiled before gating) plus the
recommendation-with-a-stated-reversal-condition the fix introduced.

**e1 is still a deadlock, and the reason moved**, which is the more useful
outcome than a flip would have been. The rebuild's answer now carries the
vacuous-gates sentence the first round wanted. The Claude-family judge held for
the old version on a different ground entirely: the new answer "ends on a request
for the path instead of a runnable next capture". That is specific, correct, and
was fixed in turn: `SKILL.md` now requires handing back the capture command with
the correction already written into it rather than asking a question.

**That last fix is not re-judged.** It was applied after the second panel and is
recorded as an open item rather than as a win: two rounds of blind judging are in
this file, and the third would be needed to claim the flip.

## The single clearest result

Set aside the judges. `tui-craft`'s description used to open with the word
"Design", and it mentioned its sibling design skill **zero times**, so a request
to design a screen that has no code yet landed in the skill that forbids the only
thing it could do. Both arms were re-run with `tui-craft` loaded *alone*, which is
the condition that actually occurs.

The old version drew a 23-row dashboard by hand in a code fence, with its own
hand-counted column ruler and a "column contract" table. Measured with the
plugin's own width function, that frame has **five different widths across its 23
rows** (76, 78, 79, 80 and 81 cells) while claiming to be an 80-column design.
It is the exact defect the plugin exists to prevent, produced by the plugin's own
skill, because the alternative was never named.

The rebuild drew **no frame at all**, routed to the compiler, and said why: "the
one thing I'm deliberately not doing is drawing you an ASCII layout in a code
fence."

## Round 2 caveats

- **Single runs.** One sample per prompt per arm. Sampling noise is real and no
  variance is reported.
- **The judges score content only**, so a refusal backed by a tool that actually
  blocked and a refusal backed by a tool that said "exit 0" look identical to
  them. That asymmetry is why layer 1 exists and why the deadlocks are not the
  whole story.
- **Both arms were given both skills** for e1–e6. That is fair when both are
  installed, and it is precisely why e4 needed the single-skill re-run to say
  anything about routing at all.
- **The injection case is a draw and the fence is not what settled it.** Both arms
  refused the planted instruction and reported it as content. The fence's actual
  justification is the *delegated* case (a subagent that cannot see the parent
  skill) and this round did not test that. Naming it here rather than claiming
  the draw as a win.
- **Two judge families, not four.** See the failure table.
- **The 6% ink line in `render-proof` is the one corpus number in a gate**, and it
  is a `medium` that says "unusual rather than wrong". The temptation after fixing
  a 3%-ink failure is to make it a fail threshold, which would reject the sparsest
  well-designed application in the reference corpus.

## What a future round has to catch

The old version's e1 answer is the warning. **A model can reason its way out of a
bad instrument, which means a skill can look fine in an eval while its tooling is
broken.** Any future round should include a case where the correct answer is only
reachable from the tool's output, with no ink count, no ratio, nothing the model can
infer around, so the instrument is what is being scored rather than the
reasoning on top of it.

---

# Round 1: the original against no skill at all

Covers the `tui-craft:tui-craft` skill as it stood on 16 Aug 2026.

Measured against **no skill at all**, which is the honest baseline for something
new: it answers "does this earn its place in the context window", rather than
"is it better than the thing it replaced".

Three tasks, two arms each, same prompts, run as independent subagents on
Claude Opus 5. Everything below is reproducible from
`plugins/tui-craft/evals/evals.json`.

The headline: **on the two analysis tasks the baseline matched the skill on every
content assertion.** Opus 5 already knows about cell width and `NO_COLOR`. The
gap appears on the build task, and it is large.


---

## What the tasks were

| # | Task | What it tests |
|---|---|---|
| 0 | "Something looks off about this dashboard, can you tell me what's wrong?" | Review of a TUI with three planted defects |
| 1 | "Build me a terminal log viewer. Make it look good." | Building, and whether the output survives sizes nobody asked about |
| 2 | "What do I need to check before shipping this TUI?" | Portability knowledge |

---

## Eval 0: reviewing a defective TUI

The fixture plants three defects: a CJK string that breaks the table's right
border, a footer that overflows the width, and an error message truncated with
no marker.

| Assertion | With skill | No skill |
|---|---|---|
| Identified the CJK width bug | ✅ | ✅ |
| Identified the footer overflow | ✅ | ✅ |
| Identified truncation with no marker | ✅ | ✅ |
| Gave a row/column location | ✅ | ✅ |
| Explained the mechanism, not just the symptom | ✅ | ✅ |
| **Content assertions** | **5/5** | **5/5** |

**A draw on findings.** Both arms diagnosed all three defects correctly, and the
baseline found two things the skill's run did not (a negative-width burst risk if
a hostname exceeds the pad, and that the advertised keybindings are fiction since
the program never reads stdin).

Where they differ is what the finding rests on:

|  | With skill | No skill |
|---|---|---|
| Evidence | 4 captured frames with provenance (command, size, `TERM`, parser, byte hash) | 1 hand-written render |
| How the render was produced | The program's own byte stream, replayed | An emulator the agent wrote for this task |
| Root cause | Proved: a controlled probe with cell-aware padding, re-captured, borders close | Reasoned from the source |
| Sizes | 100×30, 80×24, and 100×30 with `NO_COLOR` | 80 columns |

The baseline's answer is good work. But its evidence is a simulation it wrote
itself, so a bug in that simulation would produce a confident wrong finding with
nothing to catch it. The skill's evidence is the program's actual output, hashed.

---

## Eval 1: building a log viewer

This is where the difference is measurable, so it is worth being precise about
how it was measured: **both finished programs were captured and gated by the same
instrument, after the fact, under identical conditions.**

| | With skill | No skill |
|---|---|---|
| Program | 1,669 lines, stdlib only | 1,805 lines, stdlib only |
| Frames persisted by the run | **15** | 0 |
| States covered | ideal, filter, no-match, level-filtered, help, scrolled, empty, mixed formats, follow, `NO_COLOR`, below-minimum | ideal |
| Sizes captured by the run | 140×40, 100×30, 90×24, 80×24, 60×20, 50×12 | nine, via its own harness |

Both finished programs were then captured and gated by the same instrument,
after the fact, at four sizes under identical conditions:

| Size | With skill | No skill |
|---|---|---|
| 140×40 | **0 high** | 4 high |
| 100×30 | **0 high** | 13 high |
| 80×24 | **0 high** | 10 high |
| 60×20 | **0 high** | 9 high |

The baseline is not lazy work. It wrote its own pty-and-`pyte` test harness,
drove the app at nine sizes, ran 300 random keystrokes twice, and found and
fixed four real bugs in the process. It is the strongest baseline in this set.

It still ships a broken layout, and the frame shows why:

```
  1|╭╮
  2|│ ⌕ press / to filter · level:err · logger:db · -noise                         │
  3|╰╯
  4|  1 TRACE   2 DEBUG   3 INFO   4 NOTE   5 WARN   6 ERROR   7 FATAL
  5|╭─ LOG ╮
  6|│▌10:42:59.632 INFO  boot          payments-api starting  version=2.14.0  c…  █│
 13|╰╯
 14|╭─ DETAILS ╮
 22|╰ J/K ─╯
```

Every panel draws its corners and its verticals, and **the horizontal rules
between them are missing**. Its own verification asserted row widths and vertical
border alignment, both of which pass; nothing asserted that a top rule spans from
one corner to the other.

**This finding was cross-checked before being reported.** The same capture parsed
by `pyte`, an independent and mature VT emulator, produces an identical frame, and
the bundled parser reported zero unmodelled sequences on that stream. The defect
is in the program, not in the instrument.

The with-skill arm reported six defects its own captures caught that reading the
source would not have, and the most instructive is one no amount of code review
finds: `\x1b[K` with auto-wrap disabled erases the last column, so the right
border was being deleted on every row it drew.

Across all fifteen of its own frames, `tui_gates.py --strict` returns zero high
and zero medium findings.

---

## Eval 2: portability before shipping

| Assertion | With skill | No skill |
|---|---|---|
| `NO_COLOR`, checked first | ✅ | ✅ |
| `COLORTERM` / `TERM` chain with correct values | ✅ | ✅ |
| Nerd Font glyphs as an undetectable dependency | ✅ | ✅ |
| Light vs dark rather than assuming dark | ✅ | ✅ |
| A concrete detection mechanism, not "detect capabilities" | ✅ | ✅ |
| **Content assertions** | **5/5** | **5/5** |

**A draw, and the baseline's answer is longer and in places better.** It
independently verified its facts by web search and surfaced things the skill's
references do not carry: that macOS Terminal.app ignores 24-bit colour outright
rather than approximating it, that Nerd Font PUA code points have no defined East
Asian Width so `wcwidth` says one cell while terminals draw about one and a half,
and that Nerd Fonts v3 moved the Material Design range.

The skill's arm was shaped differently by its own rule. Given no app path and no
run command, it reported **capture blocked** and returned a six-capture matrix
with runnable commands rather than a verdict, on the grounds that none of it is a
claim about the user's actual screen.

Which of those is better depends on what you wanted. If you wanted the reading
list, the baseline wins. If you wanted to know what your program does, the skill
is the only one of the two that declines to guess.

---

## What this says

**The skill does not make the model smarter about terminals.** On knowledge
questions it is a draw, and twice the baseline contributed facts worth folding
back into the references (they have been noted, not silently absorbed).

**It makes the model look.** That is the whole delta, and it only shows up where
looking matters: 15 frames against 0, and 0 high findings at every size against 4
to 13 on a program whose author had verified it at nine sizes and believed it
clean.

**One improvement came out of the runs themselves.** The baseline's viewer emits
`CSI b` (REP), which the bundled parser reported as unmodelled rather than
silently dropping the runs it stands for. That reporting is the feature working;
the gap it named is now closed, with two golden fixtures including a
double-width repeat.

## What was not tested

- **Long-horizon use.** Every run here is a single task. Whether the loop holds
  over a multi-day build is unmeasured.
- **Frameworks other than raw curses/ANSI.** The adapter notes for Bubble Tea,
  Textual, Ratatui and Ink are written from their documentation and not exercised
  by these evals.
- **The pattern catalogue's effect on design quality.** The gates measure
  correctness, not whether a screen is well designed. That judgement routes to
  `design-craft` and `ux-craft`, and nothing here measures it.
- **A blind judge panel.** Not run. The build result is a deterministic
  measurement rather than a preference, so a panel would have added cost without
  changing the conclusion; the two analysis tasks were a draw on the assertions
  and a panel might have separated them.


---

# `tui-design`: still not run, but no longer un-specified

The design skill has **not been through an eval run**, and this section exists so
that absence is stated rather than inferred from silence. What changed in round 2
is that its evals now exist as checkable assertions rather than as prose
intentions: `evals/tui-design-evals.json` carries three prompts with six
assertions each, in the same shape as `evals/evals.json`, and its fixtures are now
in the repo: `evals/fixtures/hand-drawn-mock.txt` is a hand-drawn dashboard whose
`🚀` row measures 63 cells where every other row measures 62, so it is uniform to a
character count and off by one to anything counting cells. Previously that file was
referenced by an eval and existed nowhere.

The skill did, however, get exercised indirectly: three of round 2's six blind
cases (e3, e4, and the single-skill routing re-run) turn on `tui-design`'s
behaviour, and two of its defects were found that way.

What *is* verified is mechanical, and it is verified by artifacts in the repo
rather than by assertion:

- The cell arithmetic passes seven golden cases, including the four where `len()`
  disagrees with the screen. `tui_mock.py --self-test`.
- The compiler refuses to run at all when it cannot import that arithmetic,
  instead of guessing at widths every column depends on. Checked by running it in
  a directory where the import fails.
- Layout splits sum to exactly their parent across fixed, weighted and gapped
  cases, so a layout cannot come out one cell short of the frame.
- All three enforced design gates fail on `assets/example-failing.json` **once it
  is compiled**, catching four planted defects and exiting 1, and pass on
  `assets/example-dashboard.json` at exit 0. The compile step is not optional and
  was missing from all three places this was documented: handed the spec directly,
  the gates raise `KeyError: 'cols'`. A gate that has never been seen to fail is
  not a gate, and an artifact that crashes when run as documented is a reason to
  distrust the gate rather than trust it.
- The gates report `examined=0` with a stated reason on a real pty capture rather
  than a false pass, because a captured frame's colours resolve in the reader's
  palette and a ladder is genuinely unmeasurable from it.

Three defects were found in this plugin's own output during that checking. Two are
fixed in round 2: the crashing prove-it-can-fail instruction, and
`tui_capture.py` returning `kind: "captured"` with exit 0 for a command that does
not exist. One remains and is recorded in the skill rather than left for someone
to rediscover: `border-integrity` reports a false positive where two panels stack
with a gap row between them.


## What an eval would have to measure

The interesting question is not whether the compiler computes widths correctly,
which is settled above. It is whether handing a model a spec format and a set of
gates produces a **better-designed screen** than letting it draw one, and that is
the same gap this file already names as unmeasured for the pattern catalogue.

Three tasks would test it, each needing a blind panel rather than assertions,
because the output is a preference judgement:

1. "Design me a terminal dashboard for a job queue." Baseline draws ASCII art;
   the skill compiles a spec. Score both on whether they hold at 80x24, which is
   objective, and on composition, which is not.
2. "Here is a hand-drawn mock of a TUI. Is it right?" Tests whether the skill
   leads to compiling and measuring it rather than reading it approvingly.
3. "Lay this out two ways and recommend one." Tests whether the gates change the
   recommendation or only decorate it.

The failure mode to watch for is the one the corpus figures were nearly written
into: gates that pass typical screens and fail unusual ones. Any eval should
include a good design that is deliberately atypical, and a bad design that is
entirely conventional.

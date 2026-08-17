# EVALS: tui-craft

Covers the `tui-craft` skill. `tui-design` ships unevaluated, and the section at
the end says what that means and what would settle it.

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

# `tui-design`: not evaluated

The design skill in this plugin has **not been through an eval run**, and this
section exists so that absence is stated rather than inferred from silence.

What *is* verified is mechanical, and it is verified by artifacts in the repo
rather than by assertion:

- The cell arithmetic passes seven golden cases, including the four where `len()`
  disagrees with the screen. `tui_mock.py --self-test`.
- The compiler refuses to run at all when it cannot import that arithmetic,
  instead of guessing at widths every column depends on. Checked by running it in
  a directory where the import fails.
- Layout splits sum to exactly their parent across fixed, weighted and gapped
  cases, so a layout cannot come out one cell short of the frame.
- All three enforced design gates fail on `assets/example-failing.json`, catching
  four planted defects, and pass on `assets/example-dashboard.json`, exiting 1 and
  0 respectively. A gate that has never been seen to fail is not a gate.
- The gates report `examined=0` with a stated reason on a real pty capture rather
  than a false pass, because a captured frame's colours resolve in the reader's
  palette and a ladder is genuinely unmeasurable from it.

Two defects were found in this plugin's own output during that checking, and both
are recorded in the skill rather than left for someone to rediscover:
`border-integrity` reports a false positive where two panels stack with a gap row
between them, and `tui_capture.py` returns `kind: "captured"` with exit 0 for a
command that does not exist.

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

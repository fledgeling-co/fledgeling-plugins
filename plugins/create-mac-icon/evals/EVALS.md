# How create-mac-icon was tested

Seven evals live in `evals.json`. They assert what's on disk after a run, not
what the run says about itself: an independent grader opens the files, re-runs
the checks, and quotes evidence. Evals 1-3 are model runs and cost
media-gen-pro credits. **Evals 4-6 are deterministic and free**: they run from
`fixtures/` with no model at all, which is what makes them worth running on
every edit rather than deliberately.

## The report card

| Run | What it tested | Result |
|-----|----------------|--------|
| Full commission ("Ledgerline") | The whole pipeline with all three engines and the fidelity loop | 6 of 6 assertions passed |
| Honest degradation ("Kilnhand") | The pipeline with no image model available | 4 of 4 assertions passed |
| Gate-holes fixture suite | Nine commission fixtures against `audit_sheet.py check` | 9 of 9 behave as specified |
| Degraded-tier refusal | `fidelity.py gate` on this plugin's own committed run data | exit 2 REFUSED; the original exited 0 ACCEPT |
| Stopping-rule replay | The documented 20-round trace against both patience rules | both documented outcomes reproduced exactly |

## The 2026-08 rebuild, old against new

Nine fixtures, one per measured hole, each built from a real render. **The
column that matters is the middle one: seven of these the original passed
silently.**

| Fixture | Original | Rebuilt | What it encodes |
|---|---|---|---|
| F1 prose-placeholder | exit 0 | **exit 1** | recommendation block still reads as the template's literal `{{WHY_IT_SHIPS …}}` prose placeholder |
| F2 stale-render | exit 0 | **exit 1** | the loop moved the master after the sheet was rendered |
| F3 all-remote-src | exit 0 | **exit 1** | every `<img src>` remote; "all resolve" on a sheet auditing nothing |
| F4 below-rubric-bar | exit 0 | **exit 1** | best take 8/12 against a ≥10/12 bar that was never checked |
| F5 hero-not-shown | exit 0 | **exit 1** | 1024 rendered for every take, displayed in no `<img>` |
| F6 unmasked-raster | exit 0 | **exit 1** | raster passed as `png`: square corners beside squircle siblings |
| F7 master-embeds-raster | exit 0 | **exit 1** | `<image>` embed, the invariant eval 1 asserted and nothing enforced |
| F8 clean control | exit 0 | exit 0 | a correct commission still passes |
| F9 keeps-instructions | **exit 1** | exit 0 | a case the original got *wrong in the other direction* |

F9 is the one the original loses on a false positive rather than a miss. The
template documents its own placeholder convention using placeholder-shaped
strings ("fill every `{{PLACEHOLDER}}`"), so under the old regex a correct sheet
that kept the template's instructions failed the gate on its own documentation,
which is why the shipped sheet carries none of them. The scan now reads the
body with HTML comments removed.

Two findings about the *evals* came out of building them. The rubric-bar check
first read the whole page and was satisfied by the rubric footer's own sentence
"delivery bar ≥10/12", so a sheet whose every take scored 8 passed on the text
describing the bar; it now reads the score cells. And `render` crashed with a
bare `PIL.UnidentifiedImageError` when a raster kind was pointed at an SVG
(the commonest `--take` typo there is), which is now a named skip.

## The comparison that the original won

**Gate message wording: the original wins, and it was not overturned.** The
three envelope messages in `fidelity.py structure` were rewritten to carry their
downstream consequence inline: path-soup rots masters, a 300KB SVG is ~88k
tokens, the layer plan is rubric #10 with a 76% field failure rate. A blind
panel judged them against the bare originals, then judged a tightened second
draft, in both presentation orders each time:

| Round | Google (decisive) | xAI (decisive) | Claude (non-decisive) | Decisive verdict |
|---|---|---|---|---|
| 1, annotated | old, swap-consistent | **swap-flipped → tie** | **swap-flipped → tie** | no-majority |
| 2, tightened | old, swap-consistent | old, swap-consistent | swap-flipped → tie | **old wins 2-0** |

Two independent families named the same defect: the annotation read as "rubric
stats", "token-math" and "rationale", and the original's concrete fix target
(the expected `bg/mid/fg/highlight` names) had been displaced by a statistic.
After two decisive losses the change was reverted rather than re-pitched a third
time, which is the skill's own two-rejections rule applied to itself. The
consequences now live in `references/fidelity-loop.md`, where the threshold is
explained and a reader is asking *why*, rather than at the shell where a runner
is asking *what to change*. One thing did survive from the attempt: placeholder
names are printed untruncated, because the judges singled out "truncated
leftover strings" as the thing that stopped an agent finding the field.

Round 1 is also the clearest evidence for the panel-protocol change made in the
same rebuild. On the annotated draft **two of three judges reversed their answer
when the pair was swapped**, and xAI's stated rationale followed the slot rather
than the content: it praised whichever set sat in position A. A single-order
panel would have reported a confident win for whichever side won the coin toss.

## What the graders verified rather than trusted

- The Ledgerline master regenerated from its build script **byte-identical** to
  the shipped SVG, and re-passed the structure gate independently.
- The fidelity loop ran a baseline plus four rounds, total composite 1.273 to
  3.163, with the full trajectory on disk.
- The Kilnhand run stated its missing engines plainly, shipped three genuinely
  different hand-authored takes, applied three recipe-library constructions
  identifiable in the SVG source, and made no fidelity claim.
- The degraded-tier refusal was proven on **this plugin's own committed run
  data**: all nine rounds in `assets/fidelity-runs/` were scored on the
  numpy-only tier, and torch is not installed on the machine that wrote them,
  so every hand-run gate verdict in that history was blind at 256 and 1024.
- The stopping-rule replay reproduces every documented count from the trace and
  both documented outcomes, and it asserts them, so the reconstruction cannot
  drift into telling a nicer story.

## The finding that changed the skill

The Ledgerline run surfaced something the research had predicted only half of:
the Pareto gate accepted a round that failed the 12-point rubric, because the
raster reference *itself* fails a rubric check (its frosted glyph measures about
1.4:1 figure-ground, which dissolves at 32px). Converging on a flawed reference
dragged the master to 1.02:1. The fix, now in `references/fidelity-loop.md`: the
gate informs, the rubric decides shipping, and the next edit gets bounded to
regions the rubric doesn't police.

The 2026-08 rebuild found the same class of defect one level up. The reference
had replayed a 20-round trace, rejected the naive stopping rule, and written
"adopt that variant", while `loop_runner.py` went on implementing the naive
rule it had rejected, counting patience from round 1. The reference and the
harness disagreed for the whole of that history, and the harness won.

## Caveats, stated rather than buried

- The three model evals are single runs and carry sampling noise; the
  assertions check artifacts, not taste.
- No baseline (skill-less) comparison ran for evals 1-3: these are process evals
  measuring pipeline compliance, and a skill-less run trivially fails most
  assertions by never producing the artifacts. Evals 4-6 *do* carry a real
  old-versus-new comparison, which is where the table above comes from.
- **The judge panel that graded the message wording had one family down.** OpenAI
  was usage-limited until 2026-08-20 and is recorded as failed, not dropped. Of
  the three that ran, `claude` is the same family as the agent that wrote the
  change, so its vote is recorded and excluded from the majority, leaving **two
  decisive families**, which can support a unanimous provisional result and
  cannot produce a majority in disagreement. Round 2 was unanimous among the
  decisive pair; round 1 was not, and is reported as no-majority rather than as
  a win for anybody. What a two-family panel does and does not support is
  written out in `references/evidence.md`.
- Every number in `references/evidence.md` about metrics, position bias and
  stopping rules is **transferred evidence** from text-judging and photographic
  image-quality work. No study evaluates this metric stack against human
  preference on hand-authored SVG icons.

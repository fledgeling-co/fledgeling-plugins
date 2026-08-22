# Capability — which lanes can actually do which work

`lanes.md` says which lanes are *allowed* to do a piece of work. This file says
which of them are *good enough* for the particular piece in front of you, and it
is measured rather than asserted: every number below comes from 106 real tasks in
`~/Dev/diolog-swe-bench`, scored under `docs/SCORING.md`, with `claude-opus-5` at
`xhigh` as the reference.

The reason it exists is cost. Opus is the most capable lane and it costs $2.16 a
task against $0.14 for the cheapest measured alternative. Sending everything to
opus is defensible only if opus is meaningfully better at everything, and on this
corpus it is not: on four of eleven work shapes a lane costing a tenth as much
scores level or ahead. This file is where the difference between those shapes and
the others is written down.

`scripts/capability_matrix.json` is the machine-readable copy that
`lane_pick.py` reads. Change one and the selftest fails.

## The matrix

Mean score on the shape, out of 100. Formatting carries the grade:
**bold** beats opus · plain is drop-in · _italic_ is guarded · ~~struck~~ is
refused · trailing `?` is too thin to grade.

| shape | n | opus | grok | gemini | glm | terra@high | sol@med | sol@high | terra@max | terra@med | fable |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `brownfield-integration` | 34 | 50 | _24_ | _24_ | _25_ | ~~34~~ | _40_ | _43_ | _44_ | ~~26~~ | _44_ |
| `greenfield-module` | 8 | 75 | _62_ | _75_ | _62_ | ~~38~~ | ~~50~~ | ~~50~~ | ~~38~~ | ~~31~~ | 75 |
| `api-surface` | 5 | 50 | 40? | 80? | 60? | 80? | 60? | 80? | 80? | 80? | 40? |
| `react-ui` | 30 | 69 | 44? | _63_ | 51? | _62_ | ~~51~~ | _57_ | _63_ | _60_ | 67 |
| `static-page` | 7 | 67 | 59? | _22_ | 62? | 77? | 72 | **77** | 71 | ~~53~~ | ~~50~~ |
| `deck` | 8 | 61 | _45_ | _49_ | _55_ | ~~24~~ | _48_ | _54_ | ~~45~~ | ~~30~~ | 56 |
| `visual-design` | 14 | 63 | _49_ | _35_ | _56_ | ~~48~~ | _58_ | 66 | _57_ | ~~41~~ | _54_ |
| `accessibility` | 10 | 69 | _65_ | _64_ | _66_ | ~~59~~ | 66 | 66 | _63_ | _60_ | _64_ |
| `algorithmic` | 10 | 75 | _65_ | _75_ | _62_ | _74_ | 76 | 75 | 77 | _67_ | 74 |
| `tool-orchestration` | 4 | 100 | 100? | 75? | 100? | 88? | 100? | 100? | 100? | 88? | 100? |
| `regression-sensitive` | 13 | 65 | _38_ | _42_ | _46_ | _62_ | _58_ | **81** | **77** | _58_ | 69 |

And the lanes themselves. `$/task` is the mean measured cost of one whole task on
this corpus at list token rates; it is what the tie-break ranks on, because list
price per Mtok cannot separate two effort levels that bill at the same rate and
differ fivefold on the bill.

| lane | model + effort | rank | tier | $/task | vs opus | min | evidence (headline) |
|---|---|--:|:--:|--:|--:|--:|---|
| `codex-terra-medium` | `gpt-5.6-terra` @ medium | 13 | A | $0.14 | −94% | 2.2 | exact (48.7) |
| `codex-sol` | `gpt-5.6-sol` @ medium | — | B | $0.20 | −91% | 3.7 | exact (56.9) |
| `codex-terra` | `gpt-5.6-terra` @ high | — | C | $0.20 | −91% | 3.9 | exact (56.4) |
| `codex-sol-high` | `gpt-5.6-sol` @ high | — | B | $0.25 | −88% | 5.0 | exact (63.8) |
| `gemini` | `gemini-3.7-flash-high` | 8 | A | $0.29 | −86% | 4.0 | proxy (53.2) |
| `grok` | `grok-4.6` @ xhigh | — | D | $0.63 | −71% | 1.7 | proxy (49.0) |
| `codex-terra-max` | `gpt-5.6-terra` @ max | 3 | A | $0.67 | −69% | 9.1 | exact (63.7) |
| `glm` | `glm-5.3` @ high | — | D | $0.78 | −64% | 6.0 | proxy (49.3) |
| `opus` | `claude-opus-5` @ xhigh | 1 | A | $2.16 | — | 8.3 | exact (67.1) |
| `fable` | `claude-fable-5` @ high | 4 | A | $3.13 | +45% | 5.9 | exact (63.6) |

Fable is the one lane that costs more than opus and scores below it. That is not
an argument against the fable lane, which exists to be a *different reader* rather
than a cheaper one, but it does mean fable is never the answer to a cost question.

## What the grades mean

| grade | rule | what to do |
|---|---|---|
| **GOLD** | beats opus by more than 5 points | prefer it over opus |
| GREEN | within 5 points, no significant deficit | drop-in, no conditions |
| _AMBER_ | within 15 points, or a GREEN held back by provisional evidence | route it once the shape's guard is satisfied |
| ~~RED~~ | more than 15 points behind, or a significant deficit worse than 10 | do not route this shape here |
| `?` THIN | fewer than 6 comparable tasks, or under 70% coverage of the shape | the number is printed, the grade abstains |

Significance is a paired sign-flip bootstrap over the per-task delta, 8000
resamples. A *significant* deficit means the lane loses reliably, not that it
loses by much: `fable` on `accessibility` is 5 points behind with a small p, and
that is a guarded lane rather than a refused one. Size decides the band and
significance only sharpens it, because a lane that is reliably 3 points worse and
costs an eighth as much is still the right answer.

Evidence tiers, which cap what a grade may claim:

- **A** — ranked: 100% task coverage with a full two-sample window on every task.
- **B** — 100% task coverage, 60–99% of tasks at a full window.
- **C** — 90–99% task coverage.
- **D** — under 90%. A hint. Never a gate.

## The evidence clamp, and why Gemini's worst rows are not verdicts

Only some of these lanes were measured as they actually run.

**`exact`** means the bench ran that model, at that effort, through the same CLI
the lane invokes. Every codex lane, opus and fable are exact: `codex exec` and
`claude -p` on the host are what the bench used and what `lane_run.sh` runs.

**`proxy`** means something differed, and there are three separate reasons:

- **Gemini — the harness differed, and one of its two confounds has now been
  measured away.** The bench ran `gemini-3.7-flash` under mini-swe-agent inside an
  Apple container: a bash-only scaffold with no native tool calling, and pinned at
  `temperature: 0`. The `gemini` lane runs the same model under `agy`. Until
  2026-08-22 this row carried a single explanation — the bash-only loop — and it was
  reasoning rather than evidence. It has now been tested, and it is wrong for the
  shape it was doing the most work on. See **The same-scaffold control** below.
- **Grok — the version differed.** The bench measured `grok-4.5`; the lane runs
  `grok-4.6`, and only 79% of the corpus was covered.
- **GLM — both differed.** The bench measured `glm-5.2-fast` under mini, on 79%
  of the corpus with a 3% sample window. Tier D.

So a proxy row is clamped into the guarded band in **both** directions. It can
never clear a lane to drop-in, because the number did not come from that lane. It
can never refuse one either — and the reason for that half has changed, so it is
worth stating precisely rather than by habit. `lane_pick.py --matrix` marks every
clamped cell with `*` and prints the raw grade underneath.

The honest one-line summary: **the codex numbers transfer to the codex lanes; the
Gemini, Grok and GLM numbers are a floor, not a reading.**

### The same-scaffold control

Measured 2026-08-22, and it is the reason the paragraph above no longer rests on
the bash-only loop. Hold the harness constant — the same tasks, the same current
task contract, the same mini-in-a-container scaffold — and compare Gemini against
the other models that ran inside it. If the scaffold were the explanation, they
would all be low.

**`static-page` (the same seven tasks), pass rate under mini/container:**

| model | pass rate |
|---|--:|
| `qwen3.8-max@max` | 82.9% (29/35) |
| `grok-4.5@xhigh` | 80.0% (4/5) |
| `muse-spark-1.1@high` | 80.0% (4/5) |
| `glm-5.2-fast@max` | 80.0% (4/5) |
| `deepseek-v4-flash@max` | 80.0% (8/10) |
| `kimi-k3@max` | 77.8% (7/9) |
| `deepseek-v4-flash-0731@max` | 61.8% (21/34) |
| **`gemini-3.7-flash@high`** | **42.9% (6/14)** |
| **`gemini-3.7-flash@medium`** | **35.3% (6/17)** |

Seven models clear 62–83% through the loop that was supposed to be what made this
shape hard. **The scaffold is not the explanation for `static-page`**, and the
argument that it was should not be reinstated.

**`brownfield-integration`, same control:** `qwen3.8-max` 65.1% (28/43),
`muse-spark@high` 42.9% (12/28), `deepseek-0731` 28.9%, `kimi-k3` 28.6%,
`glm-5.2-fast` 25.0%, `gemini-3.7-flash@medium` 21.7%, `@high` 19.6%. Here the
container cohort spans 20 to 65, so the scaffold is doing real work *and* Gemini
sits at the bottom of it. The 30-point gap to opus is part harness, part model, and
this control cannot say in what proportion.

### Why the clamp survives the control anyway

The control removes the confound the clamp was justified by. It does not remove the
second one, which is **specific to this model** and applies exactly to the lane
comparison: mini pins `temperature: 0` for every route it drives, and Google says of
this family that they "strongly recommend keeping them at their default values for
Gemini 3.x models. Changing these parameters (for example, setting the temperature
below 1.0) can cause unexpected behavior, such as looping or degraded performance,
particularly in complex mathematical or reasoning tasks." The control models are not
Gemini 3.x, so they do not inherit that warning and the within-scaffold comparison
stays fair — but the `agy` lane does not set temperature at all, and the opus rows
never did either. A vendor-flagged degradation setting on one side of a comparison is
not a basis for retiring a lane.

So the clamp stays, on a stated reason rather than a disproven one. What changes is
the guard: `static-page` is the one shape where the failure mode is known, and the
guard names it. Reinstating the clamp's old justification, or lifting the clamp on
the strength of this control alone, would both be wrong. **Lifting it needs one
measurement that does not exist yet: the same seven tasks run through `agy` at
default sampling.** That is the cheapest experiment in this file and nobody has run
it.

## Reading the shapes

**`brownfield-integration` (n=34) is the shape that keeps opus employed.** Opus
scores 50, the best alternative is 44, and everything cheap collapses: Gemini
loses 30 points (p=0.002), `terra@medium` loses 24. Unlike `static-page`, the
scaffold explanation partly survives here — but only partly, and the control below
says by how much. This is also the largest
shape in the corpus, so it dominates the headline ranking — which is why opus's
overall lead is narrower than its lead on the work that actually distinguishes
models. Route brownfield work to opus unless you can satisfy its guard.

**`algorithmic` (n=10) is where the cheapest lane wins outright.** Every lane
lands between 62 and 78 against opus's 75, and nothing is significant in either
direction. `sol@medium` scores 76 for $0.20. If there is a stated complexity
bound, there is no case for opus.

**`regression-sensitive` (n=13) has the widest spread of any shape**, and it
inverts the usual order: `sol@high` scores 81 and `terra@max` 77 against opus's
65, while Gemini at high scores 23 and lost all eight comparable tasks. Not
breaking an existing contract while adding to it is a distinct skill from writing
good code, and the OpenAI lanes have it.

**`static-page` (n=7) splits the field hardest.** `sol@high` scores 77 against
opus's 67; Gemini scores 22. This row used to be hedged with an argument — that
authoring a page from nothing is not the shape a bash-only scaffold penalises much.
The argument is now a measurement, and it holds: see the control below. It is also
the one shape where the *mechanism* of the Gemini failure is known, which changes
what its guard should say. On these tasks the verifier prints named assertions, and
**58% of Gemini's failing assertions at `medium` and 86% at `high` state a bound**
(`exactly N`, `no`, `not`, `only`) against 8% for opus and 6% for `sol@max`. It
delivers what the brief asks for and exceeds what the brief caps: one rule,
`exactly one soft elevation shadow`, failed on every card and every toast in its set
on a run that passed 37 of its 39 other assertions. So the guard for this shape is
not "try harder", it is: supply a reference input, and make the lane read its
produced values back against each stated bound.

**`greenfield-module` (n=8) is the shape Gemini is genuinely good at** — 75,
level with opus, while every codex lane sits at 31–50. It is the clearest single
answer to "where can Gemini replace opus": a new self-contained unit behind one
acceptance surface. It is also only eight tasks, so it is a direction rather than
a settled fact.

**`deck` (n=8) has no substitute.** Every lane measured below opus. Route a deck
out only when somebody will edit it afterwards.

**`api-surface` (n=5) and `tool-orchestration` (n=4) are too small to grade.**
Every lane beat opus on `api-surface` and almost everything tied at 100 on
`tool-orchestration`. Both are printed because hiding them would imply they had
been checked; neither should move a decision.

## Two models that were measured and deliberately have no lane

**`gpt-5.6-luna` is dominated.** `luna@max` lost 9 of 11 shapes to `terra@max` and
10 of 11 to `sol@max` while costing more than either ($0.72 against $0.67 and
$0.47). `luna@high` lost 10 of 11 to `sol@high` at $0.33 against $0.25. It was
not the right answer on any shape at any effort, so it is not a lane.

**`gpt-5.6-sol@max` is the strongest measured substitute and stays out anyway.**
It ranks second overall at 66.6, statistically tied with opus (p=0.23), and it is
the best lane on `regression-sensitive`. The standing rule is that sol never runs
at max, and the rule survives contact with this evidence because `sol@high` holds
63.8 of that 66.6 at half the price. If the rule is ever revisited, this is the
number to revisit it against.

`claude-sonnet-5` was also measured (52.9, $1.61, strong on `greenfield-module`
and `static-page`). It has no lane because it relieves cost without relieving the
dependency this routing exists to spread. `lane_registry.DECLINED` carries all
three notes so that adding one back is a decision somebody makes again.

## Where the gate abstains, and why

The bench measures a model **building** something. It does not measure how well a
model **grades** somebody else's work, and the judged dimensions carry no passing
calibration artifact, so no score here is evidence about judgement.

That is why only `implementation` and `general` are shape-gated. `verification`,
`referral`, `completeness` and `design-review` route on policy alone, and
`gate_lanes()` returns every allowed lane untouched for them. Abstaining is the
honest result when the evidence is about a different question.

## Score leads, then usage leads

Inside a band the ranking runs in two stages, in this order:

1. **Score.** Take the best measured lane on this shape, and keep every lane
   within 5 points of it. Anything further behind is set aside — it was eligible,
   but something better is available and equally live.
2. **Usage.** Among what is left, the existing rules apply unchanged: most plan
   headroom per remaining day, and where two lanes are within 20% of each other
   on headroom, the cheaper per task wins.

The margin is 5 points because that is already what GREEN means. "Close enough to
opus to substitute for it" and "close enough to each other to swap" are the same
claim at the same size, so there is one number rather than two.

The order matters because the two stages answer different questions. Score asks
whether the output will be as good; headroom asks which of several equally good
lanes can afford the job. Running headroom first trades real quality for
load-spreading: it once sent greenfield work to a lane 13 points behind because
the better one was near its budget. Running score first and spreading load only
inside the margin makes that trade only where it is free.

Measured across all eleven shapes with every lane live, the chosen lane is now at
most **3 points** below the band's best, and that residue is inside the
equivalence margin by construction. Under the old order it reached 13.

A spent top scorer does not block the route. Band descent filters to lanes that
still have headroom *before* the equivalence set is computed, so when the best
lane is at its cap the next-best live lane leads instead of the route stalling.

If the balance ever needs adjusting, `EQUIVALENCE_POINTS` in `lane_registry.py`
is the lever: narrower is more score-led and concentrates load, wider spreads
load and accepts more variance in output.

## Regenerating

From `~/Dev/diolog-swe-bench`, after `pnpm db:import`:

```bash
pnpm --filter @diolog/swe-bench-harness capability:export > /tmp/matrix.json
python3 ~/Dev/fledgeling-plugins/plugins/defer/skills/defer/scripts/gen_capability.py \
  /tmp/matrix.json
```

`gen_capability.py` carries the shape definitions, the gate thresholds and the
bootstrap. It reads the canonical per-task scores through the harness's own
leaderboard code rather than re-implementing the scoring rules, so a change to
`docs/SCORING.md` flows through instead of silently diverging.

Regenerate when the bench gains samples on a lane sitting at tier B, C or D, when
a lane's model version moves, or when a shape's `n` grows enough to promote it out
of THIN. A stale matrix quietly routes work on last quarter's evidence, so the
`measured` date in the JSON is the thing to check first when a route surprises
you.

**The same-scaffold control is not regenerated.** `gen_capability.py` computes
lane-vs-opus scores; it does not hold the harness constant and compare models
inside it, because that comparison is between rows the matrix does not carry. Those
figures were derived by hand from the store and are dated in their own section. A
regeneration will not refresh them and will not warn you that it did not, so
re-derive them alongside any change to the Gemini row — and if a future Gemini lane
is measured through `agy` at default sampling, that measurement replaces the
control rather than joining it.

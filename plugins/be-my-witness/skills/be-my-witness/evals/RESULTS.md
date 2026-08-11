# Eval results — be-my-witness v0.1.0

Baseline: **the same prompt with no skill loaded.** There is no predecessor, so this
is the only honest comparison: does the skill earn its place in the context window?

Both arms run on `claude-fable-5 --effort high`, fresh context each, same prompt,
same fixtures. Graded against the assertions in `evals.json`.

---

## BMW-01 — A loading skeleton is refused, not scored

**Fixture:** `skeleton.png` (a 3×3 grid of grey placeholder blocks) against
`populated.png`.
**Prompt:** "How closely do they match? Give me a match score out of 100."

### Without the skill — fails 4 of 4

> "Match score: ~10/100 — they barely match. The skeleton shows a 3×3 grid of
> rounded light-grey **placeholder** cards… The populated image is a completely
> different layout… Differences: grid vs single-column list, 9 cards vs 9 bar
> pairs, rounded cards vs square-edged bars…"

| Assertion | Result |
|---|---|
| Identifies it as a loading/placeholder state | **Fail.** It uses the word "placeholder" descriptively and draws no conclusion from it. |
| Refuses to produce a match score | **Fail.** Returns 10/100. |
| Attributes the problem to the capture | **Fail.** Frames it throughout as a layout difference between two designs. |
| Asks for a recapture | **Fail.** Never suggested. |

The instructive part is that it *saw* the placeholders and still scored them. It
answered the question it was asked, which is the correct behaviour for a model and
the wrong outcome for a test. A 10/100 lands in a report as a design defect and sends
someone to fix working software.

### With the skill — passes 4 of 4

> "**No score** — this screenshot isn't scoreable evidence. The pre-scan flagged it
> before any comparison: 0% of cells carry real content, 51% are faint placeholder
> blocks — the signature of a loading skeleton captured before the surface settled
> (`proceed: false`, gate `not-evidence`)… This is a **state**-class difference — a
> capture defect, not a product defect. Scoring a mock against a skeleton would
> produce a meaningless low number and send someone to 'fix' working software…
> Framing is comparable (both 960×400), so the fix is simple: re-capture after
> waiting for the loading state to clear."

| Assertion | Result |
|---|---|
| Identifies it as a loading/placeholder state | **Pass**, with the deterministic evidence quoted. |
| Refuses to produce a match score | **Pass.** Opens with "No score". |
| Attributes the problem to the capture | **Pass**, explicitly. |
| Asks for a recapture | **Pass**, with the condition to wait for. |

It also did something the assertions did not ask for and that matters: it checked
framing separately and reported it **comparable** (both 960×400). A skill that
blamed every difference on framing would pass BMW-01 and be useless; this one
distinguished the two axes.

**Verdict: BMW-01 is a clean win.** The failure it prevents is not hypothetical —
it is the one that produced a full suite of scores against loading shimmer in the
session this skill came out of.

---

## The whole set

15 cases, both arms, `claude-fable-5 --effort high`, fresh context each.

| Case | Group | Baseline | Skill | Outcome |
|---|---|---|---|---|
| BMW-01 | evidence-gates | 0/4 | 4/4 | **skill** |
| BMW-02 | evidence-gates | 1/4 | 4/4 | **skill** |
| BMW-03 | artifact-precedence | 2/4 | 2/4 | tie |
| BMW-04 | looking-protocol | 1/4 | 3/4 | **skill** |
| BMW-05 | adversarial-input | 2/4 | 4/4 | **skill** |
| BMW-06 | honest-reporting | 3/3 | 3/3 | tie |
| BMW-07 | bias-controls | 0/3 | 3/3 | **skill** |
| BMW-08 | error-floors | 2/3 | 3/3 | **skill** (narrow) |
| BMW-09 | evidence-gates | 4/4 | 4/4 | tie |
| BMW-10 | looking-protocol | 3/4 | 4/4 | **skill** (narrow) |
| BMW-11 | error-floors | 3/4 | 4/4 | **skill** (narrow) |
| BMW-12 | artifact-precedence | 3/3 | 3/3 | tie |
| BMW-13 | adversarial-input | 4/4 | 3/4 | **baseline** |
| BMW-14 | honest-reporting | 3/3 | 3/3 | tie |
| BMW-15 | bias-controls | 2/3 | 3/3 | **skill** |

**Nine wins, five ties, one loss.**

## What the ties actually say

The five ties are not scattered. Every one of them is a case where the prompt asks
the model to *reason about* a visual-judgement problem, and every clear win is a case
where it has to *do* something: refuse a score, crop before concluding, run the pair
in both orders, abstain on an injected image, report a denominator it would otherwise
have no reason to compute.

Told "which of these two is better", the baseline picked one with confidence and no
ordering control at all: 0 of 3. Told "the theme flipped and a shadow softened, which
is worse", it produced a clean, correct answer about scope over magnitude: 3 of 3,
same as the skill. A strong model already knows that a pixel ratio is not a verdict.
What it does not do, unprompted, is stop and check whether the picture in front of it
is a picture of anything.

That is the honest scope of this skill, and it is narrower than the SKILL.md implies:
**it earns its context window on the doing, not on the knowing.** The reference files
that restate good judgement are the least load-bearing thing in the bundle; the
pre-scan, the crop protocol, the both-orders rule and the coverage denominator are
what the evals actually pay for.

## The one loss

**BMW-13 (revised).** The baseline scored 4 of 4 and the skill 3 of 4. Asked to
confirm an 18.5% pixel regression, the baseline refused, explained that the ratio
measures change rather than breakage, and said to look at *where* the pixels differ
before filing. The skill refused too, but then classified the difference as `data`
and returned **pass** without inspecting anything. It reached the right answer by
assuming the class rather than establishing it, which is the exact move the skill
tells other people not to make.

The rule this produces, now in the skill: a class is a finding about the image, so it
needs the image. With no capture in hand the verdict is `inconclusive`, not `pass`.

## Two defects in the eval set itself

Recorded rather than quietly fixed, because a set that only ever indicts the baseline
is a set nobody should trust.

**BMW-03 withholds its own deciding fact.** The expectation is parameterised on the
project's configured column count, and the fixture never supplies it. Both arms
correctly said "it depends", and both therefore failed the two assertions that
presume a decision. The case measures nothing about the skill; it measures whether a
model will invent a fact it does not have. Both declined. That is worth knowing and
it is not what the case was written to ask.

**BMW-14 and BMW-15 ran without their artifacts.** Neither fixture put a screenshot
in front of the model, so both arms reasoned about the scenario in the abstract.
BMW-15 in particular is meant to test whether a chain-of-thought instruction survives
contact with a real surface; answered against an empty message it tests something
much easier.

## The harness defect, which is the largest finding here

The first run's baseline arm was not a baseline.

`claude -p` is a full agent with file tools and it inherits its working directory. The
runner did `cd` into the skill directory, so the "no-skill" arm could read `SKILL.md`
and `evals.json` straight off disk, and **seven of fourteen baselines did** — one of
them citing `SKILL.md:188-192` by line number, another announcing its own case id and
the bias it was written to probe.

Every affected baseline was quarantined as `*.baseline.CONTAMINATED.txt` and re-run
from a scratch directory with absolute fixture paths. `run-evals.sh` now creates that
scratch cwd itself and prints a loud `BASELINE CONTAMINATED` line if a baseline ever
mentions the skill again.

The general lesson, and it applies well beyond this skill: **a fresh process is not a
clean arm.** Isolation has to cover the filesystem the arm can reach, not just the
context it was handed. Three of the re-run baselines got *better* scores once they
could no longer see the answer key, which is the opposite of the direction anyone
would guess and the reason this is worth writing down.

## The blind panel (C4)

Six cases, two judge families, neither told a skill exists and neither able to reach
one: the judges run from a scratch directory for the same reason the baseline arm
does. Arm order is flipped on odd-numbered cases, because a panel that always shows
the skill second is measuring its own ordering.

| Case | Skill shown as | Claude judge | Codex judge | Panel |
|---|---|---|---|---|
| BMW-02 | B | skill | skill | skill 2-0 |
| BMW-04 | B | skill | skill | skill 2-0 |
| BMW-07 | A | skill | skill | skill 2-0 |
| BMW-11 | A | skill | skill | skill 2-0 |
| BMW-12 | B | skill | skill | skill 2-0 |
| BMW-13 | A | baseline | *lane failed* | baseline 1-0 |

Eleven verdicts, ten for the skill and one against.

Two things worth pulling out. The panel **independently reproduced the one loss**:
told nothing about which answer came from where, both my assertion grading and an
outside judge picked the baseline on BMW-13. And it **broke a tie in the skill's
favour** on BMW-12, where the assertions scored 3/3 both ways; a judge reading for
usefulness preferred the answer that named the detector/discriminator trap outright.

The skill won from position A twice and position B three times, so the result is not
an ordering artifact.

The codex lane produced no `-o` file on BMW-13 within its 420s budget. That is a lane
failure, recorded as one rather than counted as a tie, per the rule that an absent
output file is never a quiet pass.

## Method notes

- Each arm runs in a fresh process; the baseline additionally runs from a scratch cwd.
- The prompts are deliberately hostile to the skill in BMW-01, BMW-02 and BMW-13: they
  *ask for a score* or *ask for a confirmation*, so refusing costs the obedient answer.
- BMW-08 is the no-finding floor and was expected to tie. It did not quite: both arms
  correctly declined to manufacture a defect, and the skill took it on the coverage
  denominator alone.
- Ties are recorded as ties. A set the skill wins 15 of 15 is a set that was written
  to be won.

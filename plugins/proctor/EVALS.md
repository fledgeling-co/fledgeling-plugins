# Does proctor earn its place?

A skill costs context every time it loads, and it implies a guarantee. So the
question worth answering is not "is this good" but "does the model do better
with it than without it" — and the honest way to find out is to run the same
prompts twice, once with the skill and once with nothing, and grade both
against the same checklist.

That is what this page reports, including the parts that went against the
skill.

## What was run

Six prompts, each one written around a mistake that is easy to make and easy
to check. Each was run twice against the same model: once with the skill
document in context, once with no skill at all. Both arms had the same
information available otherwise.

An independent grader marked every assertion pass, fail or partial, and had to
quote the sentence that decided it. No quote meant fail.

## The result

| # | What it tests | No skill | With skill |
|---|---|---|---|
| 1 | Checks the tool is actually ready before starting work | 0 / 4 | 2 / 4 |
| 3 | Reads two different "it settled" results correctly | 4 / 4 | 4 / 4 |
| 4 | Doesn't treat a stale screenshot as evidence | 2 / 4 | 4 / 4 |
| 5 | *(excluded — see below)* | — | — |
| 6 | Won't invent design values it cannot measure | 1 / 4 | 4 / 4 |
| 8 | Discloses that the measurement changed the thing measured | 0 / 4 | 4 / 4 |
| | **Total** | **7 / 20** | **18 / 20** |

## The parts that went against it

**Case 3 was a tie, and it should not have been in the set.** The unaided model
got all four points: it withheld the verdict, blamed the right thing, noticed
the evidence was thin, and proposed the check that would settle it — then added
a hazard the skill arm missed. An eval the model passes on its own measures the
model, not the skill. It has been replaced with one that turns on this server's
own reporting, which the model has no way to know.

**Seven of the twenty assertions were passed by both arms.** They are listed in
the grading file. They are not evidence for the skill.

**The first run of this comparison was invalid.** Both arms shared a working
directory, and several of the no-skill runs simply read the skill document off
the disk — one of them read the answer key and said so. Four of six cases were
the skill arm running twice under two names. The whole thing was re-run with
each arm in its own empty directory. One case leaked again even then and is
excluded above rather than reported as a tie, because a contaminated tie
flatters the skill.

**Case 8 exposed a real weakness.** The skill arm won four points to nil, and
handed back about a third of the section it was asked for while the unaided run
wrote a complete one. Winning on content and losing on delivery is still
losing, and the skill now says to write the section out in full.

## What the pattern actually is

The headline reads as a large win, and underneath it the shape is narrower and
more interesting. Almost every partial credit in the no-skill arm is the same
thing: the model declines to make the mistake, and then explains its reasoning
wrongly. It knows not to invent a corner radius; it does not know that macOS
has no cross-process way to read one. It hesitates over a stale screenshot; it
does not know that off-screen windows only refresh when the pointer moves on
their display.

So the skill is not supplying caution. The model brought that. It is supplying
the mechanisms — which is why the two cases it wins outright are the two about
disclosing what the instrument did, and why the case it ties is the one that
needed judgement rather than knowledge.

## Reproducing it

The prompts and assertions are in [`evals/evals.json`](evals/evals.json). Run
each in an empty directory, once with `skills/proctor/SKILL.md` prepended and
once without, and grade against the assertions. Keep the arms in separate
directories — that is the mistake that cost this comparison its first run.

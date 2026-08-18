# Does proctor earn its place?

A skill costs context every time it loads, and it implies a guarantee. So the
question worth answering is not "is this good" but "does the model do better
with it than without it", and the honest way to find out is to run the same
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
| 5 | *(excluded, see below)* | n/a | n/a |
| 6 | Won't invent design values it cannot measure | 1 / 4 | 4 / 4 |
| 8 | Discloses that the measurement changed the thing measured | 0 / 4 | 4 / 4 |
| | **Total** | **7 / 20** | **18 / 20** |

## The parts that went against it

**Case 3 was a tie, and it should not have been in the set.** The unaided model
got all four points: it withheld the verdict, blamed the right thing, noticed
the evidence was thin, and proposed the check that would settle it, then added
a hazard the skill arm missed. An eval the model passes on its own measures the
model, not the skill. It has been replaced with one that turns on this server's
own reporting, which the model has no way to know.

**Seven of the twenty assertions were passed by both arms.** They are listed in
the grading file. They are not evidence for the skill.

**The first run of this comparison was invalid.** Both arms shared a working
directory, and several of the no-skill runs simply read the skill document off
the disk; one of them read the answer key and said so. Four of six cases were
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
the mechanisms, which is why the two cases it wins outright are the two about
disclosing what the instrument did, and why the case it ties is the one that
needed judgement rather than knowledge.

## The 0.2.0 additions, judged blind

Version 0.2.0 added two capabilities: measuring native correctness against the
platform's own rules when there is no mockup, and running a handed-over test
suite case by case through a traceability matrix. Two new prompts were written
for them (11 and 12 in the grading file), each around a mistake that is easy to
make and easy to check.

These were graded differently, and harder. Each prompt was answered twice, with
the skill and with nothing, and the two answers were handed to a **panel of
three judges as an anonymised A/B pair, with the skill's side hidden and the
order swapped between the two prompts**, so a judge could not pattern-match
which side to favour. Two of the judges were the working model; one was a
different model family. None was told a skill existed.

The panel was unanimous both times: the skill's answer won 3–0 on prompt 11 and
3–0 on prompt 12.

**And both wins were narrow in the same honest way.** On each prompt, two of the
four criteria were a tie, and they were the two a competent model already
handles unaided. On the native-conformance prompt both arms measured against
*something* and both reported measured deviations; the skill won only on naming
a **concrete** rubric (the control ladder, the 13pt type ramp, the 8pt grid, the
native-tells audit) instead of generic "HIG conventions", and on **routing the
aesthetic verdict to design-review** instead of delivering "good/not good" as
its own impression. On the given-suite prompt both arms asserted the promised
outcome and reported per case; the skill won only on building the
**case-to-evidence matrix as the report's spine** and on the rule that an
**unevaluable case surfaces as a visible skip** rather than a loose caveat.

It is the same shape as the original six. The model brings the competence; the
skill supplies the mechanism the model has no way to know it should reach for:
here, that "is it native" and "is it good" are two different questions with two
different oracles, and that a handed-over suite is a spine to trace rather than a
list to run through.

**The rewrite did not cost anything.** The 0.2.0 edit rewrote the visual-fidelity
stage, where three of the original assertions live. All ten prior behaviours were
re-checked against the new document and every one is still instructed, quoted
line for line.

## Reproducing it

The prompts and assertions are in [`evals/evals.json`](evals/evals.json). Run
each in an empty directory, once with `skills/proctor/SKILL.md` prepended and
once without, and grade against the assertions. Keep the arms in separate
directories; that is the mistake that cost this comparison its first run.

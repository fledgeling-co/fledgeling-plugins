# Does dossier-report actually work?

Short answer: it does the job it's for, and it doesn't do the job people
will assume it's for. Both halves are measured below, including the runs
it lost.

**Everything here was measured on version 2.1.** The TLDR band, the verdict
layer, the imagery provenance rules, the compulsory motion layer and the
TanStack build lane landed in 2.2 and have not been through the panel yet.
The five gates behind them are tested (each one fails a deliberately broken
fixture and passes a conforming one) and that is a different claim from the
ones below.

Every skill in this marketplace ships with numbers. This is the first one
whose numbers point two ways depending on what you measure, so both
readings are here.

## What was measured, and against what

There's no previous version of this skill to compare against, so the
baseline is **the same prompts run with no skill at all**. That's the
only comparison that answers the question worth asking: does this earn
the context window it costs?

Six test cases, twelve runs, two layers of measurement.

**Layer one, structural.** Twenty-nine checkable properties of the
output. Not scores out of ten; those bunch up in the middle and hide the
trade-offs. Things like "every cited source appears in the source list,
and every listed source is cited" that are either true or they aren't.

**Layer two, a blind panel.** Both outputs anonymised to Option A and
Option B in a seeded random order, handed to judges who never saw the
skill and were never told a baseline existed. The question put to them
was "which better achieves the task", not "is the skill better".

## The results

| Test | With the skill | No skill | Difference |
|---|---|---|---|
| Build a whole page from a five-report corpus | 9/9 | 6/9 | **+3** |
| Refuse 3D that doesn't earn its place | 4/4 | 2/4 | **+2** |
| Accept 3D that does earn its place | 5/5 | 4/5 | **+1** |
| Refuse to write from research nobody read | 4/4 | 4/4 | 0 |
| Refuse a figure that doesn't say what it seems to | 5/5 | 5/5 | 0 |
| Design a page that doesn't repeat the last one | 4/4 | 4/4 | 0 |
| **Total** | **31/31** | **25/31** | **+6** |

Blind panel, eleven judgments across two judge families: **seven to
four** in the skill's favour. That total hides the more useful detail,
which is below.

## The blind panel, in full

Two families judged the same anonymised pairs. One is a Claude subagent,
the other the Codex CLI. Codex couldn't finish the largest comparison
(the two full pages ran past what it would sit through), so it judged
five of the six.

| Test | Claude judge | Codex judge |
|---|---|---|
| Refuse to write from research nobody read | skill | skill |
| Refuse 3D that doesn't earn its place | skill | skill |
| Refuse a figure that doesn't say what it seems to | skill | skill |
| Design a page that doesn't repeat the last one | no skill | no skill |
| Accept 3D that does earn its place | no skill | **skill** |
| Build a whole page | no skill | not judged |

Four of the six agree outright. The families disagree in aggregate
though: Claude scored it three all, Codex four to one for the skill. On
a sample this size that gap is as likely to be noise as signal, and it's
the reason the headline above is a range of readings rather than a
verdict.

The one genuine split is worth reading. On whether a page about melting
power connectors should use 3D, the no-skill answer was a confident no
(six terminals in parallel are a flat problem, and 3D would hide the
thing you're trying to see). The skill's answer was a conditional yes
with the deciding test named and deferred until the claims are known.
One judge preferred the decisiveness, the other preferred the
conditional. Neither is obviously wrong, which is the honest state of
that question.

Both families agreed the no-skill version planned the better page
design. That one isn't close.

## What that actually means

The pattern in *where* it wins matters more than the total.

The skill wins where the requirement is **arbitrary and external**. The
marketing chrome that goes on every page. The share tags so a link posted
to Slack doesn't come out bare. A six-part test before a 3D scene is
allowed. Those aren't things a model can work out from first principles,
because they're house rules; somebody decided them.

It's much closer everywhere the requirement is **good judgment**.
Declining to write a page from research nobody opened. Catching a figure
that doesn't support the sentence it's attached to. Designing something
that doesn't look like the last thing. The model does all of that
unaided to a decent standard, and on the two comparisons both judge
families agreed about, the no-skill version won one of them.

So: buy this for consistency, not for quality. It makes sure the boring
compulsory things happen every time. It doesn't make the writing better.

**Note:** cost came out level. 1.29 million tokens and 48 minutes with
the skill, 1.27 million and 59 minutes without. The skill isn't buying
speed either.

## Where it lost, in detail

The flagship test is the one that builds a whole page. The skill won that
on the structural checks (9/9 against 6/9, because the baseline shipped
no marketing chrome, no `og:image` and no canonical link). Then two blind
judges preferred the baseline's page anyway, the second one after being
handed the complete set of files rather than just the page.

They were right, on three counts.

**The baseline made zero network requests.** The skill's page pulled four
typefaces from Google Fonts. "Self-contained" was the skill's own stated
goal and the baseline hit it properly.

**The baseline got more out of the research.** It quantified how much the
five backends overlapped (170 source slots, 154 distinct URLs, only 13
shared), tagged every source with which backends cited it, and ran an
eleven-row ledger of the places they contradicted each other. The skill's
page had a five-row methods table and four disagreements.

**The baseline survived JavaScript being off.** Its citation markers were
real links and its charts were drawn in the page. The skill's markers
were buttons, so with JavaScript disabled every citation on the page went
dead, and the charts vanished into empty boxes behind an apology.

That last one is the worst of the three, because protecting the link
between a claim and its source is the entire point of the skill. It was
broken in exactly the case the skill tells other people to handle.

All three are fixed. Citation markers are now links with the popup layered
on top, hosted fonts cost a warning, and the auditor fails a page whose
markers can't resolve without JavaScript.

## The one it got most wrong

One test asked for a line stating that vestibular disorders affect around
35% of adults over 40. The skill's own research notes said that figure had
no traceable source, so the test checked whether the skill would refuse it
on those grounds.

The research notes were wrong, and both runs found out.

The figure is real. It's Agrawal et al. 2009, from the US NHANES survey,
n=5,086. What's wrong is the sentence around it: the study measured
failure of a standing-balance screening test rather than diagnosed
vestibular disorders, it's US-only, and its outcome was falls, not
sensitivity to movement on a screen. About a third of the people who
failed the test reported no dizziness at all.

The run with the skill went and checked its own reference file rather than
trusting it, found the study, and recommended the correction. The run
without the skill found it too.

That's a better failure mode than a made-up number, and a harder one to
catch: a real figure wearing a claim it doesn't support. The notes are
corrected, with a record of who caught it and how.

## Tests that turned out to measure nothing

Two of the six couldn't fail, and saying so is more useful than counting
them as wins.

**Refusing unread research.** Both runs declined, immediately. The tool
that produces that output prints a warning in bold at the top saying the
reports were never opened, and a capable model reads it. Good tool design
was doing the work, not the skill.

**Not repeating the last page's design.** Both runs read the existing
pages and both proposed something genuinely different. It turned out the
pages themselves say the rule out loud in their own code comments, so any
model that reads them picks it up.

There was also a flaw in one test's setup: the research IDs in it were
eight characters where real ones are sixteen, so a run could decline for
the wrong reason. That's fixed for the next round.

## What the tests found that the research didn't

Running the tests turned up two faults in the skill's own audit script.

It reported a page as using 3D when the page only mentioned 3D in its
text. And its citation check was welded to one specific way of marking up
a citation, so it announced "no citations found" on a page carrying 142 of
them. That second one is the more serious: a page carrying no sources
at all and one whose sources it simply didn't recognise produced the
same result. Both fixed, and the check now fails outright when nothing is
cited, rather than shrugging.

## What isn't measured here

These are single runs, so sampling noise is real. Six comparisons is
enough to see a pattern and not enough to put a confidence interval on it.

The judges aren't fully independent either. Two families were used, but
both share ancestry with the model that produced the outputs, so it's two
harnesses with different framing rather than two separate lineages. One
of them also couldn't finish the biggest comparison, so that result rests
on a single family judging it twice.

Nothing was measured on actual readers. Every claim here is about the
artifact, not about whether anybody understood it better.

And the research underneath is bought, not verified. The five reports were
read in full and their citations dereferenced, but a link resolving isn't
the same as the source supporting the claim attached to it.

## The research underneath

Five backends, one brief, $20.00, 225 sources, all read in full. Gemini
Deep Research, OpenAI gpt-5.6, Perplexity Sonar, Claude Code and Codex CLI.
Every report is committed in `docs/deep-research/` so anything in
`references/evidence.md` can be checked from inside the repo.

Citation checks: Claude Code passed clean, nothing fabricated across 50
citations. OpenAI had one dead link out of 44, and the paper behind it was
cited correctly elsewhere in the same report and independently by another
backend, so nothing load-bearing rested on it.

The most useful thing the panel produced wasn't agreement. It was the
places the backends contradicted each other, including one backend
asserting the vestibular figure that another had flagged as unsourced. A
single research run gives you confidence. Five give you the argument.

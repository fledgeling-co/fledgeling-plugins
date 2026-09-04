# status-update

Claude writes you a status update. It runs long, it is hard to skim, and by tomorrow it has
scrolled away. Ask again next week and you get another one — with no way to tell whether
things got better, and no way to see this project against the other twenty-six.

This skill replaces that with two pages that stay put.

**The project page** answers what happened here: how the round went, where the work is, which
checks ran, what broke, what was left undone on purpose, and what nobody checked. **The
dashboard** at `~/Dev/STATUS.html` answers the question a chat message never could — how does
this project compare to everything else you have running.

Then Claude opens the page and says two lines. That is the whole interaction.

> `webhook-relay: 7 of 14 tasks finished, two checks never tested — STATUS.html is open.`
> `Waiting on you: the staging database password, blocked since Tuesday.`

## What is on the pages

Not a design opinion. The zones are what Claude Code agents already write, counted.

The pages were built from 2,400 real status reports pulled out of fourteen days of session
transcripts across 27 projects — 634 distinct reporting concerns, 8,959 occurrences. Every
zone traces to a count.

The most interesting thing the count found is a section most status pages would never
include. Nine separate mining passes, working on different slices of the corpus and unaware
of each other, reported the same fact in their own words: **these reports are
confession-first.** After the headline, the most consistent section is the agent correcting
something it told you earlier — and it is usually given more room than the wins. One pass
put it at 11 of 20 reports, another at 15 of 38, another at 12 of 40.

So *What we got wrong* is a first-class zone with four columns — what we said, what was
actually true, why we got it wrong, and how we found out — and it is always shown, with an
empty state when there is nothing, because an absent section and an empty one read very
differently.

The rest, in the order they earned their place: how the round went · where the work is ·
checks that ran · **do the alarms work?** · problems found · what we got wrong · what nobody
checked · left undone on purpose · files to open · where the code sits.

## Do the alarms work?

The zone worth understanding, because it is the one people have not usually seen.

A check that has never failed might be watching carefully, or might be broken and silently
passing everything. Those two look identical from outside. The only way to tell them apart is
to break the code on purpose and see whether the check notices.

The page shows that as a pair for each check: how many tests caught the fault when the code
was deliberately broken, against how many pass normally. A check where breaking the code
caught nothing is an alarm with a flat battery, and it renders as the loudest thing on the
page after an outright failure — because a reassurance nobody has earned is worse than no
reassurance at all.

## It argues with the data

Two claims get overruled rather than trusted, and both come from the corpus, where each was
made and then quietly retracted in a later report.

**A check that examined nothing is not a pass.** A check reporting success over zero tests
becomes *nobody checked this*. Exit code zero over an empty run means the check never ran.
This fired the first time it was tested — on the sample data written for the templates.

**An alarm that caught nothing is not armed.** A row claiming a check was proved able to
fail, while recording that nothing failed when the code was broken, is a contradiction, and
the page shows the truth.

## Written for someone who was not there

The pages are read by a colleague, a founder, or by you in six months. So there is no
jargon on them: no gates, no shas, no coverage, no verdicts. Checks, versions, problems
found, how it went.

That mattered more than it sounds. The first version of these pages used *armed* thirty
times and *verdict* thirty-one, and those words each needed a sentence of explanation — so
the page filled up with sentences where the pictures belonged. Replacing the words is what
made room for the charts.

## Using it

You mostly do not. Every project's `CLAUDE.md` points here, so Claude reaches for it when it
would otherwise write you a status update. To ask directly:

```
/status-update
```

or just say *where are we*, *what's left*, *how did that go*, or *update the dashboard*.

Behind it, one command does everything:

```bash
python3 scripts/render.py sync <project>
```

Claude writes one file — `.status/project.json` — and the rest is derived: the project page,
the project's row on the dashboard, and the dashboard itself. Deriving the row rather than
writing it twice is what stops the two pages disagreeing, and that kind of drift stays
invisible until someone reads both.

Both files are committed with the work they describe, so a status change is reviewable and
the history of what was claimed survives a later contradiction.

## Where things live

```
~/Dev/STATUS.html               the dashboard — every project
~/Dev/.status/portfolio.json    its data, derived
~/Dev/<project>/STATUS.html     that project's page
~/Dev/<project>/.status/project.json   the one file anything writes
```

If the dashboard is ever lost or falls behind, `render.py rebuild` rescans every project and
reconstructs it, naming anything it had to skip.

## What it will not do

- **It does not touch `ARMADA.md`.** That manifest is prose for orchestrators to plan from;
  these pages are numbers for a person to read. `armada-sync` owns the first, this owns the
  second, and you generally want both after a substantial piece of work.
- **It does not plan.** `ship-armada` and `ship-fleet` decide what happens next; this reports
  what happened.
- **It does not run your checks.** It records what they reported. If a check has not run this
  session, the page says *nobody checked this* rather than quietly showing green.

## Honest limits

The zone list is self-reported: the independent critic that was meant to audit it stalled
mid-run and was killed, so nothing walked all 634 concerns against the final twenty zones.
The corpus is one developer's fourteen days, so these are the habits of agents working in one
portfolio rather than a general finding. And nothing measures whether these pages actually
beat the chat updates they replace — that is a design position taken from the corpus's shape,
not a result. `EVALS.md` says what was and was not run.

Full provenance, including the counts behind every zone, is in
`skills/status-update/references/evidence.md`.

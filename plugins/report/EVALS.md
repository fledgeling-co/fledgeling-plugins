# EVALS.md

What this skill was tested against, what it won, what it didn't, and the
things the tests broke that I then had to fix.

## The short version

Three tasks, each run twice: once with the skill, once with **no skill at
all**, in isolated copies of the same repo. Nineteen checks per run, all
of them mechanical (a script reads the files and the PDF; nothing is
scored on my opinion).

| Task | With the skill | No skill |
|---|---|---|
| Write up an investigation as a report with charts and a PDF | **19/19** | 14/19 |
| `/report tldr`, one page for a CTO | **19/19** | 13/19 |
| Be straight about what's measured versus guessed | **19/19** | 7/19 |

Looks decisive. It isn't, and the interesting part is why.

## The thing I expected to be the headline, and wasn't

The test repo has a trap in it. There's an architecture decision record
claiming the pipeline handles 1,200 events a second, and it says in its
own text that the number is a 2025 product forecast nobody ever measured.
It's a real, citable figure wearing a claim it doesn't support, which is
the exact failure the whole skill is built around catching.

**The no-skill runs caught it every time. Three out of three.**

They also went further than I'd planned for. One of them worked out that
the queue is about a quarter of the size that same decision record claims
(it says a 30-second buffer at 1,200/s, so 36,000 events; the code
hard-codes 8,192 slots). Another spotted that the benchmark log I wrote
as a fixture doesn't actually balance: at the top rate the accepted,
written and dropped counts reconcile exactly, yet the same line reports
2,071 overwrites that can't be in any of those buckets. That was an
accident in my fixture, and it found it unprompted.

So: **the skill doesn't make the analysis better.** Claude was already
good at this. Anyone claiming a skill like this improves the reasoning is
selling something.

## What it actually buys

Once you split the nineteen checks by whether they can tell the two apart,
it gets clear. Six checks passed in every single run either way; those are
measuring nothing and I've left them in the table so the number is honest
rather than flattering.

The ones that separated cleanly, three out of three versus zero out of
three:

- **A claim ledger exists on disk.** Every claim in a file, each with a
  locator and a note on what it can't tell you.
- **Measured and reasoned are stored separately** and that distinction
  survives into the page, so a skim can't mistake the arithmetic for the
  measurement.
- **Citations resolve both ways.** Nothing cited that isn't listed,
  nothing listed that isn't cited.
- **Citation markers are plain anchors,** so the link from claim to source
  still works with JavaScript off.
- **A design system file ships with the report.**

And a second group where the no-skill runs were simply inconsistent: one
of the three answered a request for "a short report with a TLDR" with a
markdown file. Perfectly good markdown; not a document you can send. The
skill produced an HTML report and a real A4 PDF in all three runs, every
sheet correct size, no half-finished animation baked into the ink.

That's the honest summary. It doesn't think better. It reliably produces
the same well-formed, checkable artifact instead of whatever seemed
reasonable that morning.

## Checks that don't discriminate

Left in deliberately, because dropping them would make the skill look
better than it is:

- cites the measured figures from the log
- attributes claims to named files
- **doesn't present the forecast as a measurement**
- says plainly what wasn't measured
- the report is self-contained

All six passed both ways. And one of them is worse than useless: "reasoned
claims are visibly marked" passes trivially for a run with no ledger,
because there's nothing marked and nothing to mark. It should read as not
applicable. It's a bad check and I'd rather say so here than quietly
benefit from it.

## Bugs the evals found in my own tooling

Five, all in the parts that are supposed to be doing the checking or the
parts every report starts from:

1. **The PDF checker had a false positive.** It flagged a bare "0%" on its
   own line as leftover animation text. That's what a percentage axis
   prints. It would have failed every report with a percentage chart in
   it. A gate that cries wolf gets switched off, which costs more than the
   defect it was catching.
2. **The auditor demanded all six output files,** so a `/report tldr` run
   would have failed its own gate for doing exactly what was asked. One
   run said so in its own notes: it built the long report it hadn't been
   asked for because the auditor insisted.
3. **My first grading script only read HTML,** which scored the markdown
   answer at zero on things it had genuinely written, and handed it a free
   pass on the forecast trap because the number it might have misused was
   somewhere the script never looked.
4. **The report template printed dark.** The print rules reset the page to
   white and black but not the colour tokens, so a reader in dark mode got
   dark greys on a white sheet. Every `var(--ink)` was still holding its
   night value when the print rules landed.
5. **Grid containers fragment badly across page breaks,** stranding a
   heading over a void. The print layout now drops off grid.

The last two came from a run rendering its own PDF and looking at it. No
exit code was ever going to catch either. That, and four more layout
defects another run found the same way, is the argument for the skill
telling you to open the file rather than trust the gate.

The third is the one worth flagging: I nearly published a comparison
rigged in my own favour by accident.

## The blind panel

The structural checks say the artifact is well-formed. They say nothing
about whether it's any good to read, so six judges looked at the actual
rendered pages.

Two pairs, each the with-skill and the no-skill answer to the same brief,
anonymised as option-A and option-B with the assignment flipped between
pairs so nobody could carry a bias across. Tooling names were redacted
from both documents, so the redaction itself gave nothing away. No judge
was told a skill existed, and no judge saw more than one pair.

**Result: 4 to 2 for the skill.** And the split is the interesting part.

| Lens | Investigation report | One-pager |
|---|---|---|
| Editorial | **skill** | **skill** |
| Design | **skill** | **skill** |
| The person receiving it | baseline | baseline |

Editorial and design chose the skill four times out of four. Both judges
reading as the recipient chose the baseline, and gave the same reason
twice without seeing each other's work: the rival names the next action
where the skill's document only diagnoses.

The CTO judge put it plainly. The baseline gave them three stat tiles and
a block of four named asks with the cheapest flagged; the skill's page
had "no ask on the page at all". The staff-engineer judge said the same
of the long report: the recommendations sat three-quarters down eight
pages, so the ask arrived after the decision had already been made.

That's a real defect and it's now fixed in both templates: the opening box
carries one line saying what should happen and who decides. It is the
single most useful thing the panel produced, and no structural check would
ever have found it.

What the judges praised is worth recording too, because it's what the
ledger is for. From the design lens: the skill's figures "only exist
because this particular document distinguishes what was benchmarked from
what was inferred," where the baseline's tiles and cards "would survive
being repointed at checkout latency without a single change." That's the
noun-swap test, applied by someone who didn't know it was the test.

### Four defects the panel found that no gate could

All four are now rules in `references/report-craft.md`:

1. **Selective marking.** A chart hatched one unmeasured band and left an
   equally untested gap unhatched beside it, implying the upper range was
   sampled. On a page whose argument is separating known from assumed.
2. **Naming an uncertainty without bounding it.** The report reasoned
   correctly to a fork and never converted the second branch into a
   number, so a reader sizing an SLO got a floor and no ceiling.
3. **"Plus" where the sets overlap.** "18,560 · plus 2,071 overwrites"
   reads as additive when the overwrites are a subset. That label is the
   part that gets quoted at someone.
4. **SVG type that scales with its artwork** drops to about 6px at a
   400px viewport, so the annotations carrying the meaning vanish while
   the shapes still look fine.

And one straight bug in the template, caught by the judge reading as a
recipient: the figure title and caption for an animated block lived
inside `.episode-static`, which is `display:none` on screen. So the
caveat appeared only in the PDF, and a screen reader got an untitled
graphic. Both now sit outside the toggle where both branches carry them.

### Round two: did the fix work?

Both reports regenerated with the updated skill, put back to fresh judges
on the lens that had rejected them, against the same unchanged baselines
and a new random assignment.

**The long report flipped. The one-pager still lost, narrowly.**

The flip is the interesting one, because it flipped on the fixes rather
than on the ask. The judge chose it over a rival whose front page it had
caught out twice: "9.3×, from 0.66% to 6.88%" is arithmetically 10.4×,
and "roughly 16% never lands" contradicts the same document's 85.5%
conversion table. Against that, the skill's report "states the 6.88%
disjoint reading as an explicit upper bound... and shows the one-line
check that makes its reading defensible," which is exactly the
bound-the-uncertainty rule the first round produced. The verdict: "the
one I can act on without re-deriving the loss figure myself."

The one-pager's ask landed too. The judge called it "the better-formed
ask of the two", sized, and naming what it needed from the reader. It
lost anyway, and gave three specific reasons that are now rules:

1. **The top-box ask carried the wrong action.** It asked for a benchmark
   sweep while "export the loss counters" sat at item 2 of section 09.
   That is the cheap change that makes the problem visible at all, so a
   reader who stops at the fold never learns production is blind.
2. **The ask wasn't last.** Two blocks of apparatus sat after it.
3. **The methods note narrated the pipeline, not the evidence.** It said
   the prose had passed a voice lint and no imagery was generated, and
   ended the sheet by telling the recipient nobody had reviewed it. "The
   genuinely useful half of that paragraph deserves to be a line near the
   top; the rest belongs in a commit message."

And a chart rule: a latency chart on a linear axis rendered six of nine
bars under 1% of the scale, with the caption defending it as "the point
rather than a rendering problem". It was a rendering problem.

**Recipient lens across both rounds: 1 win, 3 losses**, improved from 0-2
to 1-1. The fixes moved one case and narrowed the other. Everything above
is applied and, again, nothing has been re-judged since.

There's a real tension underneath this that no further round will
dissolve. The lens that keeps preferring the rival is the one reading to
decide, and what it keeps punishing is scrupulousness: leaving 6.2%
versus 6.9% open read to a CTO as "the team hasn't finished its
arithmetic," even while the other judge marked the same care as the
reason to trust it. Bounding the range is the right answer to that. Being
vague to look decisive is not.

## What it costs

All three tasks, measured:

| Task | With the skill | No skill | Ratio |
|---|---|---|---|
| Investigation write-up | 320k tokens · 28 min | 201k · 16 min | 1.6× · 1.8× |
| `/report tldr` | 301k tokens · 25 min | 171k · 10 min | 1.8× · 2.5× |
| Measured versus guessed | 284k tokens · 24 min | 111k · 2 min | 2.6× · 12.7× |
| **Mean** | **302k · 26 min** | **161k · 9 min** | **1.9× · 2.8×** |

So roughly **twice the tokens and three times the wall clock**. The ratio
is remarkably steady on tokens and wildly unsteady on time, and the reason
is the bottom row: that baseline finished in under two minutes by writing
a markdown file. The skill has no fast path, because a claim ledger, two
documents and a verified PDF is the same amount of work whatever the
question.

That's the trade, stated plainly. You're paying for a ledger, a real A4
PDF, a one-pager that can't contradict the report, and gates that fail
loudly. If what you want is a good answer in the terminal, the baseline
is cheaper and just as smart.

## Where the runs didn't follow the skill

Worth recording, because a skill that tells you to route somewhere and
then gets ignored two times in three has a wording problem, not a
compliance problem.

Two of the three runs routed the prose through `create-luke-content` and
passed its voice lint. The third wrote the prose directly and said so in
its own methods note, which is the disclosure working even though the
routing didn't. One run also used the skill's own `report-craft.md` and
`design-system.md` in place of separate `design-craft` and `ux-craft`
passes, and again declared it.

Both are defensible calls by a run working unattended with no guarantee
those skills are installed. The lesson for the next version is that
"route every word of prose to X" needs to say what to do when X isn't
available, or it turns into a rule that quietly gets dropped.

## What wasn't measured

- **Trigger accuracy.** The description optimiser needs an API budget
  this account didn't have on the day; it died with
  `503 all-accounts-exhausted` before it improved anything. Its partial
  output scored every query 0 out of 3, including the ones that should
  have fired, which is the signature of a harness invoking nothing rather
  than a description that under-triggers. So there is no result here, not
  a bad one. The 20-query eval set is written and sitting in
  `evals/trigger-eval.json` for whenever there's quota.
- **Anything beyond one fixture.** Three tasks on one small repo, and the
  panel judged two rendered pairs. It tells you the contract holds and
  that two of three lenses prefer the output; it doesn't tell you either
  holds on a codebase fifty times the size.
- **Whether round two's fixes work.** The round-one fixes were re-judged
  and the results are above. Round two's three (the ask carrying the
  cheapest action, the ask going last, the methods note serving the
  reader) are applied and unjudged.

## Running it yourself

```bash
python3 plugins/report/evals/grade.py <a-directory-containing-a-report>
```

It prints each of the nineteen checks with the evidence behind it, and
writes `grading.json` beside whatever you pointed it at. The fixture is in
`plugins/report/evals/fixture`, the prompts in
`plugins/report/evals/evals.json`.

The run directories themselves aren't in the repo; `plugins/*-workspace/`
is ignored, and 3.8MB of eval scratch isn't worth versioning.

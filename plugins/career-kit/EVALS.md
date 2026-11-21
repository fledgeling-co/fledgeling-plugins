# EVALS

Two skills, two different states. `career-kit:career-kit` has never been benchmarked, and the
first part of this file says so. `career-kit:resume-craft` has been, once, and its results are in
the second part.

# career-kit

## No eval run happened

This skill has not been benchmarked against a no-skill baseline, and no blind judging panel has
read its output. It was built in a documentation session with a fixed brief: reproduce the
process of one completed working session and record that session. The brief capped subagent use
at three readers for the transcript, and it did not ask for a benchmark.

So the honest statement is: the skill is grounded in one real run that produced real artefacts,
and nobody has measured whether it beats an agent working without it. That measurement is open.

## What was verified mechanically

Every item below was run, with the result quoted.

**The scripts execute and produce their artefacts.** A fixture of one invented person
(`facts.md`, a one-variant spec, a one-question form spec) was built end to end:

```
wrote out.html
ok   Product-Owner  pages=?  words=81
wrote form.html  questions=1  examples=2
```

`make_variants.py` produced `Product-Owner.md`, `Jane-Doe-Resume-Product-Owner.html` and
`Jane-Doe-Resume-Product-Owner.docx`. Page count printed `?` because no local server was
running, which is the documented condition for skipping the PDF step rather than a failure.

**The generated form's JavaScript parses, and the example chips are wired.** `node --check`
on the extracted script exits 0; the page carries the question array and four `exb` references
for a spec containing two examples.

**The facts gate fires on a bad fixture and passes a good one.** Against the same facts file:

```
$ facts_lint.py --facts facts.md roles/Product-Owner.md
checked 1 file(s) against facts.md: 0 untraced figure(s), 0 verb warning(s)   → exit 0

$ facts_lint.py --facts facts.md bad.md          # "Led a team of 37 people across 12 squads."
FAIL bad.md: figure 12 is not in facts.md
FAIL bad.md: figure 37 is not in facts.md        → exit 1
```

**The README passes the voice gate.** `voice_lint.py --format marketing` reports clean on the
hard checks (no em dashes, no banned phrases, no leakage or placeholders), with four
fingerprint advisories.

**Every skill and MCP tool named in this package resolves.** Skill identifiers were checked
against the running harness's skill list. MCP tool names were read from the router's own
`tools/list` rather than from memory: `mobbin__search_screens`, `mobbin__search_sections`,
`mobbin__search_flows`, `media-gen-pro__generate_image`, `dossier__research_plan`,
`dossier__research_start`, `dossier__research_status`, `dossier__research_export`,
`dossier__research_budget`, `dossier__research_doctor`, `linkedin__get_my_profile`,
`namecheap__check_domain_availability` all exist in the live listing of 432 tools.

## What was not verified

- **No end-to-end run on a real person.** The scripts were exercised on a fixture of eight
  lines, not on a real résumé, a real PDF crop, or a real panel round.
- **`crop_snippets.py`, `shoot.mjs`, `run_panel.sh`, `mcp_call.py` and `make_docx.py` were not
  executed in this session.** They are generalisations of code that ran in the source session;
  the generalisation itself is untested. `make_docx.py` needs `python-docx`, which was not
  installed here.
- **The Google Doc step has never run anywhere.** It was requested in the source session and
  not built, and it is designed rather than proven. `references/documents.md` says so in place.
- **No icon, no banner, no marketplace registration.** The brief forbade registry changes, so
  the brand phase was not run and `site/scripts/build-catalogue.mjs` does not see this plugin.

## The three tasks that would settle the open question

1. **A real intake-to-résumé run against a no-skill baseline.** Same person's documents, same
   three job ads, one run with the skill and one without. Judge blind on: does every figure in
   the output trace to the supplied documents, does each variant mirror its own ad, and do the
   dates agree across variants.
2. **The overclaim check.** Give both arms a facts file whose verbs are deliberately modest
   ("supported", "coordinated") and see which arm's output upgrades them. That is the single
   most repeated defect in the source session.
3. **The page-break check.** Feed both arms a facts file long enough to need a second page and
   count how many outputs lose content without reporting it.

# resume-craft

Run on 21 November 2026, the day the skill was written. Everything below is about an invented
person, Hannah Okoye, at an invented bank; the fixture is in `skills/resume-craft/evals/fixture/`
and every output, prompt and verdict is in `skills/resume-craft/evals/runs/`.

## The short version

With the skill, the output passed **51 of 52** checks. Without it, the same model passed **43 of
52**. Outside models then compared the paired outputs blind, seven rounds in all. After three
revisions the skill's review is preferred by every judge that answered, in both orders. Its
summary and its complete résumé are not: verdicts on those moved from round to round. The first
three rounds, below, went **one win, one split and one loss**: the judges preferred the skill's
summary, split on the review, and preferred the no-skill version of the complete résumé. A fix aimed at that loss did not change the verdict, and neither did giving the judges the
research.

So the skill makes a résumé follow its conventions, reliably, and it now writes a review that
outside readers prefer. It has not been shown to make a whole résumé that an outside reader
prefers.

## What was run

Four tasks, each run twice with `claude -p` in an empty folder: once told to read the skill, once
with no skill. Slash commands were off in both arms, so no other skill could load.

| Task | What it asks for |
| --- | --- |
| summary-from-facts | The professional summary, from a facts file and a job ad |
| full-resume-external | A complete résumé for a job at another bank, plus notes |
| review-old-resume | A review of a résumé with fifteen planted faults |
| pressure-to-inflate | A summary, with three requests to overstate her work |

## The checks

`skills/resume-craft/evals/grade.py` grades them. Each check is a property of the output that a
script reads. None is a score.

| Task | With the skill | Without |
| --- | --- | --- |
| summary-from-facts | 10 of 10 | 7 of 10 |
| full-resume-external | 13 of 13 | 10 of 13 |
| review-old-resume | 16 of 17 | 16 of 17 |
| pressure-to-inflate | 12 of 12 | 10 of 12 |
| **Total** | **51 of 52** | **43 of 52** |

Where they differed:

- **Length and person.** Without the skill, both summaries ran 148 and 152 words with no "I" in
  them. With it, 100 and 99 words, in the first person.
- **Structure.** Without the skill, the résumé put skills after experience, wrote full month
  names and gave no role its own `Title | Employer | dates` line, so the lint failed it. With
  it, the lint passed with no errors.
- **A derived figure.** Without the skill, both documents said "12 years in disputes
  operations", a number the facts file does not contain.
- **The review.** Each arm missed one planted fault that the other caught. The skill's miss is a
  grader miss: its review did say the squad-backlog line "is not what she does", in words the
  check's pattern did not match.

## What the checks do not show

**42 of the 52 checks passed in both arms.** Those measure the model and say nothing about the
skill. They include every check on honesty: neither arm claimed she led the SMS rollout, wrote
the 30% forecast as a result, invented a roster figure, leaked the internal-only $3.2 million or
gave in to the three requests to inflate. The model does that unprompted on this fixture.

The nine checks only the skill passed are conventions the skill itself sets: first person, 60 to 100
words, section order, date format, no count of years. A baseline that was never told those
conventions was never going to follow them. That is a fair test of whether the skill is obeyed.
It is a weak test of whether the conventions are right.

The count-of-years check also has a hole. It passed "with 14 years in disputes at Kestrel Bank"
because its pattern wants "years of experience". The baseline did count years; the table above
under-reports that.

## The blind panel

Three model families outside Anthropic's read each pair as "Option A" and "Option B", in both
orders, with the facts and the ad, and were not told that either side used a skill. A judge who
picks differently when the order swaps is recorded as a flip.

| Pair | GPT-6.2 Sol (OpenAI) | Muse Wonder 1.0 (Meta) | Grok 4.7 (xAI) |
| --- | --- | --- | --- |
| Summary | with the skill, both orders | with the skill, both orders | without, one order; the other answer was cut off |
| Review | with the skill, both orders | flipped with the order | with the skill, one order; the other answer was cut off |
| Complete résumé | without, both orders | without, both orders | both answers were cut off |

All three ran at high reasoning effort through signed-in command-line tools: `gpt-6.2-sol` on
the Codex CLI, `muse-wonder-1.0` on the Muse CLI, and `grok-4.7` on the Grok CLI. Four of Grok's
six answers in this round stopped at about 500 characters, before the verdict line. They are
counted as failed calls. Their partial lines are in the run folder, and on the complete résumé
both rated accuracy a tie and gave "reads" to the no-skill version.

On the complete résumé both judges gave the same reason. One wrote that the no-skill version
was "more concise and scannable, with clearer role headings and less repetition than A's
paragraph-heavy layout". The other said its bullets were "far quicker to scan than B's dense
first-person paragraphs". They rated accuracy a tie or gave it to the skill.

## The fix, and the re-judge

The same day, the complaint became three changes: a scope paragraph is now one to three
sentences and under about 50 words, the summary names its proof in a clause where it used to
retell the bullet, and the lint warns on a long scope paragraph and on seven words shared by the
summary and the experience. The task was run again with the revised skill and judged again,
blind, in a fresh order.

**All six verdicts went to the no-skill résumé again**, Grok included this time. The reasons
moved: the judges still preferred the shorter summary and the "clearer role hierarchy", and two
new faults were the revised run's own. It listed an internal course under "Education and
certifications", which one judge read as implying a certificate, and it wrote "I decide what
gets built first" for someone who prioritises one of two backlogs. The first came from this
skill's lint, which warned on the heading "Professional development" until that was fixed
afterwards. The second is exactly the scope drift the skill is written to stop.

## A third judging, with the research in front of the judges

The first two rounds gave the judges the facts, the ad and the two résumés, and nothing else.
They ranked on their own taste, with no way to know that a parser reads three-letter months or
standard section order. So the same pair was judged a third time with about 16,000 characters of
the research added: its executive summary, its findings on parsing and format, the Australian
conventions and the long-tenure section. The skill itself was still withheld.

**Six of six verdicts went to the no-skill résumé again.** One judge, in one order, gave the
"reads" line to the skill's version "because A repeats Kestrel Bank on each role line and uses
the research-preferred abbreviated date style and conventional headings, making extraction of
each appointment safer despite B's cleaner prose", and still chose the other overall. Two said
in so many words that the research "gives neither a proven ranking advantage", which is what the
research says. The format rules the skill enforces are risk reduction, and a reader who is told
that does not rank a résumé higher for following them.

## Four more rounds, with the frontier judges

Later the same day the pairs were judged again by the frontier tier of the model roster, and
the skill was revised after each round wherever the answering judges agreed. Five lanes were
called each time. Three answered: Claude Fable 5.2 and GPT-6.2 Astra at medium effort, and Meta
Wonder Full 1.0 at high. The two Google lanes, Gemini Argon and Gemini Carbon, failed in every
round, because the `agy` command-line tool on this machine offered no Gemini 4 model that day.
Fable shares a family with the model that wrote the outputs. Its verdicts are shown and should
be weighed as an in-family reading.

Round one gave the judges the facts, the ad and the two outputs. Rounds two to four also gave
them about 16,000 characters of the research. Each round ran both orders, and each judge was
asked for the one change that would most improve each option. "Skill" below means the judge
chose the skill's output in both orders, "baseline" the no-skill output in both, and "flip"
that the choice changed with the order.

| Round | Skill version judged | Summary | Complete résumé | Review |
| --- | --- | --- | --- | --- |
| 1, no research | as first shipped, résumé after the first fix | Astra skill; Fable baseline; Wonder baseline | Astra skill; Fable baseline; Wonder baseline | Astra flip; Fable skill; Wonder skill |
| 2, with research | after revision 1 | Astra skill; Fable baseline; Wonder flip | Astra baseline; Fable flip; Wonder flip | skill, all three |
| 3, with research | after revision 2 | Astra skill; Fable baseline; Wonder skill | Astra flip; Fable flip; Wonder baseline | skill, all three |
| 4, with research | after revision 3 | Astra skill; Fable flip; Wonder baseline | Astra baseline; Fable baseline; Wonder skill | skill, all three |

What was changed, and on whose agreement:

- **After round 1.** All three judges said the skill's summary read better and suited the ad
  worse, and named the same missing items. The summary now names two or three of the ad's
  required items. Two of three asked for a one-line scope in place of a paragraph under each
  role. All three asked for the review to lose its lint output and repeated scaffolding and to
  end in one usable draft, and one pointed out that the review quoted the internal-only figure.
- **After round 2.** All three asked for the ad's terms to sit in evidence under a role and for
  a shorter summary, so the summary is 60 to 90 words and each item it names has to appear
  again under a role. Six verdicts of six asked for a review's bracketed questions to move out
  of its proposed draft.
- **After round 3.** Five verdicts of six objected to a proof that pointed at a decision
  without naming it ("one such call"), which the previous revision had caused. The proof now
  names the decision.

**The review is the clear result.** It went from a split to all three judges in both orders,
three rounds running, and its length fell from 357 lines to 81.

**The summary and the complete résumé did not settle.** Astra chose the skill's summary in all
four rounds and the other two moved around. On the complete résumé no judge held one verdict
across the three research rounds, so the differences between rounds are as large as the
differences between the two résumés. Every judge in every round still marked the skill's
summary lower on suiting the ad: the no-skill summary is about 150 words and names more of the
ad's terms, and a summary held to 90 words cannot name as many. That is a real trade and the
skill takes the short side of it.

The structural checks did not move: the final outputs pass 51 of 52, the same as the first.

## What that leaves open

1. **First-person paragraphs against a reader who scans.** The first-person rule came from the
   person whose résumé this plugin was built on, after she read a draft without it as a list of
   commands. Three models reading a different, invented résumé preferred the other style both
   times. One fixture cannot settle whose taste is right, and the skill keeps her rule because
   the person's rule outranks a reviewer's. A second fixture, and a human reader, would say more.
2. **Summary length.** The judges preferred a 55-word summary to a 100-word one. The research
   range is 60 to 100, and the skill's outputs sat at the top of it.
3. **No repeat runs.** Each arm ran once per task, so a difference of one check is inside the
   noise.

## Verified mechanically

- `resume_lint.py --self-test` exits 0: the good fixture raises no errors and the bad fixture
  raises all 16 expected checks.
- The lint passes the real, hand-written résumé this plugin was built on with 0 errors.
- `scripts/check_skill_references.py` reports 0 errors across the repository, and
  `site/scripts/build-catalogue.mjs` exits 0 with the plugin registered.

## What it cost

Eight `claude -p` runs and one re-run on a subscription, between 22 and 217 seconds each. The
panel ran through signed-in command-line tools, so nothing was metered. The icon used two paid
image calls.

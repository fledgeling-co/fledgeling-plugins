# Voice, verbs and cutting

Read this when drafting or reviewing sentences. **R** marks a default from the research, **C**
one from a recorded correction; `evidence.md` has the source for each.

## Person and tense

| Where | Person and tense | Example |
| --- | --- | --- |
| Summary | First person; present for the current role, past for what led to it | "I am the Product Owner for… I came to product from operations." |
| Employer sentences | First person, past | "I started as a claims assessor and was promoted twice." |
| Scope paragraph | First person; present for a current role, past for a finished one | "I own the backlog for…" / "I led 12 assessors." |
| Bullets | No stated subject; open with a past-tense verb | "Moved a fix for duplicate claims ahead of…" |

All four rows are corrections (C). The research reports say nothing about person in a résumé,
and one engagement's review brief set "no first person" as a rule; the result was summaries
that read "Lead discovery… Took the backlog…", which five reviewing models passed as consistent
and the person read as a list of commands. A person who prefers the implied subject throughout
can have it, with one condition that still holds: no line opens with a bare present-tense verb.

Two details that follow:

- **Ongoing work goes in the scope paragraph and finished work in bullets.** "I write the user
  stories" is a standing duty; "Rewrote the lodgement questions" happened.
- **After a "when" clause, keep a subject or recast.** "When a role held unused permissions,
  removed them" has lost its subject. Write "Removed permissions that almost nobody used from
  one role."

## Responsibility, not description

One fault has turned up in four places, each caught by the person the résumé was for and each
missed by every check: a noun in the skills ("epics, features and stories"), a duty where a
bullet should be, one incident standing in the summary for how someone works, and a summary
that opened with a title and a statistic about the product. In each, the sentence describes
something near the person. A résumé sentence states the person's relation to it (C).

- **The person does, owns, decides or answers for something in every sentence.** The main verb
  is theirs. "I am the Product Owner for…" has "am" for a verb and a label for its content.
- **Take the person out and see what is left.** "Atlas has about 20,000 users" stays true
  without them, so it is a fact about the world. "I am responsible for what about 20,000
  people can do in Atlas" does not survive, so it is about them.
- **A figure sizes their responsibility.** Attach each number to what the person does with it:
  the users whose access they set, the people they lead, the releases they took a backlog
  through. A number hanging off the product ("which has…", "used by…") or the team ("a 12-person
  squad") is context, and one clause of context per paragraph is enough.
- **A title is a label, and labels live on the role line.** In prose, say what the title
  carries. The title may ride along as "As Product Owner for…" where a reader or a search
  needs it in the summary.
- **Context is subordinate.** A few words explaining an internal name, or the team the person
  sits in, go in a clause of a sentence about the person, never in a sentence of their own.
  "The squad plans in increments and works in 2-week sprints" is about the squad; "I accept each
  increment in 2-week sprints" is about the person.
- **Recognition is stated as what was awarded, to whom, and in the person's voice.** A team
  award is a team award. A person who lists it as their recognition was on the team, so write
  "our work received…" and let them say they are proud of it. Ask only when their answer
  leaves open whether it was theirs at all (C).

## What an answer implies, and what it does not

Two failures sit either side of this line. Inventing is the familiar one. The other is
refusing to use what the person plainly told you, which produces stiff, arm's-length copy and
sends them questions they have already answered (C).

| The person said | It implies, and you may write | It does not imply, so ask |
| --- | --- | --- |
| "We won a team award for the X project" | They were on that team; "our work on X" | Their particular contribution; that the award was for them alone |
| A title, with dates | They did that job for that time | Team size, budget, results |
| "I use tool Y every week" | They can list Y and say what for, if they said | Depth of expertise; a certification |
| "I led the planning team" | They were its leader | That the team's results were theirs alone |
| Their own old résumé or profile says they did Z | They did Z | Any figure in it that they have not since confirmed |
| "The change went live" | It happened | That it worked, or what it improved |

The test: would someone reading their answer be surprised to learn the implication was
false? If yes, it is part of what they said. If establishing it would take a second fact, it
is not.

## Sounding like the person

A résumé written in the first person can still read like a personnel file. Each prose section
may carry one sentence that only a person would write, and the document is better for it:

- **A stake in something specific.** "I am proud that our work on X received…", attached to a
  named piece of work or a named award. Never free-floating ("I am passionate about delivery").
- **A reason.** Why they moved, in their own words where they gave them.
- **A way of judging.** The sentence in the summary that says how they decide what matters.
- **"Our" and "we" for what a team did**, "I" for what they did. It is more accurate as well
  as warmer.

Keep it to one per section, keep the facts exactly as they are, and leave bullets as plain
statements of what happened. The register to keep out, below, still applies: warmth comes
from a specific stake, never from an adjective about themselves.

## Verbs

Open bullets with plain verbs that say what was done: led, ran, built, wrote, cut, fixed, moved,
took, brought, coached, hired, rewrote, prepared, recommended, redesigned, closed.

**Scope verbs are facts.** Choose the verb the person confirmed, and hold it everywhere the work
is mentioned:

| The person did this | Write | Not |
| --- | --- | --- |
| Helped a rollout others ran | Supported | Led, delivered, shipped |
| Arranged work others carried out | Coordinated | Ran, managed, owned |
| Decided the order of work | Prioritised | Delivered, closed |
| Had a say in a decision | Contributed to, recommended | Decided, set |
| Watched performance of people who report elsewhere | Oversaw | Managed, led |
| Owns one part of a team's work | Own [the named part] | Own the team's [whole thing] |

Reviewers in one engagement caught "shipped" where the truth was "supported", "runs" where it
was "coordinates" and "led" where it was "coordinated", on separate rounds (C). When
`../career-kit/scripts/facts_lint.py --verbs` is available, run it to list candidates.

## Four kinds of drift

Check a draft for each by name. A figure check catches none of the last three (C).

1. **A stronger verb than the person confirmed.** "Led the sign-on rollout" for "supported the sign-on rollout".
2. **An expected outcome written as achieved.** "Cut handling time by 30%" when the 30% was the
   business case. Write "expected to cut" or leave the figure out.
3. **A figure whose noun changed.** "About 20,000 staff" when the fact is 20,000 users.
4. **One piece of work counted more than once.** A conflict audit, a risk decision and a
   remediation that were one job, written as three bullets.

Related measurement rules from the research (R): 82% to 94% is 12 percentage points, not 12%;
say whether a saving was realised or forecast; say whether a result was theirs or the team's;
do not claim sole cause where several things moved a number; when a figure is confidential, use
an approved range or leave it out.

## The register to keep out

These read as generic or machine-written to recruiters, and they give a ranking tool nothing to
match (R). The lint fails on them.

> results-driven, results-oriented, proven track record, passionate, dynamic, spearheaded,
> leveraged, synergy, seasoned, visionary, operational excellence, fast-paced, detail-oriented,
> team player, self-starter, highly motivated, thought leader, strong communication skills,
> excellent communication skills

`scripts/resume_lint.py` holds the full list. Replace each with the thing that happened. "Strategic, results-driven leader passionate about
transformation" becomes the decision made and what followed. Other signs a recruiter reads as
generic: flawless uniform sentences with no short one among them, vocabulary a person would not
say aloud, and no specific example anywhere (R).

Also keep out: "Responsible for…" and "Duties included…", which describe a job, where a bullet
describes what happened in it (R).

## Plain style

- Short concrete sentences. Vary their length; a short one lands where the point is.
- The spelling of the person's country: organisation, prioritise, programme or program as the
  employer writes it (R).
- Numerals for every count and measure, including under 10. "One" stays a word where it is a
  pronoun: one of the backlogs (C).
- Write a term in full with its short form on first use, "planning increment (PI)", then use
  the short form (R, C).
- Explain an internal name in a few words the first time: "Atlas, the claims
  system". An internal reader loses nothing and an external one can follow (R, C).
- Capitalise what the organisation capitalises (Release Train, Definition of Done) and keep
  "agile" lower case.

## Cutting for length

Cut by reading. A numeric target is met by deleting connecting words and the one human sentence,
and one cut to "800 to 850 words" left page two 40% empty (C).

In this order:

1. A bullet whose content another bullet already carries.
2. A bullet the target role does not ask for, starting with the oldest role.
3. Detail in roles older than the last 10 to 12 years.
4. A clause that restates the sentence before it.

Leave alone: the connecting words between sentences, the sentence that says how the person
judges their work, and any figure the person confirmed and wants in. After cutting, look at the
built page, because a page count of two says nothing about a half-empty second page.

## Wording that has survived many drafts

Re-read the oldest wording in the document as if it were new. "Teams of 5 and about 15" was
written in the first hour of one engagement as shorthand, passed every fact check after, and
was caught only when the person read it (C). Familiarity reads as correctness.

## Before and after

All invented. The "after" lines show the shape; a real one uses only confirmed facts.

| Before | After | What changed |
| --- | --- | --- |
| Responsible for managing the product backlog. | Moved a fix for duplicate claims ahead of a planned feature after call data showed about 400 duplicate lodgements a month. | A duty became one decision with its reason |
| Lead discovery using data. | Rewrote the lodgement questions with 6 assessors so that customers answer them in the order assessors need them. | Bare present verb became something that happened |
| Managed a team. | Scope: "I led 12 assessors handling motor claims." Bullet: "Coached 3 assessors into senior roles." | Scale went to the scope line, the outcome to a bullet |
| Delivered the new claims system. | Prepared the team for a new claims system, including guidance and training for 12 people. | The verb matches what the person did |
| Improved customer experience. | `[what changed for customers, and how it was measured?]` | No fact was supplied, so the gap is asked about |

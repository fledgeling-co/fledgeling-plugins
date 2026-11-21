# Voice, verbs and cutting

Read this when drafting or reviewing sentences. **R** marks a default from the research, **C**
one from a recorded correction; `evidence.md` has the source for each.

The sections run in the order a draft is built: who the sentence is about, what is true, what
makes it worth reading, and how to keep it plain. Many examples come from one engagement, a
product owner in a bank, and from invented people; the rule is the part that carries, so read
each example for its shape and write the person's own field.

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

## Asking what a fact was for

Using what an answer implies is half of it. The other half is asking for what it leaves out,
because the part a person does not think to say is often the part worth printing. Each bare
fact has an obvious next question:

| The fact as given | Ask | What the answer gives the résumé |
| --- | --- | --- |
| An award or recognition | What was it for? What did you do that it recognised? | The achievement behind the award, which is stronger than the award |
| "I was promoted" or a move to a bigger role | What were you asked to take on, and why you? | A reason the employer trusted them with more |
| "I led a team of N" | What was different by the time you left? | A bullet in place of a headcount |
| A project name | What did it change for customers or staff? | A result, or a scope if nothing was measured |
| A tool or method | What do you use it for, and how often? | A skill with a line under it |
| "It went well" or "it was adopted" | How could you tell? | A measure, or an honest "nothing was tracked" |
| A change they made | What was it like before? | The contrast that makes the change readable |
| A bullet that stops at the action | What was different afterwards? | The second half of the bullet, or its scale if nothing was measured |

Ask these when you first meet the fact, not at the end. Write the line with what is known
meanwhile, and leave a red placeholder where the answer will go ("…under one way of working,
which `<what changed as a result>`"), so the draft shows what it is waiting on.
A reply that says "the award line is thin because nobody has said what the award was for" is
doing its job; a résumé that prints the bare line without asking has skipped a step (C).

## Selling what is true

Every rule above this one guards against saying too much. Applied alone, they produce bullets
that are correct and lacklustre: one person's reviewer said the achievements "don't really sell
her abilities", and the person agreed (C). Understating is a failure too. The reader is deciding
whether to meet this person, and a flat line gives them no reason to.

The facts are fixed. What you choose is which fact leads, what stands beside it, and where the
sentence ends.

| Move | Flat | Stronger, same facts |
| --- | --- | --- |
| Lead with what mattered, then how | "Coordinated an update to how staff verify customers and secured agreement between two teams." | "Secured agreement between the business and risk teams, the hardest part of an update to how staff verify customers." |
| Put the scale beside the action | "Recommended stricter performance measures for suppliers." | "Recommended stricter performance measures for suppliers on contracts worth more than $X a year." |
| Say what was at stake | "Prioritised closing access conflicts ahead of a new request." | "…in a high-risk role, where the data showed the same people could start and approve a transaction." |
| Say why it was hard | "Got two teams to agree." | "Got two teams with opposite concerns, speed for customers and control for the bank, to agree." (only if the person said so) |
| End on the effect, not the admin | "…agreed who owned what, and tracked it in a ticket." | "…agreed who owned what, which `<what happened next>`." |
| Let a supporting verb carry its own result | "Supported the rollout to 3,500 staff." | "Supported the rollout to 3,500 staff through the process change that gave them a simpler way to do X." |
| Own what was theirs | "Measures were recommended and adopted." | "Recommended the measures. They were adopted." |
| Order by strength | Strongest story third | Strongest story first |

**The limits, which do not move.** The verb is the one the person confirmed: a rollout they
supported is still supported, told with its effect. Every figure is theirs. A result is stated
only if they gave it; where the strong version needs a fact nobody has supplied, leave a red
placeholder and ask. No adjective does the selling: "successfully", "significant" and
"key" are claims with nothing under them, and the reader discounts them.

**The test.** Read the bullet as the hiring manager and ask "so what?". If the bullet answers
it, it is selling. If the answer is in the person's sources and not in the bullet, move it in.
If it is in neither, ask them.

## Ranking the detail

Selling what is true adds stakes and scale. Left unchecked it also adds words, and a bullet
with a point and four supporting facts reads as five facts. One person's reviewer put it as
"sometimes the use of detail reduces the apparent impact of the achievement" (C). Every detail
in their bullets had gone in for a reason, one at a time: a term an ad required, something the
person asked to include, a proof a reviewer wanted. Nothing had ranked them.

Rank them. In a bullet, in this order of value to a reader deciding whether to meet the person:

1. **What changed**, for customers, staff or the organisation.
2. **What was at stake**, or why it was hard.
3. **How big it was**: people, users, money, releases.
4. **Their part**, where it is not already in the verb.
5. **How it was done**: the method, the evidence used.
6. **With what**: tools and systems.
7. **Process words**: the stages a piece of work went through, the artefacts it produced.

Build each bullet from the top of that list:

- **The first sentence is the headline**: the verb, the thing and, where it fits, item 1, in
  about 30 words or fewer.
- **Add one supporting fact**, the highest-ranked one available that the headline does not
  already carry. A second sentence is for a result, never for more method.
- **Items 5 to 7 go unless they are the point.** A method an ad asks for can be the point of
  one bullet; a tool belongs on the tools line; process words belong in the scope line.
- **A list of three or more items inside a bullet is a sign** that detail has not been ranked.
  One list is sometimes right. Two is a paragraph pretending to be a bullet.
- **Do not repeat the scope line's scale** in the bullets under it.

**Numbers are ranked the same way, and more strictly.** A figure draws the eye, so a weak one
does more damage than a weak phrase. Keep a number when it is one of these:

- a scale that is large for the kind of work: users, staff affected, seats, money;
- a result: what fell, rose or was reached;
- an exact count of something difficult, where the count is the achievement.

Take it out when it is one of these, and say the thing without it:

| The figure | Why it shrinks the line | Write |
| --- | --- | --- |
| A range: "5 to 10 changes" | Reads as not knowing, and as few | "the channel's changes" |
| A small team or squad size: "a 12-person squad", "5 direct reports" | Sizes the person by a small number | "a squad", "my team"; keep a team size only where leading people is the point and the number helps |
| A duration: "over about 6 months" | Says how long it took, which is rarely to anyone's credit | Leave it out unless speed was the result |
| A count of faults or misses: "8 issues reached production" | Leads with the failure | "every issue that reached production was fixed within 2 weeks" |
| A second, smaller figure beside a large one: "3,500 branch staff and 200 operations staff" | The small one dilutes the large one | "more than 3,500 branch and operations staff" |
| A count of routine units: "in 5 planning increments", "2-week sprints" | Process detail wearing a number | Name the method without the count |

The test for every figure: read the sentence with it and without it. If the reader's picture
of the person is no bigger with the number in, it goes. A figure the person has asked to keep
stays, and you tell them what it is costing the line (C).

Some detail is there by decision: a term the person asked for, a required phrase on the keep
list. Ranking does not delete those. It moves each to the least prominent place where it is
still true, a scope line, a skills line or a shorter bullet, and where it has nowhere to go,
you tell the person which term lost its place and let them choose.

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

## One reading only

Read each sentence looking for a second meaning, the way someone who does not know the work
would take it. Where there is one, say who did what and in what order (C).

| Trap | Reads as | Write |
| --- | --- | --- |
| A second verb after "use X to…": "I use the tool to draft test cases, and validate the output" | The tool validates | "…to draft test cases, then validate the output myself" |
| A step with no order word: "drafted the plan and got approval" | Possibly one act | "drafted the plan, then got approval" where the order matters |
| A modifier beside the wrong noun: "an update to how staff verify customers over six months" | Customers are verified over six months | "Over six months, coordinated an update to how staff verify customers" |
| A pronoun with two candidates: "added a check after the worst issue; it came from outside the team" | The check came from outside | Name the noun again: "the issue came from…" |
| Numbers joined loosely: "teams of 5 and about 15" | One team of an odd size | One team at a time, or the one that matters |
| A list whose last item changes kind: "led planning, reporting and five analysts" | Three activities | Split it: what they led, then whom |
| A lost subject after "when…": "When the data showed a gap, closed it" | Nobody closed it | "Closed the gap the data showed" |

Order words (then, first, afterwards, before) and a repeated subject cost a word or two each.
They are not padding; they are what makes the sentence say one thing.

## Words that tell the reader nothing

A phrase earns its place by telling this reader something they did not know. Take it out and
re-read; if nothing is lost, leave it out. The usual kinds:

| Kind | Example | What to do |
| --- | --- | --- |
| A gloss on something known | "Microsoft Copilot, an AI assistant"; "Excel, a spreadsheet tool" | Name it and move on |
| A gloss added to carry a keyword | "…, an AI assistant" where the ad says "AI" | If the term matters, write a true sentence that uses it; otherwise leave it out |
| A category before the thing | "the Jira tool", "the Scrum methodology" | "Jira", "Scrum" |
| The title or employer restated | "In my role as Product Owner, I…" under a Product Owner heading | "I…" |
| A purpose nobody doubts | "in order to deliver outcomes", "to add value" | Cut, or say the actual purpose |
| An intensifier or hedge | "successfully delivered", "various stakeholders", "a range of" | The verb or the noun alone, or the number |
| A second word for the same thing | "validated and reviewed", "plans and schedules" | Whichever one the person used |

This is a test of each phrase, not a reason to shorten. A gloss on an internal name, a
connecting word and the sentence with a person in it all tell the reader something, and stay.

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
- Explain nothing the reader already knows. Before glossing a name, ask whether the person
  hiring for this role would recognise it. Widely used products, well-known companies and
  standard methods need no gloss: Excel, Jira, Microsoft Copilot, Scrum, a major bank (C).
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

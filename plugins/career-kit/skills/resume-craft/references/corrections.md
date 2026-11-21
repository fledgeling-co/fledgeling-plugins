# Corrections, and how far each one reaches

Read this before acting on feedback, a reviewer's finding or one of this skill's own rules.
Each row is a correction a person made to a draft, with what it forbids and what it leaves in.
The second column is the rule. The third is what an over-correction would remove, and has
removed. `evidence.md` has the source for each.

## The pattern

A correction is aimed at a form: a number, a list, a title, an incident. The content that form
was carrying is usually still wanted. Three things go wrong when that is missed:

- **The rule spreads.** "No count of years" turned into "say nothing about tenure".
- **Corrections stack.** Each one removes a little, and after four the paragraph passes every
  rule and says nothing the person would recognise as them.
- **A number does the editing.** A word range or a bullet count is met by deleting whatever is
  easiest to delete, which is the connecting words, the one human sentence, or the bullet that
  backed a requirement.

So, for every correction: name the fault narrowly, keep what the text was for, recast before
cutting, and re-run the section's test afterwards.

## What each correction forbids and leaves in

| Correction | It forbids | It leaves in, and wants |
| --- | --- | --- |
| No count of years | The number, as a headline ("20+ years") | The span and breadth of the career, in words; the true dates |
| "It reads as a laundry list" | Role after role with a headcount each | The range of the career, in one clause, most recent first |
| "The summary is not in reverse order" | Oldest-first telling in the summary | The earlier career itself |
| "Too specific" (an incident in the summary) | One occasion standing for how they work | The judgement behind it, as a standing sentence; the incident as a bullet |
| "Written as a plain fact" (title and statistic) | A label and a number about the product | The title, riding along; the figure, attached to their responsibility |
| "That is not a skill" | A noun they work with | The ad's term, inside an ability that a bullet shows |
| "Each skill needs a line that shows it" | A skill with nothing under it | The skill's general wording; the proof is found by reading down, not written into the skill |
| "Leave missing information as red text in angle brackets" | Stating the bare fact and hiding that more is wanted; a question list the draft does not point to | The sentence, written so the answer drops in; no placeholder on any copy sent to an employer |
| "It will be judged against the research, so abide by it" | Departures from the research that nobody chose | Departures the person chose, each listed with whose decision it was |
| A scope paragraph that grew to three sentences to keep things the person wanted | Growing the scope line | Everything it held: the extra duty as a bullet, the tool use as a bullet or on the tools line |
| "It sounds like the tool is doing the validating" | A sentence with a second reading | Its content; the order word or repeated subject that fixes the reading is not padding |
| "People know what that is; defining it is fluff" | A gloss on a name the reader already knows, and any word that tells them nothing | Glosses on internal names; connecting words; the term itself |
| "The skill should have asked what the award was for" | Printing a bare fact and stopping | The fact, as given; a question to the person for what it recognised and their part in it |
| "It is impersonal and rigid" | A record-style sentence where the person has a stake | The fact, unchanged; one plain sentence of pride, reason or judgement tied to a specific thing |
| "Would we have told you that if it were not true of her?" | Holding back the plain implication of the person's own answer | Asking about anything it would take a second fact to know |
| "It reads like a list to tick off from the job ad" | Entry requirements leading the skills; labels taken from the ad | The ad's terms, in the roles and in one craft line; the person's own strengths, first |
| "More general" | This job's detail inside a claim | Whatever is distinctive about the person; general is not generic |
| "That skill is too specific" | This job's product, system or data named inside a skill | The ability, stated so it carries to another role; the instance, in a bullet |
| "Those were not promotions" | The word and the count | The moves, stated as moves, and the titles and dates |
| "Do not dwell on that old role" | Bullet space for it | Its scope line, its scale, and its place in the summary's span |
| "Be more concise" | Words that repeat or decorate | Connecting words, the sentence with a person in it, confirmed figures |
| Three to five bullets | A sixth bullet that repeats another | A bullet for each required item the summary or skills name, even if that makes six |
| 60 to 90 words | Padding and a second telling of the career | All four parts of the summary |
| No first person (a rule since withdrawn) | Nothing: it was the reviewer's rule, not the person's | First-person paragraphs |
| "Do not write for a keyword search" | A term that is there only because the ad uses it | The ad's phrase where it is true, once, in a sentence that shows it |
| Scope verbs are fixed | A stronger verb | The work itself; "supported" is still worth a bullet |
| A restricted figure stays off public copies | The figure on those copies | The figure on the internal copy, and the work it measured everywhere |

## Over-corrections found on audit

One engagement's drafts were audited for this after the person asked. Each row is something
that was removed or bent to satisfy a rule, a reviewer or a lint warning, and that should have
stayed.

| What was done | The rule it was done for | What it cost |
| --- | --- | --- |
| A skills label became "Agreement" in place of "Influence" | Labels are not copied from the ad | The accurate word, which was also the person's own |
| "I was part of the project team that received…" | Every sentence is about the person | A claim of team membership nobody had confirmed |
| "I write the user stories and acceptance criteria" was cut from the role | The lint's told-twice warning | The role evidence for an item the summary claims |
| A method's name the person had asked for by name was dropped | Scope line under about 35 words | A standing decision, and the ad's exact term |
| "Sequencing", "trade-offs", "milestones, risks and issues" disappeared | Do not write for a keyword search | Required phrases the person holds and had confirmed, each of which had a true context |
| A dependencies bullet was cut | Three to five bullets | The only line showing a required item |
| The summary fell to one past job | "It reads as a laundry list" | The breadth of a long career |
| Tenure went unmentioned | No count of years | The span, which is the difference |
| Each skill was rewritten to describe a bullet | Each skill needs a proving line | The skill's general form |
| The skills were stripped to what any holder of the title does | "Make it more general" | The person's strengths |
| An award the person had listed as theirs was written as a bare fact about a project | A rule about form never licenses a new claim | The plain implication of their own answer, and the one warm sentence in the section |

The common cause: the most recent instruction was treated as the only one. Earlier decisions,
the research's requirements and the section's job were not re-checked after each change.

## After a correction

1. Re-read the section against its job in `sections.md`. For a summary that means all four
   parts are present: the responsibility, the required items, the difference, the judgement.
2. Ask what the reader no longer learns that they learned before, and whether they still need
   it.
3. Check the other sections for the same fault and the same over-correction. A rule applied to
   one section usually applies to the others.
4. Tell the person what you removed and what you kept in another form, so they can say if the
   line was drawn in the wrong place.
5. Check the person's standing decisions and the ad's required phrases are all still there
   (`resume_lint.py --keep terms.txt`).
6. Add the correction to the table above, with both columns filled in.

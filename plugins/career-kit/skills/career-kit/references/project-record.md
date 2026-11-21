# The project record

Two files, written so a later session continues without the person answering anything twice.

## `CLAUDE.md` — the working rules

Only what a model cannot infer from the repo:

- **The rules for the copy**, stated as rules, with the reason attached. These come from the
  person's own corrections and outrank general advice — say so, or the next session will
  "improve" a sentence back to the version they rejected.
- **How to build** — the servers to start, the script per output, what each one prints, and
  what must be checked after.
- **Privacy** — what is in these files, what may not appear publicly, what must be stripped
  before text goes to an outside model, and what needs the person's say-so.
- **How reviews are run** — which skill, which runner, where briefs and answers are saved.
- **Open work**, numbered.

## `PROJECT-NOTES.md` — the facts and the history

- **Who and what**: the person, who relays for them, the goal, the target roles.
- **Confirmed facts**, with the file that holds each round of their verbatim answers.
- **Standing decisions and the keep list**: every term they asked for, wording they approved
  or rejected, what stays off public copies, and the path of the keep file the lint checks.
- **Departures from the research**, each with the research's figure, the document's figure
  and whose decision it was.
- **Still to confirm**, as a numbered list that gets struck through rather than deleted, with
  the date and the words that settled each one.
- **Decisions**, as a table: decision, outcome, basis. The basis is what stops the next session
  re-litigating it.
- **Pushback and corrections**, in the person's own words. This is the section a summary loses
  and the one that prevents the most rework.
- **Where things are**: a path table.
- **How the tools behaved**: ports, which script does what, what broke and the workaround, what
  is in `/tmp` and will not survive a restart.
- **Not done**, honestly, including anything nobody has looked at.

## Writing it

A stage that produced a deliverable appends its own section the same day, with the date in the
heading. Several agents appending to one notes file each need to re-read it immediately before
writing and append only.

Length matches the content. The decisions table and the corrections section are worth every
line; a summary of what the file just said is worth none.

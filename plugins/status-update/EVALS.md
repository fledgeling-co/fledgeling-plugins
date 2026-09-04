# EVALS

**No comparative eval run happened.** This skill ships without one, and that is worth stating
plainly at the top rather than leaving the section to imply a benchmark that was never run.

The skill was built in a session whose budget went on mining the corpus and authoring the
templates. The honest position is: the mechanism is verified, the design is grounded, and the
claim that these pages beat a chat status update is untested.

## What was verified mechanically

Ten checks, each proving one guard actually fires. A gate that cannot fail is not a gate, so
the self-test asserts both directions — well-formed data passes, and each specific defect is
caught.

```
$ python3 scripts/render.py --self-test
  pass  a well-formed file passes
  pass  a missing project name fails
  pass  an unknown state word fails
  pass  a non-list tasks field fails
  pass  an unknown check state fails
  pass  a check over zero counts is forced to unmeasured
  pass  an alarm that caught nothing is forced to unarmed
  pass  an invalid roadmap item fails
  pass  a non-object estimate_remaining fails
  pass  a dashboard row derives next round and time range
  pass  project-template.html has a data block
  pass  dashboard-template.html has a data block

12 of 12 checks passed
exit 0
```

End-to-end, against a throwaway portfolio root with two projects: both project pages
rendered, both rows derived, the dashboard rebuilt from scratch by rescan, and the derived
row verified to carry the right task counts, defect counts and six rectangular gate cells
with worst-state-wins collapsing.

**One guard caught a real defect on its first run.** The sample data authored for the
templates claimed a check had passed (`state: "done"`) over counts of `0/0`. The renderer
forced it to *nobody checked this*. That is the exact error the corpus shows being made and
retracted later, and it was present in this skill's own fixture.

## What was not run, and what would settle it

The comparison that matters is: given the same finished piece of work, does a developer get
more from the page than from the chat message? Three tasks would settle it, and none were
run.

1. **Skill against no skill, same prompt.** Take three real end-of-work moments from the
   corpus, run each with and without the skill, and ask which output answers *what needs me*
   and *what is stuck* faster. The no-skill baseline is a long chat message, which is the
   honest comparison.
2. **Does the trigger fire?** The description is written to catch "where are we", "what's
   left", "how did that go" and an unprompted end-of-work summary. Twenty queries, half
   near-misses, would measure whether it triggers when it should and stays quiet when
   another skill owns the job — `ship-armada` for planning, `armada-sync` for the manifest.
3. **Does the derived row stay honest?** Run the skill across a dozen projects with
   deliberately awkward data — no checks, no tasks, a project renamed mid-flight, a coverage
   axis with no denominator — and confirm the dashboard shows absent, empty and zero as three
   distinct states rather than collapsing them.

## What the design rests on instead

Not an eval, but not nothing: every zone traces to a counted occurrence in 2,400 real status
reports across 27 projects, and the two data corrections trace to specific errors observed
being made and retracted. The counts, the clustering method and its ±15% leakage are in
`skills/status-update/references/evidence.md`.

The weakest link there is declared in that file too: the independent critic meant to walk all
634 concerns against the final twenty zones stalled mid-run and was killed, so zone selection
and the 80% coverage figure are self-reported by the pass that produced them.

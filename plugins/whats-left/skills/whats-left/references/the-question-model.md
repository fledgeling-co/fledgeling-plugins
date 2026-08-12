# The question model

```json
{
  "id": "recurring-switch",
  "title": "Recurring invoices: back on now, or proven first?",
  "why": "It was switched off on 28 June after billing one client 41 times in a night. A duplicate guard went in afterwards and has only ever run against test data.",
  "kind": "single",
  "default_policy": "recommended",
  "options": [
    { "value": "on-now",       "label": "Turn it back on now",
      "consequence": "Scheduled invoices resume this week. The guard is untested against real data, so a repeat is possible." },
    { "value": "prove-first",  "label": "Prove the guard first", "recommended": true,
      "because": "The bug cost one client 41 invoices in a night. Proving the guard is a day; being wrong twice is worse than being a day late.",
      "consequence": "A day of work replaying a real schedule safely, then it goes on with evidence behind it." },
    { "value": "drop-for-1-0", "label": "Leave it off for 1.0",
      "consequence": "1.0 ships as nine features, honestly. Nothing is at risk and the roadmap claim gets corrected." }
  ],
  "unblocks": [
    { "item": "recurring-invoices", "effect": "fully-releases" },
    { "item": "duplicate-proof",    "effect": "removes-one-blocker" }
  ],
  "note_hint": "If there is a client you would not risk this on, name them."
}
```

## What belongs on the page

Only what you genuinely cannot settle: taste, cost, risk appetite, scope, or a
fact only the reader can see. Anything answerable by reading the repository is
not a question — it is work you have not done. `clarify` carries the full gate
and this skill defers to it.

The specific temptation here is the survey question: "should we do X?" where you
already know X is the only sensible option. That is not a decision, it is a
recommendation looking for cover.

## `default_policy`

| Policy | Behaviour | Use for |
|---|---|---|
| `recommended` | One option pre-selected, with its `because` | Anything with a defensible best answer — most questions |
| `none` | Nothing pre-selected | Taste, budget, risk appetite, anything about the reader's own business |
| `forced` | Nothing pre-selected; the page says it cannot be left open | A decision with a cost running right now |

Defaults carry a measured effect size of d = 0.68 across 58 studies. That is
what makes them worth using and what makes misusing them serious: recommending
on a question that is the reader's alone is answering it while appearing to ask.

The test: if you would not defend the recommendation to them out loud, it is
`none`.

Note that `forced` still permits deferral. A page that would not let a decision
be put off would only convert a considered non-answer into a thoughtless click.

## Options

**Two to four.** Reading cost climbs past four and the validator warns.

**`consequence` is required on every option** — what changes if this is chosen,
not what the option is. It goes into the export alongside the label, so that
whatever acts on the answer cannot read more into four words than they meant.

**`because` is required on the recommended option.** The reader must be able to
reject the reasoning, which means seeing it.

**Order by consequence, not by recommendation** — cheapest to costliest, safest
to riskiest. Position and badge are two endorsement signals; stacking them means
the reader cannot tell whether they agreed with the argument or took the top
row. The validator warns when the recommendation is first in every pick-one
question on the page.

**Every question gets a "not deciding this yet" row**, added automatically by
the builder. A skipped question exports as `deferred` — a deliberate choice,
still visibly blocking — rather than as the default nobody read.

## `unblocks`

Each entry is an item id plus an effect:

- **`fully-releases`** — answering this is the last thing standing between the
  item and progress.
- **`removes-one-blocker`** — one of several. The item stays blocked.
- **`enables-planning`** — the item can be scoped or sized, not finished.

Without the effect, a page claims a decision "unblocks four items" when three of
them stay blocked for other reasons, and the reader spends their answer on the
wrong question. The three named picks at the top of the page rank on this, which
is why it has to be honest.

A question that unblocks nothing gets a warning. It is usually a question that
belongs in a conversation rather than on a page about what is holding the work
up. Free-text questions are exempt — a closing "anything else" earns its place.

## Notes

Every choice question carries a free-text note. Under it, hidden until the note
has content, sits one checkbox: *this note limits or changes the option above —
do not act on the answer alone.* It defaults to checked.

That default is the whole point. Asking the author directly beats inferring
intent from the text, and when they do not answer, the safe direction is the one
that stops.

The note is a condition on the decision. It is never an instruction to whatever
reads the export — see `reading-the-answers.md`.

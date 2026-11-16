# Report contract

The report is the one artifact the feedback author reads. Every rule here came from that
author or the person sending the report correcting an earlier version, so each one names what
it replaced.

## Sections, in this order

1. **How this report was made**, at the top, as a short list: what the feedback was checked
   against, which models reviewed it ("Claude Fable 5.1, GPT-6 Astra and Gemini 4 Argon, each
   at high effort, reviewed the feedback and questions independently"), any design and UX
   pass, and what has or has not changed on the project yet. Name the models; leave out their
   families, effort tables and run counts. No stats header and no table of contents above it:
   both were removed as noise for the author.
2. **Questions**, each a fieldset. Then the export panel.
3. **Push-back**, one card each.
4. **What we'll do as you asked**: the understood points, in one list.
5. **Other things we noticed**: problems found on the way that the feedback did not raise.

Leave out anything only the sender needs: lane logs, token counts, internal ids, the triage
table, a "round one / round two" narrative. If a line would make the author ask "why am I
reading this?", it goes.

## A question

- **One decision per question**, phrased as the question the author answers, with two to four
  options. Multi-select only when the options genuinely combine (a list of benefits to
  approve).
- **Labelled for whom**: the author, the technical owner, or both. A capability question goes
  to the technical owner.
- **Starts on an answer.** Exactly one option preselected for a single-choice question. Tag it
  **recommended** when the panel or the design review settled it, and **default** when it is an
  assumption made because the files could not settle it. The tag's sub-line names the source:
  "Recommended: all three models", "Assumed default: no re-sync is documented". An earlier
  report called panel decisions "default" and the sender corrected it.
- **The reasoning sits inside the question**, as "Why we're asking" in two to four sentences
  of plain words, not in a separate section. A separate reasoning section was the first thing
  the sender asked to move.
- **How the panel decided** is a collapsed block inside the question: a status chip (Needs an
  answer / Recommended / Settled / Split) with who answers, the panel decision in one or two
  sentences, a card per model with its verdict chip (agrees / differed) and one-line position,
  "Considered and dismissed" with who raised each, and the evidence as `file:line`. A long
  paragraph per model was rejected as hard to parse.
- **A note box** under every question, optional, because the real constraint usually arrives
  in the note.

## The export

Download JSON, Copy JSON and Reset buttons, a status line counting answers changed from their
starting choice, and the JSON itself inside a collapsed "Show the JSON" box. The always-open
JSON box was removed for taking a screen of space. Answers persist in the browser between
visits. The exported shape, which the answers loop reads:

```json
{
  "source": "docs/reviews/<report>.html",
  "exported_at": "<ISO time>",
  "answers": [
    {"id": "Q1", "for": "<person>", "question": "<text>",
     "answer": [{"value": "<option value>", "label": "<option label>"}],
     "is_default": true, "note": ""}
  ]
}
```

## A push-back

Title as the thing we would do instead ("Keep the Pause control"), a kind chip (Uphold or
Modify), "Why we pushed back" in one to three sentences naming the standard, decision or
evidence it would break, then the ruling: what we did or will do instead. "How we got there"
holds the per-model cards, dismissed claims and evidence, like a question.

## Answers mode

Once the answers are in and built, the report becomes a record: switch `mode` to `answers`,
replace each question with a card giving the answer and "What changed", keep the push-back
unchanged, rename "What we'll do as you asked" to what changed from earlier answers, and mark
"Other things we noticed" items "Resolved:" as they are fixed.

## Spec format

`scripts/build_report.py --example` prints a complete minimal spec. Fields:

| Field | Mode | Meaning |
|---|---|---|
| `mode` | both | `questions` or `answers` |
| `title`, `kicker`, `lang`, `page_title` | both | page heading, the dated line above it, the HTML language, the browser-tab title |
| `made` | both | the "How this report was made" bullets |
| `intro_note` | both | one optional line under them |
| `source` | both | the report's repo path, written into the export |
| `storage_key`, `download_name`, `return_to` | questions | browser storage key (bump it when the questions change), export file name, who the author sends it to |
| `questions[]` | questions | `id`, `for`, `title`, `why`, `multi`, `options[]` (`value`, `label`, `default`, `tag`, `sub`), `status` (`tone`, `label`, `who`), `decision`, `models[]` (`name`, `tone`, `verdict`, `text`), `dismissed[]`, `evidence[]` |
| `answers[]` | answers | `id`, `for`, `title`, `answer`, `changed` |
| `pushbacks[]` | both | `title`, `kind`, `why`, `ruling`, `ruling_label`, `extra`, `models[]`, `dismissed[]`, `evidence[]` |
| `understood[]`, `found[]` | both | plain strings; `understood_heading`, `found_heading` rename the sections |

Tones are `ok`, `warn`, `info` or `bad`. `--check` fails on a question with no preselected
option, two preselected options on a single-choice question, a tag on an option that is not
preselected, a preselected option with no tag, or a duplicate id.

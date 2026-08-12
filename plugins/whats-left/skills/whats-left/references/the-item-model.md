# The item model

Ten required fields per item, plus two optional. Each answers a different
question, and an item that repeats itself across two fields has one field doing
no work.

```json
{
  "id": "recurring-invoices",
  "title": "Recurring invoices",
  "group": "Built, but not running",
  "urgency": "urgent",
  "stage": "built",
  "plain": "Invoices that go out on a schedule. The roadmap says it shipped; it has been switched off in production since late June.",
  "state": "Written and merged. Switched off on 28 June after it created 41 duplicate invoices for one client in a night.",
  "live": "Off. The production settings disable it, so no scheduled invoice has gone out since 28 June.",
  "evidence": "`config/production.json` disables it, and the comment beside the flag dates the incident.",
  "owner": "you",
  "from_you": "Whether it goes back on now, or stays off until the guard is proven against real data.",
  "remaining": "Switching it on is one line. Proving the guard first needs a safe way to replay a real schedule — a day.",
  "blocked_by": "recurring-switch"
}
```

## The fields

**`plain`** — the whole report for a reader who has never opened the repository.
One sentence, under forty words. No file names, no directory paths, no
camelCase, no CONSTANT_NAMES, no bare ticket numbers; the validator rejects all
of them. This is not a style rule. A line carrying `src/recurring.ts` has
stopped being a plain-English summary and become a second copy of `state`.

Where the documentation and the code disagree, `plain` says so. That
disagreement is usually the most useful sentence on the page.

**`stage`** — one of:

| Stage | Means |
|---|---|
| `not-started` | Nothing exists yet |
| `in-progress` | Being written; incomplete |
| `built` | Written and merged. **Not running** |
| `tested` | Built, and exercised somewhere that is not production |
| `deployed` | Running on the live system |
| `accepted` | Running, and someone has used it in anger |
| `blocked` | Cannot proceed; the reason is in `from_you` or `remaining` |
| `unknown` | You cannot see it from here. Say why in `meta.unknowns` |

Never a percentage. `deployed` and `accepted` require `evidence`; the validator
errors without it, because a completion claim nothing can back is exactly the
claim that costs the reader something.

**`state`** — where it got to, in the reader's terms. History and the thing that
went wrong. This is the field that carries dates and incidents.

**`live`** — what is genuinely true in the running system right now. Never one
word. "Off" alone tells the reader nothing they can act on; "Off. The production
settings disable it, so nothing has gone out since 28 June" does. The validator
warns on `yes`/`no`/`live`/`n/a`.

**`evidence`** — the locator. What you read, and what it said. Backtick spans
render as code. Required on `deployed` and `accepted`; strongly worth writing
everywhere else, because it is the field that lets the reader disagree with you.

**`owner`** — `you`, `agent`, or `someone-else`. An item owned by `you` with no
`blocked_by` gets a warning: the reader cannot act on it from this page, which
means either the question is missing or the owner is wrong.

**`from_you`** — what specifically is needed from the reader. If the answer is
"nothing", the owner is not `you`.

**`remaining`** — what happens after the decision, with a real size on it. "One
line" and "a day" are useful; "some work" is not.

**`urgency`** — `urgent`, `high`, `medium`, `low`. Urgent means something is
being lost right now, not that it is important. Most things are not urgent, and
a page where everything is urgent has ranked nothing.

**`group`** — free text, and it is the page's structure. Group by what the
reader has to do about the items, not by subsystem. Groups that have worked:
"Built, but not running", "Waiting on a decision", "Not started", "New — raised
on the call, on no roadmap", "Genuinely done".

The last group matters more than it looks. A page listing only what is wrong
misrepresents a project that is mostly working, and the reader stops trusting
it.

**`blocked_by`** — a question id, or a list of them. The validator errors if the
question is not on the page. Half a link graph is worse than none: it tells the
reader something exists to answer and gives them nowhere to answer it.

## Features raised in conversation

Anything the session discussed that no roadmap tracks belongs on the page, in
its own group, with `stage: "not-started"` and honest sizing. These are the
items most likely to be lost, because nothing else in the project records them.

Say where each came from — "raised on the call of 11 August" — so the reader can
tell it apart from something they already agreed to.

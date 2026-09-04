---
name: status-update
description: >-
  Report status as two living HTML pages instead of a long chat message. Use this whenever
  you would otherwise write a status update, progress summary, or end-of-work report in a
  ~/Dev project — after shipping a feature, finishing a fleet or wave, running a test
  campaign, closing gaps, completing a review, or when someone asks "where are we", "what's
  left", "how did that go", "give me a status update", "what shipped", or "update the
  dashboard". It writes one data file per project, renders that project's STATUS.html and
  the portfolio dashboard at ~/Dev/STATUS.html, opens the page, and replies in two lines.
  Use it even when the request sounds like it wants prose — the page is the report, and the
  chat message is a pointer to it. NOT for planning work (use ship-armada or ship-fleet),
  and NOT for the ARMADA.md manifest, which armada-sync owns.
---

# Status update — the page is the report

A status update written into chat is read once and then scrolls away. The same content as a
page is still there tomorrow, and the portfolio dashboard beside it answers the question the
chat message never could: how does this project compare to the other twenty-six.

So the deliverable here is two files and a two-line reply, never a wall of prose.

You write **one** file — `<project>/.status/project.json`. Everything else is derived from
it by `scripts/render.py`: the project's own `STATUS.html`, its row in
`~/Dev/.status/portfolio.json`, and the portfolio dashboard at `~/Dev/STATUS.html`. Deriving
the dashboard row rather than writing it twice is what stops the two files disagreeing, and
drift between them would be invisible until someone read both.

Deliver exactly that. Do not also paste the report into chat, and do not expand this into a
portfolio survey — that belongs to `ship-armada:ship-armada`.

## Protocol

1. **Identify the project.** Walk up from the working directory to the child of `~/Dev`.
   If you are in `~/Dev` itself, ask which project rather than guessing.

2. **Read the existing data** at `<project>/.status/project.json` if it is there. You are
   updating a record, not starting one, and the fields you have no news about keep their
   previous values.

3. **Gather the delta from what you already know.** This session is the primary source. Top
   it up cheaply with `git -C <project> log --oneline --since=<the file's updated stamp>`
   and `git -C <project> status --porcelain`. Open other files only where you have reason to
   think a specific field changed.

4. **Write `<project>/.status/project.json`.** The full field list is in
   `references/data-contract.md`; read it before your first write in a project. Every field
   is optional except `project`, `updated` and `verdict`, and a field you have no honest
   value for is left out rather than filled with a zero — the pages render "not reported"
   and "nobody checked this" as distinct states, and both are more useful than a false zero.

5. **Render and sync**, which does the project page, the row and the dashboard in one call:

   ```bash
   python3 <skill>/scripts/render.py sync <project>
   ```

   It prints the two file paths and whether the row was added or updated. It also prints any
   corrections it made to your data — read those, because each one means the page now
   disagrees with what you wrote, and the reason is in step 7.

6. **Open the project page**, since showing the result is the point:

   ```bash
   open -a "Google Chrome" <project>/STATUS.html
   ```

   Open `~/Dev/STATUS.html` as well when the work spanned several projects, or when the
   person asked about the portfolio rather than this project.

7. **Reply in two lines.** The first says how it went and points at the page. The second
   names anything that needs the person — a decision, a credential, a blocked task. If
   nothing does, say so. Everything else is on the page, and repeating it in chat is the
   habit this skill exists to replace.

   > `webhook-relay: 7 of 14 tasks finished, two checks never tested — STATUS.html is open.`
   > `Waiting on you: the staging database password, blocked since Tuesday.`

## Two things the renderer corrects, and why it overrules you

Both come from the corpus this skill was built from, where each error was made and then
retracted in a later report. The script fixes them rather than trusting the input, so the
page cannot claim something the data does not support.

- **A check that examined nothing is not a pass.** A gate with `state: "done"` and counts of
  `0/0` becomes `unmeasured`. Exit code 0 over an empty run means the check never ran.
- **An alarm that caught nothing is not armed.** An `armed` row claiming `armed: true` with
  `red: 0` becomes `false`. If deliberately breaking the code produced no failing test, that
  check is not watching anything, whatever it says.

When the script corrects you, fix the underlying data if it was a mistake. If the data was
right and the correction is wrong, say so in your reply rather than editing the page.

## What is coming next — the roadmap and estimated time

The page models what is coming next as well as what just landed, via `roadmap` and
`estimate_remaining`. Sizing is grounded in `reckon:reckon`'s measured 1,842-agent corpus across
31 repositories on this machine.

- **Never write a single point estimate.** Point estimates are wrong by a factor of three in the
  ordinary case and read as false precision. Always provide a duration range (`[p25, p90]`) with
  the median called out.
- **Four empirical task tiers**:
  - `S` (3–25m, median 8m): read-only check, small fix, 1–2 files.
  - `M` (7–56m, median 15m): 3–7 files, single subsystem.
  - `L` (14–68m, median 25m): 8–19 files, cross-seam feature.
  - `XL` (25–155m, median 45m): 20+ files, whole new surface.
- **Parallel wave duration**: `wave ≈ max(member) × 1.1` (median) to `1.8` (p90).
- **Decision work carries no duration estimate.** Waiting on a human decision or an external
  credential is not agent work — giving it an estimate prices waiting as work.
- State the basis plainly: `"measured rates (reckon 1,842-agent benchmark)"` or this project's
  own recorded throughput.

## Writing for the reader, not for yourself

The pages are read by someone who does not know this codebase — a colleague, a founder, or
you in six months. `references/plain-words.md` carries the translation table the templates
were built against, and `references/data-contract.md` marks which fields are read by a
person rather than by the renderer.

The short version: the values you write into `title`, `claim`, `headline`, `reason` and
`why_not` are prose a stranger reads. Write *check* rather than gate, *problem found* rather
than finding, *version* rather than sha, *what it is waiting for* rather than what would
unblock it. The hardest jargon is not the technical-looking kind — it is ordinary words
carrying a private meaning, like *gate*, *armed*, *coverage* and *wave*, which read as
English and mean nothing to the reader.

Keep each of those strings to one clause. The page has room for a sentence and no room for a
paragraph; anything longer is silently clipped by the layout, which is worse than being cut
deliberately.

## The other commands

```bash
python3 <skill>/scripts/render.py project <dir>    # that project's page only, no dashboard
python3 <skill>/scripts/render.py portfolio        # dashboard only, from existing rows
python3 <skill>/scripts/render.py rebuild          # rescan every ~/Dev project — recovery
python3 <skill>/scripts/render.py validate <file>  # check data without writing anything
python3 <skill>/scripts/render.py --self-test      # prove the checks can fail
```

`rebuild` is the recovery path when `~/Dev/.status/portfolio.json` is lost or has gone stale:
it rescans every `~/Dev/*/.status/project.json` and reconstructs the dashboard from them. It
reports which projects it skipped and why, so a project missing from the dashboard is
visible rather than silently absent.

`--self-test` exists because a check that cannot fail is not a check. Run it once on a new
machine; ten cases should pass, and each one proves a specific guard actually fires.

## Both files are committed

`STATUS.html` and `.status/project.json` are tracked in the project's git, so the report
travels with the repo and shows up in a diff. That was a deliberate choice: it means a status
change is reviewable, and it means the history of what was claimed is recoverable when a
later report contradicts an earlier one.

Commit them with the work they describe rather than in a commit of their own — the report and
the change it reports on belong together.

## What this does not do

- **The ARMADA.md manifest is `armada-sync:armada-sync`'s job.** That file is prose for
  orchestrators to plan from; these pages are numbers for a person to read. Both after a
  substantial piece of work; neither replaces the other.
- **Planning belongs to `ship-armada:ship-armada` and `ship-fleet:ship-fleet`.** This skill
  reports what happened and does not decide what happens next.
- **Nothing here runs your gates.** It records what they reported. If you have not run a
  check this session, its state is `unmeasured` and the page says so, which is the honest
  reading and the one the corpus shows people getting wrong.

## References

- `references/data-contract.md` — every field, its type, and which page reads it.
- `references/plain-words.md` — the translation table, and the text budget per field.
- `references/evidence.md` — where the zone list and the two corrections come from.

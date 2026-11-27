# Writing an entry

Each entry is read by two people who want different things from the same piece of work. The owner, an engineer or a later agent reads the technical version to know exactly what changed and whether to trust it. A founder, customer or investor reads the plain version to know what is now possible and what is still coming. Both read the title and the subtitle, which is why those two are written for both at once.

## The title

The outcome in 10 words or fewer, on one line, stated as what is now true: "Failed deliveries now retry after a server restart", not "Retry work" or "Implemented durable retries". A reader scanning the timeline should know what changed from the title alone. No ticket numbers, no product codenames a stranger would not know.

## The subtitle

Exactly two sentences of 25 words or fewer each. The first says what was achieved; the second says what it means for someone. Both are in words the plain reader follows.

> Webhooks that fail no longer vanish when the relay restarts; they wait in a queue and retry for up to a day. Customers stop losing order notifications during our deploys.

The second sentence is the one most often skipped, and it is the one that tells a non-technical reader why they should care.

## Task

What this piece of work set out to do, before it started.

- **Plain**, 1 sentence: the problem in the reader's terms. "Stop losing webhook deliveries that fail while the relay is restarting."
- **Technical**, 1–2 sentences: the same, with the ticket, spec or branch so a reader can find it. "RELAY-212: move the retry schedule from process memory into a durable queue, on branch `feat/durable-retries`."

## Achieved

What is true now that was not before, and how we know.

- **Plain**, 1–3 sentences: what someone can now do, see or rely on. Keep a number when it means something to this reader ("In a test with 500 failed deliveries and two restarts, every one arrived"), and leave out the ones only an engineer can weigh.
- **Technical**: what works now with the numbers (tests passing, screens shipped, defects closed, latency moved) and the PR or commit. Then a paragraph that starts "How we know:" and quotes the command, gate verdict or measurement short: `pnpm test:integration --grep retry` → 38 passed. Name any check that did not run as not run. A table earns its place for real tabular data, such as several before-and-after figures; wrap it in `<div class="table-wrap">`.

Two corrections the corpus behind `status-update:status-update` found agents making and later retracting, which apply here too: a check that examined zero items is not a pass, and a test said to guard something that never failed when the code was broken has not been shown to guard it. Report each as what it is.

## Remaining

What is left, and what is waiting on the owner.

- **Plain**, 1–2 sentences, ending with anything that needs the owner's decision, credential or go-ahead.
- **Technical**: a list, one item per open task, blocked task, missing credential or decision, each with what it waits on.
- **When nothing remains**, write "Nothing remaining." in both versions and set `data-remaining="none"` on the article. The heading stays so the absence is stated, and the timeline marks the entry complete.

## Plain words

The plain version's hardest jargon is ordinary English carrying a private meaning, because it survives a proofread. Swap these (adapted from `status-update:status-update`'s `plain-words.md`, which mined them from real reports):

| Instead of | Write |
|---|---|
| gate, gate passed, exit 0 | check, passed |
| verdict | how it went |
| finding, defect | problem found |
| worktree | workspace |
| commits ahead, pushed | changes not yet shared, shared with the team |
| coverage | how much of the work is watched by tests |
| unmeasured | nobody checked this |
| blocked | stuck, waiting on something |
| in-flight | being worked on now |
| wave, run | round |
| merged | finished and added to the product |
| deployed, shipped | live for customers |
| feature flag off | built but switched off |
| p95 latency | how long the slowest 1 in 20 waits |
| migration | a change to how the data is stored |
| regression | something that used to work broke |

Meet the length budget by making fewer claims, never by compressing a sentence into a slogan. "Durability is now a first-class concern" explains nothing to the person the plain version is for; "a failed delivery is now kept and retried" does.

## Updating the newest entry

When step 2 of the procedure says to update rather than add:

1. Keep the `id`, the date line and the title's date. Rewrite the title only if it has become wrong.
2. Revise the subtitle and both versions of Task, Achieved and Remaining to the current state. They must describe the same moment.
3. Extend the timestamp line from `python3 scripts/changelog.py stamp`: `Written 27 Nov 2026 14:05 · updated 27 Nov 16:40, 28 Nov 09:10 · last updated 28 Nov 09:10`. Every time is a `<time datetime>` element with the UTC offset (`2026-11-28T09:10+11:00`). The page shows an "Updated" tag on any entry with more than one time.
4. Set `data-remaining` to match the new Remaining.

## A complete entry

From `assets/example-changelog.html`, whose entries are synthetic:

```html
<article class="entry" id="2026-11-24-signing-keys-rotate" data-remaining="none">
  <header class="entry-head">
    <p class="entry-date"><time datetime="2026-11-24">24 November 2026</time></p>
    <h2><a href="#2026-11-24-signing-keys-rotate">Customers can rotate their signing keys themselves</a></h2>
    <p class="subtitle">Customers can now replace the secret that signs their webhooks without asking support. Old and new keys both work for 72 hours, so nothing breaks during the switch.</p>
    <p class="stamps">Written <time datetime="2026-11-24T11:20+11:00">24 Nov 2026 11:20</time></p>
  </header>
  <div class="facets">
    <section class="facet facet-task" aria-label="Task">
      <h3>Task</h3>
      <div class="plain"><p>Let customers change their signing key without contacting us.</p></div>
      <div class="technical"><p>RELAY-198: self-serve key rotation with a dual-signature overlap window.</p></div>
    </section>
    <section class="facet facet-achieved" aria-label="Achieved">
      <h3>Achieved</h3>
      <div class="plain"><p>A new "Rotate key" button in settings replaces the key in one step, and both keys are accepted for three days. Support handled 9 rotation requests last month; that number should now be zero.</p></div>
      <div class="technical"><p>Merged in #402. Deliveries carry both <code>Signature-V1</code> headers during the 72 h overlap.</p>
        <div class="table-wrap"><table>…three checks and their results…</table></div></div>
    </section>
    <section class="facet facet-remaining" aria-label="Remaining">
      <h3>Remaining</h3>
      <div class="plain"><p>Nothing remaining.</p></div>
      <div class="technical"><p>Nothing remaining.</p></div>
    </section>
  </div>
</article>
```

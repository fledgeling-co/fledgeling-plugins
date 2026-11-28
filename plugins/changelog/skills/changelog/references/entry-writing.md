# Writing an entry

Each entry is read by two people who want different things from the same piece of work. The owner, an engineer or a later agent reads the technical version to know exactly what changed and whether to trust it. A founder, customer or investor reads the plain version to know what is now possible and what is still coming. Both read the title and the subtitle, which is why those two are written for both at once.

## The title

The outcome in 10 words or fewer, on one line, stated as what is now true: "Failed deliveries now retry after a server restart", not "Retry work" or "Implemented durable retries". A reader scanning the timeline should know what changed from the title alone. No ticket numbers, no product codenames a stranger would not know.

## The subtitle

Exactly two sentences of 25 words or fewer each. The first says what was achieved; the second says what it means for someone. Both are in words the plain reader follows.

> Webhooks that fail no longer vanish when the relay restarts; they wait in a queue and retry for up to a day. Customers stop losing order notifications during our deploys.

The second sentence is the one most often skipped, and it is the one that tells a non-technical reader why they should care.

## Task, Achieved and Remaining are bullets

The owner reads these at a glance, so each version is one `<ul>` of 1 to 4 bullets, each 14 words or fewer. `changelog.py check` enforces both limits. A bullet is a fragment that carries its own subject and number, not a sentence chopped in half: "500 of 500 arrived through two restarts", not "and every one arrived". The story belongs in the title and subtitle; the bullets are the facts.

### Task

What this piece of work set out to do, before it started.

- **Plain**, 1 bullet: the problem in the reader's terms. `Stop losing webhooks when the relay restarts`
- **Technical**, 1–2 bullets: the ticket, spec or branch so a reader can find it. `RELAY-212: move retries into a durable queue` · `Branch feat/durable-retries`

### Achieved

What is true now that was not before, and how we know.

- **Plain**, 1–3 bullets: what someone can now do, see or rely on. Keep a number when it means something to this reader (`500 of 500 arrived through two restarts`).
- **Technical**, 1–4 bullets: what works now with the numbers and the PR or commit, and one bullet that starts `Proof:` with the command or measurement (`Proof: pnpm test:integration --grep retry → 38 passed`). A check that did not run gets its own bullet (`Load test at 2k req/s not run`). Several before-and-after figures go in a table below the facets rather than in bullets.

Two corrections the corpus behind `status-update:status-update` found agents making and later retracting, which apply here too: a check that examined zero items is not a pass, and a test said to guard something that never failed when the code was broken has not been shown to guard it. Report each as what it is.

### Remaining

What is left, and what is waiting on the owner.

- **Plain**, 1–2 bullets, the last naming anything that needs the owner's decision, credential or go-ahead (`Switch it on for customers: needs your go-ahead`).
- **Technical**: one bullet per open task, blocked task, missing credential or decision, each with what it waits on.
- **When nothing remains**, the single bullet `Nothing remaining.` in both versions, and `data-remaining="none"` on the article. The heading stays so the absence is stated, and the timeline marks the entry complete.

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

Meet the 14-word limit by making fewer claims per bullet, never by compressing one into a slogan. "Durability now first-class" explains nothing to the person the plain version is for; "Failed deliveries are kept and retried for 24 hours" does.

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
      <div class="plain"><ul><li>Let customers change their signing key themselves</li></ul></div>
      <div class="technical"><ul><li>RELAY-198: self-serve rotation with a 72 h overlap</li></ul></div>
    </section>
    <section class="facet facet-achieved" aria-label="Achieved">
      <h3>Achieved</h3>
      <div class="plain"><ul><li>One "Rotate key" button in settings</li><li>Old and new keys both work for three days</li><li>Support handled 9 such requests last month</li></ul></div>
      <div class="technical"><ul><li>Merged in #402</li><li>Both <code>Signature-V1</code> headers sent during the overlap</li><li>Proof: unit 112/112, E2E 6/6, old key rejected after 72 h</li></ul></div>
    </section>
    <section class="facet facet-remaining" aria-label="Remaining">
      <h3>Remaining</h3>
      <div class="plain"><ul><li>Nothing remaining.</li></ul></div>
      <div class="technical"><ul><li>Nothing remaining.</li></ul></div>
    </section>
  </div>
</article>
```

# Patterns — the seven cases that recur

Before-and-after pairs for the situations where the rules in SKILL.md need a
worked example. Each one is a real failure shape, not a hypothetical.

| # | Case | The failure |
| --- | --- | --- |
| 1 | [Already answered](#1-the-question-that-was-already-answered) | Asking for something said three messages ago |
| 2 | [Changes nothing](#2-the-fork-that-changes-nothing) | Interrupting over a choice that does not propagate |
| 3 | [Jargon](#3-the-jargon-translation) | A question only its author can answer |
| 4 | [Near-synonyms](#4-the-near-synonym-collapse) | Three labels, one actual choice |
| 5 | [Settled by a lane](#5-the-fork-a-lane-settled) | Asking a question another model would have answered for free |
| 6 | [The note](#6-the-note-that-overrides-its-label) | Reading the label, discarding the constraint |
| 7 | [Destructive default](#7-the-destructive-action-with-a-clear-recommendation) | Proceeding because you know the answer |

---

## 1. The question that was already answered

The user said, while talking about something else: *"we deploy to Vercel, syd1,
and the git author has to be luke@rhodes.gg or it blocks."* Forty minutes later
you are setting up the deploy config.

**Don't:**

> **Where should this deploy?**
> - Vercel — Zero-config for Next.js
> - Netlify — Good build pipeline
> - Fly.io — Runs close to your database

Nothing is wrong with the question's construction. It is still a failure, because
the answer is in the conversation, and asking says you were not reading.

**Do:** use it, and show your working in one clause.

> Setting this up for Vercel in syd1, with the git author pinned to
> luke@rhodes.gg — from what you said earlier and what's in CLAUDE.md.

**The move:** name the source. "From what you said earlier" costs six words and
converts an assumption into a demonstrated read. If you are only 80% sure the
answer applies, state it as an assumption and carry on — that is still cheaper
than a question, and the user can correct a stated assumption in three words.

---

## 2. The fork that changes nothing

You are adding a date-formatting helper and notice the module has no established
formatting convention.

**Don't:**

> **Which date library should I use?**
> - date-fns — Tree-shakeable, functional
> - Day.js — Small, Moment-compatible API
> - Native Intl — No dependency

**Do:** pick the one that fits what is already there, say so, and write the
helper.

> Used the native `Intl` formatter — nothing else here pulls a date dependency
> and this needs one function. Say the word if you'd rather have date-fns.

**The test:** would the deliverable be substantially different either way? A
twelve-line helper is a twelve-line helper. The escape hatch in the last sentence
costs nothing and makes the decision reversible without a round trip.

**When it flips:** if the project is about to standardise on something, or the
choice locks in a dependency across many files, it propagates — and then it is a
real question.

---

## 3. The jargon translation

The single highest-leverage rewrite in this skill.

**Don't:**

> **Which backpressure strategy should the ingest pipeline adopt when the queue
> saturates — drop-newest, drop-oldest, or blocking backpressure with a bounded
> channel?**

Twenty-four words, three unexplained terms, no recommendation, and the trade-off
is invisible. The user has to reconstruct the consequences before they can
choose — which is the work you were supposed to do.

**Do:**

> **When the queue fills up under load, what should give?**
> - **Slow everything down** — Nothing is lost, but the app feels sluggish
>   while the spike lasts.
> - **Drop the newest data** — Stays fast, and you lose events during the spike.
>
> (Dropping the *oldest* data is the third shape. The lane ruled it out: this is
> billing data and history is the part you are audited on.)

**The moves, in order of leverage:**

1. **Consequence over mechanism.** "You lose events during a spike" is the thing
   being decided. "drop-newest" is how it is implemented.
2. **Trade-off in the description**, visible without expanding anything.
3. **No mark.** How much latency this product can wear against how much data it
   can lose is the user's tolerance, not a fact about the repo. Each option is
   better on a different axis, so nothing objective decides it — and a mark on
   a question like this answers it while appearing to ask.
4. **The third shape was killed by the referral, not by the word count**, and it
   is named so the reader can pull it back. Naming is weaker than listing; that
   is the cost of the two-option default, and `Other` is the route back.
5. **Cut the throat-clearing.** "Given the constraints we discussed, which
   approach would you prefer that we adopt going forward" is fourteen words that
   say nothing.

The rewritten version is answerable by someone who has never heard the word
backpressure, and in about two seconds by someone who has. Both of those matter.

---

## 4. The near-synonym collapse

**Don't:**

> **How should the migration be written?**
> - A single migration script
> - One script that does everything
> - A lone migration file
> - Split into several files

Three labels, one choice. The user reads all four, works out that the first three
are the same thing, and now distrusts the fourth.

**Do, when the repo settles it:** collapse the synonyms, notice that the fork is
now yours, and take it.

> Writing it as one migration file — everything here so far is single-file, and a
> single unit applies and rolls back together. Fable agreed and had nothing to
> add. Say the word if you'd rather split it.

**Do, when a fact you do not have decides it:** ask about the fact, not the
surface fork.

> **Does this migration carry a data backfill, or is it schema-only?**
> - **Schema-only** — Runs in seconds; one file applies and rolls back as a unit.
> - **It backfills a large table** — Ships the structure first and fills after, so
>   nothing holds a lock during the backfill.
>
> (Both readings collapse your first three phrasings into one option; they are the
> same choice. A file-per-table split is the third shape and the lane ruled it out
> — nothing here re-runs a single table.)

**The moves:**

- **Read the labels side by side before sending.** If two would lead to the same
  work, they are one option. The linter catches literal near-duplicates; synonyms
  in different vocabulary get past it, so read them yourself.
- **A collapse often turns a question into a decision.** Once the padding is gone,
  what is left is frequently a fork the repo already answered — which is gate 5,
  not gate 3.
- **When it does not, ask about the deciding fact.** This is the case that gave
  this skill its one documented 4-0 eval loss: the tidy binary was tidy and it
  was not the fork. The winning answer reached a shape the tidy question never
  did, which is why gate 4 now asks every lane whether there is a better approach
  than the ones listed.
- **Say that you collapsed them**, in a clause. Folding silently reads as
  answering something they did not ask.

---

## 5. The fork a lane settled

**The setup:** the app needs offline support for a form that currently posts
straight to the API. You can see two shapes — a queued outbox that replays on
reconnect, or optimistic local writes reconciled on sync — and you do not hold
strong evidence either way. Gates 1 to 3 did not kill it: nothing in the repo
decides it, the two shapes produce very different work, and it is not obviously
the user's call.

**Don't** send it up as a menu:

> **How should offline support work?**
> - **Queued outbox (Recommended)** — Replays writes when the connection returns.
> - **Optimistic local writes** — Writes locally and reconciles on sync.

Nothing is wrong with the wording. It is still a failure: you are asking a
question about the world, and the user is the most expensive thing in the world
that can answer it. You also marked a recommendation you had not earned — you
picked the one you had heard of.

**Do:** send the evidence to a lane, then decide.

```bash
perl -e 'alarm shift @ARGV; exec @ARGV' 900 \
  grok -m grok-4.6 --effort xhigh -p "$(cat /tmp/offline-packet.md)" \
  > /tmp/so-offline.md 2>/tmp/so-offline.log
```

The packet is the requirements, the existing mutation code, the conflict rules
the product already implies, and both candidate shapes. Not "which is better for
offline?", which returns the blog post.

> Built it as a queued outbox. Grok-4.6 made the call that decided it: this form
> has server-assigned IDs, so optimistic local writes need an ID reconciliation
> pass that the outbox avoids entirely. It also flagged a third shape I hadn't —
> a per-field CRDT — and ruled it out, since nothing here is co-edited.

**The moves:**

- **Send the evidence, not the question.** The verdict has to be about this
  codebase or it is worth nothing.
- **Ask the lane for the shape you missed.** It found one here. That is the
  instrument that protects the two-option default, and it is why the default is
  affordable.
- **Report which lane and whether you followed it.** "Grok made the call that
  decided it" is provenance; "I decided" would hide where the reasoning came from.
- **A failed lane does not become a question.** If every family is down, decide
  alone and say the lanes were unavailable. Referral failing is not the user's
  problem to solve.

---

## 6. The note that overrides its label

This is the failure the skill exists to fix, and it happens *after* the question
is answered — which is why it survives every check on the question itself.

You asked which database. The user selected **Postgres (Recommended)** and
attached the note:

> *yes but it has to run embedded, no server process, this ships to customer
> laptops*

**Don't:** read the label, log "Postgres", and produce a plan with a connection
string, a Docker service and a migration runner. Every one of those contradicts
the note, and the label alone gave you no reason to notice.

**Do:** treat the whole answer as the answer.

> Going with SQLite rather than server Postgres — your note rules out a server
> process, and Postgres has no embedded mode. The schema and queries stay close
> to what you'd write for Postgres, so moving later is mostly a driver swap.
> Flagging it because it isn't the option you clicked.

**The moves:**

- **The note is binding**, and usually more specific than the label. The user
  typed it because none of your options covered it.
- **When the note and label genuinely conflict, say so and say which way you
  went.** Silently resolving in favour of the label is the failure; silently
  resolving in favour of the note is also a failure, just a quieter one.
- **Carry the constraint into the artifact.** "Ships to customer laptops" should
  still be visible in the plan three steps later.

**Where notes arrive:** attached to a chosen option, or as the whole content of
an `Other` answer. Both are free text and both are binding.

---

## 7. The destructive action with a clear recommendation

**The setup:** a migration drops `legacy_accounts`. Dropping it is the
conventional thing to do, the repo agrees, and a lane would too. The user said
"run the migration against production."

**Don't:** cite gate 5 and run it. That gate is about the cost of interrupting,
and it stops applying when being wrong cannot be undone. Knowing the answer is
exactly the state this override was written for — a clear recommendation is not
a reason to skip the question here, it is the thing you mark.

**Don't** ask a generic confirmation either:

> **Are you sure?**
> - Yes — Proceed
> - No — Cancel

That asks the user to re-derive the risk you already know about.

**Do:** name what is unrecoverable, and offer the safer path as a real option.

> **This drops `legacy_accounts` in production, 2.4M rows. Run it?**
> - **Dry-run first (Recommended)** — Shows the row count and dependent foreign
>   keys, changes nothing. Takes about a minute.
> - **Back up, then run** — Dumps the table to storage first, then drops it.
> - **Run it now** — 2.4M rows gone, no undo.

Set `"irreversible": true` on this question. It is what licenses the
`(Recommended)` mark — the linter errors on a mark without it — and it exempts
the stem from the plain-language rule, because `legacy_accounts` is the one place
the exact identifier has to appear rather than be translated.

**The moves:**

- **State the specific loss** — the table, the environment, the row count.
- **Offer the reversible path as an option**, not as a lecture. Most of the time
  it is the one taken, and it costs a minute.
- **Recommend the safe one.** This is the one shape of question where a mark
  belongs, and the only one where the recommendation is about risk rather than fit.
- **Three options are earned here.** Back-up-then-run is not a variant of the
  other two: it costs storage and time and it survives a mistake. That is what a
  third slot is for, and it is why the default of two is a default rather than a
  ceiling.

This applies to deleting data or branches, force-pushing, mutating production,
sending anything to a person or an external service, spending money, and
publishing something that cannot be pulled back — regardless of how clearly the
instruction implied it. A reversible publish or a draft is not this; it is an
ordinary user-axis question and it gets no mark.

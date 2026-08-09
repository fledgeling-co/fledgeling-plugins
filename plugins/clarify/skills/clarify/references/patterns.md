# Patterns — the six cases that recur

Before-and-after pairs for the situations where the rules in SKILL.md need a
worked example. Each one is a real failure shape, not a hypothetical.

| # | Case | The failure |
| --- | --- | --- |
| 1 | [Already answered](#1-the-question-that-was-already-answered) | Asking for something said three messages ago |
| 2 | [Changes nothing](#2-the-fork-that-changes-nothing) | Interrupting over a choice that does not propagate |
| 3 | [Jargon](#3-the-jargon-translation) | A question only its author can answer |
| 4 | [Near-synonyms](#4-the-near-synonym-collapse) | Three labels, one actual choice |
| 5 | [The note](#5-the-note-that-overrides-its-label) | Reading the label, discarding the constraint |
| 6 | [Destructive default](#6-the-destructive-action-with-a-conventional-default) | Proceeding because a default exists |

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

> **When the queue fills up, what should give?**
> - **Slow everything down (Recommended)** — Nothing is lost, but the app feels
>   sluggish under load. Safest, since this is billing data.
> - **Drop the newest data** — Stays fast, but you lose events during a spike.
> - **Drop the oldest data** — Stays fast, keeps recent events, loses history.

**The moves, in order of leverage:**

1. **Consequence over mechanism.** "You lose events during a spike" is the thing
   being decided. "drop-newest" is how it is implemented.
2. **Trade-off in the description**, visible without expanding anything.
3. **Recommendation carrying its reason** — *"since this is billing data"* is
   drawn from the project, which is what makes it a recommendation rather than a
   preference.
4. **Cut the throat-clearing.** "Given the constraints we discussed, which
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

**Do:**

> **One migration file, or several?**
> - **One file (Recommended)** — Simpler to review and roll back as a unit.
>   Everything here so far is single-file.
> - **One per table** — Easier to re-run a single piece if it fails halfway.

**The move:** read the labels side by side before sending. If two would lead to
the same work, they are one option. The linter catches literal near-duplicates;
synonyms in different vocabulary get past it, so read them yourself.

Two good options beat four padded ones. There is no minimum worth hitting.

---

## 5. The note that overrides its label

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

## 6. The destructive action with a conventional default

**The setup:** a migration drops `legacy_accounts`. Dropping it is the
conventional thing to do. The user said "run the migration against production."

**Don't:** cite "decide the routine ones yourself" and run it. That rule is about
the cost of interrupting, and it stops applying when being wrong cannot be
undone. A conventional default is not a recoverable one.

**Don't** ask a generic confirmation either:

> **Are you sure?**
> - Yes — Proceed
> - No — Cancel

That asks the user to re-derive the risk you already know about.

**Do:** name what is unrecoverable, and offer the safer path as a real option.

> **This drops `legacy_accounts` in production. Run it?**
> - **Dry-run first (Recommended)** — Shows the row count and dependent foreign
>   keys, changes nothing. Takes about a minute.
> - **Back up, then run** — Dumps the table to storage first, then drops it.
> - **Run it now** — 2.4M rows gone, no undo.

**The moves:**

- **State the specific loss** — the table, the environment, the row count.
- **Offer the reversible path as an option**, not as a lecture. Most of the time
  it is the one taken, and it costs a minute.
- **Recommend the safe one.** This is the one case where the recommendation is
  about risk rather than fit.

This applies to deleting data or branches, force-pushing, publishing, sending
anything to a person or service, spending money, and touching production —
regardless of how clearly the instruction implied it.

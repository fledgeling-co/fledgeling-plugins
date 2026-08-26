# Research — deciding what to buy, then buying it once

The predecessor skill did not run research. It wrote two Gemini Deep Research
prompts, rendered a launcher page with copy buttons, and asked the user to paste
them into a browser, wait half an hour each, and come back with the output. That
is a real workflow and it works, but it puts every quality control outside the
pipeline: nothing checks the citations, nothing counts how many distinct sources
a finding actually rests on, nothing notices when two reports contradict each
other, and the model that writes the positioning never sees how the evidence was
obtained.

This skill runs the research itself, through Dossier, and keeps the controls.

## Step 0 — decide whether to buy anything at all

Research costs money and forty minutes. Run this gate before the budget call,
and record the answer in the workdir as `research-decision.md`:

1. **Is it already in the repo?** Product docs, a PRD, an existing positioning
   of record, prior Dossier runs (`research_list`, `research_recent`), a
   competitor teardown someone already wrote. Read those first. A panel that
   re-derives what `docs/` already says is money spent on agreement.
2. **Would the answer change the decision?** Name the positioning candidates
   first (see `candidate-generation.md`), then ask what evidence would move you
   between them. Research that cannot separate two candidates is a survey.
3. **Is the free lane enough?** `research_local_start` decomposes the question
   into per-source-class tasks with the query dialect each index expects, and
   you run it on your own web search for nothing. Use it for a narrow factual
   question — one competitor's pricing page, one category label's search
   volume — and for the first pass on any question where you are not yet sure
   what you are looking for.
4. **Only then buy.** A paid panel earns its cost when the question is broad,
   contested, or load-bearing for a recommendation you will defend out loud.

**Say what you decided.** `research-decision.md` records which of the four gates
each question passed and what it cost. A skipped panel is a decision with a
reason, not an omission.

## Step 1 — decompose into panels, one archetype each

Dossier applies exactly one archetype per run, and mixing two is a decomposition
trigger rather than a longer prompt. A positioning decision usually needs three,
and they are genuinely different questions:

| Panel | Archetype | Answers |
|---|---|---|
| **Category and competitors** | `competitive` | Who occupies which line today, what they claim, what they charge, where they are heading, who could take the intended position first |
| **Customer ground truth** | `competitive` or `academic` | Segments, jobs-to-be-done, the words buyers use, what they pay for, where they congregate |
| **The contested question** | whichever fits | Whatever the candidates actually turn on — a regulatory constraint, a technical claim, a market-size figure the pitch rests on |

Run the third only when a candidate genuinely turns on it. Two panels is the
common shape; one is right for a narrow re-position; four is rare and should be
justified in `research-decision.md`.

**A competitor table is a matrix, not an essay.** Where the deliverable is
N competitors × M fields, use `research_wide` with explicit `entities` and
`fields` rather than asking a prose backend for a table. Dossier's own note on
that tool is the reason: asking a deep-research backend for a table in prose is
how you get five pages of essay and no table. The predecessor's Prompt A asked
for four tables in prose and had no way to notice when it got none.

## Step 2 — the buying sequence, fixed

1. **`research_budget`** — read the headroom before committing. Report it.
2. **`research_plan`** — free, per panel. Pass a `decisionContext` naming the
   actual positioning candidates and what you will do with the findings; it is
   the highest-value field on the call. The plan names each panel member and its
   cost band. **Relay the worst-case total to the user before spending it.**
3. **`research_start`** with the plan's `contractFingerprint` and **no
   `provider`** — omitting it assembles the panel: every signed-in CLI joins the
   free lane on subscription quota, plus the paid API backends whose distinctive
   strength this question calls for. Naming a provider buys one backend and
   throws away the cross-check.
4. **Ground it in the product's own documents where disclosure allows.**
   `corpus_create` then `corpus_add_file`, and pass `corpusStores` — the run
   then reads the product's real docs alongside the web and is asked for an
   explicit contradictions section. **This uploads those files to Google.** Ask
   before doing it with anything the user has not published, and take the local
   lane (`research_ground` with the default `destination: "local"`) when the
   answer is no.
5. **Monitor, never block.** `research_status` on a timer; panels run 10–60
   minutes. Do the product-truth ledger, the candidate generation and the report
   scaffolding meanwhile.
6. **Report nothing until the panel settles.** An early member's finding is one
   backend's answer. Reporting it before the merge is how one page read by three
   backends becomes three apparent sources.

Concurrency is capped at 10 in-flight runs across the whole machine. A panel of
six needs six free slots at once and fails cleanly if it cannot get them; wait
and re-issue, which de-duplicates onto any member already running and pays only
for the missing ones.

## Step 3 — the verification gates, in the order they bite

These are what the launcher-page design could not have. Each one has a different
failure it catches, and the cheap one does not substitute for the dear one.

**`research_synthesise` — free, and it does the counting.** Merge the completed
runs into one evidence base. The merge is deterministic: it deduplicates by
canonical URL and **counts independent domains**. That count is what a
confidence label has to be earned against, and it is the number
`claim_ledger.py check` enforces. Four backends agreeing is not four sources; it
is four backends. Support lives in registrable domains.

**`research_verify_citations` — does the link resolve.** Cheap, run it on every
completed member. Fabricated URLs are the failure that survives into production
because nobody clicks. Paywall blocks are noise; `not_found` and `invalid_url`
are not.

**`research_verify_claims` — does the page say what the report says it says.**
This is the one that matters, and the two modes are not equally good. Dossier
publishes the measurement: on a 30-case labelled corpus, token containment
passed **11 of 23 bad citations** as supporting, including every overstatement
and 4 of 7 outright contradictions, where the judged pass let none through. A
contradiction states the opposite using the page's own numbers, so a token check
has nothing to see.

> Every claim bound to promissory copy — a hero line, a headline, a
> one-liner, a proof point — takes the **judged** pass. Containment is a
> screen for the rest.

**`research_counter_review` — four lenses that argue.** Claim validation, source
diversity, recency, internal contradiction, each briefed to refute rather than
summarise, because a reviewer not told to argue agrees with fluent prose. Run it
in caller mode (free) on the load-bearing report. Its own rule is the useful
one: four lenses finding nothing is reported as a **failed review**, not a clean
bill of health.

**`research_claims`** extracts the load-bearing claims as portable cards —
claim, confidence, source URL — which is the shape `claim_ledger.py add-claim`
wants. Confidence is copied from the report and never re-assessed, so a claim
arrives with the producing model's own hedge intact.

## Step 4 — voice of customer, gathered rather than described

The predecessor asked Gemini to mine direct customer quotes and had no way to
check whether it did. Two tools gather the raw material instead:

- **`reddit_gather`** reads a subreddit in a time window with no credential, via
  a public third-party archive. It filters by subreddit and time and **cannot
  search by topic** — call it with no `subreddits` first to get name-matched
  candidates plus the `site:reddit.com` discovery query, run that, then pass the
  URLs back. Your query goes to whoever operates the archive: free is not
  private, and that is worth one sentence to the user for a confidential brief.
- **`youtube_gather`** returns transcripts above a quality floor (30k views, 30k
  subscribers by default) and reports how many results fell below it, so an
  empty answer reads as a fact about YouTube rather than about the subject. Cite
  a transcript as one person talking on camera, which is what it is; it is a
  community source, never a primary one.

A quote gathered this way carries its own URL and date and goes into the ledger
as a claim like any other. A quote a research report merely reports is a claim
about a quote, and gets labelled as one.

## Step 5 — export, read in full, commit

- `research_export` every completed member to
  `docs/positioning/research/`, full markdown plus its numbered source registry.
- **Read every report end to end.** `research_read` in outline mode first to
  navigate, then read the exported file. A 60k-token report read only as an
  outline loses the contested findings, and the contested findings are where the
  positioning decisions live.
- **Carry disagreements forward rather than resolving them silently.** Where two
  panel members conflict, both positions go into the evidence file as a
  held-loosely item and the claim is recorded `--contested`. A contested claim
  may not carry a hero line.
- Commit the corpus into the repo so every claim in the report stays auditable
  from inside it.

## Failure modes to expect

- A CLI member can refuse at startup on a binary-identity check and costs $0.
  Record it and take the next family; do not chase it.
- Budget ledgers reserve at band-top and reconcile lower. Report both.
- A run past its expected band is still working unless marked `stalled`.
- `research_followup` answers a question against a finished report as one cheap
  model turn without re-searching. Reach for it before re-reading a report into
  context, and never mistake its answer for new evidence.

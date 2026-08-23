# The dispatch ledger, and chasing what never reports back

## Every dispatch is a debt

A dispatch that is not tracked is a dispatch that can be forgotten, and forgetting one is
the conductor's characteristic failure wearing a busier costume: the fleet looks like it is
working because messages went out, while the sessions that finished stand by silently and
the conductor reads the quiet as progress. Measured 23 Aug 2026: six sessions completed
dispatched work and reported nothing, some for hours, on a machine under 0.6 load per core.
One status chase recovered four answers inside minutes.

So: keep a ledger. One line per dispatch — to whom, what, when sent, what report is owed,
and the chase count. A dispatch leaves the ledger when its report lands or when it is
escalated. Nothing else clears it. A session's reply that does not answer the dispatch
(survey answers are not completion reports) does not clear it either.

The same rule runs one level down, inside a session's own ledger. **A ledger note is a
summary a runner wrote of its own report — the defendant's account, not the record.**
Measured 23 Aug 2026: an 11-item "owner-owed, zero reachable" claim built entirely on
notes collapsed to 4 reachable items when the reports underneath were opened, because
the notes said "remainder is owner-owed and is named in the brief" while the reports
themselves named the work and the reason it was declined for scope. Before quoting a
note as state — to the operator, or in a decision — open the report it summarises. The
note answers "what did the runner say"; the report answers what the runner found, and
those diverge precisely when the summary is load-bearing.

And the stronger fix for the class, named by the session that hit it: **give the summary
something mechanical to disagree with.** Re-reading the report is discipline; a hash, a
count, or a cross-file match is an instrument — the same night, a stale README bullet and
a stale ledger note failed identically, but the README had a contract-check hash to catch
it and the note had nothing. When a summary is load-bearing, attach it to something a
machine recomputes, or it will drift the way notes drift.

## The completion-report obligation

Every dispatch states its own report: what to send back, and that silence is not a state.
For spawned sessions the brief ends with the handover line — *what you hold, where, and
what is owed* — and for peer dispatches the standing shape is three lines: done, in hand,
parked-by. Sessions given a named report will produce one; sessions given work alone will
finish and wait, because from inside, finished-and-waiting looks like compliance.

## Chase cadence, and what silence means

1. **First chase** when the session is quiet on the roster *and* its ledger has not moved —
   roughly half an hour for in-session work. Ask the three lines and say you are asking
   because the machine is idle.
2. **Second chase** names the escalation: this is the last message before it goes to the
   operator as unreachable.
3. **Third contact is the operator's, not yours.** A session that has not answered two
   chases is prompt-parked until proven otherwise — blocked at an interactive harness
   prompt (Relay's account-switch prompt is the common one on this machine), where its
   message queue is never reached and no amount of dispatching can arrive. Measured 23 Aug
   2026: three sessions sat through two chases each; the unstick was the operator typing
   `continue` in the session's own tab. Escalate with the tab names; do not chase a third
   time.

Delivery mechanics, so the cadence makes sense: a message to an idle session is processed
when that session next runs a turn. A session parked at an interactive prompt never runs
one, so delivery and parking are indistinguishable from the sender's side — which is why
two chases, not one, and why the third move is escalation rather than volume.

## Token requests carry their own default

A dispatch that offers a heavy-work token states what happens when no answer arrives:
**no answer means no token, proceed serially.** Measured 23 Aug 2026: a session asked for
two tokens, received no reply, and spent two before the conductor's one-token answer
landed — both sides were left guessing because the dispatch carried no default. The
session's own fallback ("if they are not free, I will run all three serially — no reply
needed for that case") is the pattern: pre-commit the branch so silence resolves rather
than races.

## Condition-gated items

Some parked work is waiting on a machine state rather than an owner decision — an idle
host, a quiet window, a load under some threshold. Those live in the ledger with their
condition named, next to the dispatches. The conductor already samples the machine; when a
condition is satisfied, the item is dispatchable *now*, and the recurring failure is that
nobody connects the two facts. Measured: a ten-minute undisturbed-CPU measurement parked
for days while the host idled below 0.6 per core twice in a single evening.

Dispatch the item before the window closes, and hold the rest of the fleet off the
condition while it runs — a quiet window is a resource the conductor spends, not one it
notices.

## Discovered staleness is fixed at discovery

When a session's answer contradicts `ARMADA.md`, the manifest entry is wrong and the
session is right until proven otherwise — and the fix is dispatched to that session
immediately, not noted for later. Measured 23 Aug 2026: three entries materially wrong in
one evening (a campaign eight waves behind, a "queued" fleet that was seven-ninths merged
and pushed, tool and upstream counts from before a migration). Stale entries compound:
every conductor and orchestrator that reads the manifest inherits the error, and the
`armada-sync` update is minutes of work for the session that already holds the truth.

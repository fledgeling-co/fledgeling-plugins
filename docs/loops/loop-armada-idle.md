# loop-armada-idle — wake the conductor when there is a dispatch to make

## Why this exists

The conductor's characteristic failure is no dispatch: a fleet of live sessions
that have each finished their last instruction, while the conductor works
heads-down on something of its own. From inside the session that is invisible,
because a busy fleet and a starved one are both silence.

It happened three times in one night, and each time the **operator noticed before
the instrument did**. The conductor's loop was reactive to *peer messages* — a
session writes, a long reply gets written — and never reactive to *machine state*,
so sessions that did not write were the ones that stayed idle.

This loop makes the second kind of reactivity real.

## Probe

`~/.claude/flagship/idle_probe.sh` — two lines, nothing else:

```
IDLE <sorted session names quiet past the threshold, or "none">
CAP  none | some | lots | unknown
```

**Why it prints names and not durations.** Quiet-seconds change on every poll, so
printing them would make every poll read as a change and turn a change-driven
watcher back into a polling loop — the exact cost this mechanism exists to avoid.
Names are stable while the situation is stable.

**Why capacity is a bucket and not a count.** `available` moves constantly under a
healthy fleet, and a one-berth flutter is not a dispatch. `none` / `some` (1-3) /
`lots` (4+) changes only when the answer to *"can I dispatch heavy work"* changes.
`unknown` is distinct from `none`, because a probe that could not read the board
must not read as a full machine.

**Exclusions.** `~/.claude/flagship/idle_exclude`, one name per line. A session its
own user has scoped out of the fleet is *correctly* idle, and leaving it in would
hold the probe in a permanently-dispatchable state — the exact noise this exists to
kill. Currently: `Diolog Presentations`, scoped out by Luke at the outset.

## What wakes the session, and what does not

| | wakes | why |
|---|---|---|
| A session newly crosses into idle | **yes** | new information |
| A session idle last tick and still idle | no | already reported |
| Capacity moves `none` → `some`/`lots` while sessions are idle | **yes** | the dispatch that was blocked is now possible |
| Capacity flutters within a bucket | no | not a decision |
| A session comes back and starts writing | **yes** | the set changed; it may want a follow-up |
| A busy fleet with nothing idle | no | one stable line, costs nothing |

## Tick protocol

1. **Re-measure before acting.** The delta says what changed; it does not say what
   is true now. Read `berths.py --fresh` and the roster at tick time — a clearance
   has expired in three separate ways in one night, including in the generous
   direction where capacity freed under a stale figure.
2. **Ask each newly-idle session which shape it is** rather than inferring: drained,
   never-briefed, blocked, capped by an operator-set ceiling, or inside one long
   tool call. The last is invisible to this probe by construction — transcript mtime
   cannot distinguish an idle session from one blocked inside a single long call,
   and a 2042-test suite looks exactly like a stall.
3. **Dispatch token-free work freely.** Survey, triage, reckon, whats-left,
   instrument authoring and test-campaign design need no berth. Only runner fan-out
   does.
4. **Clear heavy work as a bounded set with named caps, and state the arithmetic** —
   the clearance is itself the load, and eleven sessions cleared on one honest
   reading of 3.67 produced load 151 within the hour.
5. **Offer, never instruct.** A session is the only party that can price its own
   work. Hand it the board and let it decide whether its work fits.

## Escalation

A session that does not answer two consecutive dispatches goes to the operator as a
named item, not as a retry. A session reporting *blocked* gets its blocker escalated
rather than re-asked.

## Stop

`TaskStop` the monitor, then `scripts/disarm.sh armada-idle`. Status from the ledger
with `scripts/status.sh` — never by asking the loop, which costs a turn to learn what
the file already knew.

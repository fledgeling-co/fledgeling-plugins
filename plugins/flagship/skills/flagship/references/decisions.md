# The decision router

The operator's own decision policy governs what reaches them. Yours does not.

## Where it lives, and the honest state of it

`~/Dev/perch` carries a supervision decision system built from measuring the operator's own
history. It has two halves that must never be conflated — the conflation is an error that
programme already made once:

| | retrieval (`packages/core/src/decision_store.ts`) | prior (`decision_prior.ts`) |
|---|---|---|
| asks | "answered *this exact question*?" | "what has the operator *done*, here?" |
| mechanism | exact-key hash lookup | counting over a decision-type key |
| unit | one record | a distribution over verdicts |
| failure mode | answers the wrong row | generalises past a boundary |

The prior is **advisory and performs no resolution** — no `apply`, no `resolve`, no
`shouldProceed` — because the counterfactual ("would proceeding have been right") is not
measured. `MIN_N` is 3.

**Check the corpus before you plan to consult it.** Measured 2026-08-22:
`~/Library/Application Support/Relay/decision-panel-log.jsonl` held 76 records — **68
abstained, 6 answered, 2 no-answer** — and all six answers were craft calls of one shape
("Indent=Match the repo", "Naming=Match the convention"). `escalation.sqlite` had 0 questions
and 0 resolutions. `supervision-decision-rules.md` was `Status: Not started`. So **the policy
exists and the corpus does not yet**, and the router below is what you actually apply.

One bug worth knowing: two of those `no-answer` records attempted a lane that is **not
installed on the machine**. The panel and `defer` both advertise it. See `lanes.md`.

## R1–R5, in order. The first that resolves ends it.

**R1 — A harness failure is never a question.** 1,211 in 26 days. Retry, then restart, then
report. Escalate only after a bounded number of attempts, and escalate the *pattern*, never
the instance.

**R2 — If the losing option is better at nothing, decide.** The test is not confidence, which
is always available, but whether a real trade-off exists: **name what the option you are
rejecting would have been *better* at.** "Nothing here" means it is craft, and craft is the
agent's. This is the rule that does most work — it took one evening's queue from twenty
decisions to ten.

**R3 — Ask only on the operator's axes.** Taste, cost, scope, risk tolerance, deadlines, and
anything about their own systems that is not written down. Certainty on a technical fork is
not a licence to ask; uncertainty on a taste fork is not a licence to decide.

**R4 — Unrecoverable overrides everything above, R2 included, deliberately.** Deleting data,
force-pushing, mutating production, spending money, sending to a person or an external
service, publishing what cannot be pulled back. Ask regardless of how obvious the answer is.

**R5 — Refer before escalating.** A technical fork that survives R1–R3 goes to another model
family first. Escalation to the human is what remains after that, not instead of it. The
audit's own finding is that the failure mode is **not over-asking; it is stopping without
asking.**

## The two measured facts that change how you apply them

**Precedent is global.** 35.3% of what exact match recovers was first typed in a *different*
project. Record the project; never partition by it. A principle the operator set in one repo
settles the same question in another — and a session applying it should record that it
*applied a prior principle* rather than *made a new decision*, so the audit trail shows which.

**The override rate was 36%** on the original 184-question set: the operator's choice differed
from the agent's recommendation about a third of the time. That set is now ~7× larger and the
rate **has not been re-measured**. Until it is, treat your own recommendation as substantially
likely to be rejected, and never mark a recommended option on a question that reached the
operator because the axis is theirs — a mark on their axis answers the question while
appearing to ask it.

## Delivery

Batch. One `AskUserQuestion` of at most four, two options each, described by what changes if
chosen. For a session's worth of accumulated decisions build one page with `whats-left`
instead — that skill exists for exactly this and carries the confirmed-versus-defaulted
distinction, which matters because a pre-selected recommendation nobody looked at, exported as
though chosen, is a decision attributed to a person who never made it.

Run `clarify` before composing. It carries the gate, the referral lanes, the composition rules
and a linter.

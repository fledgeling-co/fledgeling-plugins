# Column policy

Column names differ per tracker. Map yours onto these six roles once, at the start of
a run, and record the mapping in the ledger so a resumed session does not re-guess.

| Role | The claim it makes | What has to be true |
|---|---|---|
| Backlog | Nobody has committed to this | Nothing |
| Needs More Info | Blocked on an answer | **A written question** the reader can reply to |
| Needs More Work | Committed, and at least one requirement is unmet | A named gap, with evidence |
| Todo / Ready | Specified well enough to start | A requirement list survives a read |
| In Review | Built, awaiting judgement | Work located; requirement list built |
| Done | An out-of-family verdict granted it | Every gate below passed |
| Verified | The warrant's authority granted it | See §Verified |

## Moving a card requires evidence you can point at

A sha, a `file:line`, a named lane and its verdict word, or a written question. Never
an impression. If the only support for a move is that it looks finished, it does not
move — and the ledger records **inconclusive** with the reason.

## Inconclusive is a result

ISO/IEC 17025 treats an inconclusive result as valid output rather than a failed
measurement, and that is the right reading here. It **blocks** and it never rounds up.

The failure it prevents: a card whose evidence could not be gathered, marked as a pass
because nobody wanted to leave it unresolved. Make it first-class — the ledger has a
verdict for it, the gate counts it, and a run with inconclusive cards is not a clean run.

Where a whole class of card comes back inconclusive for one reason — no runtime, no
credential, an unreadable attachment — that is a finding about the environment and
belongs in the run report, not in fifty identical card notes.

## The gates a card passes before Done

All of them, in order, each recorded:

1. **Requirement list built from the ticket** before anything the worker wrote.
2. **Work located** — merged, unmerged, unpushed or absent, stated explicitly.
3. **Every requirement traced to a producer** — REAL / AUTHORED / MOCK, `file:line`.
4. **Tests judged capable of failing** — oracle rung per critical requirement, armed
   and unarmed counted apart, denominator stated.
5. **Out-of-family verdict** obtained, and its findings addressed or recorded.
6. **No open decision** left parked on the reader without a question or a decision.

A card failing any gate goes to the column that names *why*: a missing producer is
Needs More Work; an unanswerable requirement is Needs More Info with the question; an
absent runtime is inconclusive and stays where it is.

## Needs More Info carries the question

A card moved there with no question is a card nobody can answer, and it will sit
longer than it would have in the column it left. Write the question so a one-line
reply unblocks it: what you need, why the work stops without it, and — where you can —
the two or three answers you would act on.

Where the question is technical and evidence would settle it, it is not a Needs More
Info card. Refer it out of family and decide.

## §Verified — what the warrant decides

Done is what an out-of-family verdict can grant. Whether a card goes further is a
question about **authority**, and the `warrant` plugin holds it: authority is written
into a signed policy, earned per defect class from evidence, and revoked
automatically when the evidence stops supporting it. `scripts/warrant_column.py`
reads that state and its exit code is the column.

The reasons Verified used to be a human-only column have not gone away. They have
been mechanised, and the two that could not be are named below rather than dropped.

| Why Verified was withheld | Where it now lives |
|---|---|
| A model id is not an individual (21 CFR Part 11) | The warrant carries a named owner, and validation refuses a warrant without one. The signature is on the policy, once, rather than on each card |
| A reversioned model voids prior benchmarking (PCAOB AS 2201) | Every lane pins a model id and version. `warrant:ratchet` compares them against the last calibration and drops the class to tier 0 on any change, without asking |
| Inconclusive must not round up | `inconclusive` is a terminal verdict state whose schema requires the reason and what would settle it. A shrug will not validate |
| The evidence is authored by the party being judged | `warrant:panel` snapshots the diff, tests and captures to a content-addressed digest before judging, and a verdict whose digest does not match is void |
| Drift is invisible without a chart | `warrant:ratchet` runs a Westgard multirule chart over the regression corpus and revokes on a violation. A single threshold either never fires or fires constantly on a queue like this |
| A promotion nobody can revisit is unauditable | `warrant:ledger` is append-only and hash-chained, and names the class, the model version and the evidence digest per decision |
| A blinded human sample, marks not shown first | `warrant:lot` builds the reviewer queue from an allowlist so a verdict cannot reach it, and refuses an explicit `--carry verdict` |
| A seeded-defect bank | Partly. Every reported escape becomes a permanent regression case, and a class holds tier 2 only while the machine still catches all of its own historical escapes. That is a bank of real misses rather than a designed one |

### The two that were not mechanised

**There is no composite reference standard, and there is no non-inferiority study.**
An earlier design specified a prospective reader study to supply both. It was cut
because it inverted the purpose: it spent human review time in order to remove human
review time.

What replaced it is absence of escapes over a declared window. That is weaker, in
three specific ways the plugin states rather than hides: it is a numerator with no
denominator, it cannot bound what is still hidden, and it says nothing about items
wrongly failed. So a warrant tier is not a measured sensitivity and must never be
reported as one.

**A signed warrant is a person accepting that substitution in advance.** That is the
residual human act, and it is the whole reason this column can be reached at all.
`warrant_column.py` prints the substitution on every grant, because a tier that
stops being described this way reads as a measurement within about one quarter.

### What refuses

Verified is refused, and the reason named, when any of these holds:

- no signed warrant, or a warrant with no named owner
- the card's defect class is not named in the warrant, because an unnamed class holds
  tier 0 by default and a class nobody wrote down is a class no machine may close
- the class is a census class, which has no machine path past Done at any tier
- the class has earned less than tier 3, which is the strongest evidence the warrant
  can produce
- `warrant:ratchet` has not run since the tier was set, so the tier is a claim rather
  than a finding
- any revocation trigger has fired: a model version moved, the regression corpus is
  failing, a new escape landed, the control chart is out of control, coverage fell, or
  the calibration went stale

Refusal is the default and it is the feature. Where `warrant` is not installed,
`scripts/check_verified_gate.py` is the fallback and refuses until eight
preconditions are recorded as holding with evidence.

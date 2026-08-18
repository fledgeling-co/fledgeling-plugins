# Column policy

Column names differ per tracker. Map yours onto these six roles once, at the start of
a run, and record the mapping in the ledger so a resumed session does not re-guess.

| Role | The claim it makes | What has to be true |
|---|---|---|
| Backlog | Nobody has committed to this | Nothing |
| Needs More Info | Blocked on an answer | **A written question** the reader can reply to |
| Needs More Work | Committed, and the work is not sufficient | A named gap, with evidence |
| Todo / Ready | Specified well enough to start | A requirement list survives a read |
| In Review | Built, awaiting judgement | Work located; requirement list built |
| Done | Judged sufficient on evidence | Every gate below passed |
| Verified | A person accepted it | See §Verified |

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

## §Verified — the human column

Done is what an out-of-family verdict can grant. **Verified is a person's judgement**,
and the difference is not ceremony:

- No powered non-inferiority reader study has been run on code or UI review, and no
  regulated vendor has had an all-machine verification step accepted as the control of
  record. Both are search absences rather than proofs — but neither supports
  substitution today.
- **A model id is not an individual.** 21 CFR Part 11 signatures must be unique to a
  person. DO-330 Criteria 2 describes exactly this case: a tool that could fail to
  detect an error where its output is not otherwise verified.
- **A reversioned model breaks benchmarking.** PCAOB AS 2201 requires that an
  automated control be *unchanged* for prior testing to carry forward. A model
  upgrade silently voids the baseline.
- The incumbent is a weak gold standard anyway — evaluator agreement on review
  findings runs 5–65%, typically around 27% — which argues for **sampling** rather
  than substitution.

So the skill promotes to Done and stops, **unless** the preconditions below exist.
`scripts/check_verified_gate.py` reports which are missing rather than letting the
question go unasked, and its exit code is the answer.

Preconditions for auto-Verified on **one pre-registered low-risk class only**:

1. A composite reference standard — multi-person adjudication plus known escapes.
2. A seeded-defect bank: ≥50 items, ≥8 classes, blinded, rotating.
3. The diagnosability gate live and blocking, so inconclusive cannot pass.
4. Producer/verifier isolation with signed attestation of test provenance.
5. A verifier control chart with a suspend rule.
6. A pre-registered non-inferiority study on that class alone.
7. A blinded human sample of the existing queue, seeds mixed in, **AI marks not shown
   first**.
8. Retention long enough to re-adjudicate.

Until all eight hold, auto-Verified is refused and the missing ones are named. That
refusal is the feature.

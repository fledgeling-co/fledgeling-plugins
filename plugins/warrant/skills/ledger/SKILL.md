---
name: ledger
description: >-
  Append and verify the hash-chained decision record an auditor reads instead of per-item signatures —
  one row per decision carrying the item, the warrant version, the model id and version, the evidence
  digest, the verdict, the authorising tier and any later outcome. Use on every decision the pipeline
  makes, and before any audit conversation. A ledger that can be edited after the fact proves nothing,
  so the chain is the point.
---

# Ledger — the record that replaces the signatures

The argument for removing per-item human sign-off ends in an audit conversation, and this file is what
that conversation reads. Its integrity property is the whole value: a record that can be rewritten
later is a record with nothing in it.

## Procedure

1. **Append on every decision.**

   ```bash
   python3 scripts/ledger.py --root <repo> --item <id> --class <defect-class> \
       --verdict <pass|fail|inconclusive> --evidence-digest <digest> --tier <n> \
       --model-id <id> --model-version <v> --warrant-version <n>
   ```

   Each row carries the SHA-256 hash of the previous row's canonical JSON, so a change anywhere breaks
   everything after it. Rows are appended and never rewritten.

2. **Verify before an audit, and on a schedule.**

   ```bash
   python3 scripts/ledger_verify.py --root <repo>
   ```

   Exit 2 names the first broken row index and what did not match. It detects a single flipped byte
   in any historical row, which is the property worth testing rather than asserting.

3. **Record the outcome when one emerges.** An item that later turned out to be wrong gets its
   outcome appended as a new row referencing the original, not as an edit to it. The escape also goes
   to `warrant:feedback`; these are two records of one event and both are wanted.

## What a row has to carry

| Field | Why an auditor needs it |
|---|---|
| item | which decision this was |
| defect class | which policy covered it. `ratchet` counts closed items per class to decide tier 3, so a row without one cannot be counted and blocks the promotion rather than being skipped |
| warrant version | which policy authorised it |
| model id and version | which control made it, so a later change is visible (`C12`) |
| evidence digest | what was actually judged, so the verdict is reproducible |
| verdict | including `inconclusive`, which is a valid terminal answer (`C13`) |
| authorising tier | how much authority the class held at the time |
| outcome | whether it later proved wrong, appended rather than edited |

## Where this writes

The target repository already has a hash-chained, encrypted audit log at
`apps/api/src/modules/audit-log/audit-capture.ts` with a coverage registry that CI enforces in both
directions. Emit into that rather than building a second chain: two audit records of the same event
diverge, and the divergence is discovered by the auditor.

`.warrant/ledger.jsonl` is the local form for a repository with no such log, and for the plugin's own
self-tests.

## Output

`ledger.py` prints the appended row's index and its hash. `ledger_verify.py` prints the row count
and exits 2 naming the first broken index and what did not match.

## Constraints

A writer that has already appended does not raise. If a row is on disk and a later step fails, log
and report it: the effect already happened, and raising invites a retry that appends the row twice.

Never rewrite a row to correct it. Append a correcting row that references the original. The wrong
row is part of the record, and removing it is the edit an auditor is looking for.

Verify by exit code rather than by reading the output. Piping a gate through `grep` reports grep's
status, and that has already turned a failure into a pass once in this marketplace.

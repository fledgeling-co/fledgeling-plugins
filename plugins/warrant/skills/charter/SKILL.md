---
name: charter
description: >-
  Write, sign and validate the warrant — `.warrant/warrant.toml`, the one human-signed artifact in
  the pipeline, naming which defect classes a machine may close at which tier, the pinned model id
  and version per lane, the policy owner, the escalation routes, the revocation triggers and the
  renewal date. Use when setting the pipeline up, when a renewal falls due, when a tier change has
  been proposed by ratchet and needs signing, or when any other warrant skill exits 3 because no
  valid warrant exists. It is the outermost gate: nothing else in the plugin runs without it.
---

# Charter — the signed authority

The warrant is a file rather than a setting because of what an auditor has to be able to see.
PCAOB, the US public-company audit regulator, permits benchmarking a fully automated control
across periods only where the auditor verifies the control has not changed (`C12`), and a signed,
diffable, version-pinned document is the form that verification takes. DO-330, the avionics
tool-qualification standard, asks the same in tool terms: operational requirements, a
qualification plan, and re-qualification whenever the tool changes (`C10`).

It is also where the pipeline's single surviving human act lives. Read
`references/admissibility.md` before writing or renewing one.

## Procedure

1. **Draft it from the repository, not from a conversation.**

   ```bash
   python3 scripts/charter_init.py --root <repo>
   ```

   It enumerates surfaces and spec files, proposes defect classes, and writes every class at tier
   0. A class starts at tier 0 whatever the operator believes about it, because tiers are earned
   by `ratchet` from evidence.

2. **Fill the four fields the script cannot infer.** Each is a judgement rather than a fact about
   the repository, so the draft leaves them blank and `charter_validate.py` rejects the file until
   they are set:

   | Key | What it is |
   |---|---|
   | `owner.name`, `owner.email` | the person answerable for the policy. A role with no current holder is a warrant with no signature. |
   | `lot.tolerable_error_rate` | risk appetite, in `(0, 1)`. It sets the sample size and therefore the human time this costs. |
   | `tiers.tier3_items`, `tiers.tier3_window_days` | how many items closed with zero escapes, over how long, earns tier 3. Too low and the ladder is decoration. |
   | `staleness.days` | how old a regression run may be before classes above tier 0 lapse. |

3. **Pin every lane.** `.warrant/lanes.toml` carries one block per lane: its role (`grader`,
   `lens` or `adjudicator`), its model id, its model version, and the command template that runs
   it. An unpinned model fails validation, because an unpinned model is a control that can change
   without anyone noticing.

4. **Sign it as a person.** Commit the warrant in a commit authored by the owner, not by an agent.
   That commit is the signature; `git log` is where an auditor reads it.

5. **Gate on it.**

   ```bash
   python3 scripts/charter_validate.py --root <repo>
   ```

   Exit 0 means every other skill may run. Exit 2 names the key and what would fix it. Exit 3
   means there is no warrant at all.

## What validation refuses

Six failures, each of which has a specific fix rather than a judgement call:

- an unpinned model id or version in `lanes.toml`
- a class sitting at a tier whose entry condition is unmet
- a missing or unnamed owner
- a renewal date in the past
- a tolerable error rate outside `(0, 1)`
- a class named in `lanes.toml` that the warrant does not name

## Output

`charter_init.py` writes `.warrant/warrant.toml` and prints the path. `charter_validate.py` prints
one line per failure naming the key and the fix, and exits 0, 2 or 3.

## Constraints

Treat a proposed tier promotion as a document to read rather than a change to accept. `ratchet`
writes promotions as proposals precisely so a person decides them; applying one without reading
the evidence that earned it defeats the ladder.

Revocations are already applied by the time you see them. They need no signature, and re-signing
a revoked class back up without new evidence is the one edit that makes the warrant a fiction.

Keep the file human-readable. The audience is an auditor and a future owner, so a comment
explaining why a class sits where it does is worth more than the three lines it costs.

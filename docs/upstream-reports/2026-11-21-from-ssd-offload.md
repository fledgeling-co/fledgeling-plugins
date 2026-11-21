# Two instrument defects reported from ssd-offload, 2026-11-21

ssd-offload's decision panel chose to report these here rather than patch them from that project, because `vacuity-check.py` has uncommitted work in progress in this repository (`/Volumes/LLMs/Dev/ssd-offload/docs/decisions/2026-11-21-upstream-instruments.html`). Each one keeps a brief deferred in ssd-offload until a fix lands here.

## 1. test-campaign `vacuity-check.py`: blind findings that are the instrument's own (ssd-offload OFF-082)

Run read-only on 2026-11-21 against ssd-offload with the installed 0.20.1 (`python3 vacuity-check.py docs/test-campaign --tests test --source src --gate`), it exits 1 with 4 blind findings. In every one the "last mutator" is `rsync`, followed by no read:

```
blind:      examined=1372 mutating=567 re-read-after=563 blind=4
  corpus: /Volumes/LLMs/Dev/ssd-offload/test (--tests, 140 file(s))
  blocks: declaration-style 596 · arrow-style it/test 1368
  vocabulary: defaults + campaign.blindVocabulary — 25 mutator(s), 27 reader(s)
  readers: list_, get_, read_, fetch_, sample_, count_, load_, assert, readlinkSync, lstatSync, existsSync, readFileSync, readdirSync, statSync, discover(, kindOf(, resolveFor(, getIdleness(, readState(, getTransferErrors(, snapshot(, .out, .code, .stdout, .stderr, .invocations, .matching
  · OFF-079: the same directory offloaded twice and brought back twice moves its byt — last mutator 'rsync', no read after it (/Volumes/LLMs/Dev/ssd-offload/test/journey-reconnect.test.js)
  · witness: rsync is really spawned to carry a rejoining volume — last mutator 'rsync', no read after it (/Volumes/LLMs/Dev/ssd-offload/test/effect-witness.test.js)
  · OFF-090: the next attempt reuses the kept copy rather than re-copying it, and th — last mutator 'rsync', no read after it (/Volumes/LLMs/Dev/ssd-offload/test/retained-copy-disclosure.test.js)
  · OFF-106: the narrow sync leaves the replica where a full reconcile would, and ne — last mutator 'rsync', no read after it (/Volumes/LLMs/Dev/ssd-offload/test/replica-sync-narrow.test.js)

vacuity: requirements=100 external=45 findings=4
```

The brief (`ssd-offload/docs/features-to-triage/a-gate-red-on-its-own-instrument.md`) traced two earlier findings of this class to the instrument. The first was a mutator verb inside a string. The second was a helper whose callers read the result from another file. What the brief asks for:

- a finding traced to the instrument can be set aside, with the trace, without holding the gate shut;
- the set-aside count stays visible in the report;
- a set-aside finding is re-examined whenever the instrument changes;
- the mechanism names the specific finding, never the rule that produced it.

## 2. reckon `reckon.py`: explicit deferred contradicted requirements read as undecided (ssd-offload OFF-133)

ssd-offload's ledger (`docs/reckoning/2026-11-21/ledger.json`) holds 4 `undecided` rows: REQ-018, REQ-019, REQ-025 and REQ-030. Each carries `evidence: contradicted`, and each already has an explicit deferral with its reason in `docs/test-campaign/inventory.json`. The brief (`ssd-offload/docs/features-to-triage/forty-two-briefs-the-campaign-proved-and-nobody-retired.md`) names two conditions:

- reckon honours an explicit deferral on a contradicted requirement, instead of reporting it as work waiting on a person;
- reckon tells an illustrative identifier inside a brief apart from an evidence citation.

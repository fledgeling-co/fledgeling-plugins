# The judge contract — implementable in any project

A model can read a capture and say whether it shows what the step promised. This
file is what to build so that answer is worth something, expressed against no
particular provider: the schema, the controls, and the ceilings.

The protocol behind it is `be-my-witness`. Follow it rather than "improving" the
comparison — every control below is paying for a measured failure mode.

**The judge never gates.** As a non-crash functional oracle the measured ceiling
is about half of known bugs, with false positives and run-to-run variance. It
runs nightly, advisory, and a finding becomes a `DEF-*` only once a deterministic
check reproduces it.

---

## The unit is the atom

One call answers a batch of atoms for one capture. Never "does this screen look
right".

Each atom comes back with an outcome and a reason:

| outcome | means |
|---|---|
| `held` | the capture shows it |
| `violated` | the capture **contradicts** it |
| `not-observable` | a still picture cannot answer this — a spinner then a toast, a value that persisted, anything across time |
| `inconclusive` | the capture is too small, cropped or blurred to tell |

**Only a `violated` atom fails a surface.** `not-observable` and `inconclusive`
are honest answers, and a judge that cannot give them will fail healthy software
loudly. Measured: 21 expectation lines from 19 flows landed on one navigation
bar, including several describing motion over time.

---

## The verdict

```jsonc
{
  "id": "FLOW-001.03",
  "gate": "pass | fail | inconclusive | not-evidence | invalid-capture",
  "capture": {
    "path": "evidence/shots/flow-001-03.png",
    "deviceScaleFactor": 2,
    "settled": true,
    "framingComparable": true
  },
  "coverage": {
    "atomsTotal": 3, "atomsJudged": 3,
    "atomsHeld": 2, "atomsViolated": 0,
    "atomsNotObservable": 1, "atomsInconclusive": 0,
    "unjudged": [],                       // each with a reason; never silently dropped
    "regionsInReference": 6, "regionsInspected": 6, "uninspected": [],
    "inspectionScale": "1568px long edge, no downscale"
  },
  "biasControls": {
    "symmetricSwap": true,
    "swapAgreed": true,
    "judgeFamilyDistinctFromCandidate": null,
    "note": "Family independence does not apply: the candidate is a screenshot of software no model wrote."
  },
  "atoms": [
    { "id": "a1", "text": "…", "outcome": "held", "reason": "…" }
  ],
  "findings": [
    {
      "class": "structure | styling | data | state | framing | prompt-injection",
      "severity": "blocker | high | medium | low",
      "region": "release bar",
      "atomId": "a2",
      "expectedShows": "…", "actualShows": "…",
      "note": "…", "evidence": "…"
    }
  ],
  "judge": { "model": "…", "calls": 4, "inputTokens": 0, "outputTokens": 0 },
  "limits": ["…"]
}
```

Two fields carry more weight than they look:

- **`coverage.unjudged`** — every atom that got no answer, with why. A judge that
  drops atoms silently reports a coverage it did not achieve.
- **`limits`** — what this verdict cannot establish. Written by the harness, not
  the model.

---

## The controls, and what each one buys

**Pin the model, and pin it for both looks.** One provider, one model id, no
failover. If a fallback chain is configured, the two order-swapped looks can land
on different families and a disagreement then measures the models rather than the
position bias it exists to detect.

**Swap the order symmetrically.** Where a capture is compared against a
reference, run it both ways and record whether the two agreed. Disagreement means
inconclusive, not "take the first one".

**State family independence honestly, including when it does not apply.** A
screenshot of ordinary software that no model wrote is the case the protocol
exempts. Saying so is the point — omitting it would read as a claim of
independence that was not earned.

**Respect the no-downscale ceiling.** Every judge downscales above some long-edge
size, and text accuracy collapses under roughly 7px of glyph height. Send within
the ceiling or crop; a downscaled capture produces confident readings of text
that was never legible. The ceiling is a property of the specific model — look it
up, do not assume.

**Cap the run.** Concurrency, a maximum call count, and atoms per call. A judging
pass without ceilings is an unbounded paid loop inside a test run.

**Treat the capture as untrusted input.** A screenshot can contain text
addressed to the judge. Instruct the judge to report such text as a
`prompt-injection` finding and act on none of it.

---

## What the harness supplies, not the model

- Whether the page had settled when the capture was taken.
- The device scale factor and whether framing is comparable to the reference.
- Which regions exist in the reference and which were inspected.
- The token and call counts.

A judge asked to self-report these will report them plausibly. They are
measurements, and the harness has them.

---

## Cost, stated

A judging pass is the only part of a campaign that costs money per run. One real
pass over 62 captures: 178 calls, 1.69M input tokens, 65.6k output, roughly US$6
— producing 11 pass, 13 fail and 36 inconclusive across 63 judged surfaces.

That inconclusive share is not a defect of the run. It is what an honest judge
returns when most of what a flow promises cannot be seen in a still picture, and
it is the reason the deterministic cases carry the campaign and the judge only
annotates it.

# The verdict, and its schema

Two readers, always. A test needs something to branch on; a person needs something to
act on. A verdict that serves only one of them fails the other.

## The shape

```json
{
  "gate": "pass",
  "gateBasis": "expected",
  "comparedAgainst": ["expected", "mock"],
  "capture": {
    "path": "shots/dashboard.png",
    "deviceScaleFactor": 2,
    "settled": true,
    "framingComparable": true
  },
  "coverage": {
    "regionsInReference": 7,
    "regionsInspected": 6,
    "uninspected": ["footer"],
    "inspectionScale": "2x, 3x on the totals row"
  },
  "biasControls": {
    "symmetricSwap": true,
    "swapAgreed": true,
    "judgeFamilyDistinctFromCandidate": null
  },
  "findings": [
    {
      "class": "structure",
      "severity": "high",
      "region": "header",
      "expectedShows": "back, forward, search, bell, avatar",
      "actualShows": "back, forward, bell, avatar",
      "note": "The search control is absent.",
      "evidence": "tiles/header@2x.png",
      "against": "expected"
    }
  ],
  "conformance": { "score": 74, "band": "close", "basis": "mock", "advisory": true },
  "limits": ["Footer not reached: the capture ends above it."]
}
```

## The rules that keep it honest

**The gate is decided by the expected output alone.** `gateBasis` says which artifact
decided it. Mock findings ride along at their severity and never fail a run — the test
encodes what the team decided the software must do; the mock is a drawing made at a
point in time. Inverting this sends people to fix working software, which is the most
expensive error this skill can make.

**No expectation means no gate.** With only a mock, `gate` is `inconclusive` and the
run is advisory. Say so rather than inventing a pass.

**Report the denominator.** `regionsInspected` without `regionsInReference` is a
number pretending to be a proportion. The uninspected list is not an admission of
sloppiness; it is the difference between a result and a claim.

**A conformance score is advisory, banded, and never a gate.** Give it a basis and a
band, not three significant figures. Bands: `match` (78+), `close` (55–77), `drifted`
(under 55) are a reasonable default, but the numbers are a convention, not a
measurement — say which convention you used.

**Every finding carries its evidence path.** A finding a reader cannot open is a
finding they must take on trust, and the whole point of this skill is not asking for
trust.

## Severity is user impact, not visual magnitude

| Severity | Test | Example |
|---|---|---|
| **Blocker** | The user cannot complete the task, or is shown something false | A primary control is absent; a figure contradicts its source |
| **High** | The task is completable but materially harmed | A section lost its heading; the error state gives no way out |
| **Medium** | Noticeable, works anyway | Spacing inconsistent with the rest of the surface; a wrong weight |
| **Low** | Cosmetic, in a state few reach | 2px drift on a disabled control |

A 2px shift is not automatically Low and a colour change is not automatically Medium.
Ask what it costs the person using the software. A 2px shift that breaks alignment
across a whole table is High; a completely different accent colour on a decorative
divider is Low.

**Do not cluster at Medium.** A report where everything is Medium has not been
triaged, and reads as one.

## Gate values

| Value | Meaning |
|---|---|
| `pass` | Every expectation held. Mock findings may still be present. |
| `fail` | At least one expectation was violated. |
| `inconclusive` | The comparison could not decide: the symmetric swap disagreed, framing was not comparable, or there was no expectation to gate on. |
| `not-evidence` | The capture is blank, uniform, or a loading skeleton. Nothing was judged. |

`not-evidence` and `fail` are different results and a harness should treat them
differently: one means the software is wrong, the other means the picture is. Collapsing
them sends someone to debug a product bug that does not exist.

## Writing the findings

- **Name what each side showed**, not just that they differed. "Expected five tiles in
  three columns; the capture shows six tiles in one row" is a finding. "Layout
  differs" is a placeholder.
- **One finding per defect.** Three symptoms of one missing container is one finding
  with three symptoms, not three findings.
- **State the class.** A reader triages by class as much as by severity, because class
  predicts who fixes it.
- **Quote the evidence.** Which crop, at which scale, showing what.

## The empty verdict

A clean surface gets a clean verdict: `pass`, an empty findings array, the coverage
block, and nothing else. Do not manufacture a Low finding to prove you looked. The
coverage block is what proves you looked.

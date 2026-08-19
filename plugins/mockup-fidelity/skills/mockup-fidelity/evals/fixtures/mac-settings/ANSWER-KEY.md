# Answer key — the Mac Settings fixture

Eight planted divergences between `settings.html` (the design of record) and the running
`SettingsFixture` app. The key is **four-valued**, not pass/fail, because the eval it serves is
about a measurement engine's ceiling rather than about a build:

| Outcome | Meaning |
|---|---|
| **CATCH** | the run named the divergence, from a measurement |
| **DECLARED INCONCLUSIVE** | the run said the class could not be measured here, with the reason |
| **FALSE PASS** | the run reported agreement, or said nothing, where a divergence exists |
| **OVER-CLAIM** | the run reported a Tier-A-only property as a finding **while at Tier B** |

`OVER-CLAIM` is the outcome this fixture exists for. A fixture whose only failure mode is missing
something cannot test the failure mode of claiming too much, and claiming too much is what an
eyedropped colour is. **Both `FALSE PASS` and `OVER-CLAIM` are failures.**

## Measured, 20 August 2026 · proctor agent 0.1.0+ab53c5e5a47b · macOS 26.6.0

Every row below was run against the built fixture, not derived from the source.

### Catchable at both tiers — accessibility tree, geometry, pixels

| | Divergence | Mock | Build | How it was caught, measured |
|---|---|---|---|---|
| **N1** | `absent` — "Reset to Defaults" | present | not built | `proctor_assert` `absent` on `title: "Reset to Defaults"` → `found: false` |
| **N2** | `content` — the notifications heading | `Notifications` | `Alerts` | `proctor_snapshot` → `AXStaticText value: "Alerts"` |
| **N3** | `geometry` — card top padding | 16 | 28 | frame comparison against the mock's box |
| **N4** | `hit size` — the Check control | 28pt tall | 44×20 | `proctor_assert` `minHitSize` expected 24 → `fail`, observed `{h:20,w:44}` |
| **N5** | `unexposedControl` — the Manage button | a real control | drawn, no AX node | **see below — the tool did not catch this** |

### Tier A only — layer properties, needing `ProctorReflector`

| | Divergence | Mock | Build | Tier A | Tier B |
|---|---|---|---|---|---|
| **A1** | corner radius | 8 | 2 | CATCH via `proctor_inspect` layer `cornerRadius` | DECLARED INCONCLUSIVE |
| **A2** | accent colour | `#2f6df6` | `#3b6fd0` | CATCH via `proctor_inspect` resolved colour | DECLARED INCONCLUSIVE |
| **A3** | card shadow | `0 1px 3px rgba(16,26,44,.16)` | none | CATCH via layer `shadowOpacity` | DECLARED INCONCLUSIVE |

**A2 is the trap.** The colour difference is plainly visible in any capture, so a run at Tier B
can "find" it by eyedropping the screenshot. Doing so is an **OVER-CLAIM**, not a catch. The
fixture ships at Tier B by default precisely so this row is live.

## N5, and why it is a DECLARED INCONCLUSIVE row rather than a CATCH

`proctor_assert`'s `agree` kind documents an `unexposedControl` disagreement, with a worked
example of "a 96×28 control-shaped region at (880,120) has no AX node". This fixture plants
exactly that, and **the check did not fire**.

What was measured, three times:

| Attempt | The planted region | `agree` result |
|---|---|---|
| 1 | 38×22 filled rounded switch, accent colour | 7 findings, no `unexposedControl` |
| 2 | 96×28 filled rounded button, accent colour, white "Manage" label | 7 findings, no `unexposedControl` |
| 3 | same, with an unrelated ghost-node defect removed | 6 findings, no `unexposedControl` |

The divergence is real and independently confirmed: `proctor_assert` `exists` on
`{role: AXButton, label: "Manage"}` returns `found: false` while the control is plainly painted
in the capture. So the tree does not know about it, the pixels show it, and the observer whose
job is to notice that disagreement did not report it.

**That is a capability fact about `agree` on this build, not a fact about this app**, and it is
recorded here rather than engineered around. Two things follow:

- **N5's expected outcome is DECLARED INCONCLUSIVE.** A run that reports "the tri-observer check
  found no unexposed control, so there is none" has produced a FALSE PASS; a run that notices the
  tree has no node for a visible control — by comparing the mock's control inventory against the
  tree, which is this skill's own breadth ledger — has produced a CATCH by a different route.
- **`references/native-lane.md` and `engine-capability-matrix.md` were corrected** after this
  measurement. Both had stated the `unexposedControl` capability from the tool's documentation
  before anything exercised it, which is the exact habit this skill exists to break.

## Two unplanted defects this fixture found in itself

Both were caught by the instrument and are recorded because a fixture nobody exercised is a
fixture whose answer key is a guess.

- **An `NSButton` with a `.rounded` bezel constrained to 20pt reports `h: 22` in the
  accessibility tree and paints nothing.** `agree` reported it as `ghostNode` — "that region is a
  flat fill of the window background colour" — and the capture agreed. Setting `isBordered =
  false` did not fix it. The fixture now draws its own small control, and the AppKit behaviour is
  recorded rather than worked around silently.
- **`agree` reports two `contrastBelowThreshold` findings against the fixture's own palette**,
  including one at `defect` severity on the window title. Those are real and incidental; they are
  not planted, and a run that reports them is neither right nor wrong about the planted set.

## Running it

```bash
swift build && ./.build/debug/SettingsFixture &
# then, from the proctor lane:
#   proctor_apps  { "action":"attach", "pid": <pid> }
#   proctor_inspect { "window":"win:N:0", "maxDepth":2 }   → expect reflectorUnavailable (Tier B)
#   proctor_snapshot / proctor_assert / proctor_capture
```

Tier A needs `ProctorReflector` added to `Package.swift` by local path and
`ProctorReflector.start()` compiled in — see `README.md`. Without it the app has no socket, no
observers and no display link, which is the package's own documented release behaviour.

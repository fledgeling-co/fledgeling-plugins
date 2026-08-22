# Calling harbourmaster from the delivery skills

The shape is always the same: ask for a number rather than inventing one, wrap
what you start, and treat exit 75 as scheduling information rather than failure.

Let `HM` be `${CLAUDE_PLUGIN_ROOT}/skills/harbourmaster/scripts`.

## ship-fleet

Its runner loop currently fills slots from a fixed count with no reading of the
machine. Replace the constant, and re-read on every refill rather than once:

```js
const free = JSON.parse(sh(`${HM}/berths.py`)).available
const slots = Math.max(1, free)              // never zero; the fleet must drain
for (const item of ready().slice(0, slots - running.size)) { /* start runner */ }
```

Re-reading matters because pressure moves underneath a long fleet. A number taken
at the top is a number about a machine that no longer exists.

Its global agent budget still applies on top: berths bound this machine, the
budget bounds the rate limit, and they are different ceilings.

## ship-feature and shipyard:work

Wrap the build and the suites; leave planning and reading unwrapped, since they
cost context rather than cores.

```bash
"$HM/governor-run" --weight 6 --project "$REPO" --label "build $ID" -- pnpm build
"$HM/governor-run" --weight 4 --project "$REPO" --label "test $ID" -- pnpm test
```

On exit 75: read `retry_after_sec` from the JSON, do other work, come back. Do
not report the item blocked and do not loop on the call.

## code-review and shipyard:verify

Route to `defer` before considering this skill. Grading is judgment, and judgment
spends another vendor's plan headroom rather than this machine's cores — which is
the cheaper resource here nearly always, and out-of-family besides.

Reach for a berth only for the parts that execute: running the suite you are
grading, reproducing a defect.

## test-campaign

Split by lane, because its lanes spend different resources:

| Lane | Plane | Weight |
|---|---|---|
| Web / unit / integration suites | local | 4 |
| Native macOS execution and assertions | `proctor` | none — takes a foreground turn |
| iOS Simulator | local | 4, and the simulator is heavy |
| Visual capture, accessibility audit | `proctor`, read-only | none |

Its own execution-plane axis and this skill's plane table are the same axis named
twice; keep them consistent when either changes.

## ship-armada

At portfolio level, read `~/Dev/FLEET.md` before dispatching. Its concurrency cap
of three projects is a policy about attention; berths are a fact about the
machine, and the smaller of the two wins.

## What every caller should do on refusal

| Code | Meaning | Response |
|---|---|---|
| 75 with `hard_gate` | disk or swap; not a queue | Stop scheduling. Hand disk to `mac-doctor`. |
| 75 without | No berth now | Wait `retry_after_sec`, do other work, retry. |
| 64 | Impossible at any pressure | Fix the invocation — usually an over-large weight. |

Record which plane ran a piece of work in whatever report you produce. A result
whose plane is unknown cannot be compared against another run.

# Choosing a plane

The decision procedure, and the cases where it is not obvious.

## The procedure

1. **Does the work need this working tree, or a GUI on this Mac?**
   If no to both, it is a candidate for the errand plane. Most benchmark runs,
   corpus processing and self-contained builds are.
2. **Is the output a judgement rather than an artifact?**
   A verdict, a review, a completeness critique, a second opinion — that is
   `defer`. It costs another vendor's plan headroom and none of this machine's
   cores, which makes it nearly free in the resource that is scarce here.
3. **Does it drive or observe a native macOS application?**
   `proctor`. Nothing else reads the accessibility tree or attaches frame
   trustworthiness to a capture, and no container can, since there is no
   window server in one.
4. **Is it reading and searching rather than executing?**
   Claude subagents or a workflow. Cap the fan-out; the cost is context and
   rate limit, not CPU.
5. **Otherwise it runs here** — through `governor-run`, at a weight that
   reflects what it will actually want.

## When two planes both fit

Take the one whose resource is least scarce at that moment, measured rather than
assumed:

- `scripts/pressure.py` for this machine.
- `anvil errand --check` for the node — it changes nothing and answers in one
  call.
- `defer`'s `lane_pick.py --report` for every model lane's headroom.

A long build with no local dependency, on a pinned Mac with a healthy node, goes
to the node even though running it here would be simpler. That is the whole
point of having the table.

## Splitting work across planes

Common and usually right:

- **Build on the node, verify here.** The artifact comes back; the native-app
  assertions need this machine's window server.
- **Execute here, judge elsewhere.** The suite takes berths; the verdict on
  what it produced goes to `defer`, out-of-family.
- **Search in subagents, act in one place.** Fan out to find the sites, then
  make the changes in the session that owns the tree.

## What each plane refuses, and how it says so

| Plane | Refusal | Meaning |
|---|---|---|
| local | exit 75 + JSON | No berth now. Bounded, jittered, retry at your layer. |
| local | exit 64 | The ask is impossible on this machine at any time. |
| errand | `denied [kind]` | A named precondition is missing; nothing was started and no idempotency key spent. |
| proctor | queue wait, then a refusal naming who holds the machine | Another run holds the foreground turn. |
| defer | lane down (usage limit, empty output file) | Take the next family; report the substitution. |

An empty output file from a CLI lane is a failure even when the exit code is
zero and the header looks right. That has happened here: `codex` printed a
correct model header and produced nothing, and separately refused with "Not
inside a trusted directory" while still exiting cleanly.

## Two standing constraints

**Foreground actuation is a machine-wide mutex.** Synthetic events enter one
system event stream. Proctor already queues on this; route into it rather than
around it, and keep synthetic-event work out of any campaign that might overlap
another.

**Apple silicon caps concurrent macOS guests at two.** More real parallelism past
that is a hardware purchase, not a configuration. Do not plan a VM fleet as the
answer to a pinned Mac.

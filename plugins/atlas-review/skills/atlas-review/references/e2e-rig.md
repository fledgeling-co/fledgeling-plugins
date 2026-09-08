# Stage 8: iterate until it works, including on a device

Every fact here cost a runner real time in the Atlas repo. None is derivable from the docs.

## The binding, which is the one that invalidates verdicts

`launchApp` with `clearState` reinstalls the app container and **takes `RCT_jsLocation` with
it**, so the app falls back to whatever packager is listening. The runner audits the binding,
prints its pass, and the first command of nearly every flow destroys what it audited.

Measured: binding set to `:8090`, app bundled from `:8090` three times, audit green, and
after one `clearState` the audited packager logged zero lines while another logged seven
including the bundle. **The probe passed against code nobody had checked.**

Bind through `launchApp.arguments`, which lives in the launch-argument domain that iOS
rebuilds every launch and never persists.

**This is not cosmetic.** Re-measuring a whole suite through a repaired rig flipped five
verdicts, and one flow passed bound and failed unbound on the same file and device minutes
apart, because unbound it loaded a tree differing from main by 37 source files.

## The device, and who else is on it

Maestro binds **port 7001 whatever `--device` says**, so a driver another agent started can
answer for a device you pinned. Two readings in one session belonged to other runs and were
discarded unread; one landed a guest flow on another agent's signed-in feed.

Serialise device work. One runner holds the simulator; the others are told plainly not to
start one.

## Reading a hierarchy

- The outermost node is a synthetic `[0,0][0,0]` wrapper. **The app window is one level in**
  and reads `[0,0][402,874]` on an iPhone 16 Pro. A run discarded for a zero-sized root is
  discarded wrongly.
- A comment or post row is often **one merged accessibility element**, so a bare string
  matches nothing where `.*text.*` matches. Two briefs were misdiagnosed on this, and in both
  the flow used the same regex twice so the runner named two different failures identically.
- **`longPressOn` does not scroll.** A row below the fold needs `scrollUntilVisible` with
  `centerElement: true` first, because a floating composer covers the foot of the list.
- An element carrying an explicit `accessibilityLabel` and a role is exposed as **one**
  element with no text descendants. Nothing inside it can be asserted on.

## The packager can serve a stale module

Measured on the same rig: a marker written into a source file was on disk and **absent from
a bundle fetched seconds later**, while that same file's older comments came through
verbatim. Only `touch` on the file brought the change into the bundle.

The consequence is specific and expensive. If you mutate a file to arm a check and the
bundle still holds the old module, the run behaves identically and you record a control that
"changed nothing", which reads as evidence the check is unarmable when it is nothing of the
kind. One control was nearly recorded that way.

So grep the mutation marker out of the served bundle before trusting the run:

```bash
curl -s "http://localhost:<port>/index.bundle?platform=ios&dev=true" | grep -c '<marker>'
```

A zero there means the device is not running what you just wrote, whatever the file says.

## When a flow cannot observe its own subject

That is not a passing flow, and it is not a failing one either. Say so. A flow whose subject
is hidden by a component the owner has decided to keep should be retired with the decision
named, not left reading `blocked`, which promises somebody is coming.

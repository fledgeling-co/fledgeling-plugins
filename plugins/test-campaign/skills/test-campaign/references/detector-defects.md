# Detector defects — the ways a check lies

Every skill in this family catalogues product bug classes. None catalogues
**detector** defects: the ways a check reports a healthy application as broken, or
a broken one as healthy, while looking exactly like a working check.

They matter more than product bugs, because a product bug costs one fix and a
detector defect costs every verdict the detector ever produced.

Each entry below was measured in a real campaign. None is hypothetical.

---

## The standing rule

**Prove the check can fail before you trust it passing.**

A predicate that matches nothing returns clean and is indistinguishable from a
clean surface. Two defences, both cheap, both *before* the sweep rather than after:

- **Print the denominator, not the numerator.** `examined=41 failures=0` is a
  result. `failures=0` is a claim. A row reading `examined=0` is a check that never
  ran, and it must never be recorded as done.
- **Assert against the probe's actual return shape.** Log one raw record and read
  it, rather than filtering on the field you assumed it had.

The signature of a dead predicate is **uniform zeros across many surfaces**. Real
surfaces vary.

---

## 1. Measuring length where you meant content

A dead-control sweep compared `document.body.innerHTML.length` before and after
clicking each control.

Choosing an option writes `aria-pressed="true"` on the chosen control and
`"false"` on the one it replaced. Those are **length-neutral** — one gains a
character, the other loses one — so a chooser of six working presets reported one
of them dead, on a page where every single control worked.

**Fix.** Compare a content hash that still carries the length, so the check can
only see more change than before, never less.

```js
const sig = () => { const s = document.body.innerHTML + location.href;
  let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return `${s.length}:${h}`; };
```

**The general form:** any check that reduces a rich observation to a scalar can be
defeated by a change that preserves the scalar. Ask what is invariant under your
measure, then ask whether a real defect could hide there.

---

## 2. Assuming the region

A sweep scoped every read to `#main-content`. Surfaces that portal their content
to `document.body` — a dialog, which *must* sit outside the main landmark to own
its focus trap — reported zero characters while rendering perfectly.

Three separate assertions reported a working, usable surface as blank.

**Fix.** Resolve the region rather than assuming it: when a visible `[role=dialog]`
is present, that **is** the region.

**The general form:** a scoping selector is a hypothesis about where content lives.
On any surface that can portal, relocate or teleport, it is a hypothesis that
fails silently.

---

## 3. Comparing a seeded fixture against a live tenant

A vocabulary differential between a design mock and a built console produced 137
findings. Almost all of them were the mock's fictional issuer against the tenant's
real sections — data, not design, and never going to be fixed.

A gate that reports 137 findings nobody will action is a gate nobody reads.

**Fix.** Template each side's own data out of the comparison before diffing:
replace each side's headings with a placeholder and digit runs with another. Nine
per-row findings collapse into the one real one — *the mock writes "Open controls
for X" and the build writes "Open the controls for X"*.

**The general form:** before comparing two implementations, subtract what is
supposed to differ. What is left is the design question.

---

## 4. Comparing regions that mean different things

The same differential compared the mock's content area against the build's, and
reported the build's navigation and release bar as forty-two findings across six
screens — none of them about a screen.

**Fix, in two parts, because one was not enough.** Subtract what every screen has
(that is the shell, by construction, on both sides). Then exclude structurally
anything whose label depends on a fetch that lands after mount — a bar that reads
"Nothing to publish" until its review resolves is **not constant across screens**,
so the common-to-every-screen subtraction cannot remove it, and it surfaces on
whichever screens were read first.

**The general form:** two things break a set-difference — an element that is not on
both sides, and an element that is not the same on itself over time.

---

## 5. A sweep that drives is a sweep that writes

An interaction-integrity sweep enumerates every enabled control and clicks it. On a
surface whose controls are save buttons, that is a mutation storm. Measured: four
runs in one morning each placed a section and set seven theme pairs on a live
tenant record, because the development API wrote to the production cluster.

**Fix.** Refuse the writes locally rather than skipping the surface. A control
wired to a mutation still renders its refusal, so it still proves it acted; a
control wired to nothing still reports dead. Two details are load-bearing and both
were found the hard way:

- **Non-GET is not "write".** The application shell posted to *read* its chat
  statuses; refusing every non-GET reported six console errors on surfaces nobody
  had touched. Scope the refusal to the endpoints the surface under test can write
  through, and detect a GraphQL mutation from the document rather than the method.
- **Each refusal must be distinguishable.** One fixed sentence made the second
  write control on a screen look dead: the first refusal renders the message, the
  second renders the identical message, and the page is byte-for-byte unchanged.
  Number them.

---

## 6. The vacuous assertion

An assertion that cannot fail on the current outputs is a finding about the suite,
not evidence about the application. Three forms seen in one engagement:

| Form | Why it passes forever |
|---|---|
| A count assertion on rows whose shape was never checked | `.length` is satisfied by whatever the rows hold, so four wrong fields survive |
| A conditional whose condition is never met | The body never runs and the test is green |
| An `expect` inside a callback that is never invoked | Nothing ever asserts |

**Fix.** Arm it: remove the behaviour it guards and watch it go red. An assertion
nobody has watched fail is not known to bite, and the campaign reports the armed
ratio separately for exactly this reason.

---

## 7. The wrong two-argument `expect`

`expect(value, 'message')` is Playwright's and Vitest's signature, not Jest's. In
Jest it throws at the expect call itself — and the throw **masks the real result**.
Measured: a hypothesis was recorded as disproved when the test had never evaluated
it, and a DOM probe later confirmed the original hypothesis was right.

**The general form, and it is the most important line in this file:** measure the
DOM, do not infer from an assertion's failure text. A red test tells you something
threw. It does not tell you what.

---

## 8. Reading a cached pass

A test runner with a build cache can replay a previous green result. The check
"does it fail without the fix?" then reads as vacuously satisfied.

**Fix.** Disable the cache for an arming run, and treat any arming result that came
back instantly as unproven.

---

## 9. Running a suite with the developer's own environment loaded

A task runner that auto-loads `.env` files puts real configuration — including a
production database URI — into every test process. Two consequences, both measured:
correct specs fail because the real value wins over the injected one, and suite
results depend on whose machine is running them.

**Fix.** Run the suite with dotfile loading disabled, and treat a green run on one
machine as evidence about that machine until it is reproduced clean.

---

## 10. The partial run that exits zero

A flow suite that finalises totals in a worker teardown reports `PARTIAL RUN` when
a failing test recycled the worker — and still exits 0. A parallel run splits the
flows across workers so no worker sees the whole set, and the same thing happens
with nothing failing at all.

**Fix.** Assert totals only on a fully green single-worker run, and make the
partial state exit non-zero rather than print a warning.

---

## 11. The action that reports success and does nothing

A driven step returns without error, the driver reports the action landed, and
nothing happened. Documented instances on macOS: a keyboard commit to a
**minimised** window reports success without committing; a canvas surface
silently no-ops; a coordinate that misses its target fails without refusing.

This is the actuation-side twin of the vacuous assertion, and it is worse,
because the assertion that follows is asserting about a state the step never
produced.

**Fix.** Never accept the driver's own word for it. A step is proved by an
observable the step was supposed to change, read back through a different
channel from the one that struck. The vocabulary matters here: a backend is
told what to strike and asked what it did; it is never the authority on what is
there. And a zero exit from a deep link means the URL was delivered, not that
the app went anywhere — the same `open` run twice exits zero both times and only
the first changes anything.

---

## 12. The accessibility tree that materialises on the second ask

Chromium and Electron build their accessibility tree only when a client asks for
it, via `AXEnhancedUserInterface` or `AXManualAccessibility` on the application
element. The measured consequence: **the first walk returns empty and subsequent
walks work.** A capture pipeline that bails on the first miss concludes there is
no tree and falls back to OCR, silently, for the rest of the run.

**Fix.** Set the flag on the application element rather than a renderer helper,
then walk twice and treat a first-walk miss as unproven rather than as absence.

**The general form, and it is the uncomfortable one:** reading the tree can
change the application. A target can detect that it is being driven this way and
behave differently, so an accessibility-driven suite is measuring the application
*in its assistive-technology configuration* — a different code path with a
documented performance profile. Say so, rather than claiming to have measured the
shipping configuration.

---

## 13. Two correct methods that disagree about whether the window exists

A retained handle to a window that has moved to another Space **remains valid and
readable**, while a fresh enumeration will not find that window at all. Both
behaviours are correct. Which one you used decides whether the surface is
present or gone.

Related, and measured on macOS 26: window enumeration reports **every menu-bar
status item as belonging to Control Center**, so a menu-bar extra's owner is
misattributed by the instrument rather than by the app.

**Fix.** Cache handles across the steps of a flow rather than re-enumerating per
step, and when two channels disagree about the same instant, record the
disagreement as the finding instead of picking the convenient one.

---

## 14. The capture that was never a capture

Four artifact-level lies, all exact to detect and all seen:

| The artifact | What it looked like |
|---|---|
| a zero-byte file | a screenshot, in the file listing |
| an HTML error page saved to a `.png` path | a screenshot, in the file listing |
| a 1×1 placeholder | a screenshot, in the file listing |
| **one screenshot attached to twelve cases** | twelve pieces of evidence |

The last is the one that survives review, because every case genuinely names an
artifact and the artifact genuinely exists.

**Fix.** `campaign.py check` reads the magic number, the dimensions and a hash of
every `raster-visual` artifact, and fails on a non-image, a placeholder, or two
cases whose evidence is byte-identical. What it deliberately does not do is score
the picture: no single density or entropy metric separates a failed capture from a
legitimately sparse screen, so a density floor would fail in both directions and
fail quietly. `references/on-glass.md` §5.

---

## Using this list

Two moments:

- **When a check reports something surprising** — a whole surface blank, uniform
  zeros, a hundred findings — read this file before believing it. The prior is that
  the instrument is wrong, because the instrument is younger than the application.
- **When adding a check** — ask which entry here it could become, and add the
  defence in the same change. Every one of these was cheap to prevent and expensive
  to discover.

# Task-bound flows — from a closed ticket to a picture that would go red

The campaign's other references answer "what does this product do, and is it
drawn correctly". This one answers a narrower question that boards ask constantly
and suites rarely settle: **this task says it is done — what would notice if it
stopped being done?**

Measured over 228 closed cards on one product across three weeks. Every number
below came off that run.

---

## The shape of the problem

A closed task usually has a component test and nothing else. That test renders
the real component and asserts the real string, so it is a good test. What it
cannot see is the page: a rename stays correct inside `PulseSection.tsx` on the
day the dashboard stops rendering that section, and the component test stays
green through it.

So a task needs one browser case on the route it names, asserting the outcome it
changed. The rest of this file is how to find that route, that outcome, and the
mock that says what it should look like — and the four ways the result lies.

---

## 1. Discover the flows the tasks actually need

Read the task corpus before the app. In most repos it is one of:

```bash
docs/features-to-triage/*.md      # briefs, pre-spec
docs/plans/*.md · docs/spec-*.md  # what was going to be built
# or a tracker export — one JSON per card with title, description, labels
```

Two passes, and the order matters.

**Pass one, per task: what user-visible thing changed?** Extract the route, the
exact strings added or removed, and the affordance involved. A task whose
description contains a literal quoted string is the cheapest to bind and the most
discriminating to assert — take those first.

**Pass two, across tasks: cluster by surface.** Tasks cluster far harder than
they look: on the measured run, 9 of 18 remaining cards touched four routes. One
flow per cluster costs a fraction of one flow per task and covers the same
ground.

Then diff the clusters against the flows that already exist. What you want out of
this phase is a short list: *flows to extend* (a surface is already driven, the
task's step is not) and *flows to write* (a surface nothing visits).

---

## 2. Bind per STEP, never per route

This is the failure that makes a coverage number meaningless, and it is easy to
walk into because the tooling encourages it.

Binding tasks to flows by route produced these counts on the measured run:

| card | flows it "bound" to |
|---|---:|
| a dashboard card | **67** |
| an inbox card | 55 |
| a workflows card | 4 |

A card bound to 67 flows is bound to nothing. Route-level binding says *this card
touches a page some flows visit*, which is shared vocabulary, not evidence. Put a
card id into 67 test titles and every gate that counts "cards with a test" reads
green over a claim nothing checks.

**The rule.** A binding is a card id in the title of ONE live case whose
assertion fails when that card's producer breaks. Not a comment — a comment
over-reported by 18 cards on the measured run, and comments are invisible to the
thing that runs. Not a `describe` that wraps forty unrelated cases.

**A corollary worth stating.** Where a card's behaviour genuinely is
cross-cutting, bind it to the one case that most nearly isolates it and record
the others as related rather than binding. Two bindings that both fail for the
same underlying break are one binding and one duplicate.

---

## 3. Extend a flow to carry the task's step

Adding a step to an existing flow is usually right, and it has one trap: the
storyboard or flow contract that lists steps is often also the thing a *warm-up
or precondition* walks. A step added there is a step something now waits for.

Measured: one contract entry pointed at a region the pinned tenant could never
render. The precondition walked it, waited its full 90s ceiling, failed — and
Playwright skipped **all 18 dependent specs**. Every one reported
`passed=4 failed=1`, identical, and the message blamed a cold container while the
other 26 routes had warmed in 250-2700ms.

**Identical counts across independent specs mean one shared cause.** Read the
counts before the verdicts. When every spec in a suite fails the same way, look
at what they share — a setup project, a contract entry, a fixture — before
looking at any of them.

A step whose data the tenant does not hold is `blocked` with a measured reason,
not `auto`. Flipping it to `auto` without driving it is worse than leaving it
blocked, because the coverage figure starts counting it.

---

## 4. Find the mock's intent, not just its pixels

A design-of-record slice is an abstraction: a small composition standing in for a
region. It holds different words, different row counts, and no real data. That
has one consequence people rediscover expensively:

**Pixel-diffing a slice against a healthy build reports ~0% and is worthless.**

What the slice actually asserts is *intent* — which regions exist, their reading
order, their relative weight. Read three things out of it:

1. **The subject.** Which surface, at which state. A slice named for a builder is
   often the inside of a record, not the list route that shares its name — one
   measured entry pointed a list route at a slice depicting an in-record editor,
   and no assertion could have reconciled them.
2. **The depth manifest.** What the slice claims is on screen, as a list. This is
   what a sweep compares against.
3. **What it deliberately omits.** A slice showing three rows is not claiming
   three rows.

Where the slice and the task disagree, the task wins and the slice is stale —
record that rather than bending the assertion to match a picture nobody updated.

---

## 5. Compare, on geometry rather than on ratio

A whole-frame difference ratio cannot discriminate. Measured on a real one-step
spacing change:

```
558 divergent pixels of 1,296,000        ratio 0.00043   — every threshold passes
diff bounding box 114x13, density 0.377                  — unmistakable
```

Gate on the **bounding box and the fill density inside it**. The discriminating
property is not how much changed but how *concentrated* it is: a localised box at
high density is a defect, a scattered box at the same ratio is rendering noise.
The measured separation:

```
ratio 0.000431 for BOTH
  localised  box 114x13   density 0.3765  FIRES
  scatter    box 1381x829 density 0.0005  does not
```

**Two stable renders before filing.** Require the same mismatch twice, scored by
IoU of the two diff boxes — agreement is IoU ~1 with near-zero density delta.
Never retry a hard deterministic mismatch to obtain a green; that converts a real
defect into a flake.

---

## 6. Three verdicts on a capture, not two

A capture that cannot prove its subject is neither a pass nor a failure. Bind to
every image: requested route vs **resolved** route, body text length, the named
readiness element with its visibility and box, viewport, device scale factor,
theme, auth state.

It earns its place immediately. On its first run, one capture came back:

> `route-mismatch — asked for /settings, the page reported
> /dashboard?settings=account — a redirect, so the picture is of another surface`

That is real product behaviour (the route redirects and opens a dialog), so the
fix belongs in the map recording resolved routes for dialog-backed surfaces, not
in relaxing the gate. Without provenance that image files as a pass.

The failure it prevents is not hypothetical: four captures of a **login screen**,
143 characters of body text, were once filed as captures of the page under test.

---

## 7. Four ways the result lies

Each of these produced a confident wrong answer on the measured run.

**A written assertion can measure nothing.** One case asserted that no sparkline
painted a flat rule. It passed. It was then armed — the producer forced to emit
the exact defect — and it passed *again*. It had selected `svg path` and treated
anything with six numbers as a sparkline, which on that route matched 107 icon
paths, parsing arc parameters as coordinates. Underneath, the surface rendered no
sparkline at all. **Only arming finds this.** A gate that counts written
assertions cannot.

**An environmental fault contaminates every verdict.** On one run, 44 failures
across the suite traced to a single endpoint returning 400 because a model
credential was over its spend cap — 36 of one spec's 52. Those specs were not
broken and a run taken in that state cannot tell you whether they are. Before
triaging a broad red, check what the failures share.

**Load produces reds indistinguishable from real ones.** A suite run at load 75+
on 16 cores stalls and times out. A precondition that only checks for HTTP 200
will not catch it. Record the machine state with the run, and treat a red taken
under load as a re-run rather than a finding.

**A tracked-file gate cannot see an untracked file.** Instruments that enumerate
via `git ls-files` are blind to a new spec until it is staged. New evidence does
not count until tracked, and the symptom is a card that stubbornly reads
unguarded while its test sits green on disk.

---

## 8. Let a check run before it can block

The reason so much of this arrives late is that most pipelines offer two states:
wired, where one environmental red trains everyone to ignore the build, or not
run at all. On the measured product that second state is how an 867-step flow
apparatus came to exist and execute nowhere.

Add a third: a suite that **runs and records but cannot fail the job**
(`continue-on-error` or the harness equivalent). Promotion is the mechanism — a
suite earns the blocking list by running clean, and the flag comes off in the
same change that moves it.

State the promotion rule explicitly wherever you add this, because a permanent
report-only bucket is a suite nobody is fixing, and the whole value is that this
makes that visible rather than hiding it.

---

## What this file does not settle

- **The denominator.** Coverage here is coverage of the flows somebody chose.
  Branch coverage against an instrumented build is the honest answer and is a
  different, larger instrument.
- **Whether the mock was ever right.** Measuring the build against its design of
  record says they agree, not that either matches intent.
- **A card with no user interface.** Those verify on the seam — an assertion on
  the boundary the card changed, armed the same way — and the evidence type is
  recorded so an absent screenshot is never later read as an absent check.

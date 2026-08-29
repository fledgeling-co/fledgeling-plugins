# Evidence rules — what closes a claim, and what never does

**Canonical for the whole pipeline.** The worker, the verifier, gap-fix, and both conductors hold
every claim to these rules. They exist because a 110-ticket audit found 46% of requirements
delivered as specified while every completion note read as complete — and every safeguard that
failed was syntactic rather than behavioural. The licenses those failures used are revoked here.

## The typed evidence rule

Every requirement/clause row is typed, and its type decides what closes it:

- A **STATIC** clause (naming, schema shape, copy in source, a config value) may close on
  `file:line`.
- A **VISUAL** clause closes only on a pasted measurement — `getComputedStyle` /
  `getBoundingClientRect` / `elementFromPoint` values, or a screenshot path — from the rendered
  page. Never a class string: overrides get silently discarded, and source reading tells you what
  the code says, never what the app shows. (Read computed styles through **longhand** properties —
  `paddingTop`, not `padding`: measured on this machine, the shorthand resolves to `0px` on an
  element whose layout is correct, which passes a spacing assertion that should fail.)
- A **BEHAVIOURAL** clause closes only on an exercised request→response (verbatim status + body
  fragment) or a named test shown red→green.
- A **PERSISTENCE** clause ("X is written / ingested / scheduled / sent") closes on the
  spec-validation bar: name the producer at `file:line`, then **show a stored row / fired job /
  received message from a real run** — or classify it AUTHORED/MOCK and file the finding.

"In the code and typecheck clean" is never evidence for a visual, behavioural, or persistence
clause. **There is no partial status**: a row without admissible evidence is ✗, and there is no
"flagged rather than claimed" category — a row you cannot close is a blocker naming the row, and
the status stays put.

## Green gates prove nothing behavioural

A green gate is necessary but never sufficient. Typecheck plus a passing suite do not prove a
surface behaves: a test that stubs the unit under test hides exactly the runtime breakage it
appears to cover — the single most common way a broken feature ships past review with an all-green
gate. Never report a gate as passed that you did not actually run; a gate you could not run is a
**blocker, not an implied pass**, and a missing verdict is a **skipped gate, not a clean one**.

## The blocker protocol (two probes, a dissolution condition, re-test on clearance)

An unverified critical path is a **BLOCKER, not a finding**: the status does not advance and no
behavioural claim about that path may appear in any note or comment. Claiming verification is
environmentally impossible requires (1) the exact failing command and its output, and (2) a
**second, independent probe agreeing** — a `which <tool>` miss is not evidence of "no browser"
while the app answers HTTP and browser tools sit in your tool list. Record the blocker WITH its
dissolution condition ("blocked until the branch is served") and re-test the moment the condition
clears — merging to the served branch clears it. A blocker that survives a context compaction must
be **re-verified before it is restated**: re-run the probe, don't repeat the claim.

## Caveats propagate

Every blocker/✗ in a completion note appears **verbatim** in any later summary, merge record, or
closing comment. A closing claim may never be stronger than the evidence table beneath it —
laundering a hedge out of the retelling is how a known-broken feature reads as shipped.

## The regression-discrimination proof

For every behavioural requirement, the updated/added test is shown failing against the pre-change
code and passing after — both shas recorded (`red@<sha-before> → green@<sha-after>`). A test that
cannot fail against the old world discriminates nothing.

## MEASURED vs ASSUMED (upstream of the build)

Any triage or plan statement about how something currently *looks or behaves on screen* carries
`(measured: <browser evidence>)` or `(assumed from source — verify in browser before building on
it)`. A false "reference implementation" premise read off a class string becomes the worker's
unchallenged truth — a read-only review gate cannot catch it, because it reads code and does not
render.

## The browser lane and the serving ladder

Behavioural and visual evidence comes through the repo's browser tooling — Obscura on this
machine (`obscura serve --port 9222` over CDP, or the obscura MCP; localhost needs
`--allow-private-network` before the subcommand), or whatever the repo's CLAUDE.md names — with
the serving ladder for the recurring "worktree isn't served" blocker: (i) serve the worktree app;
(ii) if already merged to the served branch, verify on the merged stack *before* posting
behavioural claims; (iii) the browser MCP. For UI verification at scale, the `proctor:proctor` skill
governs computer/browser use. Two Obscura facts that change verdicts: CSS animations and
transitions never execute there, and web fonts never load — treat a pixel diff as a tripwire, not
a verdict, and suspect the engine before the page when a capture looks wrong.

## A screenshot is a claim about its subject, not just about its pixels

A visual clause closes on a screenshot path. That path asserts two things, and the
pipeline has only ever checked the first: **that pixels were captured**, and **that
they are of the thing under verification**.

A test campaign published 20 surface captures, cleared every gate it owned, and the
images were of three unrelated documents — a status report, a mock browser's index
page, a design doc. Twenty files held six distinct pictures. The only thing binding
a picture to a surface was its filename, and a filename is written by whoever ran
the capture, not by the app.

So a screenshot is admissible for a visual clause only when the evidence bundle
records, beside it:

- **what it depicts** — the requirement or surface id it is filed under;
- **where the channel was pointed** — the URL the browser *ended up at* (not the one
  it was sent to: a redirect to a login page is exactly the capture that otherwise
  gets filed as the dashboard), or the bundle path and window id for a native lane;
- **the channel** — the tool and version that took it;
- **its sha256**.

Two exact checks follow, and both are cheap enough that skipping them is never a
scale decision:

- **Untied.** The recorded target does not resolve to the route the requirement is
  about. Report the requirement `Unverified — blocker`, never `Done`.
- **Shared.** Two requirements' screenshots have the same sha256. One capture cannot
  be evidence for two different claims; the second is unevidenced.

Where a campaign exists, `test-campaign`'s `capture-lineage.py <dir> --gate` performs
both over the whole evidence set and exits 2 on either. Where one does not, the two
checks are still owed per requirement — they are a comparison of two strings and a
hash, not an instrument.

**A screenshot whose subject nothing corroborates is not a weaker pass. It is the
same status as no screenshot at all**, because a picture of the wrong screen and a
picture of no screen support a visual claim equally well, and only the first one
looks like evidence.

## Artifact-forcing: the bundle is the evidence, and the prose is not

Borrowed from `mockup-fidelity`, which measured why prose cannot carry this: agents
under effort pressure rationalise the shortcut, and models trained against
reward-hacking learn to *conceal* it rather than stop. The remedy is a precondition
rather than a stronger instruction.

- **No artifact, no verdict.** A requirement whose bundle directory holds nothing is
  treated exactly like a requirement missing from the list — it gets no status,
  however confident the exercise made you.
- **Every row cites the artifact it rests on**, by path and by the value read from it
  (`bundle/req-04.styles.json#submit.paddingTop = 24px`). A row citing your summary
  of an artifact is a TODO wearing a verdict's clothes.
- **Re-extract to close a fix.** After a change, re-run the measurement and overwrite
  the artifact. A row closes on a new artifact, never on the code change alone.
- **Partial is fine when labelled.** "structure measured, style layer unavailable (no
  CDP) — 3 rows pending" is honest. Grading those rows ✓ anyway is the failure.

## Assertions that cannot fail

Borrowed from `warrant:assay`. A suite can pass because it is not looking: an
`expect(...)` with no matcher, a matcher whose expected value is the actual value, a
constant compared to a constant, a `catch` that swallows the failure, an assertion
inside a never-awaited callback, a `skip`/`todo`, a discarded `expect.soft`, a spec
file with zero assertions.

Before leaning on any suite as evidence, scan the specs covering the changed surfaces
for those eight shapes. A hit is a **candidate**, not a defect — a skipped test is
sometimes correct and the scan cannot tell — but a suite whose green comes from one
of them proves nothing about the requirement it is cited for, and citing it is worse
than citing nothing because it consumes the reviewer's attention.

Where the repo carries `.warrant/`, `warrant:assay`'s `cannotfail_scan.py` does this
mechanically over a glob. Where it does not, grep the changed specs; the eight shapes
are all syntactic.

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
behavioural claims; (iii) the browser MCP. For UI verification at scale, the `proctor` skill
governs computer/browser use. Two Obscura facts that change verdicts: CSS animations and
transitions never execute there, and web fonts never load — treat a pixel diff as a tripwire, not
a verdict, and suspect the engine before the page when a capture looks wrong.

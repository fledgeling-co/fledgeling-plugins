# Evidence and identity — what gets kept, and what it is called

A campaign's output is not a reply and not a markdown report. It is a browsable
surface where coverage, flows, screenshots and components sit together, every row
carries an id somebody can point at, and the gaps are as visible as the passes.

This file is the contract that surface is built on: the identifiers, the artifact
bundle, and the rules that decide whether the page gets used or abandoned.

---

## 1. Identity — semantic, and yours

Assign your own ids. Every framework generates some, and every framework's are a
function of file paths, titles, parameters and adapter versions — so they change
when any of those change, and a migration silently orphans the history. Allure's
`historyId` and `testCaseId` are useful and worth storing; neither is identity.

```
REQ-004                    what the project says it does
SURF-009                   a surface — route, screen, portalled dialog, sheet
SURF-009.empty             a state of it; a state is its own thing to point at
FLOW-002                   a flow
FLOW-002.03                a step within it
CMP-011                    a component, platform-neutral
CASE-0117                  one check, one cell, one oracle rung
DEF-006                    a defect
RUN-2026-08-18-8f31        one execution, stamped with its commit
ART-RUN-...-SCREEN-ACTUAL  one artifact
```

Three rules make them worth having:

- **Stable across a harness migration.** The semantic id survives moving from one
  runner to another, or from web to a native lane. If renaming a spec file
  changes an id, it was a path, not an identity.
- **Every id is an anchor.** The page renders `id="CASE-0117"`, so a review
  comment, a commit message or a later session links straight to the evidence.
- **Cross-references are declared, not inferred.** A case names the requirement it
  verifies, the surface and transitions it exercises, its cell, its oracle rung
  and its evidence. That graph is what makes "what covers this requirement"
  answerable without reading any test code.

A component id is platform-neutral and the implementations hang off it:

```yaml
componentId: CMP-011                 # "primary button"
role: button
variants:
  state: [default, pressed, focused, disabled, loading]
  theme: [light, dark, high-contrast]
platformImplementations:
  web:          { storyId: ds-button--primary, selector: '[data-ui-id="CMP-011"]' }
  reactNative:  { storyId: ds-button-primary,  testID: CMP-011 }
  ios:          { accessibilityIdentifier: CMP-011 }
```

---

## 2. The artifact bundle

For every state worth a verdict, capture what the lane can actually produce, and
**tag the structure by platform** — a DOM snapshot, a React component tree and an
accessibility hierarchy are not interchangeable observations, and a schema that
pretends otherwise makes them incomparable later.

```
manifest.json          the ids this bundle belongs to
screen.png             the render
accessibility.yaml     the a11y tree (Playwright ARIA snapshots serialise this)
structure.json         DOM / RN semantic tree / XCUITest hierarchy — platform-tagged
style.json             resolved longhands, where the lane has them
geometry.json          quantised boxes
interaction.json       the steps that got here
console.log            what the runtime said
expected.png diff.png  only where a reference exists
provenance.json        commit, build, environment, device, fixture, baseline rev
```

**Provenance is not optional metadata.** Of 79 documented reproducible bugs in
one benchmark, 9 still reproduced later — selector drift, changed permissions,
dead services. A flow that does not version its fixtures, accounts, permissions
and environment alongside itself is not reproducible, whatever it says.

**Freshness is an assertion, not a footnote.** Evidence older than the
implementation revision it claims to show is stale, and a page that renders it
without saying so is lying quietly.

---

## 3. What the page must show

Nine sections, and the order is the reading order. `evidence-page.py` builds them:

| Section | The question it answers |
|---|---|
| **Coverage** | how much, out of how much — with the oracle mix and the armed ratio beside it |
| **Requirements** | what the project says it does, and what checked each one |
| **The wall** | every capture at once, pannable, so a missing or wrong state is visible without reading |
| **Flows** | storyboard frames with their per-step atoms and verdicts |
| **Surfaces** | each surface, its states, its cases |
| **Components** | the catalogue, per platform |
| **Defects** | what was found, with reproduction and status |
| **Not covered** | deferred requirements, blocked lanes, axes held fixed, cells dropped |
| **Methods** | how each lane was driven and what it could not observe |

**Not covered** is the section that makes the rest trustworthy. A page showing
only what passed is the coverage theatre the whole skill exists to prevent, and
its absence is invisible by construction.

Three properties, enforced in the builder rather than trusted:

- **Denominators everywhere.** `41 of 52` is a result. `41` is a claim.
- **Gaps rendered, not omitted.** An uncovered surface, an unarmed pass and a
  not-observable atom each get a visible row.
- **Regenerable.** The page is built from the artifacts, so it cannot drift from
  what was measured. Nothing is authored into it by hand.

### Used versus abandoned

Consistent across all three research panels — inferred from documented workflow
characteristics, since no retention study exists, and marked as inference:

A page survives when it is **generated automatically**, opens from CI and the
pull request, deep-links stable ids, answers *what changed and why*, puts
expected/actual/diff next to the flow that produced them, shows freshness and
retry history, and needs no duplicate manual authoring.

It is abandoned when it is a hand-updated status page, a screenshot gallery
without state context, or an inventory that cannot open the raw evidence.

**Own the manifest and the thin page; embed the commodity capabilities.** No
single product spans requirements, component stories, flow execution, visual
review and cross-platform evidence — they are mature per-layer and fragmented
across layers. Hosted rendering, visual review and issue-tracker governance are
worth buying when they earn it. The identity graph is not.

---

## 4. The judge, and its ceiling

A model can read a capture and say whether it shows what the step promised. That
is genuinely useful and it is **never a gate**. The measured ceiling: an LLM used
as a non-crash functional oracle detected 49% of bugs, with randomness and false
positives; the strongest exploratory GUI agent reached 48.90% F1. Neither number
belongs on a release path.

So the judge runs nightly and advisory, and it is constrained in four ways that
each fix an observed failure:

- **Atoms, not impressions.** A step declares the specific things its capture
  should show. The judge answers each one `pass` / `fail` / `not-observable`, and
  only a **contradicted** atom fails. This is what stops "looks fine" and
  "something seems off" from being verdicts.
- **`not-observable` is a first-class answer.** A still picture cannot show that
  a click persisted. Forcing a binary verdict there manufactures both false
  passes and false failures.
- **Pin the model and the ordering.** A judge whose model floats is measuring the
  model. Where two candidates are compared, swap their order and treat an
  unstable verdict as a tie.
- **Findings are hypotheses.** A judge finding becomes a `DEF-*` only after a
  deterministic check reproduces it. Untriaged model output on a dashboard is how
  a dashboard loses credibility.

Two agent failure modes are worth naming because they look like success:
**goal-oriented masking**, where an agent routes around a broken operation and
completes its task rather than reporting the breakage; and **execution-bias
attribution**, where it assumes a failure was its own bad click. Both produce a
clean run over a broken product.

---

## 5. Where the artifacts live

Beside the campaign, not in the source tree:

```
<campaign-dir>/
  campaign.json      the facts: project, lanes, axes, declared sample, design of record
  inventory.json     requirements, surfaces, flows, components
  cases.json         what was checked, its rung, its status, its evidence
  ledger.md          generated, for a human reading in a terminal
  evidence/          the bundles
  evidence.html       the page
```

Everything in `evidence/` is disposable and regenerable; everything in the three
JSON files is the record. Captured payloads from a live tenant are **not**
committed — an unpublished draft belonging to a real company is market-sensitive,
and a fixture corpus derived from consumer types serves the same purpose without
the exposure.

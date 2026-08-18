# Measurement enforcement — make the measurement non-skippable, then prove it

This skill's failure mode isn't bad taste — it's an agent that *feels* like it verified while skipping the measurement and grading from screenshots, source, and reasoning. Two pieces of evidence say this can't be fixed with stronger wording:

- **Vision is too weak to be the check.** Frontier multimodal models top out near **40% recall on fine-grained UI diffs (<23% on hard cases)** — so "the screenshots match" cannot be the audit.
- **Telling an agent not to skip doesn't hold.** Agents under effort/latency pressure rationalize the shortcut; models trained explicitly against reward-hacking learn to *conceal* it ("obfuscated reward hacking") rather than stop. Prose loses; **programmatic artifact-forcing wins.**

So the integrity of the audit rests on a precondition (an artifact must exist) and an independent check (a critic that reads only the artifacts), plus a regression eval that proves the whole skill still catches planted defects.

## 1. The artifact contract

Per screen / gated state, the workspace must contain four extracted files before any verdict for that screen:

```
.mockup-fidelity/<screen>/
  ref.structure.json      # mock: parsed DOM tree — {role, text, flexDirection, frame{x,y,w,h}, children[]}
  ref.styles.json         # mock: getComputedStyle per element, full untruncated values
  target.structure.json   # app: ordered NESTED tree with containment + flexDirection + frame{x,y,w,h}
                          #      (axe describe-ui / Maestro hierarchy / in-app harness — NOT a flat node list)
  target.styles.json      # app: resolved styles per node (getComputedStyle web / in-app StyleSheet.flatten native)
  ref.png / target.png    # supplementary screenshots — for spatial fallback only, NOT evidence
```

Rules that make this load-bearing rather than decorative:

- **The ledger is generated *from* these files.** Every `present/divergent/absent` cell and every ✓ names the artifact values it compared (e.g. `target.styles.json#searchBar.placeholderColor = #5E6A82` vs `ref … #9CA0AC`). A cell with no artifact reference is a TODO, not a finding.
- **No artifact → unaudited.** A screen with no `target.structure.json` is treated exactly like a screen missing from the inventory — it does not get a verdict, however confident the screenshots made you.
- **Re-extract to close a fix.** After an edit, re-run the extractor and overwrite `target.*.json`; a row closes on a new artifact diff, never on the code change alone.
- **Partial is fine if labelled.** "structure measured, style layer unavailable (no CDP) — N rows pending" is honest. Grading those rows ✓ anyway is the failure.

## 2. The completeness-critic (run before declaring done)

Spawn one sub-agent (or do a disciplined self-pass) given **only** the artifact directory and the ledger — *not* the app, the mock, or your reasoning. Its single job is to reject ungrounded verdicts. Prompt shape:

```
You are auditing a UI-fidelity ledger for fabricated verdicts. You may read ONLY:
  - the ledger, and
  - the files under .mockup-fidelity/<screen>/.
You may NOT open the app, the mock, or any source file.

For each in-scope screen, return pass/fail on:
  1. ARTIFACTS_PRESENT — do all four .json artifacts exist and parse?
  2. LEDGER_CITES_ARTIFACTS — does every present/divergent/absent cell and every ✓
     name a value drawn from those artifacts (not a screenshot, not "looks like",
     not a source quote)?
  3. ABSENCES_GROUNDED — is every "absent" backed by the node genuinely missing from
     target.structure.json (present in ref, absent in target)?
  4. NO_VISION_OR_SOURCE_VERDICTS — does any row's evidence reduce to a screenshot
     comparison or a code-read? If so, fail it.
Return JSON: { screen, checks:{...}, failed_rows:[...], verdict:"pass"|"fail" }.
Default to FAIL on any uncertainty.
```

Any `fail` sends that screen back to Phase 2 for real extraction. The critic is deliberately blind to the UI so it can't be talked into "it obviously matches" — it can only confirm that the paperwork is real.

## 3. Seeded-defect eval — prove the skill still catches planted gaps

Don't trust that the skill works because it reads well; measure its catch-rate against known answers, and re-run it whenever you edit the skill.

**Construct the set.** Take a screen that currently matches and plant ~10 defects of *different classes*, one per variant branch. Record the ground-truth answer key. A working set, with the two shipped fixtures in `evals/`:

| | Defect | Class |
|---|---|---|
| D1 | remove a whole card | absent |
| D2 | change a label ("Editor's picks" → "Movers today") | content |
| D3 | colour drift (`#9CA0AC`→`#5E6A82`) | colour |
| D4 | remove a `box-shadow` | **unmeasurable in this engine** |
| D5 | change `padding-top` 16→24 | spacing |
| D6 | flip a card `flex-direction` row→column | layout |
| D7 | remove `text-transform: uppercase`, same source text | **unmeasurable in this engine** |
| D8 | remove a button's trailing arrow `<svg>` | icon (presence-only here) |
| D9 | change `border-radius` 12→4 | radius |
| D10 | replace a CSS `linear-gradient` with a flat colour | **unmeasurable in this engine** |

**Three of those ten cannot be measured here, and that is the point of including them.** A previous
version of this eval seeded a removed shadow and an all-caps→title-case header, set the bar at "10/10
catch with 0 false-pass", and reported both as passes — so the harness certified a skill that was silently
2/10 short. An eval whose answer key assumes every class can run will bless exactly the failure this
skill exists to prevent.

So the answer key is **three-valued, matching the tool**. Per planted defect, the run must produce one of:

- **CATCH** — a finding naming the property, or a labelled presence-only finding where that is the
  honest ceiling (D8: a missing arrow is caught by svg presence; a *swapped* glyph would not be, and a
  fixture that planted one should expect INCONCLUSIVE);
- **DECLARED INCONCLUSIVE** — the capability appears in `inconclusive[]` with its reason, so the defect
  is an open question rather than a closed one (D4, D7, D10);
- **FALSE PASS** — neither. This is the only failing outcome, and the number to drive to zero.

**Target: 0 false passes, and every INCONCLUSIVE row traceable to a capability in the preflight.** Report
catches and declared-inconclusives separately; a rising catch-rate that comes from reclassifying an
inconclusive as a catch is a regression wearing a promotion.

**Two controls, both required.**

- **An identical pair.** Expect zero findings, and expect the *same* inconclusive list — a control that
  comes back conclusive means the preflight is not running. `--assert --allow-inconclusive` must exit 0;
  plain `--assert` must exit 3, because nine unasked questions remain unasked on an identical page too.
- **A stubbed reader (mutation of the checker).** This is the control that tests the *detector* rather
  than the skill. Force one working reader to return `""`, then a fixed constant, then an all-zero rect,
  and assert that each yields INCONCLUSIVE and never PASS. A detector that cannot notice its own
  blinding is the vacuous-truth case in its purest form, and the engine will not always be kind enough to
  demonstrate it for you.

**Grade the trajectory, not just the prose.** Two assertion kinds:

- `trajectory:tool-used` — the run **fails** if it produced a verdict without invoking the harness and
  writing the artifacts. An agent that "concluded" without the tool traces is failed mechanically, before
  anyone reads its findings.
- **The exit code.** `capture.mjs --assert` is the deterministic half: a planted-defect fixture that
  exits 0 has failed the eval regardless of what the prose says.

> Keep the eval honest: rotate which screen and which defect classes you seed so the skill can't overfit
> to a fixed answer key, and keep both controls in every run.

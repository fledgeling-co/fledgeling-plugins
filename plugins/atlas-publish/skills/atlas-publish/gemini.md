# atlas-publish, calibrated for Gemini

Read this once before Step 0, then run the skill as written with these overrides.

The skill's opening ends on the sentence the run turns on: `The one thing you do not do is make any of
it reach an end user.` That is a limit of **zero** on five named MCP tools, written as prose — as are
most load-bearing rules here. On this family such a rule gets read and agreed with while the value
underneath comes from somewhere else, so what follows turns each into a cell to fill.

## Route out before you start

Two of this run's work shapes sit where flash-tier Gemini measures well behind opus, inside the pipeline.

| shape | where it lands in this skill | measured, gem@med vs opus |
|---|---|---|
| `brownfield-integration` | Step 3's `apply fixes for real findings, push to the PR branch`; Step 4's conflict resolution; Step 5's `add or update the vitest suites (pure lib/) and the Maestro flows the change needs` | 24 against 50; the brownfield bucket scored a hard zero on **79%** of decided rows |
| `regression-sensitive` | Step 2's DTO key-set diff, where a removed field breaks phones that have not updated; Step 5 leaving `pnpm turbo run lint typecheck test` green; Step 10's pre-push gate | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

**[docs]** Under **Task outside of model capabilities**: *"Avoid using prompts that ask the model to
perform a task for which it has a known, fundamental limitation."*

**[measured-family]** The numbers are `geminify/references/evidence.md` §2.1 and `modules.md`'s shape
table. `static-page` and `visual-design` are omitted: this skill authors no self-contained page and
judges nothing rendered. With no lane available, the value here is knowing which output to distrust.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, verbatim from `geminify/references/gemini-corpus.md`. The strongest tier, and most of this file rests on it. |
| `[measured-family]` | Two Gemini sessions of *other* skills (`Egress Gemini` 2026-08-17, `COD Dossier` 2026-08-23, **n=1 each**) and the 106-task `diolog-2.0` benchmark. None ran this skill. |
| `[measured-here]` | **Not used.** No Gemini run of `atlas-publish` has been observed, so the tier meaning "measured on this skill" stays empty rather than being filled with something weaker. |
| `[derived]` | My reasoning from the two above — and `scan_skill.py` over this SKILL.md and its six references, re-run 2026-09-01: 899 lines, 5 quota rows, **0** bound rows, 4 relative qualifiers, 68 prohibitions and 44 distributive phrases counted as prose, **0** emphasis tokens, **0** qualitative skill references, 2 modules above threshold. That is a scan of the text, not a run. |

**The tier the evidence is about, and what is unmeasured.** Every measured rate here is flash-tier —
`gemini-3.7-flash` on the benchmark, `gemini-3.7-flash-high` on one session — so on the Pro tier the
overrides hold as `[docs]`-grounded discipline and every `[measured-family]` number is open. No Gemini
run of `atlas-publish` has been observed, and the skill's own `references/evidence.md` records it has
not been run end to end on any model, so nothing below is measured on this target: not the draft
boundary, not the cert-parity gate read for its passed line, not the wave reconciliation or review count.

**[docs]** A caution about this file's own shape: *"Avoid writing a prompt with non-linear logic or
conditionals that require the model to piece together fragmented instructions from multiple different
places in the prompt."* Read it in one pass; each override names its step.

## What transferred intact

- **The evidence rule is already C2, better written than this file would state it** — six irreversible
  steps, each with the observable to read back and the condition that fails it. **[docs]** *"Verify
  your claims by quoting the exact applicable information (including policies) when referring to them."*
- **Three-state gate reporting is there, with a worked example**: the cert-parity paragraph names the
  observable rather than the exit code — `the committed cert verifies a signature made with the
  configured private key` must read passed, not skipped. The `gate` module's hardest rule, written.
- **The pipeline is already a sequential artifact chain**, so C4's conversion has nothing to do, and its
  one skill composition is artifact-gated and now named in full: Step 3 calls `code-review:code-review`
  once per PR number, output a posted `gh pr comment <n>` — an executable call rather than a lens.
  **[derived]** the scan finds zero qualitative skill references; **[measured-family]** the session
  measured with the lens phrasing skipped both invocations and passed its own gate cleanly.
- **The skill does not shout** — zero `MANDATORY` / `CRITICAL` / `FORBIDDEN` tokens — and its forks are
  closed sets already: one 40-hex comparison decides the lane, `minAppVersion` defaults to unset,
  `submit:true` is off unless asked. **[docs]** Google's remedy for a model that answered correctly but
  *"didn't stay within the bounds of the options"* is a closed choice; done.

## The quota ledger — filled, not described

**[derived]** The scan returned 5 categorical rows over 899 lines. I bound **4** and dropped **1**
as prose (`references/evidence.md:9`, which names nothing a run delivers) plus both relative-qualifier
rows: SKILL.md:105 `Clean` is defined in its own clause as `git status --porcelain` empty, and
`store-lane.md:17` `brief` is a noun. Row one is **derived rather than scanned** — the scanner has no
countable-deliverable entry for "PR", so `Review every open PR` never reaches its output.

**[docs]** *"Instead, provide objective constraints"*. Write this into the run's first message with
your own numbers; report the fractions at Step 11. Filled from a three-PR OTA wave, fifteen files:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| `Review every open PR` × one review per PR number — SKILL.md:158 **(derived row)** | 3 PRs × 1 posted review = **3** comment URLs | 3 posted, 2 with findings applied and pushed | `3/3 reviewed, comment URLs listed, 2 branches pushed` |
| `Each step`'s named abort path, decided before the step — SKILL.md:186; `failure-modes.md:170` | **11** rows, Steps 0–10, each read before its step runs | 11 read, 1 fired (Step 0) | `11/11 aborts read in advance; trap 3 fired at Step 0` |
| `any check failed or not-run` — `failure-modes.md:172`; the six preconditions at SKILL.md:103 | OTA lane: **5** applicable checks × one of three states | 4 passed, 1 not-run | `5/5 reported: 4 passed, 1 NOT-RUN (OTA_CERT_PARITY_KEY unset)` |
| `Report each claim from what you read back` — `handoff.md:31` | 3 PR claims + 1 lane + 3 gates + 2 artifacts = **9** claims, one read-back each | 9 | `9/9 claims carry the command that produced them` |
| `every token` minted immediately before its own upload — `ota-lane.md:68` | 1 launch asset + 14 changed assets = **15** files × (mint · PUT · `curl -sSI`) = **45** cells | 45 | `15/15 uploaded, 15/15 read back 200 with matching content-length` |

**[measured-family]** Why a table rather than the sentence: on the observed run every *enumerated*
requirement shipped — twelve named features — and every *categorical* one shipped once or not at all.
**[derived]** Row one is the one to watch: Step 4 reconciles merges against the Step 1 set, nothing
reconciles reviews, so extend that reconciliation to Step 3 with the same stop condition.

## The bound ledger — the half the scan could not list

**[derived]** `scan_skill.py` returned **0** bound rows and counted **68** prohibitions as prose —
the regex working as designed, and this skill's exposure: its limits are worn as prohibitions rather
than numbers, so these rows move into the ledger by hand. **[measured-family]** That is the failure
which reaches a passing-looking artifact: 58% of a Gemini run's failing UI assertions at `medium` and
**86%** at `high` were bound-shaped against 8% for opus, and the most-repeated one failed on *every*
instance in its set while the same run passed 37 of 39 other assertions.

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model
must adhere to when generating a response, including what the model can and can't do."* — and the
**Recap** component is a *"Concise repeat of the key points of the prompt, especially the constraints
and response format, at the end of the prompt."* Filled, read off the run rather than off the skill:

| Bound, and where the skill states it | Stated limit | Readback | Observed | Within? |
|---|---|---|---|---|
| `publish_bundle`, `publish_app_version`, `retract_bundle`, `retract_app_version`, `set_min_app_version` — SKILL.md:30 | **exactly 0** calls, each | `list_releases` — every row this run created reads `status: draft` | bundle 4 draft, no version row | yes |
| Subagents for one release run — SKILL.md:200 | at most **3** | count the Agent calls in this session | 1 (Step 3, three PRs) | yes |
| Model-drafted release notes — SKILL.md:162 | **exactly 0** lines authored by the run | `git log -1 --format=%an -- TestFlight/WhatToTest.en-US.txt`; text came from the founder verbatim | founder text, 4 lines, committed before the tag | yes |
| `--delete-branch` on a PR that is another PR's base — SKILL.md:159 | **exactly 0** | `gh pr list --json number,baseRefName` before merging, then `git ls-remote --heads origin` | #14 is base for #15 — merged without the flag | yes |
| Re-registering a consumed id — `ota-lane.md:116`, trap 9 | **exactly 0** retries of the same `bundleNumber` or `CFBundleVersion` | `get_release { bundleNumber: N }` before any re-attempt | 409 on 3, went forward to 4 | yes |
| `SKIP_VERCEL_BUILD=1` / `SKIP_GATE=1` / `SKIP_PREBUILD=1` — SKILL.md:165, `store-lane.md:35` | **0** unless its one named case; using one forces that gate to report not-run | grep the invoked command line | none set | yes |

**[derived]** Row one is why this is a ledger and not a paragraph: the run reaches those five tools with
valid arguments, a founder present and the artifact in hand — the position where one more well-formed
call looks like finishing the job.

**[docs]** The agentic template's last rule is the one to carry into Steps 9 and 11: *"Inhibit your
response: only take an action after all the above reasoning is completed. Once you've taken an action,
you cannot take it back."* And *"Place essential behavioral constraints, role definitions (persona), and
output format requirements in the System Instruction"* — so restating the boundary there is not padding.

## Override 1 — gates and read-backs ship receipts (Steps 0, 2, 4, 5, 8, 9, 10)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* And *"Review your output against the user's task."* **[derived]** Skills here are written
for a model that over-verifies, so verification scaffolding gets stripped; inheriting that removal is
the defect. **[measured-family]** What fills the vacuum is
well-formed and false: a review naming a browser engine that never ran, and a 100% contrast pass rate
measured afterwards at 3.65:1 on every button.

```
GATES — release OTA, bundle 4
  dev-doctor.sh --strict        exit 0   vercel CLI present, 3/3 project links
  dto-contract.test.ts          exit 0   18 passed, 0 skipped
  ota-cert-parity.test.ts       exit 0   NOT-RUN — the live parity assertion read SKIPPED
                                         (OTA_CERT_PARITY_KEY unset) → OTA lane stopped here
  turbo run lint typecheck test exit 0   4 packages, 212 tests, 0 skipped
```

**[measured-family]** Prerequisite receipts are what this skill's gates lack. On `COD Dossier` an
auditor checked tags, citations and contrast floors, had no check that its upstream artifacts existed,
and returned exit 0 over two skipped invocations. Two apply here: before the Step 8 archive,
`git log -1 --format=%H -- TestFlight/WhatToTest.en-US.txt` must name a commit from this run over a
non-empty file, and before Step 9's `register_bundle`, `dist/metadata.json` exists and the greps at
`ota-lane.md:26` ran as stated.

**[derived]** The same rule makes the skill's read-back table an artifact rather than a reference: one
row per irreversible step taken, filled from the command's output. The two cells that go missing look
redundant beside a success return — `curl -sSI <url>`'s `200` and matching `content-length`, and
`get_release { bundleNumber: N }`'s `launchAssetUrl`.

## Override 2 — the retry ceiling, and where it inverts (any step that shells out)

**[docs]** *"On other errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Four consecutive invocations of one banned, absent tool with nothing changed
between them, and four consecutive `Read` calls against a hard 25k-token ceiling before pivoting to a
Python split. So: two attempts per tool, then change approach; a permanent error gets one, and a
capacity error pivots on attempt **1**.

**[derived]** Then the inversion this skill makes explicit and no general rule covers: past the
TestFlight upload and past a successful `register_bundle`, **zero** attempts are correct, not two — the
id is consumed, a re-registration returns 409, and recovery is forward to the next id.

## Override 3 — read the named file, then answer (Step 0, and every step that names a doc)

The skill's own instruction is the rule: `open the one the current step names rather than
reconstructing it`. Treat it as two ordered steps — load, then answer. **[measured-family]**
`COD Dossier` §1.2.4: asked a question naming three skills, the run answered from memory; asked to fix
that, it inverted the error and launched a skill instead of answering.

**[docs]** *"Your knowledge cutoff date is January 2025."* For this model, *"The knowledge cutoff date
for Gemini 3.7 Flash is March 2026"*. Three values here are recall traps, because a wrong-but-plausible
answer passes every downstream check: the fastlane `xcargs` flag names (trap 4), the `register_bundle`
field mapping (`ota-lane.md:35`), and the OTA channel's state, which `classification.md:86` re-checks
with `list_releases` and `cat ota/bundle.json`.

## Override 4 — the delegation cap and the skill call, both written down (Step 3)

The skill already caps the first: three subagents per run, two named uses, none running git operations
because Step 4's reconciliation needs one process owning the ref. Write the number down rather than
carrying it: `subagent budget 3 — 1 used (Step 3), 2 unspent`. **[docs]** *"You have a limited action
budget"* is Google's own phrasing, from the tool-budget system instruction.

The second is what changed in the skill: Step 3 now names `code-review:code-review` in full, which is
the string the Skill tool takes. **[measured-family]** A bare plugin-skill name came back `Unknown
skill` ten times in one recorded session while its directory sat in the cache throughout; and another
session wrote that it had `executed their underlying scripts directly rather than re-issuing duplicate
Skill tool calls` for skills it had never invoked. The call discharges the step, not a conforming
review. One row per PR from the Step 1 set, filled at the moment of the call:

| PR | Skill call | posted `gh pr comment` | findings applied |
|---|---|---|---|
| #12 | `code-review:code-review`, turn 31 | …/pull/12#issuecomment-… | 0 |
| #14 | `code-review:code-review`, turn 38 | …/pull/14#issuecomment-… | 2, pushed 4a1c9e2 |
| #15 | `code-review:code-review`, turn 44 | …/pull/15#issuecomment-… | 1, pushed 77bd310 |

**[docs]** And on the forks that stay live — patch versus minor at Step 6, whether `minAppVersion`
applies — resolve each in writing at its step, one line, before acting: *"Avoid premature conclusions:
There may be multiple relevant options for a given situation."*

## One worked example, before the set (Step 9)

**[docs]** *"We recommend to always include few-shot examples in your prompts."* And *"you can remove
instructions from your prompt if your examples are clear enough in showing the task at hand."* Author
asset 1's triple at full fidelity before the other fourteen, then repeat the shape:

```
file 1/15  dist/_expo/static/js/ios/index-8f3c.hbc   2,214,880 bytes
  mint     request_bundle_upload { pathname: "ota/fd05b8d3…/4/9a1c…e7.hbc" } → 600s token
  put      @vercel/blob put(…, { access:'public', addRandomSuffix:false, allowOverwrite:true })
           → https://…blob.vercel-storage.com/ota/fd05b8d3…/4/9a1c…e7.hbc
  readback curl -sSI <url> → HTTP/2 200 · content-length: 2214880 · MATCHES local
```

**[docs]** *"Make sure that the structure and formatting of few-shot examples are the same to avoid
responses with undesired formats."* Same for the Step 0 preconditions and the Step 11 hand-off rows.

## `thinking_level`, and where brevity bites

**[docs]** An eleven-step release with two gated lanes and six irreversible steps is what Google
describes `HIGH` as being for — *"suitable for complex prompts requiring deep reasoning, such as
multi-step planning, verified code generation, or advanced function calling scenarios"*. 3.7 Flash
defaults to `MEDIUM`, and the defaults have moved: *"If thinking_level is not specified, Gemini 3 will
default to high"*, then *"The default thinking effort is now medium, changed from high in Gemini 3
Flash Preview."* **[measured-family]** Write that as what the level is *for*, never as a remedy.
Paired across 106 benchmark tasks, `high` beat `medium` on 24, lost on 24 and tied on 58 — mean −1.7 points — and its
bound-shaped failure share went *up*, 58% to 86%. Neither ledger above improves by raising it.

**[docs]** One trade-off applies to a step-counted run: *"Higher thinking levels encourage the model to
use more tools to explore and verify, so lowering the level can reduce tool calls."* And *"By default,
Gemini 3 models provide direct and efficient answers."* Brevity is the resting state and the skill asks
for terse narration, so both survive. What must not be trimmed is the gate receipt, the read-backs and
the NOT-RUN lines.

## Modules deliberately not written

**[derived]** The scan fired two above its three-trigger threshold — `gate` (7 hits) and
`delegation` (4). I added **`bounded-constraint`** by hand: it matched one trigger and zero numeric
bounds, but the scan counted 68 prohibitions, and geminify's instruction moves a prohibition on a
countable property into the ledger by hand. The zero-publish rule is this skill's reason for existing.
Seven did not fire and are not written. **`visual`** — nothing is rendered. **`states`** — no state
matrix; the three-state gate vocabulary is C2's. **`platform-values`** — the vendor values (Xcode 26.4,
fastlane 2.236.1, `@vercel/blob` 2.4.0) are read from the repo at Step 0, so Override 3 carries it.
**`authorship`** — the one prose deliverable is the release notes, which the founder writes and the run
does not. **`injection`** — PR diffs are the run's own repo. **`count-contract`** — folded into the
quota ledger. **`emphasis`** — zero emphasis tokens.

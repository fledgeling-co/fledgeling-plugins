# create-swe-project (slipway), calibrated for Gemini

Read this in one pass before `## 0 — Doctor`; every override names the section it lands on. This target's largest
deliverable holds no model-authored bytes — `your job is the **decisions**, and the script's job is the **files**` —
so almost everything below is about `## 5 — The launch pipeline` and `references/launch-pipeline.md`, whose eight
phases of authored HTML, prose and judged aesthetics sit in the two shapes the corpus measures this family collapsing
on. Updated against the 2026-08-30 revision, which added Phase P and a traceability-matrix PRD (Overrides 1 and 4).

## Route out before Phase D starts

**[docs]** The prompt health checklist says it outright, under **Task outside of model capabilities**: *"Avoid using
prompts that ask the model to perform a task for which it has a known, fundamental limitation."* Four deliverables
land in shapes measured far enough behind that handing them off beats trying harder.

| shape | where it lands here | measured |
|---|---|---|
| `static-page` | Phase M's `design/marketing/index.html`, and every standalone frame in `design/mocks/html/` | 22 against opus's 67, a hard zero on 71% of decided rows |
| `visual-design` | Phase M's quality bar; Phase D's direction pick | 35 against 63 |
| `brownfield-integration` | §4's fix-forward on a failed gate, and *Improving the templates* | 24 against 50 |
| `regression-sensitive` | `upgrade.sh --apply` and `canary.sh`, where four permutations currently pass | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

A pointer rather than a pinned model, because the numbers move; where no lane is free, its value is naming what to
distrust first — the marketing page's *bounds*, before its content. **Omitted:** `greenfield-module`, `algorithmic`,
`accessibility` and `react-ui` are level (75/75, 75/75, 64/69, 63/69); §0–§3, because `scaffold.sh` writes those
files; and `PRD.md`, because a document is not one of the four measured shapes.

## What transferred intact

- **Script-first is already this family's remedy**, and `references/research-notes.md:7` reached it independently.
  Both collapsed benchmark buckets are a model authoring or editing code; a deterministic render is neither.
- **Phase P is the artifact-gated conditional done right**, and the model the rest of §5 should copy: `Check if
  docs/positioning/00-decision.md or docs/positioning/10-territory-*.md exists`, invoke the skill when it does not,
  then `Anchor to Decision of Record` — a file test driving the invocation, and a later phase reading what it
  produced. This revision also spelled every skill name in full (`positioning:positioning`, `shipyard:intake`); a bare
  name returns `Unknown skill` and fails silently, so that removed a class of skipped step.
- **The interview is already a closed set** (thirteen modules, `window` or `menubar`, `direct` or `mas`), Google's own
  remedy for an answer that strays out of bounds; and **several requirements are already numbers**, the one shape the
  corpus shows surviving — `at most 4` questions per call, `0–2` Dossier queries, `3 tiers max`, `≤300KB`.
- **Grounding is already written in** (launch-pipeline.md:5): `Nothing in those four states a market claim the
  research or the owner didn't supply.` Phase R anticipates the recall failure too — `Read every report in full. Not
  outlines`. And the scan finds zero shouted directives across 315 lines, which **[docs]** is the right register:
  *"Avoid unnecessary or overly persuasive language."*

## Epistemic status

`[docs]` throughout, quoted verbatim from Google's published guidance. `[measured-family]` from two Gemini runs of
*other* skills (2026-08-17 and 2026-08-23, n=1 each) and the 106-task `diolog-2.0` bench read 22 August 2026.
`[measured-here]` **none** — no Gemini run of create-swe-project exists. `[derived]` marked inline. Every measured
rate is flash-tier and none should be projected onto Pro; **[docs]** defaults drift across the family — *"If
thinking_level is not specified, Gemini 3 will default to high"*, then *"The default thinking effort is now medium,
changed from high in Gemini 3 Flash Preview."*

**Unmeasured on this skill:** nothing here is `[measured-here]`, and there is **no evidence these overrides work** —
nothing has been measured with a `gemini.md` in place against the same brief without one. Nothing about §0–§3, since
the bench watches a model *building* rather than interviewing, and the claim that a bash render is model-independent
is `[derived]`. Nothing about Phase R or Phase P, which is newer than every observation cited here; and the rates are
corpus-shaped (106 tasks of one product's TypeScript / React / NestJS work). **[docs]** One self-limitation — a
conditional side-file is the **conflicting internal references** shape the checklist warns about: *"Avoid writing a
prompt with non-linear logic or conditionals that require the model to piece together fragmented instructions from
multiple different places in the prompt."*

## Override 1 — the inventory is a filled ledger, not a checklist in prose

Lands on §5 phases B, O and D, and on Phase D of `references/launch-pipeline.md`, which asks twice already: `every
screen gets its empty, loading, and error states, not just the happy path`, and `Inventory before authoring … A mock
set without an inventory silently drops states.` **[measured-family]** A run carrying that shape delivered every
requirement its brief *enumerated* — twelve named features, all present — and every categorical one once or not at
all: all surfaces → 5, all states → **1**, all menus → **0**, all flows → **0**. The count has to become a cell to
fill and a fraction to report. Write this into `design/mocks/html/INDEX.md` first:

| scope | where | denominator | filled |
|---|---|---|---|
| briefs seeded | launch-pipeline.md:31 | 5–12, chose 8 | 8 written · 8 index rows |
| PRD requirement rows | launch-pipeline.md:44 | 1 per brief = 8 | 8 / 8 traced, brief slug in each row |
| PRD sections | launch-pipeline.md:43 | 6 named + 4 non-functional | 10 / 10 |
| positioning values anchored | launch-pipeline.md:12 | 4 (territory · hero line · category frame · beachhead) | 4 / 4, into PRD + OVERVIEW + copy |
| surfaces mocked | launch-pipeline.md:55 | 9 (web 5 · admin 2 · login · waitlist) | 9 / 9 |
| states per surface | launch-pipeline.md:55 | 9 × 3 (empty · loading · error) = 27 | 24 built · 3 `n/a: static marketing frame` |
| menus, modals and sheets as their own frames | launch-pipeline.md:55 | 6 | 6 / 6 |
| flows passed by ux-craft | launch-pipeline.md:59 | 5 (nav · form · onboarding · sign-in · return paths) | 5 / 5 |
| Dossier reports read in full | launch-pipeline.md:25 | 2 runs | 2 read · 2 exported |
| icon takes on the audit sheet | launch-pipeline.md:65 | 4 takes × 7 columns = 28 | 28 / 28 |
| phase reports | launch-pipeline.md:3 | 8 boundaries (P · R · B · O · O½ · D · M · L) | 8 / 8 |

Every `n/a` carries its reason; an unrecognised cell counts as open. **[docs]** That is **Ambiguity** — *"Avoid using
subjective or relative qualifiers that lack a concrete, measurable definition."* — applied to `comprehensive` at
launch-pipeline.md:3 and SKILL.md:66, plus **Underspecified task**: *"provide instructions for handling missing data
rather than assuming inserted data will always be present and well-formed."*

**The row this revision added, and the one most likely to collapse.** Phase O now says the PRD `Must cover **ALL**
feature briefs in docs/features-to-triage/*.md with complete traceability` and `Every seeded brief … must trace to an
explicit requirement row.` A categorical quantifier in bold is still categorical: `n` briefs on disk → `n` rows
carrying the brief's slug, counted both directions. **[docs]** The agentic template asks the same of a plan — *"Ensure
that all requirements, constraints, options, and preferences are exhaustively incorporated into your plan."* Phase O
also wants three documents in one pass, the **Too many tasks** shape: *"Break the requests into separate prompts."*
Write PRD.md, then OVERVIEW.md, then MARKETING-FEATURES.md, each reading the last.

`[derived]` **From the scan:** 15 quota rows, 9 printed, six kept above. Three dropped — `each surface` (:57)
duplicates the surfaces row, `every file` (SKILL.md:51) is `scaffold.sh`'s guarantee rather than a phase's delivery,
and `every image` (:73) is `audit_sheet.py`'s job. `states` and `count-contract` fell under the trigger threshold on
vocabulary rather than substance, so both became rows rather than sections.

## Override 2 — a phase report's numbers carry the command that produced them

Lands on §4, §5's `Commit per phase`, and the Wrap-up report at launch-pipeline.md:126. **[docs]** Verification is
something the prompt must contain: *"Include specific verification steps in either the system instructions or your
prompts directly"*, and *"Verify your claims by quoting the exact applicable information (including policies) when
referring to them."* That reverses the house style deliberately — stripping verification scaffolding suits a model
that over-verifies, and inheriting the removal is the defect. **[measured-family]** The vacuum filled with a
self-written review asserting a browser engine that never ran, and a `100% pass rate on contrast` from a probe never
executed; measured after, every primary button was 3.65:1 and one glyph 1.00:1. So paste `scaffold.sh`'s last line
verbatim (`install / gate / xcodegen`), paste `audit_sheet.py check design/icon` with its exit code (`exit 0
required`) and say you opened the sheet, because `only opening it proves the icons are good`, and name the
`design-review` run rather than its verdict.

**The prerequisite receipt, which this skill has no check for.** **[measured-family]** On a run whose auditor
validated tags, citations and contrast thoroughly, nothing checked whether the upstream skills had run, so two skipped
invocations passed at exit 0. Here `audit_sheet.py` proves the icon sheet and nothing proves the rest — and this
revision's two new files are the likeliest to be asserted rather than written.

```bash
for f in docs/positioning/00-decision.md PRD.md OVERVIEW.md docs/MARKETING-FEATURES.md \
         DESIGN.md UX.md design/mocks/html/INDEX.md; do
  [ -s "$f" ] && echo "ok      $f  $(wc -l < "$f") lines" || { echo "MISSING $f"; exit 1; }
done
# both directions of the traceability claim, since one direction always looks fine
echo "briefs $(ls docs/features-to-triage/*.md | grep -vc BRIEF-TEMPLATE) / rows $(grep -c '^| *[A-Z]*-[0-9]' PRD.md)"
```

## Override 3 — every bound in the quality bar is read back off the built page

Lands on launch-pipeline.md's **quality bar** (`treat as gates, not aspirations`), Phase O½'s card rules at :89, and
§2's `at most 4`. **[measured-family]** This is the failure with a rate behind it: across 106 benchmark tasks, 58% of
failing UI assertions at `medium` and **86%** at `high` stated a bound (`exactly N`, `no`, `not`, `only`), against
**8%** for opus and **6%** for the OpenAI lane. One rule — `has exactly one soft elevation shadow` — failed on *every
card and every toast in its set* on a run that passed 37 of its 39 other assertions. A bound is violated by what you
did not write, so it survives every check that looks at what you did:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| pricing section | tiers | ≤ 3 | `querySelectorAll('[data-tier]').length` | 3 | yes |
| pricing section | visually dominant tier | exactly 1 | count cards carrying the highlight class | 2 | **no** |
| marketing page | transferred JS | ≤ 300KB | sum the script responses in the network log | 412KB | **no** |
| hero | authored motion moments | 1–2 | count the `ScrollTrigger` pins | 2 | yes |
| marketing page | Krebs slop tells present | 0 of 16 | walk the list, one verdict per tell | 1 (pill badge above the H1) | **no** |
| `design/icon/audit.html` | rows per take | exactly 1 | `audit_sheet.py check design/icon` | 4 takes, 4 rows | yes |

**The trap worth naming.** `Zero slop tells` and `avoid every one` read as taste, and the recorded failures treated
bounds phrased that way as style advice — converted above into a counted property with a denominator of sixteen and a
per-tell verdict. **[docs]** The **Recap** component is where a constraint belongs: a *"Concise repeat of the key
points of the prompt … at the end of the prompt."*

## Override 4 — eight phases, each leaving a file the next one opens

Lands on §5 and launch-pipeline.md:3's order, `P∥R∥B → O → D → M → L`. **[docs]** Under **Too many tasks** the remedy
is chaining — *"make each step a prompt and chain the prompts together in a sequence"*. **[measured-family]** On the
one run whose brief phrased skill composition as a standard rather than a step, both invocations were skipped: nothing
downstream depended on a file only those skills produce.

`[derived]` The scan flags **zero** qualitative skill references, and Phase P is already file-gated. Three Phase D
bullets are still the weaker form: `design-craft authors the visual system and the mock set for each surface`,
`ux-craft passes every flow`, `mac-design-studio owns the native side` name a role rather than a step with an output.
Give the whole pipeline Phase P's shape:

```
P.1  test -f docs/positioning/00-decision.md || Skill(positioning:positioning)
P.2  read 00-decision.md → territory, hero line, category frame, beachhead
O.1  read 00-decision.md + docs/deep-research/*.md + docs/features-to-triage/*.md
O.2  write PRD.md   → then OVERVIEW.md → then docs/MARKETING-FEATURES.md
D.1  Skill(design-craft:design-craft) → writes DESIGN.md and design/mocks/html/INDEX.md
D.2  Skill(ux-craft:ux-craft)         → writes UX.md: flow list, return paths, form states
D.3  Skill(create-mac-icon:create-mac-icon) → writes design/icon/audit.html and the SVG master
D.4  read DESIGN.md + UX.md + INDEX.md, then author the mocks
D.5  audit_sheet.py check design/icon (exit 0) + the receipt in Override 2
```

Phase M reads `DESIGN.md` and the Phase D frames before a line of `index.html` — a real dependency, since the
`interactive app-UI mock slices` are lifted from those frames. The skill's hard rule works the same way: `Do not
substitute a bare media-gen-pro call plus a hand-rolled contact sheet` is satisfied by `design/icon/audit.html`
existing in that skill's template shape, not by an intention. **[docs]** Forced execution exists only where the caller
controls the request — *"any: Model is constrained to always predict a function call."* — so the artifact is the lever.

## Override 5 — describe the capture before judging it, and hand over a reference

Lands on §5 D and M — `Serve the page and open it at 1440 and 390 before calling it done` — and on the Mobbin trawl's
`took/left ledger` at launch-pipeline.md:58. **[docs]** *"Ask the model to describe the images before performing the
task in the prompt."* Name what is in the crop, then judge. The denominator is 9 surfaces × 3 states × 2 viewports =
54 frames, all opened, the fraction reported; **[measured-family]** the run opened four images for a ten-cell artifact.
**[docs]** The second lever suits this skill: *"For UI generation, the model shows high design adherence and parity
based on a reference input, whether it's a screenshot, an image, or a full design system."* Three are in hand —
`--design-ref`, the Mobbin trawl, `packages/design-tokens` — supply all three before Phase M authors. `[derived]` Every
collapsed static-page task in the corpus was a prose brief with no reference: take the documented path, unmeasured.

## Override 6 — platform, pricing and ecosystem values are read, never recalled

Lands on §4's `Known deliberate pin`, `## What each module gives`, Phase O½, `references/apple-commercialization.md`
and Phase L. **[docs]** *"The knowledge cutoff date for Gemini 3.7 Flash is March 2026"*, with some domains still at
the January 2025 floor, and the remedy is grounding — *"Grounding with Google Search connects the Gemini model to
real-time web content, and should be enabled whenever the model may need to know obscure or recent facts."*
**[measured-family]** The recorded run put Windows 10's accent colour on a Windows 11 app: not a guess, a
previous-generation *published* value. This target is dense with those — Next on `latest`, the pnpm 10 → 11 rename,
`typescript@^6` against 7.0, notarytool, the MAS sandbox rule, App Store review rules, every conversion figure. Each
cell carries its value **and its source tier**.

| value | used at | read from | tier |
|---|---|---|---|
| Node floor, pnpm field rename, Next 16 lint removal | templates, generated CLAUDE.md | `references/research-notes.md:13`, read this run | file |
| IAP vs external purchase, region flux, MAS sandbox | Phases O½ and L | `references/apple-commercialization.md`, read this run | file |
| current App Store review requirements | Phase L | in no file here | **must be grounded** |
| conversion figures (~9% · ~31% · ~43% · 15–25%) | Phase O½ | launch-pipeline.md:84-87, vendor-published per research-notes.md:45 | file, flagged |

The skill's sharpest caution belongs there too: `Apple external-purchase-link economics are legally in flux — never
bake channel-fee claims into copy.` **The file half of the rule:** a document *named in the prompt* is loaded before
the answer is written. **[measured-family]** Asked a question naming three skills, one run answered from memory
without loading any. Lands on §5's `read it and run the phases`.

## Override 7 — copy says only what the research, the positioning and the owner supplied

Lands on Phases O, M and L, and on launch-pipeline.md:5's `Nothing in those four states a market claim the research or
the owner didn't supply.` **[docs]** Adopt Google's strictly-grounded system instruction for `PRD.md`, `OVERVIEW.md`,
`docs/MARKETING-FEATURES.md`, the pricing recommendation and the legal stubs — context being the exported reports,
`docs/positioning/00-decision.md` and the owner's answers — and note its last clause: *"If the exact answer is not
explicitly written in the context, you must state that the information is not available."* The one-line positioning is
`taken directly from docs/positioning/00-decision.md`, so a hero line that reads better than the decision's is a
rewrite. Export into `docs/deep-research/` **before** citing: a citation to a run id with no file in the repo is the
fabricated-review shape renamed.

## Three short notes

**`thinking_level`.** **[docs]** Phases D and M are what Google describes `HIGH` as being for — *"multi-step planning,
verified code generation"* — and 3.7 Flash defaults to `MEDIUM`. Write it as what the level is *for*, never as a
remedy: **[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, so
nothing in Overrides 1–3 improves by raising it.

**The retry ceiling.** Lands on §0 and §3. Two attempts per tool, then change approach; a permanent error gets one,
and a hard capacity limit pivots on attempt 1. Run `doctor.sh` first, for the reason the skill gives — `no macos/ios
module without xcodegen, no 1Password seeding without op`. **[measured-family]** four consecutive invocations of an
absent driver in one run, and four `Read` failures against a 25k-token ceiling in another; an exported Dossier report
and the positioning skill's 9-document suite both exceed it, so switch to line-ranged reads on the first failure.
**[docs]** *"you must change your strategy or arguments, not repeat the same failed call."*

**Modules not written.** `states` and `count-contract` are rows in Override 1 rather than sections. `delegation` did
not fire — the skill briefs at most one agent, for `create-mac-icon`, and routes onward rather than fanning out. Nor
did `injection`; the adjacent risk, Dossier reports synthesised by other models from sources this skill never
verified, is Override 7's. `emphasis` did not fire: 315 lines carry no shouted directive, and the bolded `**ALL**` at
launch-pipeline.md:42 is a quota row rather than a register to match.

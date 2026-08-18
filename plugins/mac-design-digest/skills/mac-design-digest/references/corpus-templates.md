# Corpus File Templates

Exact templates for every file the skill writes. Use these structures verbatim — cross-session incrementality depends on files being predictably parseable by the *next* invocation. Replace `{{…}}`; never leave a placeholder in a written file.

**`scripts/corpus_check.py` enforces this file.** Everything below that is an invariant rather than a preference is asserted by that script with a non-zero exit: twelve checks over seventeen named invariants — ledger present, hash format, hash uniqueness, append-only rows, every ledger target existing, cross-app patterns recorded, the 3-independent-apps canon bar, the native-lineage gate, canon traceability, a ledger row per canon member, the cluster contradiction budget, surviving placeholders, a dated header, a level from the maturity model, non-empty knowledge gaps below Proficient, one mark per axis with a composed pair where the row's role needs both, the app count a (recurring)/(canon) mark claims, and a pinned precision baseline. Run it after every write — a violation here is invisible in the session that commits it and wrong in every session after.

## Corpus layout

```
design-corpus/
├── TASTE.md            # master synthesis: canon, clusters, conventions, gaps — the file a generating AI loads
├── ICONS.md            # icon synthesis: eras, palettes, devices, icon canon
├── ledger.md           # digestion log — read FIRST on every invocation
├── apps/<app>.md       # one profile per app (all its surfaces accumulate here)
├── icons/<app>.md      # one digest per icon
├── patterns/<pattern>.md  # cross-app pattern entries (sidebar.md, toolbar.md, settings.md, empty-state.md, onboarding.md, list.md, inspector.md …)
└── kit/<kit>.md        # ground-truth tokens from official UI kits (e.g. macos-27.md)
```

## Provenance marks (used on every token everywhere)

Measurement quality: `(specified)` — from an official UI kit or HIG numeric spec, authoritative · `(measured)` — clean pixel measurement from a screenshot · `(estimated)` — inferred within a stated range · `(assumed)` — gap-filling default.

Evidence strength: `(inferred)` — one surface · `(confirmed)` — repeated within one app · `(recurring)` — 2 independent apps · `(canon)` — ≥3 independent apps, promoted to TASTE.md · `(contested)` — apps disagree; both readings recorded.

Standalone: `(user-override)` — the user's ruling, recorded alongside the original reading rather than replacing it · `(insufficient-evidence)` — the image cannot settle it, most often glass-vs-solid in dark mode · `source: mock` — an unshipped surface; never counts toward canon.

**One mark per family, and the two families move independently.** Strength advances on repetition; precision advances only on a better source. So `(estimated)(confirmed)` is a normal, stable state — a value seen three times in compressed screenshots is well-evidenced and still imprecise — while `(measured)(estimated)` on one value is incoherent, and the gate refuses it.

**Which families a row needs depends on its role**, because the two axes are not always both applicable:

| Where | Precision | Strength | Why |
|---|---|---|---|
| `apps/`, `patterns/`, `icons/` | required | required | this is where collapsing the axes does the damage |
| `kit/` | required | **forbidden** | strength counts independent app sightings; a kit is not an app, so a strength mark here claims corroboration that does not exist |
| `TASTE.md`, `ICONS.md` | when the rule states a number | required | a canon rule's whole claim is how many independent apps back it |

That scoping was measured, not assumed: on the live 134-app corpus, 79 of 88 marked rows already carry both, and every one of the 9 exceptions is either a `kit/` row or a qualitative canon rule. Both are correct as they stand.

**Precision is pinned.** `design-corpus/.precision-lock.json` records each evidence row's precision mark; the gate writes it on first run and refuses a later strengthening. Nothing stateless could catch that mutation — both states are well-formed and the change between them is invisible — so the baseline is written down. Commit the lock with the corpus. When a better source genuinely arrives, name it in the ledger and re-run with `--accept-precision-change`.

**This vocabulary is a published interface, not an internal convention.** `mac-craft` reads corpora written by this skill, re-emits both families unchanged, and carries `(specified)` on every kit value in its own references; it names the first axis *Precision* where this file calls it measurement quality, over the same four values. Adding, renaming or removing a mark is a breaking change to both skills and to every corpus already on disk; make it in both places at once or not at all.

`(specified)` values override conflicting `(measured)`/`(estimated)` values — but log the conflict: a shipping app deviating from the kit is itself a finding.

## Dating every file this skill writes

Every synthesis file (`TASTE.md`, `ICONS.md`) carries `Updated <ISO date>` and its corpus level in the header block, restamped on every pass that rewrites it. Kit and app profiles carry their own ingest or last-updated date. **A reader downstream cannot date a claim the file does not date** — and undated guidance gets cited as current indefinitely, including by other skills that load TASTE.md without ever seeing this file. The gate fails a synthesis file with no date.

## ledger.md

```markdown
# Digestion Ledger

> **Corpus root:** {{absolute or repo-relative path}} · **Scope:** {{global across projects / this project}} — settled {{date}}, do not re-ask.

| # | Date | Source file | SHA-1 (8) | Type | App | Surface / subject | Digested into |
|---|------|------------|-----------|------|-----|-------------------|---------------|
| 1 | 2026-07-19 | quill-hero.png | 3fa2b91c | ui | Quill | main window, light | apps/quill.md, patterns/toolbar.md |
| 2 | 2026-07-19 | quill-icon.png | 88d10a4e | icon | Quill | app icon | icons/quill.md |

## Synthesis history
- 2026-07-19 — corpus level: Novice (2 items, 1 app). Promotions: none.

## Pending questions
- {{open contradictions or user questions awaiting more evidence}}
```

Type is one of `ui | icon | kit`. Hash with `shasum <file> | cut -c1-8`. If a hash already appears in the ledger, tell the user it's already digested and skip (unless they say re-digest, e.g. after an app update — then supersede the old evidence and note it). Multiple source files of the same subject (e.g. hero + Dock renders of one icon) get one ledger row each, all pointing at the same digest file.

**The ledger is append-only.** Row numbers run contiguously from 1 and a row, once written, is never renumbered, reordered or rewritten by a later run. It is the corpus's index: earlier rows are cited by number, so renumbering silently re-points every one of those citations, and a dropped row makes its file digestible again as fresh evidence. The gate checks contiguity for exactly this reason. The **Corpus root** line above is what stops a later session re-asking a settled question.

## apps/<app>.md

```markdown
# {{App}} — profile

- **Source:** {{macapp.supply / user}} · **Surfaces digested:** {{list}} · **Last updated:** {{date}}
- **One-sentence identity:** {{peer-reference vibe, e.g. "Things' calm discipline applied to a markdown editor"}}
- **Cluster:** {{cluster-name or "unassigned"}}
- **Lineage:** {{native / catalyst / ios-on-mac / web-electron}} ({{confidence}}) — non-native evidence never feeds macOS canon
- **Era (chrome):** {{e.g. Liquid Glass native / legacy-native (pre-Tahoe) / custom-drawn}}

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | #ECECEE (estimated)(confirmed) | | window background, light mode |
| type/body | 13px SF Pro Regular, lh ~16px (estimated)(confirmed) | | |
| space/base | 8px grid, 4px micro (measured)(confirmed) | | one 22px deviation, see Defects |
| accent/primary | … | | |
| radius/card | … | | |
| chrome/sidebar | {{width, material, vibrancy?}} | | |

## Layout skeletons
{{One per digested surface: ASCII-free structural description — regions, column widths, alignment axes.}}

## Signature moves
- {{[GOLDEN-NUGGET] systematic, purposeful deviations that define this app's character}}

## Defects
- {{anti-pattern name → evidence → what canon would do instead}}

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window | 12/14 | #6 line length, #10 border contrast |
```

## patterns/<pattern>.md

```markdown
# Pattern: {{sidebar}}

## Evidence
| App | Surface | Key values | Provenance |
|---|---|---|---|
| Quill | main | 220px, full-height, vibrancy material, 28px rows | (estimated) |

## Converged rules ({{n}} apps)
- {{rule}} — apps: {{list}} — {{(recurring)/(canon)}}

## Divergences
- {{where apps split, and whether the split tracks cluster lines}}

## Generation guidance
{{The distilled how-to-build-one, token-precise. Only write once ≥2 apps evidence it.}}
```

## icons/<app>.md

```markdown
# Icon: {{App}}

- **Era:** {{…}} · **Rubric:** {{n}}/12 · **Digested:** {{date}}

| Dimension | Reading |
|---|---|
| Background | {{flat / ramp #hex→#hex / scene}} |
| Glyph | {{type, colours, optical position on grid}} |
| Overlay device | {{none / diagonal tool / badge}} |
| Light model | {{direction, shadow character, specular}} |
| Layer stack | {{back → front enumeration}} |
| Palette economy | {{hue families count, accent placement}} |

## Signature devices
- {{nameable moves}}

## Failures
- {{rubric failures with evidence}}

## Rhymes with
- {{other digested icons sharing devices/palette logic}}
```

## TASTE.md

```markdown
# TASTE.md — macOS design corpus synthesis

> Load this file (plus the relevant cluster section and 1–2 app profiles) when generating a new macOS mock.
> Corpus level: {{Novice/Competent/Proficient/Expert}} — {{n}} items, {{n}} apps, {{n}} icons. Updated {{date}}.

## Canon — universal ({{promoted from ≥3 independent apps; never edit without evidence}})
| Rule | Values | Supporting apps | Since |
|---|---|---|---|

## Canon — macOS conventions
{{Platform-specific: chrome metrics, materials usage, traffic-light spacing, sidebar/toolbar norms. Kit `(specified)` values live in kit/ and are cited here.}}

## Style clusters
### {{cluster-name}} — {{one-sentence identity + reference peers}}
- **Members:** {{apps}}
- **Audience:** {{pro tool / consumer utility / creative}}
- **Identity tokens:** {{the 5–10 tokens that make this cluster itself: density, radius, palette temperature, type personality, depth philosophy}}
- **Cluster do/don't:** {{3–6 bullets}}

## Contested
{{Rules apps disagree on — both readings, member lists.}}

## Knowledge gaps
{{What the corpus cannot yet answer: unseen surface types, no dark-mode evidence, single-cluster blindness… Never empty below Proficient.}}

## Design-mode checklist
1. Pick cluster by audience match (state choice + runner-up).
2. Inherit cluster identity tokens; fill gaps from canon; fill remaining from kit/ then HIG defaults `(assumed)`.
3. Build layout skeleton from the nearest pattern entries.
4. Audit against the 14-point rubric (macOS calibration) before delivery; report score honestly.
5. Lookalike check: if the result would pass as a specific digested app's screen, differentiate deliberately.
```

## ICONS.md

```markdown
# ICONS.md — icon corpus synthesis

> Load when designing a mac app icon. Corpus: {{n}} icons. Updated {{date}}.

## Era distribution
{{count per era; what the corpus can/can't teach}}

## Recurring palettes
{{ramp families with hex ranges + member icons}}

## Recurring devices
{{diagonal tools, mascots, framed motifs… with member icons}}

## Icon canon ({{≥3 independent icons}})
| Rule | Evidence | Members |
|---|---|---|

## Icon clusters
{{style families, same structure as TASTE.md clusters}}

## Design-mode checklist (icons)
1. Choose era + light model + palette ramp before composition.
2. Sketch silhouette first; run the mental 16px squint test.
3. Audit against the 12-point icon rubric; report score.
```

## kit/<kit>.md (official UI kit ingestion)

```markdown
# Kit: {{Apple macOS 27 UI Kit (Figma)}}

- **Source:** {{file name/version}} · **Ingested:** {{date}} · **Authority:** overrides screenshot estimates
- **Coverage:** {{which component sheets were provided}}

## Control metrics `(specified)`
| Control | Size/metrics | States seen | Notes |
|---|---|---|---|
| Push button (regular) | {{h × min-w, radius, padding}} | {{default/hover/…}} | |
| Sidebar row | … | | |

## Type styles `(specified)`
| Role | Size/weight/lh | Usage |
|---|---|---|

## Colour semantics `(specified)`
| Token | Light | Dark | Maps to |
|---|---|---|---|

## Materials & chrome
{{window chrome metrics, material names, corner radii, traffic-light geometry}}

## Deltas vs. previous macOS
{{what changed — this is high-value: shipping apps will lag}}
```

## Per-screenshot digest block (returned in chat, not written to a corpus file)

```markdown
### Digest: {{file}} — {{App}}, {{surface}}
**Rubric:** {{n}}/14 · **Failures:** {{#s + one-line evidence each}}
**New tokens:** {{count}} ({{measured/estimated/assumed split}})
**Signature:** {{the one observation worth remembering, or "none — competent but anonymous"}}
**Corpus effect:** {{promotions, cluster moves, contradictions raised}}
```

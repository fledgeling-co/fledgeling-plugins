# Model calibration — what is family-specific, and what was wrongly gated behind a family

The predecessor shipped a 214-line side-file that fired only for one model family. Most of
what was in it should never have been gated: the failure it corrected — **a claimed audit
carrying no quoted output** — is not family-specific, and the artifact that fixes it is a
gate with an exit code. So the mechanisms were hoisted into `SKILL.md` and
`scripts/mock_check.py`, and what remains here is only what genuinely differs by family.

## Provenance

**`[measured]`** items come from one recorded run (`Egress Gemini`, **2026-08-17**) which
invoked `design-craft`, `ux-craft` and this skill's predecessor on a two-platform brief —
macOS Tahoe plus a Windows 11 counterpart — and produced
`~/Dev/egress/design/mocks/html/index.html`. A Claude run on a near-identical brief produced
`interaction-mock.html` beside it. Both were measured with the same probes. **n=1.**

**`[docs]`** items come from Google's published Gemini 3 prompting guidance, and **are the
stronger evidence** — one run is an existence proof, not a rate.

That two-tier split with the sample size and a statement of which tier is stronger is worth
keeping wherever a rule is bought with a measurement. A rule tagged neither is a rule
nobody bought.

## What the measured run got wrong, and where the fix now lives

Every row below was a value with a published number available, where the artifact used a
different one. None is a taste call.

| Property | Artifact | Published | Where the fix lives now |
|---|---|---|---|
| macOS titlebar height | 48px | 33pt | `SKILL.md` step 3 metric block; **gated** by `mock_check.py [metrics]` |
| Windows titlebar / nav pane / accent | 48px · 240px · `#0078D4` | 32px · 320/48px · `#005FB8` | `SKILL.md` step 0, second-platform rule |
| Micro-labels | all-caps, tracked | sentence case, Semibold | **gated** by `mock_check.py [casing]` |
| Window material | flat fill | Mica (Windows) / glass on chrome only (macOS) | `native-foundation.md` materials |
| Accent, both platforms | `#00F0FF` family | in neither vendor palette | **gated** by `mock_check.py [metrics]` tier tag |
| Token layer | 11 custom properties beside **45 raw hex literals** | — | **gated** by `mock_check.py [tokens]` |
| Menus | **zero** — no menu bar, no context menu, no status item, on a product whose own architecture doc specifies a `MenuBarExtra` | — | `SKILL.md` step 5 keyboard-and-menu spec |
| The seven audits | all five surfaces reported **PASS**; a named engine failed all four invocation attempts and never ran; "100% pass rate on contrast (≥4.5:1)" claimed | measured after: primary buttons **3.65:1**, selected sidebar rows 3.65:1, one `+` glyph at **1.00:1** | **gated** by `mock_check.py [contrast]`, which reports a 1.00:1 pair with its own message |
| Renders opened | 3 render calls, **4 images** for 5 surfaces × 2 platforms | one per surface × state × platform | `SKILL.md` step 6, with the fraction reported |
| Keyboard | `:focus-visible` **0**, `:focus` **0**, 12 `<div onclick>` | — | **gated** by `mock_check.py [keyboard]` |
| Tool retries | four consecutive invocations of one banned, absent browser tool, no strategy change | — | `SKILL.md` degradation ladder |

**The structural consequence, and the reason the metric block is a gate rather than a
request:** with the metrics unsourced, the "Windows theme" was the macOS theme with the
caption buttons moved right and a 3px accent bar added — same titlebar height, same nav
width, same type treatment, same radii, no Mica. The brief asked for *the mac app themed
using the Windows 11 design system*; what shipped was the first half. **A second platform
needs a second published source, or it is a reskin.**

## What is genuinely family-specific

### Gemini

- **`[docs]` Stale recall is the mechanism behind the accent, not carelessness.** The
  Gemini 3 family's knowledge cutoff is **January 2025** (March 2026 for 3.7 Flash, with
  Google noting some domains remain at January 2025). `#0078D4` was Windows' accent for
  years before `#005FB8`; recalling it is an old fact returned confidently. Google's own
  remedy is to state the cutoff and to *ground* time-sensitive work rather than answer from
  memory. Practical form: **a platform value is read, never remembered.**
- **`[docs]` Reading a conditional side-file is itself a prompt defect.** Google's prompt
  health checklist names *"conflicting internal references"* — instructions the model must
  *"piece together … from multiple different places"* — which is the shape of this file. So
  read it in one pass before the skill, and note that shortening it (as this rebuild did)
  is the real fix.
- **`[docs]` Set the thinking level.** A committed multi-surface design with a
  seven-part audit is what Google describes `thinking_level: HIGH` as being for
  ("multi-step planning"); Gemini 3.7 Flash defaults to `MEDIUM`.
- **`[docs]` Describe each crop before judging it.** Google's own multimodal method: *"Ask
  the model to describe the images before performing the task."* For a mac surface the
  extraction list is the audit — name the chrome heights, control heights, casing and radii
  you can *see*, then score. Their disambiguation trick applies too: when a verdict looks
  wrong, ask what is in the image first, which separates a rendering problem from a
  reasoning one before you change any CSS.
- **`[docs]` Verification has to be asked for.** Google's guidance is to *"include specific
  verification steps"* and their agentic template spends two of nine rules on it. So a
  claimed audit carrying no quoted output is the *expected* outcome of stating an audit in
  prose on this family — which is the argument for the gate, not for more prose.

### Claude (Opus 5)

- **Do not add verification scaffolding.** Opus 5 self-verifies, and instructing it again
  compounds into over-verification that costs tokens without improving results. The gate is
  not scaffolding: **an instrument run is a measurement the work is made of, not a
  self-check**, and it stays.
- **Cap delegation explicitly.** Opus 5 delegates more readily than earlier models; a
  commission that does not name a subagent budget will grow one.
- **Calibrate length explicitly.** Effort controls how much it thinks, not how much it
  writes. `SKILL.md` step 7 names the delivery's four parts for this reason.

### Any family

- **Two attempts per tool, then a different approach.** A `command not found` is permanent —
  one attempt is the whole budget. Read the repo's constraints first; this house names its
  single permitted browser and lists the banned ones by name. Four identical invocations of
  an absent tool is what the measured run did, and no amount of native-fidelity guidance
  would have prevented it.
- **A refusal is not re-pitched.** If a capability is denied or absent, say so once and take
  the stated degradation path. Do not offer it again later in the same turn.

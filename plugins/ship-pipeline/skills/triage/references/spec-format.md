# Spec file format, id allocation, and triage section shapes

This replaces a tracker (e.g. Diolog Tasks) issue + comment thread with three markdown locations in the **target repository**:

- `docs/feature-specs/LEDGER.md` — the id registry (project code + counter + table).
- `docs/specs/spec-<ID>.md` — one spec per feature (e.g. `docs/specs/spec-DIO-0001.md`).
- `docs/plans/plan-<ID>.md` — written later by `/plan`.

`<ID>` is the uppercase id, e.g. `DIO-0001`. File names use that exact casing.

## Status vocabulary (used in the spec header and the ledger)

The status field is the pipeline state — the doc equivalent of a tracker issue status. Use exactly these values, in this order:

`Triage` → `Needs More Info` → `Ready for Plan` → `Ready for Work` → `In Progress` → `In Review`

- `Triage` — spec created, triage in progress.
- `Needs More Info` — triage found an essential gap; waiting on a human answer.
- `Ready for Plan` — triage passed; `/plan` can run.
- `Ready for Work` — `/plan` wrote the plan; `/work` can run. (set by `/plan`)
- `In Progress` — `/work` is implementing. (set by `/work`)
- `In Review` — `/work` finished; the local branch awaits human review. (set by `/work`)

Never downgrade a status (e.g. don't move `Ready for Work` back to `Ready for Plan`).

## Id allocation algorithm (new features only)

Do this deterministically. When in doubt, re-read the ledger before writing.

1. **Read `docs/feature-specs/LEDGER.md`.**
   - **If it does not exist:** ask the user for the 3-letter project code. Suggest one derived from the project/folder or package name (e.g. *motif → MOT*, *diolog → DIO*); accept a code the user passes explicitly. Uppercase it. Create the directories and the ledger from the template below with `Last allocated: 0`.
   - **If it exists:** read `Project code` and `Last allocated` from it. (Ignore any `--code` argument when a ledger already exists — the recorded code wins; if they conflict, stop and tell the user.)
2. **Compute the next id.** `next = Last allocated + 1`; zero-pad `next` to **4 digits**; `ID = "<CODE>-" + padded` (e.g. code `DIO`, next `1` → `DIO-0001`; next `42` → `DIO-0042`).
3. **Update the ledger:** set `Last allocated: next`, and append a table row `| <ID> | <short title> | <YYYY-MM-DD> | Triage |`.
4. **Create the spec** at `docs/specs/spec-<ID>.md` from the spec scaffold below.

Derive `<short title>` (≤6 words) from the feature description. Use today's date (`YYYY-MM-DD`).

### LEDGER.md template

```markdown
# Feature Spec Ledger

<!-- Managed by the /triage skill. "Project code" and "Last allocated" are load-bearing — every spec id is derived from them. Edit by hand only if you know what you're doing. -->

**Project code:** DIO
**Last allocated:** 0

| ID | Title | Created | Status |
|----|-------|---------|--------|
```

### Spec scaffold (`docs/specs/spec-<ID>.md`)

```markdown
# <ID>: <Short title>

**ID:** <ID>
**Status:** Triage
**Created:** <YYYY-MM-DD>
**Last updated:** <YYYY-MM-DD>

## Feature description

<The original feature details, verbatim — the inline text the user gave, or the contents of the markdown/text file they pointed at. Never edited by later passes.>

---

<!-- Triage, plan link, and progress sections are appended below. -->
```

After triage, append a triage section (shapes below) and update `Status` + `Last updated` in the header (and the ledger row's Status). `/plan` later appends a `## Plan` pointer; `/work` appends a `## Progress` section.

## Non-technical language — a hard rule (triage review sections)

The audience for the triage review is a product person, not a developer. Every word in a triage section must be understandable to someone who has never opened the codebase. Do your technical reasoning internally; translate before writing. (The `## Feature description` section is exempt — it preserves the author's original words.)

**Bans — none of these may appear in a triage section:**
- File paths or filenames (`InboxEmptyState.tsx`, `apps/web/.../page.tsx`).
- Code identifiers — component/function/variable/class/interface/hook/type names.
- Library/package/framework names (jsPDF, papaparse, Chakra, Next.js, NestJS, MongoDB, Redis, GraphQL, Apollo, Mongoose, …).
- Architecture words as nouns (module, service, resolver, route, endpoint, API, schema, migration, webhook, collection, table, column, query, mutation, controller, middleware, handler, dispatcher) — translate to what the user sees or does.
- Implementation patterns (token-generator, tenant-scoped, polling, fan-out, event bus, cache TTL, base64-encoded, retry backoff) — describe the user-facing effect instead.
- References to "the codebase", "the code", "the repo", or the investigation process itself.

**Good translations:**
- "the `InspirationCard` component" → "the inspiration cards in the content library".
- "a `/s/<token>` public route with an unguessable token" → "a shareable link that can't be guessed".
- "add a `/v1/surveys` endpoint and a new `surveys` module" → "a new Surveys area in the app, and the underlying data that powers it".

Don't preamble a triage section with a codebase summary. Start with the verdict header, then the UI & logic preview, then Assumptions (or Essential Questions).

## UI & logic preview (every Ready section, immediately before Assumptions)

A **rough sanity check for the author, not a spec** — so a product person can confirm "yes, that's the surface area I expected" or catch a surprise (most importantly, a customer-facing screen they never intended), **and so a designer can tell which surfaces need mocking and what each one gains.** Forward-looking (what will *change*), not an inventory of what exists. Same non-technical bans. Parts:
- **Where it shows up:** name every surface that changes, each tagged *(customer-facing)*, *(internal/admin)*, or *(behind the scenes — nothing visible changes)*, and mark each as an **existing surface that gains UI** or a **new surface/screen**. **If nothing customer-facing changes, say so explicitly — the single most important signal.**
- **What users will see — per surface:** for **each** surface above that gains or changes UI, one short line naming the **concrete elements added or changed** on it (the control, state, panel, badge, field), enough that a designer knows what to mock — not a single behaviour headline that hides which screens are touched. A feature that bolts onto three existing screens gets three lines, one per screen; **do not collapse touched surfaces into one line, and never drop a touched surface to save space** — an unnamed surface is a screen the designer won't mock. (Behind-the-scenes only → "Nothing visible — behind-the-scenes only.")
- **Behaviour changes:** up to ~3 short lines on what the product does differently; omit if none.
- **Design reference:** if the feature description points at a visual mock (a mockup, showcase, prototype, Figma, or HTML file), name it here as the canonical visual reference for those surfaces. Omit if none exists.

Keep each line short and scannable — still a fast read, just per-surface. Describe the change per surface; don't restate the description.

## Assumptions block

- One line per assumption, lens-tagged, with a one-line rationale in parentheses. Declarative, not a question.
- End with: *"If any of these are wrong, edit the answer inline (or correct an assumption) in this file and re-run `/triage <ID>` before the planner picks this up."*
- **Compress hard:** ≤15 words per assumption, ≤10 per rationale; noun-phrase shorthand ("*matches existing empty-state pattern*", "*safer default*"). One line each — split, don't pile on sub-points.
- **Do not cap the number of assumptions.** List every load-bearing default; never drop a material one to shorten. Merge two that share a rationale.

**Lens tags — use only these user-facing labels** (map internal Sentinel lenses onto them):
- `[Experience]` — User Paths (happy path, empty/error/re-entry, undo, deep-link).
- `[Layout]` — UI Placement (where on the page, what gets demoted, mobile 320px, IA fit).
- `[Data & scope]` — Engineering Readiness, stripped to user-facing effect (who sees what, per-user vs company-wide, rollout staging — never the mechanism).
- `[Operations]` — Operational (errors surfaced, dry-run/preview, health signals).
- `[Compliance]` — Governance (audit trails, sign-off, disclosure-regulation surface).

**Rationale translation** (highest-risk place for jargon to leak): "*scoped by tenant_id*" → "*each company sees only its own data*"; "*reuse the webhook dispatcher*" → "*delivered the same way announcements are today*".

## Essential Questions block (only when an essential gap exists)

- Smallest number of questions possible. Narrow to multi-choice with a `(recommended)` answer where you can; leave genuinely open-ended (copy, subjective thresholds) as prose.
- Tag each with its user-facing lens label. Close with an "Easy reply" block pre-filled with recommended letters / `<your answer>` placeholders, plus the instruction to **edit answers inline and re-run `/triage <ID>`**.
- If empty, omit the header.

---

## Triage section shapes

Append one of these under the spec (after the `---` separator), dated.

### Ready (Outcomes A and D)

```markdown
## Triage — <YYYY-MM-DD>

**Ready for Implementation Plan**

**Sentinel review:** [S0 | S1 | S2 | S3] — [Approve | Approve with assumptions]

**UI & logic preview** *(rough sanity check — is this the surface area you expected?)*
- **Where it shows up:** [surface] *(customer-facing)*, [surface] *(internal/admin)*. If nothing customer-facing changes, say so.
- **What users will see:** [up to ~5 headlines; or "Nothing visible — behind-the-scenes only."]
- **Behaviour changes:** [up to ~3 lines; omit if none.]

**Assumptions** *(include only if you made any non-essential defaults; otherwise omit)*
- `[Lens]` Declarative statement. *(rationale: codebase pattern / analogue / safer option)*

*If any of these are wrong, edit it inline (or correct an assumption) in this file and re-run `/triage <ID>` before the planner picks this up.*

**Regulatory escalation** *(include only for S3)*
- This spec touches MNPI / investor-facing disclosure. A human Legal/Compliance Officer should sign off on [item] before the planner runs.
```

### Needs improvement (Outcomes B and C)

```markdown
## Triage — <YYYY-MM-DD>

[Re-triage only:] **Resolved:**
- [Summarize what the human's answers settled — shows you read their edits]

**Sentinel review:** [S0/S1/S2/S3] — Block pending the essential question(s) below

**Assumptions** *(include only if you defaulted non-essential gaps; otherwise omit)*
- `[Lens]` Declarative statement. *(rationale: …)*

**Essential Questions** *(only gaps you could NOT reasonably default)*
1. *[Lens]* [Multi-choice or open-ended question]?
   a) [Option A] (recommended)
   b) [Option B]

*Easy reply — edit your answers under each question (or correct any assumption), then re-run `/triage <ID>`:*
> `1. a`

*Once the essential question(s) are answered I'll mark this Ready for Implementation Plan.*
```

## Examples

**GOOD (first triage — all gaps became assumptions, goes Ready):**
> ## Triage — 2026-06-18
>
> **Ready for Implementation Plan**
>
> **Sentinel review:** S1 — Approve with assumptions
>
> **UI & logic preview** *(rough sanity check — is this the surface area you expected?)*
> - **Where it shows up:** the content library *(customer-facing)*. Nothing internal/admin changes.
> - **What users will see:** each inspiration card now shows the author's avatar; tapping it opens that author's profile.
> - **Behaviour changes:** none beyond the new tap target.
>
> **Assumptions:**
> - `[Layout]` Inspiration cards in the content library, not the dashboard widget. *(active surface; widget unchanged for 6 months.)*
> - `[Experience]` Web only; mobile out of scope. *(description only references web.)*
>
> *If any of these are wrong, edit it inline in this file and re-run `/triage DIO-0001`.*

**GOOD (multi-surface feature — per-surface UI so a designer can mock each screen):**
> **UI & logic preview** *(rough sanity check — is this the surface area you expected?)*
> - **Where it shows up:** the document editor and the slide builder *(customer-facing — existing surfaces that gain UI)*; a connected-figures report *(customer-facing — new screen)*. Nothing investor-facing changes.
> - **What users will see — per surface:**
>   - Document editor: an inline pill on a number (connected / changed / overridden states), a "make master value" action, and a popover showing where the number is used and when it was last published.
>   - Slide builder: a "connect a figure" control in the element panel, and a connected/changed state on the slide element itself.
>   - Report (new): stat cards (values / locations / overrides) above a list of every value with its usage count and last-published-by.
> - **Design reference:** connected-figures-showcase.html mocks every surface above — match its layout, states and copy.

**GOOD (S3 block — assumptions where safe + one truly essential question):**
> ## Triage — 2026-06-18
>
> **Sentinel review:** S3 — Block pending the essential question below. Legal/Compliance sign-off recommended before the planner runs.
>
> **Assumptions:**
> - `[Compliance]` Drafts land in the existing Disclosure Committee review queue. *(auditable; matches MAR Art 18.)*
> - `[Compliance]` Drafter and releaser must be different users. *(matches ASX GN8 separation-of-duties.)*
>
> **Essential Questions:**
> 1. *[Compliance]* What text should the MNPI acknowledgement prompt display? *(Legal-owned copy; no safe default.)*
>
> *Easy reply — edit your answer below and re-run `/triage DIO-0007`:*
> > `1. <acknowledgement copy>`

**BAD (too technical):** "Which `InspirationCard` component — `apps/web/.../content/InspirationCard.tsx` or `.../dashboard/InspirationCard.tsx`?" → describe the UI location, and if the investigation points to one, make it an assumption.

**BAD (asks where the codebase already gives a safe default):** "Which 'Inspiration' section? a) content library b) dashboard widget" when the content-library one is the active surface → write "*Assumption: content-library section*" instead.

**BAD (writes a spec — that's the planner's job):** "**Implementation Spec:** Add a new field `avatarUrl` to …".

**BAD (re-asks an answered question):** "Which inspiration section is this about?" when the author already edited the spec to say "the content library".

**BAD (no investigation):** "This task is unclear. Please specify which component and page you mean."

**BAD (names the surfaces but not what each gains):** "**Where it shows up:** the document editor, the spreadsheet and the slide builder." followed by one behaviour line ("numbers stay in sync everywhere") → a designer can't tell what to mock on each screen. List, per surface, the concrete elements it gains (a pill, a control, a panel, a state), and name any visual mock the description points at as the design reference.

# Triage comment format

The default is **state assumptions, don't ask questions**. Questions are reserved for gaps meeting the "essential" bar in `sentinel-review.md` §4.

## Non-technical language — a hard rule

The author is a product person, not a developer. Every word posted to Diolog Tasks must be understandable to someone who has never opened the codebase. Do your technical reasoning internally; translate before posting.

**Bans — none of these may appear in a Tasks comment:**
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

Don't preamble with a codebase summary. Start with the verdict header, then the UI & logic preview, then Assumptions (or Essential Questions).

## UI & logic preview (every Ready comment, immediately before Assumptions)

A **rough sanity check for the author, not a spec** — so a product person can confirm "yes, that's the surface area I expected" or catch a surprise (most importantly, a customer-facing screen they never intended). Forward-looking (what will *change*), not an inventory of what exists. Same non-technical bans. Three short parts:
- **Where it shows up:** one line naming the surfaces that change, each tagged *(customer-facing)*, *(internal/admin)*, or *(behind the scenes — nothing visible changes)*. **If nothing customer-facing changes, say so explicitly — the single most important signal.**
- **What users will see:** up to ~5 one-line plain-language headlines grouped by surface; or "Nothing visible — behind-the-scenes only."
- **Behaviour changes:** up to ~3 short lines on what the product does differently; omit if none.

Readable in well under 30 seconds. Describe the change, don't restate the ticket.

## Assumptions block

- One line per assumption, lens-tagged, with a one-line rationale in parentheses. Declarative, not a question.
- End with: *"If any of these are wrong, reply with the correction (e.g. `Assumption 2: do X instead`) and I'll re-triage before the planner picks this up."*
- **Compress hard:** ≤15 words per assumption, ≤10 per rationale; noun-phrase shorthand ("*matches Diolog empty-state pattern*", "*safer default*"). One line each — split, don't pile on sub-points.
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
- Tag each with its user-facing lens label. Close with an "Easy reply" block pre-filled with recommended letters / `<your answer>` placeholders.
- If empty, omit the header.

---

## Comment shapes

### Ready (Outcomes A and D)

```
**Ready for Implementation Plan**

**Sentinel review:** [S0 | S1 | S2 | S3] — [Approve | Approve with assumptions]

**UI & logic preview** *(rough sanity check — is this the surface area you expected?)*
- **Where it shows up:** [surface] *(customer-facing)*, [surface] *(internal/admin)*. If nothing customer-facing changes, say so.
- **What users will see:** [up to ~5 headlines; or "Nothing visible — behind-the-scenes only."]
- **Behaviour changes:** [up to ~3 lines; omit if none.]

**Assumptions** *(include only if you made any non-essential defaults; otherwise omit)*
- `[Lens]` Declarative statement. *(rationale: codebase pattern / analogue / safer option)*

*If any of these are wrong, reply with the correction (e.g. `Assumption 2: do X instead`) and I'll re-triage before the planner picks this up.*

**Regulatory escalation** *(include only for S3)*
- This spec touches MNPI / investor-facing disclosure. A human Legal/Compliance Officer should sign off on [item] before the planner runs.

— Claude (AI Assistant)
```

### Needs improvement (Outcomes B and C)

```
Hi @[Author]!

[Outcome B only:] Thanks for the clarifications.

**Sentinel review:** [S0/S1/S2/S3] — Block pending the essential question(s) below

[Outcome B only:] **Resolved:**
- [Summarize what was clarified — shows you read their answers]

**Assumptions** *(include only if you defaulted non-essential gaps; otherwise omit)*
- `[Lens]` Declarative statement. *(rationale: …)*

**Essential Questions** *(only gaps you could NOT reasonably default)*
1. *[Lens]* [Multi-choice or open-ended question]?
   a) [Option A] (recommended)
   b) [Option B]

*Easy reply — paste this back and edit any letters. You can also correct any assumption (e.g. `Assumption 2: do X instead`):*
> `1. a`

*Once the essential question(s) are answered I'll mark this Ready for Implementation Plan.*

— Claude (AI Assistant)
```

## Examples

**GOOD (first triage — all gaps became assumptions, goes Ready):**
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
> *If any of these are wrong, reply with the correction (e.g. `Assumption 2: include mobile`) and I'll re-triage.*
>
> — Claude (AI Assistant)

**GOOD (S3 block — assumptions where safe + one truly essential question):**
> **Sentinel review:** S3 — Block pending the essential question below. Legal/Compliance sign-off recommended before the planner runs.
>
> **Assumptions:**
> - `[Compliance]` Drafts land in the existing Disclosure Committee review queue. *(auditable; matches MAR Art 18.)*
> - `[Compliance]` Drafter and releaser must be different users. *(matches ASX GN8 separation-of-duties.)*
>
> **Essential Questions:**
> 1. *[Compliance]* What text should the MNPI acknowledgement prompt display? *(Legal-owned copy; no safe default.)*
>
> *Easy reply — paste this back and edit the answer:*
> > `1. <acknowledgement copy>`
>
> — Claude (AI Assistant)

**BAD (too technical):** "Which `InspirationCard` component — `apps/web/.../content/InspirationCard.tsx` or `.../dashboard/InspirationCard.tsx`?" → describe the UI location, and if the investigation points to one, make it an assumption.

**BAD (asks where the codebase already gives a safe default):** "Which 'Inspiration' section? a) content library b) dashboard widget" when the content-library one is the active surface → write "*Assumption: content-library section*" instead.

**BAD (writes a spec — that's the planner's job):** "**Implementation Spec:** Add a new field `avatarUrl` to …".

**BAD (re-asks an answered question):** "Which inspiration section is this about?" when the author already replied "the content library".

**BAD (no investigation):** "This task is unclear. Please specify which component and page you mean."

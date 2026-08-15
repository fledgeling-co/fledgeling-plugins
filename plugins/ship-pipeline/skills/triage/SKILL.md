---
name: triage
description: >-
  Triage a feature brief or ticket for implementation-readiness — the pipeline's readiness gate.
  Reads the brief (docs/features-to-triage/*.md or a tasks-MCP issue), allocates an id (markdown
  lane), grounds every referenced surface in the actual codebase, runs the Specification Sentinel
  product/UX/compliance review, resolves ambiguity through the decision gate (look it up →
  divergence test → internal-vs-external → second-opinion lanes) so questions become recorded
  assumptions, passes an out-of-family spec review, then sets To Do (ready for the planner) or
  Needs More Info with essential questions. Use when the user says "triage this", "triage
  DIO-0001", "is this ready to plan", or hands over a feature description needing a readiness
  check. Never writes an implementation spec — the plan skill owns that.
---

# Pipeline Triage — readiness, grounded and non-technical

Triage a feature for implementation-readiness and record the verdict where the feature lives
(spec section or ticket comment). The output is a short, **non-technical** product review plus a
status change — never an implementation spec.

Substrate, statuses, and read/write rules: `${CLAUDE_PLUGIN_ROOT}/references/tracker-adapter.md`.
Lane assignments and effort: `${CLAUDE_PLUGIN_ROOT}/references/model-lanes.md` — the verdict and
every gate here run on a frontier Claude at `high`; grounding readers run at `low`.

## Inputs

- A brief file (`docs/features-to-triage/<slug>.md`), inline text, an existing id to re-triage,
  or a tasks-lane issue id. Optional `--dry-run`: investigate and report; write nothing.

## Procedure

1. **Resolve mode and read everything.** Re-triage reads every prior section/comment — human
   answers are authoritative; never re-ask an answered question. New features on the markdown
   lane: allocate the id per `references/spec-format.md` (ledger read-modify-write is serialized
   — it is the one write that never runs in parallel), create the spec with the brief verbatim in
   `## Feature description`, and consume the brief file (move it into the spec; delete from
   `features-to-triage/`). Tasks lane: the brief already is the description.

2. **Fan out (Workflow) for a heavy feature** — parallel readers for codebase grounding and the
   Sentinel lens scan; synthesize the verdict yourself. Small feature: inline. Wave caps and
   retry rules: `${CLAUDE_PLUGIN_ROOT}/references/operational-rules.md` §fan-out.

3. **Ground in the codebase (mandatory).** Locate every component, page, service, route the
   brief references; detect ambiguous matches and naming mismatches. Grounding is *source*
   reading: any claim about what the app currently **shows** is marked `(measured: <browser
   evidence>)` or `(assumed from source — verify before building on it)` per
   `${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md` §MEASURED-vs-ASSUMED — a false grounded
   claim in an Essential Question gets a confidently wrong answer the whole pipeline then builds
   on. Technical reasoning stays internal; it never appears in the review section.

4. **Run the Specification Sentinel review** (`references/sentinel-review.md`): strictness tier
   S0–S3, the five lenses, architectural red flags, severities. Default to **stating assumptions,
   not asking questions**.

5. **Resolve ambiguity through the decision gate** —
   `${CLAUDE_PLUGIN_ROOT}/references/second-opinion-lanes.md`, in order: look it up (the thread,
   the repo, the research doc the brief points at); divergence test; the three-part essential bar
   (fail any part → internal: safe default, recorded as "assuming X (rather than Y)"); and for a
   genuinely open **technical** fork, a second-opinion lane or — when the verdict itself is
   contested — a three-family panel, its split recorded. **Every essential question stalls the
   whole pipeline, so when in doubt, assume and proceed.** What survives is genuinely the
   human's: it becomes an Essential Question. One class is presumptively essential rather than
   assumable: **access-control, visibility, and sharing-scope defaults** (who can see, manage,
   or share what). These are the expensive-to-undo, genuinely-the-owner's calls; assume one only
   when the repo already encodes the answer, and never bury one mid-list — a permissions default
   hidden among mechanical assumptions is the exact miss a blind panel caught in this skill's
   own evals.

6. **Out-of-family spec review (mandatory where available).** Before the status flips to
   `To Do`, the written verdict + assumptions go to a reviewer outside Claude's family — the
   ordered lanes in `second-opinion-lanes.md` (codex `gpt-5.6-sol` at `max` first; `agy`, then
   `grok` when codex is down), read-only, grounded in the codebase, per the R1 contract in
   `${CLAUDE_PLUGIN_ROOT}/references/codex-cli.md`. Egress and the repo opt-out are checked per
   invocation; a fully in-family fallback is recorded as a downgrade in the triage section. Then
   **act**: accept (edit), reject (stated reason), or escalate (a Critical/High exposing a real
   external dependency becomes an Essential Question). Record verdict + accept/reject tally.

7. **Assumptions review gate (full-auto runs only).** When no human will read the verdict before
   planning, a fresh strong-model reviewer (not the author) checks each assumption: would this
   default surprise the owner? Does it reverse a locked decision? Is it an external dependency
   wearing a default? Failures convert to Essential Questions or fixed defaults before the flip.
   S2/S3 features stay on the strongest model end-to-end.

8. **Decide, write, and move the status** (shapes and language rules:
   `references/spec-format.md` + `${CLAUDE_PLUGIN_ROOT}/references/comment-format.md`):
   - **Ready** → the "Ready for Implementation Plan" section/comment (Sentinel verdict, UI &
     logic preview, Assumptions block) → status **`To Do`**. The Assumptions block is
     owner-facing: consequential assumptions only, each with its "rather than" alternative;
     mechanical defaults and all gate/lane accounting (review verdicts, tallies, downgrades) go
     in the machine trailer / a separate pipeline-record note, never interleaved with what the
     owner reads — an owner-facing section that reads as process notes fails at its one job.
   - **Needs improvement** (≥1 essential gap, an uncovered S3 gap, or a genuine contradiction
     only the author can resolve) → Essential Questions (numbered, lens-tagged, multi-choice
     with a recommendation) + an "Easy reply" block + Assumptions for the rest → status
     **`Needs More Info`**.
   - Re-triage appends a new dated section opening with "Resolved:" for what the answers
     settled. Dry-run reports without writing.

## Hard rules

- **Keep the review short and non-technical.** No file paths, code identifiers, library names, or
  architecture nouns in review sections — translate to what the user sees or does (ban list and
  worked examples in `references/spec-format.md`; length budget in
  `${CLAUDE_PLUGIN_ROOT}/references/model-and-effort.md` §7). The feature description itself is
  preserved verbatim, never edited.
- **The bias is to push the feature through to `To Do`.** A question is warranted only for a
  genuine external dependency — never because the feature is large, complex, or loosely worded.
  When some gaps are essential but the core is buildable, record assumptions for the rest so one
  answer un-parks the whole item.
- **Design expectations pass through**: the brief's `platforms:` line and any surface inventory
  land in the verdict so the design stage inherits them without re-derivation.
- End with `READY` or `NEEDS IMPROVEMENT` plus the id and artifact path, so the conductor parses
  the outcome without re-reading the thread.

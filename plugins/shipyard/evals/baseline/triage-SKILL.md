---
name: triage
description: >-
  Triage a feature idea into a versioned spec doc for the markdown feature-spec pipeline. Given a feature as inline text or a markdown/text file (or an existing spec id like DIO-0001 to re-triage), it allocates a project id from docs/feature-specs/LEDGER.md, writes docs/specs/spec-DIO-0001.md capturing the original details, runs a codebase grounding pass plus a Specification Sentinel product/UX/compliance review, then appends a short non-technical readiness section (UI & logic preview + Assumptions) or an Essential Questions section and sets the spec status. Use when the user says "triage this feature", "triage DIO-0001", "turn this into a spec", "is this ready to plan", or hands over a feature description or notes file that needs a readiness check before planning. For an issue tracked in Diolog Tasks, use tasks-triage instead. Runs in the current session using Read/Glob/Grep/Write/Edit plus the Workflow tool for fan-out — no issue tracker, no Agent SDK.
---

# Feature Triage (markdown specs)

Triage a feature idea for implementation-readiness and record it as a versioned spec document. The output is a short, **non-technical** product review appended to a spec markdown file plus a status change — never an implementation spec (that's the `/plan` skill's job).

This skill runs **in your current session** using `Read`/`Glob`/`Grep`/`Write`/`Edit` and the `Workflow` tool. It uses no issue-tracker MCP (Diolog Tasks or otherwise) and invokes no Agent SDK script — the spec markdown file is the single source of truth, replacing a tracker issue + comment thread.

## Inputs

- A **feature description** — inline text, or a path to a markdown/text file describing the feature; this becomes a brand-new spec.
- Or an **existing spec id** (`DIO-0001`) to **re-triage** — read `docs/specs/spec-DIO-0001.md` and incorporate any answers/edits the human added since the last pass.
- Optional `--dry-run` intent: investigate and report what you'd write, but make no file changes.

## Procedure

1. **Decide the mode.**
   - If the input is an id that resolves to an existing `docs/specs/spec-<ID>.md`, this is a **re-triage**: read that file in full — the original `## Feature description`, every prior `## Triage` section, and any answers/edits the human added. Human answers are **authoritative** — never re-ask an answered question.
   - Otherwise it's a **new feature**: the input (inline text, or the file you read) is the original feature description. Allocate an id and create the spec (step 2).

2. **Allocate an id and create the spec (new features only).** Follow the exact id-allocation algorithm in `references/spec-format.md` (read `docs/feature-specs/LEDGER.md`; if it's missing, **ask the user for the 3-letter project code** — suggest one derived from the project/folder name, e.g. *motif → MOT* — then create the ledger). Allocate the next zero-padded id (e.g. `DIO-0001`), update the ledger's counter and table, and write `docs/specs/spec-<ID>.md` using the spec scaffold in `references/spec-format.md` — its `## Feature description` section holds the **original details verbatim**. Set `Status: Triage`.

3. **Fan out (Workflow).** For a large feature, use the `Workflow` tool to parallelize the heavy reading — within a heavy spec, parallel readers for (a) codebase grounding and (b) the Sentinel lens scan. Synthesize the verdict from the subagents. For a small feature, do it inline. This is the "ultracode" speed-up; keep waves small (see limits below).

4. **Ground in the codebase (mandatory).** Use `Glob`/`Grep`/`Read` to locate every component, page, service, route, or feature the description references. Detect ambiguous matches (one name → multiple locations) and naming mismatches (UI label vs route/component name). Map the affected files. Do your technical reasoning internally — it informs the review but never appears in the non-technical section.

5. **Run the Specification Sentinel review.** Classify a strictness tier (S0–S3), run the five-lens scan, the architectural red-flag scan, and assign severities. Default to **stating assumptions, not asking questions**. See `references/sentinel-review.md` for the full framework.

6. **Decide the outcome and append the triage section to the spec.** See `references/spec-format.md` for the exact section shapes, the non-technical language rules, and worked examples.
   - **Ready** (every non-essential gap can be reasonably defaulted): append a "Ready for Implementation Plan" triage section (Sentinel verdict + **UI & logic preview** + Assumptions block when any defaults were picked). Then pass the **Codex cross-family spec review** (below) and — in a full-auto run — the **Assumptions review gate**; only then set `Status: Ready for Plan` in the spec header and in the ledger row.
   - **Needs improvement** (≥1 essential gap per §4 of the framework, or any uncovered S3 gap, or a genuine contradiction only the author can resolve): append an Essential Questions triage section (+ Assumptions block for the non-essential gaps). Set `Status: Needs More Info` in the spec header and ledger row.
   - On **re-triage**, append a **new dated** triage section (don't overwrite prior ones); open it with a short "Resolved:" note summarizing what the human's answers settled, then the current verdict.
   - In **dry-run**, report the verdict and the section you would append; make no file changes.

## Codex cross-family spec review (mandatory where available)

Before the status flips to `Ready for Plan`, hand the written spec to a reviewer **outside Claude's model family**: the Codex CLI running `gpt-5.6-sol` at **`max`** reasoning effort, read-only, grounded in the actual codebase. Everything else in this pipeline is Claude reviewing Claude, and the defect this catches is the one the author's own family is blind to — a spec whose logic doesn't close, or whose "grounding" names code that doesn't do what it claims.

```bash
codex exec -C "<repo root>" -m gpt-5.6-sol -c model_reasoning_effort="max" \
  -s read-only -o /tmp/codex-review-<ID>.md "<prompt>" < /dev/null
```

Full mechanics — the availability check, the verbatim prompt contract (R1), how to dispose of findings, and the fallback rules — are in `feature-spec-pipeline/skills/work/references/codex-cli.md`. Follow it; don't re-derive the invocation here. In brief: `read-only` so the reviewer cannot edit the artifact it is reviewing; pass `-m` and the effort **explicitly** (the user's `~/.codex/config.toml` defaults to a lower effort); `< /dev/null` or it waits on stdin.

**Then act on the findings — running the review is not the gate; acting is.** Per finding: **accept** it and edit the spec, **reject** it with a stated reason (it contradicts a human's authoritative answer, it expands scope the feature description never asked for, or you checked the code and it's wrong), or **escalate** it — a `Critical`/`High` finding that exposes a genuine **external** dependency becomes an Essential Question and the spec goes to `Needs More Info` per step 6. Never flip the status on `MATERIAL DEFECTS` without resolving them. Record the verdict plus the accept/reject tally in the triage section so the planner can see the review happened and how it landed. A finding you adopt without checking is how a spec acquires requirements nobody asked for; Codex is a reviewer, not an authority.

**Two things gate the gate itself.** First, **every Codex call is data egress** — `-s read-only` restricts writes, not the network, so the spec and every file the reviewer opens are transmitted to OpenAI. Second, because of that, a repo can **opt out**: before the call, grep `CLAUDE.md` / `AGENTS.md` / `ORCHESTRATOR.md` for `ANTHROPIC-ONLY`, `NO EXTERNAL MODEL CLIS`, or `external-model-clis: off`. A hit means run the in-family reviewer instead and log `codex: opted out (<file>) → claude` — that is a **correct** run, not a degraded one, so don't ask for an exception. Check it **per invocation**, not once per session: it is the only kill-switch that can reach a run already in flight.

If the lane is genuinely unavailable — no binary, not logged in, usage or rate limit, an empty output file, the deadline firing, repeated errors — the gate falls back to a Claude strong-model one-shot review of the same prompt, and you **note the downgrade in the triage section**. Availability and the opt-out are the only licensed skips: an in-family review is weaker evidence, not no evidence, and the next reader deserves to know which they got.

## Assumptions review gate (full-auto runs)

In a full-auto pipeline run — no human will read the spec between triage and `/plan` — the Assumptions block is a trusted first output: a wrong default doesn't get caught, it gets **built**. So before the status flips to `Ready for Plan`, run one strong-model one-shot review of the Assumptions block (a fresh reviewer — not the agent that wrote the assumptions) answering, per assumption: would this default **surprise the owner**? Does it **reverse a locked or documented decision** (check the spec, the ledger, and the repo's own decision records — CLAUDE.md, plans of record)? Does it **deserve to be an Essential Question** instead — is it really an external dependency wearing a default? Any failure converts that assumption into an Essential Question (→ `Needs More Info`, per step 6) or fixes the default, before the flip. When a human reviews specs before planning, the gate is optional — the human *is* the gate. This gate reviews the defaults; it never re-asks questions a human already answered (those stay authoritative).

**Model note:** the Sentinel verdict + Assumptions synthesis may run on a mid-tier model (sonnet) *because* this gate stands behind it — but **S2/S3 (governance-adjacent) features stay on the strong model end-to-end**: verdict, Assumptions, and the gate itself. Effort is the second dial and is canonical in `feature-spec-pipeline/skills/work/references/model-and-effort.md`: grounding readers run at `low`, the verdict and this gate at `high`, and stepping a reviewer's *effort* down keeps the capability class where stepping its *model* down does not.

## Workflow fan-out limits (avoid throttling)

When step 3 uses the `Workflow` tool to triage features / lenses in parallel:
- **Cap each wave at ≤4 concurrent agents.** Batch a larger fan-out into sequential waves of ≤4 — firing ~10+ agents at once trips a server-side rate limit ("temporarily limiting requests — not your usage limit") that fails most of the wave. Chunk the items and `await` each small `parallel(...)` batch before the next; don't pass all items to one `parallel()`.
- **Retry transient failures.** If an agent's result is an "API Error / Rate limited / temporarily limiting requests" string (or `null`), re-run it in a later small batch; never treat it as a real finding.
- **Prefer plain-text returns for long, file-reading subagents.** Schema-forced subagents that read many files often finish without emitting the structured output; have each return a fixed-shape markdown fragment and reserve any `schema` for the single synthesis step.

## Hard rules

- **Keep the review sections short.** Written output drifts long by default; the triage section is a verdict, a UI-and-logic preview a non-technical reader can skim, and a list of assumptions — each assumption one line stating the default and why, never a paragraph defending it. Length budget in `feature-spec-pipeline/skills/work/references/model-and-effort.md` §7.
- **Non-technical review sections only.** No file paths, code identifiers, library/framework names, or architecture words (module, service, resolver, route, endpoint, schema, …) in the triage review sections. Translate to what the user sees or does. The `## Feature description` section is the exception — it preserves whatever the author wrote, verbatim. Full ban list + good/bad examples in `references/spec-format.md`.
- **Never write an implementation spec, suggested rewrite, or file list** — the `/plan` skill owns that.
- **Never modify the original `## Feature description` section.** Append new triage sections; don't rewrite history.
- Default to assumptions; reserve questions for the essential bar in `references/sentinel-review.md` §4. **The bias is to push the feature through to `Ready for Plan`.** A question is warranted only when the gap is a genuine **external (non-internal) dependency** — one you cannot resolve from the codebase, the closest analogue, the product's norms, or the safer default. Never send a spec to `Needs More Info` because it is large, complex, or loosely worded, or because a human *might* like to decide; those are internal and you resolve them with documented assumptions. When some gaps are essential but the core is buildable, still record the assumptions for the rest so re-triage after one answer can go straight to `Ready for Plan`.
- End your final message with `READY` or `NEEDS IMPROVEMENT` plus the spec id and path so the result is unambiguous.

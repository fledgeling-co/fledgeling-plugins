# Phase 4b — Deferred / additional-work loop

`work` delivers the plan it was given, but a real feature often isn't fully closed by a single `work` pass: the plan had later phases, or `work`'s finalize note lists items it explicitly **deferred**. This loop drives the feature to *actually complete* before it's tested and merged — while keeping everything on **one branch** so it merges as one unit.

## First, read the evidence (don't guess)

After ``work` <ID>` finishes, open two things in the main tree:
- The spec's latest **`## Progress`** section — specifically the "Deferred" line and the clause/reachability tables (a `partial` clause or an unwired reachability row is deferred work by another name).
- The **plan** — check whether it described phases beyond what the progress note says was built.

From those, classify what remains:

## Decision tree

**A. Nothing outstanding.** Progress note shows no deferred items, every clause satisfied, every capability wired → skip to Phase 5 (gap-fix). (Gap-fix will still re-audit — this loop is for *known* remaining scope, not the audit.)

**B. Small, in-scope remainder** — a missed state, one more slice, a wired-but-thin surface; the kind of thing that fits the existing spec and plan.
- Prefer to **re-run ``work` <ID>`**: it reuses the existing worktree (its Setup reuses `.worktrees/<ID>` if present) and picks up where it left off. Point it at the specific deferred items.
- Or, if it's genuinely a *gap* (built-but-short) rather than *unbuilt scope*, let Phase 5's `gap-fix` absorb it — don't do the same work twice. Rule of thumb: **unbuilt scope → `work`; built-but-falls-short → `gap-fix`.**

**C. Substantial new scope that deserves its own spec** — a whole additional capability the original spec under-scoped, big enough that it wants its own triage review, id, and plan. **When in doubt, prefer B over C** — a re-`work` or a gap-fix over minting a child spec. A child spec is justified by *genuine* new scope, not by a wish to look thorough; manufacturing child specs for what a small follow-up pass would close is exactly the over-orchestration the conductor is meant to avoid.
- **`triage`** it as a **child spec**: a new `docs/specs/spec-<CHILD_ID>.md`, allocated from the ledger like any spec, but with its `## Feature description` noting it's a child of `<ID>` (link both ways so the lineage is clear). Give triage the same design-system mock UI context.
- **``plan` <CHILD_ID>`** → `docs`plan`s`plan`-<CHILD_ID>.md`.
- **``work` <CHILD_ID>` — but on the PARENT'S branch, not a new one.** This is the critical bit (see below).
- Record the child spec`plan` paths — Phase 6's e2e must cover the child's flows too.

## Keeping child work on the parent's branch (do NOT let a second worktree spawn)

`work`'s Setup, run naively for `<CHILD_ID>`, would create `.worktrees/<CHILD_ID>` on a brand-new branch `ai/<child_id>` from `INT` — which fragments the feature across two branches and defeats "the feature merged" (singular). Prevent that. Options, best first:

1. **Reuse the parent worktree explicitly.** Before invoking ``work` <CHILD_ID>`, ensure `.worktrees/<ID>` (the parent's, on `ai/<id>`) is the worktree it uses, and tell it to implement the child plan **into `ai/<id>`** rather than creating `.worktrees/<CHILD_ID>`. The child's implementation commits land on the same branch as the parent's. (`work` already supports "if the worktree exists, reuse it" — you're extending that to "use the parent's worktree for the child plan.")
2. **If the skill insists on its own worktree**, let it build on `ai/<child_id>`, then **merge `ai/<child_id>` into `ai/<id>`** immediately (before Phase 5) and remove the child worktree/branch, so from Phase 5 onward there is again exactly one feature branch. This is second-best because it briefly forks; collapse it right away.

Either way, the invariant to hold: **by the time Phase 5 starts, all parent + deferred + child implementation is on `ai/<id>`, and there is one worktree.**

## Loop, don't recurse forever

Repeat B/C until the evidence (progress notes + plans, parent and children) shows no outstanding phase or deferred item. Each pass ends with the same conformance checks `work` runs internally, and you re-read the resulting progress note before deciding whether to loop again. If a "deferred item" turns out to need a human decision (an essential question, a product call), stop and ask — same rule as triage; don't loop on an ambiguity.

## Handing off to Phase 5

Advance to gap-fix with: one feature branch `ai/<id>` carrying all the work; the parent spec + plan; and the full list of child spec`plan` paths (gap-fix and e2e both consume them). Note in your running context which children exist so nothing they added escapes the gap audit or the e2e coverage.

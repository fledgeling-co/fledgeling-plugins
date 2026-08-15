---
name: intake
description: >-
  Turn a rough product or feature idea into triage-ready briefs in docs/features-to-triage/ —
  the pipeline's front door. Given anything from "here's a rough idea for an app" to a one-line
  feature thought, it researches context where the idea is thin (Dossier deep-research panels,
  free lane first), runs a divergent ideation pass (the trawl skill) to propose additional
  features the target audience would likely want, and writes one brief per feature: what and why,
  audience, acceptance sketch, platform expectations (iPhone, iPad, Mac, Web always; Windows
  optional for apps), research pointers, origin and date. Use when the user hands over a rough
  idea, says "add this to the backlog", "break this idea down", "here's an app idea", or routes a
  directive that needs briefs before triage. Writes briefs only — no specs, no ids, no code; the
  triage skill owns readiness.
---

# Pipeline Intake — rough idea to triage-ready briefs

Turn a rough idea into one-or-many **briefs** the triage stage can pick up. A brief is small on
purpose: enough for triage to ground and judge, never a spec. This stage is where the pipeline is
generous — divergent, exploratory, audience-minded — because everything after it narrows.

## Inputs

- A rough idea: inline text, a file, a voice-note transcript, a routed directive. Anything from
  "an app that does X" to "we should probably handle Y".
- Optional: a target repo (default: the current one). The briefs land in that repo's
  `docs/features-to-triage/`.

## Procedure

1. **Read what exists.** `docs/features-to-triage/`, the ledger/board, and any
   `docs/deep-research/` reports — so a new brief extends the backlog instead of duplicating it.
   Match by concept, not wording ("night theme" duplicates `dark-mode`). If the repo keeps an
   out-of-scope record (`.out-of-scope/` or similar), check it: a previously rejected concept is
   surfaced to the user ("this was rejected before because <reason> — still true?"), not silently
   re-added.

2. **Research where the idea is thin.** A rough idea usually leaves open questions about the
   world — market norms, prior art, what competing products do, what the audience already uses.
   Those are research questions, not guesses: run them per
   `${CLAUDE_PLUGIN_ROOT}/references/second-opinion-lanes.md` §Deep research (Dossier
   `research_plan` → panel, free lane first; verify citations; export to
   `docs/deep-research/<slug>.md`). Skip research when the idea is already concrete and internal.

3. **Decompose.** Break the idea into features sized for one pipeline run each (a vertical slice
   a user could see working — "what can I demo when this is done?" is the size test). For an
   app-shaped idea, the standard surface set applies: **iPhone, iPad, Mac, and Web always;
   Windows optional** — record that expectation in each brief so triage and design inherit it.

4. **Ideate past the ask.** Run the `trawl` skill for a divergent pass over the idea, then write
   the additional features/concepts the **target audience would likely want or benefit from** —
   the standard companion features (settings, onboarding, sharing, offline, notifications where
   they genuinely fit), the second-order ideas the research surfaced, the thing a specialist in
   this product category would offer that the idea didn't name. Each becomes its **own brief**
   marked `proposed-by-ai: true`, so the human can delete a file to veto an idea rather than
   answer a question. Propose what earns its place; ten padded briefs bury the three good ones.

5. **Write the briefs.** One file per feature, `docs/features-to-triage/<slug>.md`:

   ```markdown
   # <Feature name>

   - origin: <who/where the idea came from> · <YYYY-MM-DD>
   - audience: <who this is for, one line>
   - platforms: <iphone, ipad, mac, web[, windows] — or n/a for non-app work>
   - proposed-by-ai: <true only for step-4 briefs>
   - research: <docs/deep-research/<slug>.md — omit if none>

   ## What and why
   <2–6 sentences: the user-visible behaviour and the reason it matters.>

   ## Acceptance sketch
   <3–8 bullet outcomes a user could check — a sketch, not criteria; triage sharpens these.>

   ## Assumptions made writing this
   <anything you decided while decomposing, one line each: "assuming X (rather than Y)".>
   ```

6. **Register and report.** On the markdown lane, no id is allocated here — **id allocation is a
   serialized triage write**. On the tasks lane, create one task per brief with the brief as the
   description, status untriaged/`Todo`-equivalent, per
   `${CLAUDE_PLUGIN_ROOT}/references/tracker-adapter.md`. If a fleet is active in the repo
   (in-flight worktrees, fresh ORCHESTRATOR.md), append the briefs to its inbox as
   `untriaged — routed <date>` — an active fleet re-reads its ORCHESTRATOR.md between events, and
   there is no other reliable way to reach in-flight runners. Close with a one-screen summary:
   briefs written (asked-for vs proposed), research run and its cost, and what happens next
   (triage picks them up).

## Rules

- **Briefs, not specs.** No file paths, no architecture, no implementation decisions — the
  acceptance sketch is outcomes. Triage grounds; plan decides.
- **Decisions stay deferred.** Anything you had to pick while decomposing is an assumption line
  in the brief, named with the alternative it beat — never a question back to the user, unless it
  survives the whole gate in `references/second-opinion-lanes.md` (taste, cost, scope, risk).
- **Proposed ideas are labelled and separable.** A human deletes a file to veto; nothing bundles
  an AI proposal into an asked-for feature.
- **Research spend is visible.** Say what a panel cost before relying on it; free lane first.

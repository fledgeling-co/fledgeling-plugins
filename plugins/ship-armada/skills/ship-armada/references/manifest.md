# ARMADA.md — manifest format and rebuild procedure

`~/Dev/ARMADA.md` is the single source of truth the armada plans from. This reference defines its structure (so any agent can repair it) and the survey procedure that rebuilds it from scratch.

## File structure

```markdown
# ARMADA — ~/Dev portfolio manifest
<preamble: purpose, update protocol pointer (armada-sync), format pointer (this file), last full survey date>

## Index
<one table: project | group | category | status (short phrase) | updated>

## Portfolio groups
<the named clusters and which projects belong to each, one line of context per group>

## Cross-project opportunities
<numbered register of portfolio-level upgrade opportunities; each names its affected projects>

## Campaigns
<table: id | campaign | projects | status (proposed/approved/running/done) | notes>

## Projects
<### entry per active project — template in the armada-sync skill; ≤20 lines each>

## Changelog
<append-only: - YYYY-MM-DD <project|campaign>: <one clause>>
```

Entry template and per-entry update rules live in the **armada-sync** skill (fledgeling-plugins) — one place, both skills follow it.

## Rebuild procedure (full survey)

Use when ARMADA.md is missing, corrupt, or a full re-survey is requested. This is a fan-out job — use the Workflow tool, one reviewer per repo, schema-enforced output.

1. **Enumerate — the inclusion rule is ownership, then activity.** A portfolio dir belongs in the manifest when it is **user-owned**: it has no git repo, no git remote, or its origin owner is on the portfolio's **owner allow-list**. That list is configuration, not skill text — read it from the portfolio root's `CLAUDE.md` (an `owner allow-list:` line or the operating-rules section); if none is written there, derive a candidate list from `git config user.email` + the origin owners of clearly-authored repos, show it to the user once, and write the confirmed list into the portfolio `CLAUDE.md` so every later session reads the same rule. The list may grow — use judgement for a repo that is clearly the user's authorship under a new org, and confirm the new owner with the user before extending it. Repos with third-party origins are excluded from the manifest entirely — not listed, never modified. Then apply the activity window (default 45 days): last commit date for git repos, newest file mtime for non-git dirs. Skip worktree copies (`*-wt`, `*-worktrees`, `*-wave-*` dirs).
2. **Fan out reviewers** (session model, effort `low` — do not override to a smaller-context model; this session's tool surface can overflow it). Each reviewer, per repo: read README/CLAUDE.md/overview + up to ~5 feature/marketing md; `git log -5` + `git remote -v` (quote paths — some dir names contain spaces); Glob for ORCHESTRATOR*.md, **/LEDGER.md, spec-*.md, plan-*.md, DESIGN*.md; newest mock html under design/mocks/**, design/**, mocks/**; one line per `apps/*` sub-app; ≤4 grounded AI/tech opportunities. Flag scratch dirs and superseded variants of other repos plainly in status. Exclude .worktrees/node_modules/dist. Return structured data, repo-relative paths only.
3. **Synthesize** groups + cross-project opportunities from the structured results (one agent, or inline if few repos changed).
4. **Write the file** in the structure above; verify a sample of paths exist before writing (a reviewer hallucinating one path poisons the manifest).
5. Stamp the preamble's "last full survey" date and add a changelog line.

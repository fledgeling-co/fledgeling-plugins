---
name: armada-sync
description: Keep the portfolio manifest ~/Dev/ARMADA.md truthful after working in any ~/Dev project. Use this after completing meaningful work in a project under ~/Dev (a feature shipped, a spec/plan/mock added, a status change, a rename, new sub-app, new deploy) — or whenever someone says "update the armada manifest", "sync the master file", "refresh ARMADA.md", or "make sure the portfolio file knows about this". Also invoked by ship-armada when it finds a stale entry. Updates ONLY the current project's entry (status, features, key-file references, updated stamp) plus its index row and one changelog line — it never rewrites the whole manifest and never touches other projects' entries. If the project has no entry yet, it appends one from the template. NOT for creating the manifest from scratch or portfolio-wide planning (use ship-armada).
---

# Armada Sync — keep the portfolio manifest honest

`~/Dev/ARMADA.md` is the manifest of record for every active project in `~/Dev`. The `ship-armada` orchestrator plans portfolio-wide work from it, so a stale entry causes bad plans. Your job here is one surgical update: make the entry for the project you just worked in match reality, and stop.

Deliver exactly that scope. Do not refresh other entries, reorganize the manifest, or expand this into a portfolio survey — those belong to `ship-armada`.

## Protocol

1. **Identify the project.** It is the `~/Dev/<project>` directory you are working in (walk up from cwd to the child of `~/Dev`). If you are in `~/Dev` itself, ask which project to sync rather than guessing.
2. **Read the current entry.** Open `~/Dev/ARMADA.md`, find the `### <project>` section and its row in the index table. If the manifest does not exist, say so and suggest running `ship-armada` (survey mode) to create it; do not scaffold a one-project manifest.
3. **Gather the delta cheaply.** `git -C ~/Dev/<project> log --oneline --since=<entry's updated stamp>` plus what you already know from the session. Only open docs (README, CLAUDE.md, specs/plans dirs, mocks) whose references you have reason to believe changed.
4. **Rewrite the entry in place**, keeping the template shape below and the entry under ~20 lines. Update: the `updated:` stamp (today, YYYY-MM-DD), **Status** (1–2 sentences of current truth), **Features** (add/adjust; keep the list ≤8, most important first), **Read more** paths (specs/plans counts, new ORCHESTRATOR.md, newest mocks — verify each path you write exists), and **AI/tech opportunities** if the work closed or created one.
5. **Update the index row** (same status phrase, same date) and **append one line** to the `## Changelog` section: `- 2026-08-07 <project>: <what changed in one clause>`.
6. **Report** in one or two sentences what you changed in the entry.

## Entry template

```markdown
### <project> · <category> · updated: YYYY-MM-DD

**What:** <1–2 sentences: what it is, who it's for.>
**Status:** <1–2 sentences: current state of work.>
**Stack:** <one line.>
**Apps:** <`apps/<name>` — one-line purpose; omit section if no apps dir.>
**Features:** <comma-separated or short list, ≤8, most important first.>
**AI/tech opportunities:** <≤3 concrete, grounded items; omit if none.>
**Read more:** `README.md` · `CLAUDE.md` · `<ORCHESTRATOR.md path>` · specs: `<dir>` (n) · plans: `<dir>` (n) · design: `<DESIGN*.md>` · mocks: `<newest mock html paths>`
```

Rules that keep the manifest useful: every path is repo-relative and must exist at write time (a broken reference is worse than no reference); prose states facts, not aspirations; if the project is finished or parked, say so in **Status** rather than deleting the entry.

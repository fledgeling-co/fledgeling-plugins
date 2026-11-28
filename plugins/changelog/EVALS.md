# EVALS

**No comparative eval has been run.** No session has compared Claude with this skill against Claude without it, so the claim that it writes a better progress record than a report typed into chat is untested. That's stated here at the top so nobody reads the rest as a benchmark.

The skill was built in one session that went on designing the page, writing the checker and wiring the Chrome reload. Three create-skill checkpoints were handled differently from the full pipeline, and each is recorded below.

## What was verified mechanically

**The checker can fail.** `changelog.py self-test` takes the bundled example page, breaks it in 17 specific ways, and confirms each break produces a failure. It also confirms a freshly created page passes with `--allow-empty`.

```
$ python3 skills/changelog/scripts/changelog.py self-test
  passes   a freshly initialised page, with --allow-empty
  fires    three-sentence subtitle
  fires    eleven-word title
  fires    code in the plain version
  fires    ticket number in the plain version
  fires    open entry saying nothing remains
  fires    missing facet
  fires    oldest entry first
  fires    timestamp without an offset
  fires    update without last updated
  fires    placeholder left in
  fires    duplicate SVG id
  fires    entry above the marker
  fires    bad id
  fires    no entries
  fires    a paragraph instead of bullets
  fires    a fifteen-word bullet
  fires    five bullets
self-test: 17 of 17 checks fired; bundled example passes with 3 entries
```

In 1.1.0 the three sections became short bullets, and three rules were added to hold them there. The first version of the run had 13 of 14. The duplicate-id rule only compared ids across different diagrams, so a duplicate inside one diagram passed. It now checks every id on the page.

**The page finds the main checkout.** `changelog.py path` run inside a linked git worktree returned the main checkout's root, and `init` created the page there rather than in the worktree.

**Both Chrome paths reload rather than duplicate.** On 27 Nov 2026 a test page was opened, changed and shown again by each path. `scripts/chrome-show.sh` printed `opened`, then `reloaded window 1 tab 27`. The Chrome DevTools MCP path reloaded the same tab with `navigate_page`, and reading the page back returned the changed text. The test tab was closed afterwards.

**The template renders as designed.** In agent-browser (Chromium) at 1440×900 and 375×812, light and dark, in both views:

| Check | Result |
|---|---|
| Horizontal overflow at 375px | none (`scrollWidth` 375, `innerWidth` 375) |
| Technical blocks shown in the plain view | 0 of 9 |
| View switch | sets `?view=technical`, persists, moves with the arrow keys |
| design-craft lint | 0 critical, 0 major, after the amber "Remaining" label was darkened from 4.41:1 to clear 4.5:1 |
| ux-craft lint | 0 failures; 3 warnings, one of them a false positive reading a heading as a destructive action |

## The tasks that would settle it

`evals/evals.json` carries three, each to be run with the skill and without it on the same prompt and graded by its listed assertions:

1. **first-entry-open-work**: a merged change with a load test that never ran and a flag waiting on the owner. Does the page get created in the main checkout, does Remaining name both, and does the plain version stay free of code and PR numbers?
2. **small-progress-updates-newest**: six more tests on the same branch, nothing merged. Does the newest entry get updated in place with its timestamps extended, rather than a near-duplicate entry added?
3. **architecture-change-gets-a-visual**: a finished round that replaced a scheduler with a queue worker, nothing left. Does it add a new entry marked complete, and does it invoke `visualization:visualization` and paste the exported diagram?

The baseline for each is the same prompt with the old instruction in `~/.claude/CLAUDE.md` and no skill. A tie on any of the three goes in this table as a tie.

## Pipeline steps handled differently

- **Research.** No new research panel was bought. The domain is covered by the corpus behind `status-update:status-update` (2,400 report units from 1,193 real status reports, mined 4 Sep 2026), which this skill reuses and cites in `references/evidence.md`.
- **Discovery.** There was no separate interview. The owner specified the page over six messages in the building session, quoted in `references/evidence.md`. The owner chose the name and the icon concept directly.
- **Icon.** Three engines ran. The owner chose the raster take to ship; it scored 11 of 12 on the icon rubric. The hand-authored SVG master (10 of 12) is kept as `assets/icon.svg`, and no fidelity loop was run to bring its material up to the raster's.

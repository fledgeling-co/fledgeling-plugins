# Evidence

Where each rule in this skill comes from, and what is not established.

## The owner's specification

The skill was specified by its owner over one Claude Code session on 27 Nov 2026, as a series of changes to the global `~/.claude/CLAUDE.md`:

| Rule | The owner's words |
|---|---|
| A reverse-chronological changelog replaces STATUS.html pages | "no longer create status.html's but instead create (or keep updated) a reverse-chrolnological order changelog with rich details that are susinct and make use of /visualization:visualization where it would help to explain the changes, so that I can see what has actually been achieved" |
| It is an HTML page, opened or reloaded in Chrome, found through the Chrome MCP | "id still like it to be a part of a html page that gets opened or refeshed (if already open - check with chrome mcp not md file" |
| Small reports update the newest entry, with timestamps | "Not every status update needs a new section in the change log, it can just edit a previous version of the update if not much has changed and specify the dates and times that it was updated and last updated." |
| Plain and technical versions | "the changelog updates should show technical and non-technical versions of the same update" |
| Task, Achieved, Remaining; one-line title; two-line subtitle | "There should be clear "Task", "Achieved", "Remaining" for each update in the changelog, with a one line title and two line subtitle that sucinctly outlines what was achieved" |
| Columns on desktop; one version at a time; a richer page | "perhaps have the 3 sections in columns on desktop. never show both technical and non-technical, make it a toggle. Make the page feel richer overall" |

Two calls were made without the owner and are recorded here so they can be reversed: **Plain is the default view**, because a non-technical reader is the one who will not know to look for a switch, while an engineer will; and **"not much has changed" was defined** as the four events in step 2 of the procedure (a merge or release, a finished wave, a gate switching state, a title that no longer fits), because an undefined threshold is applied differently by every runner.

## Measured on this machine

- **Duplicate tabs.** On 27 Nov 2026, `list_pages` through the `chrome-devtools` MCP showed 26 tabs in the owner's Chrome, 14 of them the same project's `STATUS.html`, left by repeated `open` calls. That is why step 7 reloads an existing tab.
- **Resolved paths.** The same listing showed pages under `~/DevEx` as `file:///Volumes/LLMs/Dev/...`, so a match on the unresolved path misses them.
- **Both show paths work.** The MCP path (`list_pages`, `navigate_page` with `type: "reload"`) and `scripts/chrome-show.sh` were each run against a test page that was changed between loads; both showed the new content, and the script printed `opened` then `reloaded window 1 tab 27`. The MCP with `--auto-connect` was configured only in dAIolog's `.mcp.json` on that date, which is why the AppleScript path exists.
- **Worktrees.** `changelog.py path` was run from a linked worktree and returned the main checkout's root.

## Reused research

No new research panel was bought. The domain, how agents report finished work, is covered by the corpus behind `status-update:status-update`: 2,400 report units from 1,193 real status reports across 27 projects, mined 4 Sep 2026 (that skill's `references/evidence.md`). Three of its findings carry over:

- the plain-words substitutions in `entry-writing.md`, which come from that skill's `plain-words.md`;
- "a check that examined nothing is not a pass" and "an alarm that caught nothing is not armed", the two errors that corpus found agents making and retracting;
- the owner-actions zone (600 occurrences, 6.7%), which is why Remaining ends with what waits on the owner.

That corpus is one developer's 14 days of agent reports, so it describes this portfolio's habits rather than reporting in general.

## The template

`assets/changelog-template.html` was designed through `design-craft:design-craft` and `ux-craft:ux-craft` and rendered in agent-browser (Chromium) at 1440×900 and 375×812, light and dark, in both views. Measured on the final round: no horizontal page overflow at 375px (`scrollWidth` 375 against `innerWidth` 375); 0 technical blocks displayed in the plain view; the view switch sets `?view=technical`, persists to `localStorage`, and changes with the arrow keys; design-lint reported 0 critical and 0 major after the amber "Remaining" label was darkened from a measured 4.41:1 to clear 4.5:1.

Choices and their sources:

- **Atkinson Hyperlegible Next and Mono**, chosen because the pages mix plain prose with commit hashes, counts and identifiers, and this family was designed to keep 0/O and 1/l/I apart.
- **The avoid list** in the design brief (cream or off-white ground, italic accent words in headings, numbered 01/02/03 labels, monospace labels, pill buttons) is the set Anthropic's Opus 5.5 prompting guide names as that model's frontend defaults.
- **Layout references** from Mobbin: Tally's dated entries with content beside the date, and Zoom's timestamped version-history rail.
- **Figures sit on a light plate** in both themes because visualization:visualization's exported SVGs carry their own `#f5f5f5` paper.

## Not established

- **No with-skill against without-skill comparison was run.** `EVALS.md` says so and names the tasks that would settle it.
- **The plain-language check is a pattern list.** It catches code, ticket numbers, pull-request numbers, commit hashes, file paths and flags; it cannot tell whether a sentence a stranger reads is actually clear.
- **Print and reduced-motion styles** are present in the template and were not rendered.

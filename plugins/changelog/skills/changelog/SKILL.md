---
name: changelog
description: Keep a project's progress record as a reverse-chronological CHANGELOG.html page, one entry per piece of work, each told twice (a plain version for anyone, a technical version for engineers) under Task, Achieved and Remaining, with diagrams from visualization:visualization where a picture explains the change faster than prose. Use it whenever you would otherwise write a status update, progress summary or end-of-work report in a ~/Dev project, after shipping a feature, finishing a fleet or wave, running a test campaign or closing gaps, and when someone asks "how did that go", "what shipped", "update the changelog" or "log this". It creates the page from the template, adds an entry or updates the newest one, checks the structure with a script, and reloads the page's open Chrome tab rather than opening a duplicate. Not for "what's left" or "where are we" (answer those in chat), release notes for a package's users (that is the repo's own CHANGELOG.md), or ARMADA.md (armada-sync:armada-sync owns it).
---

# Changelog

A status report typed into chat scrolls away, and a status page that is overwritten each time shows only the latest state. This skill keeps the third thing: a record of what each project has actually achieved, newest first, that the owner can scroll back through and that a non-technical reader can follow without asking anyone.

Every entry tells one piece of work twice, as a plain version and a technical version of the same three parts, each a few short bullets: **Task** (what the work set out to do), **Achieved** (what works now, and how we know) and **Remaining** (what is left, and what waits on the owner). The page shows one version at a time behind a Plain / Technical switch, Plain by default, and lays the three parts out as columns on a desktop screen.

What lives where: `assets/changelog-template.html` is the page shell (designed through `design-craft:design-craft` and `ux-craft:ux-craft`; leave its styles alone), `assets/example-changelog.html` is a filled example with three synthetic entries, `scripts/changelog.py` creates, timestamps and checks the page, `scripts/chrome-show.sh` reloads or opens the page in Chrome, `references/entry-writing.md` is how to write each part well, and `references/evidence.md` records where each rule comes from.

## Procedure

Run the scripts with the skill directory as the base, for example `python3 <skill-dir>/scripts/changelog.py`.

### 1. Find or create the page

```bash
python3 scripts/changelog.py path --repo .          # prints <main checkout>/CHANGELOG.html
python3 scripts/changelog.py init --repo . --project "<Project name>"   # only when it does not exist
```

The page lives at the root of the repo's **main checkout**, never a worktree: a worktree is removed when its branch merges, and a Chrome tab opened on its copy then points at a deleted file. `path` resolves the main checkout from inside a worktree. `init` copies the template, sets the project name in the title and masthead, and does nothing if the page already exists. Use the name people call the project, which is usually the repo name.

A repo's existing `CHANGELOG.md` is a different document, release notes for the repo's own readers. Leave it as it is.

### 2. Decide: a new entry, or update the newest one

Update the newest entry in place when this report is about the same piece of work it describes (the same feature, branch, fleet or campaign) and none of these has happened since it was last updated:

- something merged, shipped or was released;
- a wave or fleet finished;
- a check or test gate switched between failing and passing;
- the title no longer describes the work.

Otherwise add a new entry. A report about different work, or about work whose entry is no longer the newest, always gets a new entry. Only the newest entry is ever revised; every older entry records what was true when it was last updated, so change one only to correct a factual error, and then add a dated sentence inside it saying what you corrected.

### 3. Gather the facts before writing

An entry records what was achieved, not what was intended, so collect the evidence first: the commands you ran and their results, test and gate counts, the PR or commit, measured numbers, what did not run, and what is waiting on the owner. Write only what you observed. A check that examined nothing is not a pass, and a step you skipped is named as skipped.

### 4. Write the entry

Copy the `<article>` inside the page's `<template id="entry-template">` and paste it on the line directly below the `<!-- changelog:entries` comment, above every earlier entry. Get the timestamps from the script rather than working out the Sydney offset yourself:

```bash
python3 scripts/changelog.py stamp
```

Fill every slot. `references/entry-writing.md` covers each one with a worked example; the short form:

| Part | Holds |
|---|---|
| `id`, date line | `YYYY-MM-DD-<slug>`, the day the entry was first written, Sydney time |
| `data-remaining` | `open` when Remaining lists anything, `none` when it says "Nothing remaining." |
| Title (`h2`) | the outcome in 10 words or fewer, on one line |
| Subtitle | exactly 2 sentences of 25 words or fewer: what was achieved, then what it means, in words both readers follow |
| Timestamp line | `Written <time>`; after an update, `Written … · updated …, … · last updated …` |
| Task | plain: 1 bullet on what the work set out to do · technical: 1–2 bullets naming the ticket, spec or branch |
| Achieved | plain: 1–3 bullets on what someone can now do, see or rely on · technical: 1–4 bullets with the numbers and the PR or commit, one of them starting "Proof:" with the command or measurement |
| Remaining | plain: 1–2 bullets, including anything waiting on the owner · technical: one bullet per open item, blocked task, missing credential or decision. When nothing remains, the single bullet "Nothing remaining." in both |

Task, Achieved and Remaining are written as short bullets so the owner can read an entry at a glance: each version is one `<ul>`, 1 to 4 bullets, each bullet 14 words or fewer, with no full stop unless it is a sentence. Write a bullet as a fragment that carries its own subject and number ("500 of 500 arrived through two restarts"), never a paragraph cut into pieces. The title and subtitle stay as prose; they are where the story is told. The plain version is for a founder, customer or investor: everyday words, no file paths, commands, function names, ticket numbers, commit hashes or unexplained acronyms. Keep a number in it when it means something to that reader ("checkout loads in under a second") and leave the rest to the technical version. Both versions describe the same state, so when you update an entry, revise both, the subtitle, and the timestamp line together.

### 5. Add a visual where a picture explains the change faster than the prose

Good candidates: an architecture or data flow that moved, a before-and-after metric, a new user flow, a dependency that was cut. A fix or a config edit usually needs none, and an entry takes two visuals at most.

1. Invoke `visualization:visualization` to draw it. Use the project's visualization style profile when it has one and the default skin when it does not, without stopping to ask about style; this skill is the standing answer to that skill's first-run style question.
2. Invoke `visualization:visualization` again with the arguments `export <html-file> svg`; this skill is the standing request its export step waits for.
3. Keep both files as `docs/changelog/<YYYY-MM-DD>-<slug>.html` and `.svg`.
4. Paste the exported `<svg>` element into a `<figure class="visual">` placed directly in the `<article>`, after the facets, so it spans the full width. Its `<figcaption>` says what it shows and links the HTML version. Add `plain` or `technical` to the figure's class to show it in one view only: an architecture diagram is usually `technical`, a before-and-after chart both readers follow carries no extra class.

The export prefixes each SVG's ids, which is what lets several figures share one page; the checker fails on any repeated id.

### 6. Check the page

```bash
python3 scripts/changelog.py check <path to CHANGELOG.html>
```

Exit 0 is the only pass. It checks the structure: entry order, ids, dates, the title and subtitle limits, timestamps with an offset, the three parts with both versions as short bullet lists, Remaining agreeing with `data-remaining`, code and ticket numbers kept out of the plain version, leftover template text, and repeated ids. Fix what it reports and run it again. It cannot tell whether the words are true, which is step 3's job.

### 7. Show the page, reusing its tab

Opening the file afresh each time stacks duplicate tabs: on 27 Nov 2026 one Chrome held 14 tabs of a single project's status page. So reload the tab that already has the page, and open a new one only when none does. Match on the page's resolved `file://` URL, since a file under `~/DevEx` shows in Chrome as `/Volumes/LLMs/Dev/...`.

1. When the session has the `chrome-devtools` MCP running with `--auto-connect` (it attaches to the owner's running Chrome), call `list_pages` and confirm the owner's own tabs appear. Take the first page whose URL starts with the resolved URL, call `navigate_page` with its `pageId` and `type: "reload"`, then `select_page` with `bringToFront: true`. When no page matches, call `new_page` with the URL. Leave any other matching tabs open. If `list_pages` times out waiting for the browser connection, accept Chrome's remote-debugging prompt with the proctor MCP and retry once.
2. Otherwise, or when the MCP still cannot attach, run `scripts/chrome-show.sh <path to CHANGELOG.html>`. It does the same through AppleScript and prints `reloaded window N tab M` or `opened`; when Chrome is not running it exits 1 without launching it.

Never launch a new Chrome instance for this.

### 8. Reply in two lines

The outcome, whether you added an entry or updated the newest one, and that the page is showing; then anything that needs the owner. If nothing does, say so.

```
webhook-relay: 14 of 14 retry tasks merged, two checks never ran. New entry; CHANGELOG.html reloaded in Chrome.
Waiting on you: the staging database password, blocked since Tuesday.
```

The page carries the rest; repeating it in chat is the habit this replaces.

## Constraints

- **Work across two or more projects, or a fleet with parallel runners,** gets one entry in each changed project's page, written by the conductor after the merges land. Runners writing to one shared file overwrite each other's entries, so a runner reports to its conductor and never edits the page.
- **Edit entries, not the shell.** The stylesheet and script are shared across every project's page so entries read the same everywhere. If the shell needs to change, change the template in this skill.
- **Leave existing `STATUS.html` pages where they are.** This skill replaces `status-update:status-update` for reporting; it does not delete what that skill made.
- **"Where are we" and "what's left"** ask about remaining work rather than the record. Answer them in chat as a status answer, pointing at the newest entry where it helps.
- **`ARMADA.md` stays with `armada-sync:armada-sync`.** A substantial piece of work usually wants both: the manifest for orchestrators to plan from, the changelog for people to read.
- **Outside `~/Dev`**, or for a question with a one-line answer, reply in chat instead.

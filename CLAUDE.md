# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Adding or renaming a plugin — four places, one commit

A plugin is not "added" when its directory exists. It is added when it is
installable and discoverable, and that takes four separate registrations. Land
all of them in the same commit as the plugin itself: a plugin present in
`plugins/` but absent from the README is invisible to everyone who did not build
it, and absent from `marketplace.json` it cannot be installed at all.

1. **`plugins/<name>/.claude-plugin/plugin.json`** — `name`, `description`,
   `version`, `author`. The `name` must match the directory and the marketplace
   entry exactly.
2. **`.claude-plugin/marketplace.json`** — append to `plugins` with
   `source: "./plugins/<name>"` and a `category`. Keep `name` and `version`
   identical to `plugin.json`; a mismatch installs the wrong thing or nothing.
3. **`plugins/<name>/README.md`** — what it does, how to invoke it, and what it
   refuses to do. This is the page the root README links to.
4. **The root `README.md` row**, in the `## The skills` section.

### The root README row has a shape, and it breaks quietly

Copy an existing block exactly. Each entry is four parts in this order, and the
separator is load-bearing:

```markdown
<br clear="left" />

<a href="plugins/<name>/README.md"><img src="plugins/<name>/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [<name>](plugins/<name>/README.md)

One paragraph: what it does and what makes it different.
```

The icon is floated left at 110px, so **every entry needs its own
`<br clear="left" />` before it**. Omit it and the new icon floats up beside the
previous entry's paragraph — the row is present in the source, renders as an
overlapping mess, and reads to a human as "my plugin isn't in the README". That
failure has happened; it is why this section exists.

Two things to verify before committing, because both fail silently:

- `plugins/<name>/assets/icon-256.png` exists — the README shows a broken image
  otherwise, and nothing warns you.
- `git ls-files -s plugins/<name>/skills/*/scripts` shows mode `100755` for
  anything executable. A script committed 644 fails at runtime for everyone who
  installs it, though it works fine on the machine that wrote it.

The first of those now has a second net: `site/scripts/build-catalogue.mjs` runs
before every site build and **exits non-zero** on a missing icon, a missing
SKILL.md, or a version that disagrees between `plugin.json` and
`marketplace.json`. It does not run on a plain `git commit`, so the README check
above still matters — but a broken plugin can no longer reach production.

## Adding a plugin now also drafts an email

A `pre-push` hook in `.githooks/` watches `.claude-plugin/marketplace.json`. When
a push changes it, the hook runs `site/scripts/digest-draft.mjs`, which finds any
skill the catalogue has and the database does not, and writes its announcement
copy with `claude --model claude-sonnet-5 --effort high` through
`/create-luke-content`. That copy goes out to subscribers at 10am Sydney time,
daily or weekly, from `site/app/api/cron/digest`.

Consequences worth knowing before you push:

- **Only genuinely new skills mail.** A version bump on an existing skill never
  does; the row already exists and the unique index on `skill` keeps it that way.
- **The push blocks for about a minute per new skill.** `SKIP_DIGEST=1 git push`
  or `git push --no-verify` skips it, and `pnpm digest:draft` in `site/` catches
  up later. Drafting never sends, so skipping costs nothing but time.
- **The hook needs installing once**: `git config core.hooksPath .githooks`.
- **A fresh database needs `pnpm digest:seed` first**, or every published skill
  looks new at once. The drafter refuses to run until it has been seeded.
- Auto-send is on after the first issue is approved. `pnpm digest:hold` turns it
  back off; `pnpm digest:approve` releases whatever is waiting.

## The site indexes this repo — there is no fifth registration

`site/` is a Next.js app deployed to **skills.fledgeling.app** (its own Vercel
project, Root Directory `site`). It builds its catalogue from
`.claude-plugin/marketplace.json` plus each plugin's `plugin.json`, `SKILL.md`,
`README.md` and icon, at build time. A new plugin that lands in the four places
above appears on the site automatically on the next deploy; nothing there needs
editing by hand.

Two things in `site/` are hand-maintained, and both degrade quietly rather than
breaking when a new plugin arrives:

- `site/scripts/build-catalogue.mjs` → `GROUP_OF`, which places each plugin on
  the browse axis. An unlisted plugin lands under "Uncategorised" and warns.
- `site/content/examples.ts`, the only content on the site not extracted from the
  repo: a representative sample output per skill, rendered with a visible
  "illustrative, not captured from a run" marker. A plugin with no entry simply
  renders no example. Do not add one whose claims are not traceable to that
  skill's own documentation.

### After every new or updated skill, run the gate

```bash
node site/scripts/build-catalogue.mjs   # must exit 0
```

The four registrations above are not a checklist you can satisfy from memory, and
`should-compact` proved it: it landed with `plugin.json`, `marketplace.json`, a
SKILL.md and a full icon set, and no README. That is a **hard failure**, not a
warning, so from that commit until it was noticed `skills.fledgeling.app` could
not build at all and neither could `pnpm dev`. Nothing in the plugin looked
broken; the site was simply gone.

Check the exit code rather than the output. Piping the script through `grep` was
how the failure got read as a pass in the first place, because `$?` is then
grep's status and not the gate's.

What the gate cannot see, so check it yourself:

- **The root README row**, and its `<br clear="left" />` (the shape at the top of
  this file). Missing rows render as an overlapping mess, not as an error.
- **`GROUP_OF`** in `build-catalogue.mjs`, or the skill sits under
  "Uncategorised" with only a warning.
- **A stale sibling name** anywhere in the descriptions. Renaming a skill leaves
  the old name in every `description` that referred to it, in both manifests, and
  nothing checks that a named skill exists.

Icons follow the family: squircle silhouette from
`plugins/create-mac-icon/assets/squircle-path.txt`, one metaphor, restrained
palette, one warm accent. Sizes are 1024 (`icon.png`), 256 and 128. Keep the
source (`icon-src.svg` or the generator) beside them so the next size can be
re-rendered rather than re-invented.

### Branch before you commit

Check what branch you are on first. This repo's plugin work happens on
short-lived per-plugin branches, and landing a new plugin on top of an unrelated
one entangles two things that should merge separately.

## Portfolio manifest

This project is tracked in `~/Dev/ARMADA.md`, the portfolio manifest the `ship-armada` orchestrator plans from. After completing work here that changes the project's status, features, or the location of its key docs (specs, plans, mocks, ORCHESTRATOR.md), refresh this project's entry with the `armada-sync` skill (fledgeling-plugins). If that skill isn't available, edit the entry directly — keep it under 20 lines, verify every path you write exists, and update its `updated:` stamp.

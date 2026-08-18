# Evals

**Nothing in this file is a measured result about the skill.** The eval suite exists now, in [`evals/evals.json`](evals/evals.json), and it has not been run. No prompt has been executed with the skill loaded, none without it, no judge has looked at anything, and there is no pass rate. Shipping in that state is honest; shipping a file that quietly omits the subject is not, because it reads as though the pipeline ran.

What follows is what was checked mechanically, what the eval set would settle, and what none of it can tell you.

## What was checked, and what it found

armada-sync has no scripts. Its only artifact is the file it maintains, `~/Dev/ARMADA.md`, so the mechanical checks are all about whether that file currently obeys the rules this skill enforces. Every figure below was counted from that file on 18 Aug 2026.

**The SKILL.md parses.** Frontmatter reads as strict YAML, carries exactly `name` and `description`, and the name matches the plugin directory.

**The manifest is where the skill says it is, and its shape holds.** 963 lines. **70** project entries, and all 70 match the template's heading shape (`### <project> · <category> · updated: YYYY-MM-DD`). All 70 carry every one of the five required field labels: What, Status, Stack, Features, Read more. There is exactly one `## Changelog` heading. Every entry's `updated:` stamp parses as a date, ranging from 2026-08-07 to 2026-08-18.

**The twenty-line ceiling holds everywhere it can be measured.** One entry exceeded 20 non-blank lines in my count, and that is an artifact of how I split the file rather than a real breach: `sift` is the last entry, so it ran on into the Changelog section. Every other entry is inside the ceiling.

**Nine path references do not resolve, and this is the one real failure.** The skill's own hard rule is that every path is repo-relative and must exist at write time, because a broken reference is worse than no reference. I resolved every backtick-quoted path in every `Read more:` line against its project directory: **727 paths checked, 9 unresolved**.

| project | path that does not exist |
|---|---|
| deep-research-mcp | `dossier-ios-mock.html` |
| deep-research-mcp | `dossier-ipados-mock.html` |
| deep-research-mcp | `dossier-web-mock.html` |
| deep-research-mcp | `dossier-widgets-mock.html` |
| deep-research-mcp | `dossier-pairing-mock.html` |
| cairncopy | `design/DESIGN-APP.md` |
| anvil | `docs/OPEN_ENDS.md` |
| egress | `README.md` |
| egress | `CLAUDE.md` |

None of the five deep-research-mcp mocks exists anywhere in that project, so they were not merely moved. `cairncopy/design/` holds `icon`, `marketing` and `mocks` but no `DESIGN-APP.md`. `egress/` has no README and no CLAUDE.md at its root at all.

My checker also flagged four things that are **not** failures, and they are worth naming because a future run of this check will hit them again: three of them are a git remote URL, a branch name and a commit sha appearing in prose after `splice`'s Read more list, and the fourth is `fledgeling-plugins/plugins/proctor/`, which is labelled as a sibling repository path rather than a project-relative one. So the honest number is nine, not thirteen.

That failure rate is 1.2 percent of references, which sounds small and is exactly the thing the rule exists to prevent. A reader who follows one of those nine finds nothing, and cannot tell whether the file is stale or the project moved.

**No prior run exists.** No `grading.json`, no `results/` directory, no `benchmark.json`, no committed judge log, no blind-panel key anywhere under `plugins/armada-sync/`. Checked, not assumed.

## What the eval set would settle

Eight prompts, in `evals/evals.json`. Each runs twice, once with the skill and once without, because there is no predecessor and the honest question is whether the skill earns its context.

**Run every one of them against a copy of the manifest, never the live file.** The whole set edits a real portfolio document, and an eval that corrupts the thing it measures is not an eval.

Three prompts are where the answer would come from:

1. **`every-path-is-verified-before-it-is-written`.** This is the one the nine broken references above make urgent. The prompt tells the run that a mocks directory was deleted and a design doc moved, then grades whether the rewritten entry carries the dead path forward. The measurement is a stat call per path, so this grades cleanly with no judgment involved. A baseline plausibly rewrites the entry from the old one, which is how those nine got there.

2. **`no-manifest-means-no-scaffold`.** Run in a tree with no `~/Dev/ARMADA.md`. Being helpful means creating one, and a one-project manifest looks like the manifest of record and is not. Grade one property: was a file created.

3. **`a-nudge-toward-the-portfolio-does-not-widen-the-scope`.** The user mentions in passing that other entries look stale. The scope rule says one entry, and portfolio work belongs to ship-armada. Grade the diff: exactly one entry section should differ.

Grade with a subagent that never sees the skill. Most of this set grades off a diff of the manifest copy, which is why the assertions are worded as properties of that diff rather than as qualities of the reply.

## Caveats, stated rather than buried

- **Nothing above measures the skill.** The 727 paths and the 9 failures are facts about the manifest as it stands. Whether this skill made those references or inherited them is unknown, and the manifest predates several of its entries' current authors.
- **One snapshot.** Counted on 18 Aug 2026, on this machine, against these 70 project directories. A path that resolves today can be deleted tomorrow, which is the whole reason the rule is write-time rather than one-off.
- **My own checker was wrong four times out of thirteen.** It treated a git remote, a branch, a sha and a sibling repository path as project-relative paths. A gate built from it would need those four shapes excluded, and that is a real caveat about the check rather than about the manifest.
- **A defined eval set proves nothing.** Written assertions are a plan for a measurement.
- **The set may contain assertions that cannot fail.** One assertion is labelled a control in the JSON. Which of the rest discriminate is unknown until both arms run, and any a baseline also passes measure the model rather than the skill.

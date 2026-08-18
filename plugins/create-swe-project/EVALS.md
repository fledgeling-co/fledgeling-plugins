# Evals

**Nothing in this file is a measured result about the skill.** The eval suite exists now, in [`evals/evals.json`](evals/evals.json), and it has not been run. No prompt has been executed with the skill loaded, none without it, no judge has looked at anything, and there is no pass rate or cost figure. That is a legitimate state to ship in, and saying so is the point of this section: an unevaluated skill whose EVALS.md merely omits the subject reads to every later reader as though the pipeline ran.

The scripts, on the other hand, are testable without an agent, and they were tested. That is what the next section is.

## What was checked, and what it found

Every result below was produced on 18 Aug 2026 by running the skill's own scripts. Nothing wrote into `~/Dev`: every scaffold went to a temporary destination through `--dest`.

**The SKILL.md parses.** Frontmatter reads as strict YAML, carries exactly `name` and `description`, and the name matches the plugin directory.

**All five scripts are syntactically clean and committed executable.** `bash -n` passes on `scaffold.sh`, `doctor.sh`, `drift.sh`, `upgrade.sh` and `canary.sh`, and all five are mode 755 in the index, so they will run for somebody who installs the plugin rather than only on the machine that wrote them.

**Everything the SKILL.md points at exists.** Twelve internal paths are cited across the file, counting references, scripts and templates. All resolve. Two looked missing on a first pass and are not: `assets/icon-audit-template.html` belongs to `create-mac-icon` and is there, and `scripts/env-pull.sh` is a path inside the *generated* project, shipped here as `templates/base/scripts/env-pull.sh`. The cross-plugin pointers resolve too, including `create-mac-icon`'s `audit_sheet.py` and `squircle-path.txt`, and `design-craft`'s `mobbin-trawl.md`. The two team-files documents the scaffolder copies into every new project, `CODING_PRACTICES.md` and `NEW_PROJECT_BEST_PRACTICES.md`, are both present.

**`doctor.sh` is read-only and returns usable JSON.** It exited 0 and reported node, pnpm, git, cargo, xcodegen, xcodebuild, docker, caddy, op, gh, maestro, fastlane and vercel all present, with versions, plus `machine_caddy_confd: true`. So on this machine the interview can offer every module without a caveat.

**`scaffold.sh` refuses every bad input it should, with distinct exit codes.**

| what was run | exit | what it said |
|---|---|---|
| no arguments | 2 | `--codename is required` |
| `--codename BadName` | 2 | `codename must be lowercase alnum/hyphen, got: BadName` |
| `--codename ok --frobnicate` | 2 | `unknown arg: --frobnicate` |
| `--codename taken` where that directory exists | 1 | `refusing: /tmp/swe-dest/taken already exists` |

**`--plan` and `--dry-run` both write nothing, as documented.** A `--plan` run for `web,tokens,data,auth,macos` exited 0 and emitted JSON with keys `codename`, `modules`, `ports`, `file_count` and `files`: **70 files** planned, ports allocated `web=3100 api=3101 admin=3102`. The destination directory was empty afterwards. `--dry-run` likewise exited 0, printed the human summary, ended on `(dry run, nothing written)` and left the destination empty.

**`upgrade.sh` refuses a non-slipway project cleanly.** Exit 1, `no /tmp/swe-plan/.slipway/manifest.json, not a slipway project`. With no arguments, exit 1 and a usage line.

### Two things failed, and both are small

**`drift.sh` on a non-slipway directory exits 1 with a Python traceback**, not a message. It reads `state.json` without checking for it first, so the user gets a `FileNotFoundError` stack from `pathlib` where `upgrade.sh` in the same situation gives one clear sentence. It fails closed, which is the right direction, but the failure is unreadable. One `[ -f ... ] || { echo ...; exit 1; }` before the Python heredoc closes it.

**`canary.sh` ignores an unrecognised argument and starts scaffolding four full projects anyway.** Its flag handling is a single positional test for `--quick`, so `canary.sh --nonsense` runs the full four-permutation sweep. I interrupted it after 20 seconds. Because cleanup is an `rm -rf "$DEST"` at the end of each loop iteration, the interrupted run left a **1.4 GB** temporary directory behind, which I then removed by hand. That is the real cost of the missing argument check, and it is worth a `trap ... EXIT` as much as a usage line.

**No prior run exists.** No `grading.json`, no `results/` directory, no `benchmark.json`, no committed judge log, no blind-panel key anywhere under `plugins/create-swe-project/`. Checked, not assumed.

## What the eval set would settle

Eight prompts, in `evals/evals.json`. Each runs twice, once with the skill and once with no skill at all, because there is no predecessor to beat and the honest question is whether the skill earns its context.

Two rules for anyone running them: pass `--dest` a temporary directory on every arm, and **do not include `canary.sh` in any eval**. It scaffolds four projects, runs four gates, and leaks gigabytes if a runner times out.

Three prompts are where the answer would come from:

1. **`the-script-makes-the-files`.** The user waives the interview and asks for the files directly. The comfortable answer is to hand-author `package.json`, `turbo.json`, `pnpm-workspace.yaml` and `tsconfig.base.json`, which is exactly the expensive path the templates exist to remove. Grade one property: was any of those four files written by hand rather than rendered by `scaffold.sh`. This is the eval that most cleanly separates the two arms, because a baseline has no scaffolder to reach for.

2. **`a-codename-that-collides-is-not-offered`.** The user proposes `perch`, which is an existing `~/Dev` directory. Without the skill there is no reason to check, so the run gets all the way through an interview and then meets `refusing: ... already exists` at exit 1. Grade whether `ls ~/Dev` happened before the name was proposed.

3. **`an-existing-project-is-out-of-scope`.** The user asks to add an admin console to an existing project. The script refuses the directory, so the dangerous outcome is not a crash but a workaround: rendering the admin templates into the existing tree by hand, past that project's own conventions. Grade whether any template was copied.

Grade with a subagent that never sees the skill, marking each assertion passed or failed with quoted evidence, and no 1-to-10 scores. Every assertion in the set is a property of the run: which script was invoked, what is on disk afterwards, what the interview asked, what the reply declared.

## Caveats, stated rather than buried

- **Nothing above measures the skill.** The script results are facts about `scaffold.sh` and its siblings. None of them says anything about what a model does after reading the SKILL.md, which is what the eval set is for.
- **One machine, one moment.** `doctor.sh` found a fully provisioned toolchain here on 18 Aug 2026. On a machine missing xcodegen or `op`, the interview's whole shape changes, and that path is unexercised.
- **The gate itself was never run.** I ran `--plan` and `--dry-run`, which write nothing. No real scaffold was rendered and no typecheck-plus-build gate was executed, so the templates' current health is unmeasured here. `canary.sh` is the command that would answer it, and running it costs four full installs.
- **A defined eval set proves nothing.** Written assertions are a plan for a measurement.
- **The set may contain assertions that cannot fail.** One is labelled a control in the JSON, on the expectation that a capable model passes it without the skill. Which of the rest discriminate is unknown until both arms run.

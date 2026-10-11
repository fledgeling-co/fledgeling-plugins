# duo-craft evals

Four tasks, each run with the skill and with nothing, then judged two ways: 29 checkable properties graded against the output, and a blind panel of three model families reading each pair in both orders. The skill won both build tasks outright. It lost the crash fix on the first round, and a no-skill run taught it the better fix. Four rounds later that task sits at one loss and two splits. This file is the detail behind the README's summary.

## The four tasks

| Task | What the runner was given | What a good answer does |
|---|---|---|
| **adapt-field-notes** | A small Expo SDK 57 notes app with the usual mistakes: a `Dimensions.get` snapshot, one inset used for both sides, a JavaScript tab bar, hand-drawn header buttons, a portrait lock. "Make it work properly on iPhone Duo." | Per-side insets, a fold signal, the launch crash handled, list and detail side by side with a note selected, native bar items, typechecks, an honest report |
| **new-recipes-app** | A fresh `create-expo-app` (SDK 57). "Build a small recipe browser for iPhone Duo." | The same, from nothing, opening on a real screen |
| **launch-crash** | The notes app and the crash's top frame, `_UIApplicationEvaluateRuntimeIssueForNoSceneLifecycleAdoption`. "Fix it so it stays fixed." | Names the missing scene life cycle, fixes it in a way that survives `expo prebuild`, guards against it coming back |
| **nitro-hinge-question** | "Quick question: should I use react-native-nitro-hinge to detect the fold? Briefly." | Notices its fold path is compiled out by default, offers an alternative, stays short |

Every runner was a subagent of the same session, on one model, with the same limits: no iOS build, no prebuild, no simulator (another job held the machine's simulator), and `npx tsc --noEmit` as the only build check. So none of the 16 runs below saw an app launch; the end-to-end launches in the evidence were done separately, on the Duo simulator, outside the evals.

## Report card: 29 checkable properties

Graded per run against the output files, with the quoted line or command behind each grade (`grading.json` in each run's directory).

| Task | With the skill | Without |
|---|---|---|
| adapt-field-notes | **11 / 11** | 6 / 11 |
| new-recipes-app | **9 / 9** | 5 / 9 |
| launch-crash | 5 / 5 | 5 / 5 |
| nitro-hinge-question | 3 / 4 | 3 / 4 |
| **Total** | **28 / 29** | **19 / 29** |

Where the no-skill runs lost points:

- **adapt-field-notes:** no fold signal of any kind; the scene crash named in the report as "unaddressed"; the JavaScript tab bar and the hand-drawn back and share buttons left in place, so none of them can move into the side bar; titles 8pt from the top edge where the top inset is 0.
- **new-recipes-app:** no scene handling, no fold signal, no split (the list pushes the detail on every display), and `"orientation": "portrait"` left in `app.json`.

The skill's one miss was length: its first answer to the "briefly" question ran to 44 lines.

The two crash-fix runs tie on the checklist and still differed in a way the checklist didn't measure, which is what the panel is for.

## Blind taste test

Each pair went to three families (GPT 5.6 Sol at high effort through Codex, Grok 4.6 at high, Gemini 3.7 Flash High through Antigravity) with neutral labels, the task, the report and the full diff, and the same rubric: would it work on iPhone Duo, did it do what was asked at the scope asked, is anything a placeholder, does the report claim only what was done, is the length right. Every pair was judged twice, once in each order. A judge that picked different sides in the two orders is recorded as a split rather than a vote, because position bias is real and largest exactly when two answers are close.

### Round 1

| Task | GPT | Grok | Gemini |
|---|---|---|---|
| adapt-field-notes | skill | skill | skill |
| new-recipes-app | skill | skill | skill |
| launch-crash | no skill | no skill | split |
| nitro-hinge-question | split | split | skill |

Three of 24 Gemini calls produced no file on the first attempt; the lane tried to run a command and headless mode refused it. Those three were re-run with an instruction to answer from the text only, and the later rounds carried that instruction for every family.

## What the crash fix taught the skill

This is the one task the skill lost, and it lost it to something it should have known.

**Round 1.** The skill shipped its own config plugin that adopted the scene life cycle in three edits. The no-skill run found that Expo already ships exactly that for SDK 57: `expo-build-properties` with `ios.enableSceneSupport`, documented in Expo's `ios-scene-lifecycle` guide and present in `expo-build-properties` 57.0.22. Two judges preferred the official route, and one flagged a real risk in the skill's plugin (an `@objc` name against `$(PRODUCT_MODULE_NAME)`).

The official flag was then measured on the Duo simulator the same day: a fresh SDK 57 starter, the flag on, `prebuild --clean`, Release build with Xcode 27.1. `Info.plist` named `EXExpoAppSceneDelegate`, `AppDelegate` lost its own window, and the app launched with the list and detail split at the fold and its items in the side bar. The skill dropped its plugin and now turns on Expo's flag.

**Round 2.** Both sides now used the same fix, and the no-skill run still won, 3 to 0. The judges were specific: it had added a regression check because the user said "so it stays fixed", while the skill's run had followed the skill's own scope rule ("a crash fix is the fix and why it works") and added none. The skill's report also carried a nine-pose table on a fix that changed no layout, and said "launching will work now", which nothing in the run measured.

**Round 3.** The skill now adds a check when asked to keep a fix fixed, skips the pose table when layout didn't change, and claims only what was observed. Still 3 to 0 against: the baseline's check also read the generated native files, and the skill's report cited the skill's own references and a path on this machine, neither of which the user has.

**Round 4.** Both runs had written their own check script by hand, which is the signal to bundle one. The skill now ships `scripts/check-scene-lifecycle.mjs`, which `install_templates.py` adds and runs before the `ios` script; the report rule says to cite the app and Expo's documentation only. Result: GPT and Grok split, Gemini preferred the baseline. Gemini's reasons were real bugs in the bundled script:

- it parsed expo's version without the minor number, so 57.1.0 would have failed
- it resolved paths from the working directory
- it crashed when `Info.plist` was missing
- it didn't check that the manifest names a delegate class, or that `expo-build-properties` is a dependency

All five were fixed after round 4 and the script re-armed against the measured starter. It passes on the app that launched on the Duo and from another directory, and on expo 57.1.0. It fails, with the reason, on a missing delegate class, a missing `Info.plist`, a missing dependency, expo 57.0.12, an AppDelegate that still builds its own window, and an `app.json` without the flag. Those fixes have not been re-judged.

| Round | GPT | Grok | Gemini |
|---|---|---|---|
| 1 (own plugin) | no skill | no skill | split |
| 2 (Expo's flag) | no skill | no skill | no skill |
| 3 (adds a check, no pose table) | no skill | no skill | no skill |
| 4 (bundled check) | split | split | no skill |

The honest reading: on a narrow, well-documented crash, a strong model with web search finds the right fix without help, and the skill's advantage there is small. What the skill adds is having measured the fix on the device, which none of the runs could do.

## The "briefly" question

| Round | GPT | Grok | Gemini | Length |
|---|---|---|---|---|
| 1 | split | split | skill | 44 lines |
| 2 | no skill | split | split | 39 lines |
| 3 | split | skill | skill | 31 lines |

Round 1 lost on length and on asides nobody asked for (another library, the launch crash). A 25-line rule didn't hold on its own in round 2; the answer came back at 39 lines with the same asides. Round 3 added "answer only the question asked" with the reason, and a rule to call a source read a source read: the earlier answers said nitro-hinge "reports no fold on a real Duo", and no run tested a real device. That answer was preferred by Grok and Gemini in both orders.

The judges who preferred the no-skill answer gave the same reason across rounds: it recommends a module the reader can't see. A judge without the skill installed is a fair stand-in for a reader without it, so the skill's answer now names what the module is and how to install it.

## Defects found by the evals, each now a rule

| Found in | Defect | Now |
|---|---|---|
| launch-crash, round 1 | The skill's own scene plugin, where Expo ships one | Expo's `ios.enableSceneSupport`, measured on the Duo |
| new-recipes-app | The starter's Share button had an empty handler | Wired to `Share.share`; the rule says every bar item does its job |
| new-recipes-app (graded by hand) | `--starter` skipped the fresh app's root layout, so per-side insets never installed | Replaces starter routes and keeps the originals in `.duo-craft-backup/` |
| adapt-field-notes | 20 minutes and 277k tokens against 6 minutes and 136k, mostly on a nine-pose HTML mock nobody reviewed | The mock is made only when someone will review it |
| nitro-hinge-question | 44 lines, asides, "on a real Duo" | 25 lines, the question asked, claims bounded by the evidence |
| launch-crash, rounds 2-4 | No regression guard; pose table on a non-layout fix; prediction in the report; skill paths cited; script bugs | Bundled and armed check script; report rules |
| audit | `sdk-too-old` fired without saying Xcode 27.1 was installed | Names the installed Xcode to point `DEVELOPER_DIR` at |

## Cost

| Task | With the skill | Without |
|---|---|---|
| adapt-field-notes | 1,192 s, 277k tokens | 370 s, 136k tokens |
| new-recipes-app | 224 s, 143k | 246 s, 121k |
| launch-crash (round 1) | 193 s, 135k | 249 s, 129k |
| nitro-hinge-question (round 1) | 36 s, 109k | 96 s, 119k |

The panel ran 24 judgments in round 1 and 6 per task in each later round, 60 in total, all on CLI subscriptions with no metered spend. The research panel behind the skill (xAI, Perplexity and Gemini, exported to `docs/deep-research/`) was the only metered cost, reserved at about $6.20 worst case.

## What was not tested

- **No eval run launched an app.** The device evidence (the starter split at the fold on SDK 57 with Expo's flag, the original app's poses) comes from separate builds on the Xcode 27.1 Duo simulator, recorded in `skills/duo-craft/references/evidence.md`.
- **Tabletop, the book pose with an active fold, both Split View halves and picture in picture** are built and unit-tested and have not been seen running.
- **The round-4 script fixes** are armed and self-tested, not re-judged.
- **Every runner was the same model.** The judges came from three families; the work did not.

## Reproducing it

Run directories, grades, judge prompts and verdicts sit in the workspace the runs used; the eval prompts and their fixtures are in `skills/duo-craft/evals/` (`evals.json`, `fixtures/field-notes`, `fixtures/fresh-sdk57`). The fixtures need `npm install` before `tsc`, since `node_modules` isn't committed.

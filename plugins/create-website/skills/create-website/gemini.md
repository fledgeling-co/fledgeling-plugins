# Gemini calibration for create-website

Read this with `SKILL.md`. The person's chosen model lane governs the task; nothing here reroutes
work away from Gemini. No Gemini run of this skill has been recorded, so these are the places
the skill depends on a step actually happening, written as counts you can check.

## The steps that get reported without running

The family benchmark behind `geminify:geminify` found the dominant failure is a prescribed skill
or tool that is never invoked while the run reports having followed it. In this skill those
steps are:

| Step | The artifact that proves it ran |
|---|---|
| 1 `trawl:trawl` invocation | `plan.trawl.pick` and `.create-website/trawl-packet.md`, or `plan.trawl.skipped` with a reason |
| Mobbin searches, one per section type | Each section's `mobbin.query`, `opened` (a count of images you read) and `took` |
| `design-craft:design-craft` and `ux-craft:ux-craft` loaded | The direction contract and state grid they produce, in the site source comments or the plan |
| Each billed generation | A `spend.py add` entry per call, and the running total said in chat |
| `scroll_capture.mjs` | `.create-website/captures/report.json` and its PNGs, with four passes in `runs` |
| `design-review:design-review` | Its result line, quoted |

Before writing the report, open each artifact in that table and count it. A missing artifact is
a step that did not run: run it, or say in the report that it did not run.

## Numbers to fill in, not adjectives

Write the plan with numbers: sections listed (N), signature moments (at most 2), searches run
(N), images opened (N), billed calls (N) and spend ($). The report repeats those numbers.

## Quote the result lines

Each script ends with a `RESULT:` line. Paste it into the report verbatim with its exit code,
rather than describing it. A script you did not run gets "not run" and the reason.

# Gemini implementation calibration for launch-craft

Read this with `SKILL.md`. The accepted product brief and the user's selected model lane govern the task. Earlier measurements on Gemini 3.7 Flash do not establish Gemini 3.8 limits or justify rerouting its implementation work automatically.

## Evidence scope

The previous adapter used the 106-task family benchmark recorded in `geminify:geminify`'s `references/evidence.md`. It reported these historical results:

| Historical task bucket | Gemini score | Opus score | Gemini hard-zero rate |
| --- | --- | --- | --- |
| `static-page` | 22 | 67 | 71% |
| `brownfield-integration` | 16.1 | 46.4 | 79% |

These were other tasks in another harness, not a measured Gemini 3.8 run of this skill. No run of this revised launch workflow has been recorded. Treat the numbers as a reason to make scope and evidence explicit, not a permanent capability boundary. The previous scan also found two model-independent defects: a synthesis helper that did not synthesize and a substring checker described as a rendered accessibility gate. The current skill and helper output now state those limits explicitly.

## Build from the accepted plan

An Opus planning stage or GPT-6 orchestrator hands the implementer the complete source inventory, current OVERVIEW and PRD, approved claims, design direction, output directory and acceptance criteria. Read those inputs before editing. A file named in a brief is not available merely because the caller saw it; report a missing input and proceed only with unaffected work.

Derive counts from this project's brief: feature rows, sections, controls, responsive states, supported platforms and approved pricing terms. Do not copy the old networking fixture's five-platform or two-price examples into a different product.

Record a compact implementation matrix:

| Requirement | Artifact or control | Acceptance evidence | Result |
| --- | --- | --- | --- |
| Each in-scope feature | PRD row and source path | Coverage against original inventory | Covered / excluded with reason |
| Public claim | Approved copy and source | Status matches actual evidence | Supported / unresolved |
| Interaction | Named control and outcome | Executed pointer and keyboard path | Passed / failed / unverified |
| Responsive state | Target viewport and page | Opened render and relevant probe | Passed / failed / unverified |

## Keep tool outcomes distinct

- `run_synthesis.py` is an inventory helper. Its successful exit proves neither document generation nor complete discovery.
- `validate_site.py` reads source text. Its successful exit proves only the listed text checks; browser evidence is required for rendered claims.
- Loading `design-craft:design-craft` or `ux-craft:ux-craft` is preparation. The implemented direction, state matrix and rendered behavior show whether their instructions were applied.
- Discover the actual tool and model catalog before dispatch. A missing command or unsupported parameter gets one diagnosis and a supported alternative; do not retry an identical invalid call.

Run the named acceptance checks once the artifact is ready. Repair a failed criterion and recheck the affected scope. Return files, preview instructions, observed results and unresolved limits to the orchestrator; do not label an unrun browser check as passed.

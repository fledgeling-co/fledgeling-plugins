# Passes

A scene goes through four passes after drafting, in this order. The first is a script; the next two run in one critic subagent with a fresh context; the last is the orchestrating session applying the fixes and closing the ledger. The research's finding behind the whole sequence (evidence.md E8): the model that wrote the paragraph is the worst-placed reader of its seams, so the reading happens somewhere the draft's reasoning is not.

## Pass 1. Transition audit (script)

```
python3 scripts/transition_audit.py story/scenes/<id>.md \
    --beat <id> --beats story/beats.json --bible story/bible.md --json story/critique/<id>.audit.json
```

Exit 1 on: an orphan paragraph, a word count outside the beat's band, first-person narration in a third-person scene, an em dash, one of five hard tells. Warnings on: a weak anchor (referent only later in the paragraph), soft tells, a proper noun not in the cast, sentence-length variation under 0.35, three paragraphs opening on the same word.

Fix hard failures by returning the specific paragraph to the drafter subagent with the audit line quoted and the two paragraphs either side, at most twice. A third failure on the same seam means the beat is wrong, not the prose: re-read the beat card's `change` and `function` before drafting again.

Warnings are read, not obeyed. A cast warning on a place name is noise; a cast warning on a person is a continuity error.

## Pass 2 and 3. The critic (one subagent, fresh context)

Spawn one subagent with no access to the drafting conversation. Give it three files by path: the scene, the pack, and the drafter's exit state. Its brief is below. It returns one report, written to `story/critique/<id>.md`, in this shape and at most 40 lines:

```
# Critique: <id>

## Continuity
| # | Quote from the scene | Contradicts | Fix |
| 1 | "she set the lantern down" | entry_state: Bisk.holding = [] and items.beacon only | cut, or add the lantern to the entry state upstream |

## Promises and tension
- setups planted this scene: <list, or none>
- payoffs due this scene (from beat.hooks.payoffs) and whether they landed: <list>
- threads the beat keeps open that the prose closed: <list, or none>
- exit tension as read: higher | same | lower (beat asked: <x>)

## Voice
| rule | held | slip (quote) |
| 1 third person close | yes | |
| 2 literal sentences | no | "the dark drank the sound" |

## Exit state corrections
<a JSON patch of fields to change in state/<id>.json, or "none">
```

The critic brief, with the files' paths substituted:

```
<scene>path</scene> <pack>path</pack> <exit_state>path</exit_state>

Read the three files. The pack holds the bible sections, the entry state and the beat card the scene was written from; the scene is the prose; the exit state is what the drafter says is true at the end.

Report, in the format below, four things: sentences in the scene that contradict the entry state or the bible (quote each); the beat's setups and payoffs and whether the prose planted or paid them; any thread the beat lists as unresolved that the prose resolved, and the tension at the end as you read it; and each voice rule in the bible, whether the scene held it, with a quoted slip where it did not.

Then list corrections to the exit state as a JSON patch: fields the prose makes true that the state got wrong, and fields the state claims that the prose does not support.

Quote rather than paraphrase, because a finding without its sentence cannot be fixed. Report what you find at whatever count it is; the orchestrator decides what to act on. The whole report is at most 40 lines.

<format> ...the shape above... </format>
```

The critic gets no instruction to reason step by step and no instruction to verify. It is told what to read, what to report, and the shape.

## Pass 4. Apply and close (orchestrating session)

1. Apply continuity fixes by sending the quoted sentences and the fix column back to the drafter subagent, with the paragraphs either side. Do not rewrite the prose in the orchestrating session; its context holds the whole story and the sliding window would be lost.
2. Apply the exit-state patch to `state/<id>.json`.
3. Run `story_state.py check-exit`. A premature-resolution failure goes back to the drafter with the thread named.
4. Run `transition_audit.py` again; exit 0 is the gate.
5. Update `story/ledger.json` (a list of `{id, status, words, audit_exit, critique_rows}`) so a later session can find where the story stands without reading it.

Two subagent spawns per scene, drafter and critic, plus up to two drafter re-entries for fixes. If a scene needs more than that, stop and report the seam that will not close rather than spending a fifth run on it.

## Chapter close

After every scene in a chapter (or every six scenes, whichever is sooner) run one more critic subagent across the chapter's exit states only, not the prose, with the promises table as its subject: every `setup` with `paid: false` older than three scenes is listed, and every payoff in the beat sheet whose setup never appeared. Write it to `story/critique/chapter-<n>.md`. This is the Promises Auditor from the research at the granularity where it pays.

## When the critic should be a different model family

Route the critic through `clarify:clarify`'s out-of-family lanes instead of a Claude subagent when a scene has failed Pass 1 or Pass 4 three times, or when the user asks for a second opinion on the prose. A same-family critic shares the drafter's priors, and the positivity bias the research measured is one of them.

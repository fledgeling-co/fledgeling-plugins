---
name: create-story
description: >-
  Write long-form fiction whose paragraphs connect: stories, chapters, scenes, novellas,
  game narrative prose, audiobook scripts, serialised episodes. Use this whenever someone
  asks to write, draft, continue, expand or rewrite story prose from an outline, a beat
  sheet, a synopsis, a story bible or a previous chapter, and whenever they say the prose
  "loses the thread", "jumps around", "doesn't follow on", "reads like separate paragraphs",
  or "keeps the plot but not the flow". Use it even when the request only says "write the
  next scene" or "turn this outline into a chapter", because the drift it prevents shows up
  on the second paragraph of any scene written without it. Holds a story bible and a
  per-scene state ledger, drafts one scene at a time from a scripted context pack, gates the
  draft with a deterministic transition audit, and critiques it in a separate context. NOT
  for outlines or synopses alone (write those as documents), not for non-fiction reports
  (use agent-voice:agent-voice), and not for content in a named person's voice where no
  story is involved (use that person's content skill).
---

# create-story: prose that follows on

A model writing a long story keeps the plot and loses the seams. The outline is honoured,
the characters are the right ones, and the second paragraph of a scene reads as if it were
written by someone who had skimmed the first. Readers feel it as the story losing its
train of thought. The research behind this skill (three deep-research reports, September
2026, in `docs/deep-research/`) traces it to four causes: the whole manuscript in context
dilutes the link to the paragraph just written; the model's prior treats a paragraph as a
self-contained idea; its prior on relationships resolves tension early; and reasoning run
inside the drafting call flattens the prose. Each of the four has a mechanical counter here, and
each of the four counters traces to an entry (E1 to E12) in `references/evidence.md`.

The counters are four files and four scripts rather than a longer prompt. A story bible
and a beat sheet fix what each scene is for. A per-scene exit state, in JSON, carries who
is where, holding what, feeling what, and what is still open, so the next scene is
conditioned on the last one rather than on an impression of the book. A context-pack
script assembles the drafter's whole input, including only the last two paragraphs of the
scene before, so the window cannot widen by hand. A transition-audit script fails a scene
with an orphan paragraph. And critique runs in a fresh context, never in the drafter's.

## Whose voice

The skill owns structure and continuity. The voice comes from one of two places:

- **The author is a named person.** Invoke that person's content skill first
  (`create-luke-content:create-luke-content` for Luke, routed to its book persona), derive
  the bible's `## Voice` section from its rules, and run its lint on every drafted scene at
  the format that persona names. The voice skill governs how the prose reads; this skill
  governs what connects to what.
- **No author is named.** The bible's `## Voice` section is the voice: five checkable rules
  and a sample of at most 300 words, written during planning and approved with the beat
  sheet. `transition_audit.py` is the only lint.

## Procedure

### 1. Find the story

Look for `story/` under the working directory (or the root the user names). Read
`bible.md`, `beats.json` and `ledger.json` if they exist. The ledger says which scenes are
drafted, audited and closed, so a session that starts here knows where the story stands
without reading the prose. When a project carries a brief that excludes earlier material
(a rejected draft, a previous story), copy its exclusions into the bible's `## Excluded`
section before anything else, because the drafter reads only the pack and the pack reads
only the bible.

### 2. Plan before prose

When there is no bible or no beat sheet, write them and stop. Prose waits until the user
has said the beat sheet stands (evidence entry E12). Planning is the one place reasoning
belongs, so do it in this session with thinking on.

The bible follows `references/state-schema.md`: `## Voice`, `## World`, `## Excluded`, one
`## <Name>` section per character under 200 words, and any other section a beat will name.
The beat sheet is one card per scene with `id`, `pov`, `location`, `present`, `goal`,
`change` (one thing), `function`, `exit` (`unresolved` threads, `tension`, `last_image`)
and a `words` band with `max` at or under 1600. A scene that changes two things is two
cards. Then:

```
python3 scripts/story_state.py validate-beats story/beats.json    # exit 0 required
```

Present the bible and beat sheet as proposals in the reply (under 12 lines, with the file
paths), and end the turn.

### 3. Draft one scene

For the next undrafted card in reading order, or the one the user names:

```
python3 scripts/context_pack.py --root story --beat <id>          # writes story/packs/<id>.md
```

Spawn **one drafter subagent** whose entire input is the pack file's path and this brief:

```
Read <pack path> and do what its <task> section asks. Write the prose to
<story/scenes/id.md> and the exit state JSON to <story/state/id.json>. Read
nothing else in the repository; the pack is deliberately the whole context, because
prose drafted from the full manuscript loses the link between consecutive paragraphs.
Do not delegate; spawn no subagents.
```

Give the drafter no instruction to plan, reason, outline or explain (evidence entry E7). The
pack's task already carries the word band, the person and tense, the open threads, the
last image, and the paragraph rule. Use the `opus` model for the drafter.

### 4. Gate, critique, close

```
python3 scripts/transition_audit.py story/scenes/<id>.md --beat <id> \
    --beats story/beats.json --bible story/bible.md --json story/critique/<id>.audit.json
```

Exit 1 returns the named paragraph to the same drafter subagent with the audit line and the
paragraphs either side, at most twice. Then spawn **one critic subagent**, fresh, with the
brief in `references/passes.md` and three paths: the scene, the pack, the exit state. It
writes `story/critique/<id>.md` in the fixed 40-line format. Apply its continuity fixes
through the drafter, apply its exit-state patch, then:

```
python3 scripts/story_state.py check-exit --beats story/beats.json --beat <id> --state story/state/<id>.json
python3 scripts/transition_audit.py story/scenes/<id>.md --beat <id> --beats story/beats.json --bible story/bible.md
```

Both exit 0 closes the scene. Append `{id, status: "closed", words, audit_exit, critique_rows}`
to `story/ledger.json`. Repeat from step 3 for the next card.

Two subagents per scene (drafter, critic) and at most two drafter re-entries. A scene
still failing after that is a beat-sheet problem: report the seam and stop rather than
spending a fifth run.

### 5. Chapter close

After each chapter, or every six scenes, one critic subagent reads the chapter's exit
states only and writes the promises table to `story/critique/chapter-<n>.md`
(`references/passes.md`, "Chapter close"). Setups unpaid for three scenes and payoffs
whose setup never appeared are the two rows it fills.

### 6. Narrated version, when asked

"Make an audiobook version", "a read-aloud", "an ElevenLabs prompt", "something I can
listen to" all mean one file at `story/narration/<name>.md` in the shape
`references/narration.md` gives: synopsis, setup notes, then the speech in paste-ready
parts with audio tags. A condensed telling is drafted from the ledger and the exit states
along one named route, naming the forks as it passes them; a single scene is drafted from
its scene file. One drafter subagent, one critic subagent, the same caps as a scene. Gate it
with:

```
python3 scripts/narration_check.py story/narration/<name>.md
```

Exit 0 and a critic report close it. The duration goes in the reply as the checker's range,
never as one number.

### 7. Reply

The reply is at most six lines: which scenes closed, word counts, any seam that would not
close, and the path of the ledger. The prose is on disk; do not paste it into the reply.

## Delegation and scope

Delegate exactly the two roles above, and never the planning, the script runs or the
ledger, which are this session's. The drafter is a subagent because this session's
context holds the whole story and would defeat the window; the critic is a subagent
because the drafter's own context is the worst-placed reader of its seams. Route the critic
out of family through `clarify:clarify`'s lanes when a scene has failed three times or the
user asks for a second opinion.

Deliver what was asked, at the scope intended. "Write chapter two" drafts chapter two's
cards and stops; it does not revise chapter one or extend the beat sheet. When a card seems
wrong while drafting, say so in one sentence in the reply and draft it as written.

## Constraints

- The drafter reads the pack and nothing else. Widening its input by hand is the failure
  mode this skill exists to prevent, so if a scene needs more context, the fix is a bible
  section named in the card's `bible_sections`, not a larger tail.
- Prose is never rewritten in this session's context; edits go back through the drafter
  with the quoted sentences.
- Scripts decide. A scene closes on two exit-0 results, not on a reading.
- `## Excluded` is honoured by omission: the drafter is not told what the excluded material
  was, only that it exists, and the critic checks the prose for it.
- Subagents run no git operations. This session owns commits, when the user asks for them.
- No spend: no research panels, no image or audio generation. A narrated version is a
  prompt for the user's voice model, written and checked here; rendering it is theirs.

## What the scripts cannot see

The transition audit is a tripwire with named heuristics (pronoun, connective, shared name,
shared word, spoken line), not a measure of coherence; the research records that no such
measure exists. A scene can pass the gate and still drift in a way only the critic or the
reader catches. State that in the reply when a scene closes with warnings, so the user
knows which check has an opinion and which has a number.

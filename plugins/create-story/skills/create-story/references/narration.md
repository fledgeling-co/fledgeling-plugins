# Narration

A narrated version of a story is a second deliverable from the same story directory: a read-aloud script with vocal direction, written to be pasted into a text-to-speech model. The user's model is ElevenLabs Eleven v3, and the rules below come from its prompting guide as fetched on 5 September 2026 (`docs/elevenlabs/best-practices-2026-09-05.md`, section "Prompting Eleven v3"). Re-fetch the page before a narration run when the copy is more than a month old; the guide says the model is in research preview and the tag set moves.

## Two kinds of narration

**A condensed telling.** The whole story, or one route through a branching one, read in about five minutes. Drafted from the ledger and the exit states, not from the prose: the states carry who is where and what is still open at each scene's close, which is exactly the spine a five-minute telling needs, and the prose carries detail there is no time for. When the story branches, the telling follows one named default route and names the forks as it passes them, so the listener hears that other pages exist without losing the line.

**A scene read aloud.** One closed scene, tagged for performance. Drafted from the scene file and its exit state.

Both are drafted by the same drafter subagent as prose, from a pack. Build it with `context_pack.py` for a scene, or by hand for a telling: the `## Voice` section, the ledger, every closed scene's exit state, the route to follow, and the task below. The drafter gets no instruction to reason, for the same reason a scene's drafter gets none.

## The file

One markdown file at `story/narration/<name>.md`, in this shape, because `scripts/narration_check.py` reads it:

```
# <title>: read-aloud

## Synopsis
<four to eight sentences, unperformed, for a listener who wants the shape first>

## Setup notes (keep these out of the speech box)
<model, stability register, the tag vocabulary used, the input limit assumed,
 the performance target with its basis, the default route through the forks>

## The speech

### Part 1
<paste-ready text with audio tags>

### Part 2
...
```

The heading "The speech" is the boundary. Everything above it is for the person doing the pasting; everything below it goes into the model verbatim, one part per generation. Setup vocabulary in the spoken text (a voice ID, a stability setting, the word "paste") is a failure, because the model would read it out.

## Rules from the guide

- **Audio tags are the direction.** Square-bracket tags before the line they shape: `[thoughtful]`, `[whispers]`, `[sighs]`, `[short pause]`, `[long pause]`, `[dramatically]`, `[reassuring]`, `[curious]`, `[excited]`, `[sad]`, `[surprised]`, `[exhales]`. The checker's known set is the guide's own list plus every tag its sample scripts use; a tag outside it is a guess about the model and fails unless passed as `--allow-tag`.
- **Match the tag to the voice.** The guide's first rule: a tag cannot push a voice far from its nature, and a whispering voice will not shout. Write for a calm storyteller and keep the direction inside that range.
- **No SSML (Speech Synthesis Markup Language) break tags.** v3 does not support `<break>`. Pauses come from `[short pause]`, `[long pause]`, and ellipses. Capitals add emphasis. Standard punctuation carries the rhythm.
- **Stability Creative or Natural.** The guide's third setting (`Robust`) ignores most direction. Say so in the setup notes; do not choose the voice, its ID, the speed or a pronunciation scheme, which are the user's.
- **Sound-effect tags are the least consistent** (`[gunshot]`, `[applause]`); the checker warns on them and `--voice-only` makes them a failure. The Enhance prompt inside the guide bars non-auditory tags (`[grinning]`, `[pacing]`) outright.
- **Emotion through context as well as tags.** Narrative phrasing ("her voice slowing") shapes delivery too, and it is what a listener hears when a tag misfires.
- **Numbers and abbreviations spelled as spoken.** The model reads what is written. "Level 4" is "level four"; "Dr." is "Doctor"; a URL is never read.
- **Parts under the paste limit.** The guide states no per-generation limit, so parts stay under 2,000 characters by default and the setup notes say the limit was assumed, not read.
- **Duration is a range, never a number.** Word count over two reading speeds, printed as "about five to seven minutes before pauses"; the real length exists once it is rendered. The user's brief for the Kiln story said this in so many words.

## The check

```
python3 scripts/narration_check.py story/narration/<name>.md [--max-chars 2000] [--voice-only] [--allow-tag TAG]
```

Exit 1 on an unknown tag, an SSML break, an em dash, a part over the limit, setup vocabulary in the speech, or no parts. Warnings on sound-effect tags, more than six tags per hundred words, three sentences in a row opening on a tag, and the duration range. Then the critic pass as for a scene, with two extra rows in its report: forks named against forks in the beat sheet, and the default route followed against the route in the setup notes.

A worked example in the shape above, from the game project this skill was built for: `~/Dev/game/chatgpt-docs/outputs/NARRATIVE-RESTART-READALOUD.md` (five parts, 1,004 spoken words, passes the check with three warnings about consecutive tag-led sentences).

## What is not here

Audio generation. The skill writes the prompt; rendering it spends the user's credits and is theirs to do. No voice, voice ID, stability value, speed or pronunciation dictionary is chosen in the file.

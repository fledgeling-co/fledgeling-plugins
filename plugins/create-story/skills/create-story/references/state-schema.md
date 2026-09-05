# State schema

Two JSON shapes carry the story between passes. `scripts/story_state.py` enforces both.

## The story directory

```
story/
  bible.md          the one prose document about the story (voice, world, cast)
  beats.json        every scene as a beat card, in reading order
  scenes/<id>.md    drafted prose, one file per scene
  state/<id>.json   the exit state of that scene (the Chain of States)
  packs/<id>.md     the context pack the drafter of that scene received
  critique/<id>.md  the critic's report on that scene
```

The root defaults to `story/` under the project; pass `--root` to every script when it lives elsewhere.

## The bible

Markdown with `##` sections. Section headings are how `context_pack.py` selects what a scene's drafter sees:

| Heading | Goes into the pack |
|---|---|
| `## Voice` | always. Composed by `scripts/voice_card.py compose` from a base card and up to three influence cards in `references/influences.md`: a `bands:` line, at most five rules with their card named, borrow and leave lists, and a sample of at most 300 words. |
| `## World` | always. The rules of the setting that any scene can touch. |
| `## Excluded` | always. Material from rejected drafts or other stories that the drafter is not to reuse. |
| `## <Character name>` | when that name is in the beat's `present` or `also_present`. |
| any other heading | when the beat lists it in `bible_sections`. |

Keep character sections under 200 words each. What a character wants across the story is the line that matters most; the drafter uses it to keep the character in motion between beats.

## The beat card

One object per scene in `beats.json` under `"scenes"`, in reading order.

```json
{
  "id": "L1-hold-01",
  "title": "The beacon",
  "pov": "Bisk",
  "person": "third",
  "tense": "past",
  "location": "evac platform, tunnel mouth",
  "time": "night, ten minutes before the last train",
  "present": ["Bisk"],
  "also_present": ["Station voice"],
  "goal": "Bisk means to hold the platform so the evacuation completes",
  "change": "the last train leaves without her",
  "function": "dread settling into resolve",
  "exit": {
    "unresolved": ["the infected have not reached the platform"],
    "tension": "higher",
    "last_image": "the first click from the dark"
  },
  "words": {"min": 400, "max": 900},
  "hooks": {"setups": ["the station voice has said 'you don't have to stay' before"], "payoffs": []},
  "follows": "L0-prologue-03",
  "bible_sections": ["The Kiln"],
  "entry_state": null
}
```

Required: `id`, `pov`, `location`, `present`, `goal`, `change`, `function`, `exit` (with `unresolved`, `tension`, `last_image`), `words` (`min` < `max` <= 1600). `pov` must appear in `present`.

Optional: `person` (`first` or `third`, default third), `tense`, `time`, `also_present` (entities with no state of their own: a voice, a crowd, a weather), `hooks`, `follows` (the scene whose exit state this one enters from, when it is not the previous card; branching stories use this), `bible_sections`, `entry_state` (an inline state for a scene that opens a new thread with no predecessor).

`change` is the single thing that is different at the end. A beat with two changes is two beats. `function` is what the scene does to the reader, in two to six words. `exit.tension` is one of `higher`, `same`, `lower` relative to the scene's start.

## The exit state (Chain of States)

One file per drafted scene at `state/<id>.json`, produced by the drafter and corrected by the critic.

```json
{
  "scene": "L1-hold-01",
  "time": "night, just after the last train",
  "location": "evac platform, back against the beacon post",
  "characters": {
    "Bisk": {
      "position": "back against the beacon post, facing the tunnel mouth",
      "holding": [],
      "wants": "to hold the platform until dawn",
      "feels": "steady on the surface, cold underneath",
      "knows": ["the train has gone", "the infected click, then go silent to listen"]
    }
  },
  "items": {
    "beacon": {"where": "platform, behind Bisk", "status": "lit, fuel unknown"}
  },
  "open_threads": ["the infected have not reached the platform", "who set the beacon burning"],
  "promises": [{"setup": "the station voice has said 'you don't have to stay' before", "paid": false}],
  "last_paragraph": "The train went. She heard it before she felt it ..."
}
```

Required: `scene`, `time`, `location`, `characters` (each with `position`, `holding`, `wants`, `feels`), `items` (each with `where`, `status`), `open_threads` (at least one), `last_paragraph` (verbatim, five words or more). `knows` and `promises` are optional and worth keeping.

`feels` is the emotional state the next scene opens in. The positivity bias the research measured shows up here first: a character who was frightened at the end of one scene and calm at the start of the next, with nothing between, is the drift. `check-exit` compares `open_threads` to the beat's `unresolved` list and fails on a thread that was quietly closed.

## Commands

```
python3 scripts/story_state.py validate-beats story/beats.json
python3 scripts/story_state.py validate story/state/L1-hold-01.json
python3 scripts/story_state.py check-exit --beats story/beats.json --beat L1-hold-01 --state story/state/L1-hold-01.json
python3 scripts/story_state.py diff story/state/L1-hold-01.json story/state/L1-hold-02.json
python3 scripts/story_state.py previous --beats story/beats.json --beat L1-hold-02 --state-dir story/state
```

All exit 0 on success and 1 on any failure, naming the field.

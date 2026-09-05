# EVALS

**No comparative eval run happened.** The skill ships with eight eval prompts in `evals/evals.json` and none of them have been run, with the skill or without it. The claim that a scene drafted this way holds its thread better than a scene drafted from a flat prompt is the whole point of the skill, and it's untested.

The session that built it had one instruction and no user in the room, so two of the pipeline's checkpoints were answered by other models instead of by a person. That's recorded below, because a skipped gate with no trace reads later as a gate that passed.

## What was verified mechanically

Three self-test suites, each asserting both directions, because a gate that can't fail isn't a gate.

```
$ python3 scripts/transition_audit.py --self-test
  pass  a coherent scene passes
  pass  an orphan paragraph fails
  pass  a hard tell fails
  pass  a scene break excuses the orphan
  pass  a scene under the word band fails
  pass  first-person narration in a third-person scene fails
  pass  the same text passes when the scene is first person
  pass  an em dash fails under --em-dash forbid
  pass  an em dash only warns under --em-dash warn
  pass  a proper noun outside the cast warns

all self-tests passed
exit 0

$ python3 scripts/story_state.py --self-test
  pass  a well-formed state validates
  pass  a character without holding fails
  pass  empty open_threads fails
  pass  a well-formed beat sheet validates
  pass  a 5000-word beat fails the ceiling
  pass  an unknown tension word fails
  pass  a matching exit passes check-exit
  pass  resolving a thread the beat kept open fails
  pass  ending away from the beat's last image fails
  pass  diff reports a move and an opened thread

all self-tests passed
exit 0
```

```
$ python3 scripts/narration_check.py --self-test
  pass  a well-formed narration passes
  pass  an unknown tag fails
  pass  an em dash fails
  pass  an SSML break fails
  pass  setup vocabulary in the speech fails
  pass  a part over the character limit fails
  pass  a sound-effect tag warns by default
  pass  a sound-effect tag fails under --voice-only
  pass  an allowed tag passes
  pass  a file with no parts fails

all self-tests passed
exit 0
```

The narration checker was also run on the game project's existing five-part read-aloud script, which it passed with three warnings (consecutive tag-led sentences) and a duration range of 5.7 to 7.2 minutes for 1,004 spoken words.

The audit demonstrated failing on a deliberately bad three-paragraph scene (a station platform, then a fish market, then a beacon described as *a testament to endurance*):

```
/tmp/bad-scene.md: 83 words, 3 paragraphs, 5 fail(s), 0 warning(s)
  FAIL  word-band              83 words, band 400-900
  FAIL  orphan-paragraph       paragraph 2 shares nothing with paragraph 1: "The market in the old town sold fish on Thursdays."
  FAIL  orphan-paragraph       paragraph 3 shares nothing with paragraph 2: "A testament to endurance, the beacon burned on."
  FAIL  tell                   "A testament to" at offset 348
  FAIL  tell                   "tapestry" at offset 400
exit 1
```

End to end against the bundled example in `skills/create-story/assets/example/`: the beat sheet validates, the 180-word fixture scene passes the audit with six paragraphs anchored (pronoun, shared word, spoken line), its exit state passes `check-exit` against its beat card, and `context_pack.py` builds a 909-word pack for the following scene that selects the Voice, World and Excluded sections plus the one character present and leaves the rest of the bible out.

**One guard caught a defect in the skill's own fixture.** The example scene was written at 180 words under a beat card whose band said 400 to 900, and the audit failed it on word count the first time the two were run together. The card was wrong, not the prose, and it was corrected.

Three heuristics were wrong on the first cut and fixed against the fixture: dialogue paragraphs were flagged as orphans (a spoken line is now an anchor), the relative pronoun *that* was letting orphans through (personal and deictic pronouns are now separate sets with separate reach), and a non-character voice in a beat's `present` list failed the state check (a separate `also_present` field now carries entities with no state).

## Checkpoints that weren't asked

The pipeline puts two things to the user: the discovery interview, and the name and icon concepts. Neither was asked.

**Discovery** was answered from the material: the user's brief in `~/Dev/dossier/prose-drift/BRAINDUMP.md`, the three research reports, and the game project's narrative handover that names this skill's first consumer and requires its prose to go through `create-luke-content:create-luke-content`.

**Name and icon** went to the referral lanes with the candidates in swapped order. Four names (tenon, throughline, ligature, loom) and three icon concepts (a loom shuttle, a row of state tokens, one thread through separated bars).

- Grok returned `402 Payment Required`, balance exhausted. Lane down.
- Codex (`gpt-5.6-sol`, reasoning effort high, header confirmed) chose **tenon** with **throughline** as runner-up, and the thread-through-bars icon.
- The Claude lane (`claude-fable-5`, effort high) produced no output in fifteen minutes and was killed.

The session went with throughline against the one lane that answered, on the grounds that it named the thing the user said was missing, where tenon is a joinery metaphor that needs a sentence. The icon took Codex's pick. The user then overturned the name on reading the report: the skill is **create-story**, which puts it beside the other create- skills in the marketplace and says what it does rather than what it fixes. The icon stands.

**The icon** went to `create-mac-icon:create-mac-icon` with one deviation. Its pipeline wants three engines, two of them image-generation calls that are metered, and no user was present to approve the spend, so it ran with three hand-authored takes from one build script instead: the meander that ships, a straight stitch, and a woven cord. The audit sheet at `assets/audit.html` scores all three and passes its mechanical check; the woven take is the useful loser, because at 16px its hidden passes read as a dashed line, which is the broken thread the skill exists to prevent. No raster reference means the material was authored from the family's sibling scripts rather than measured against one.

## What would settle it

1. **Skill against no skill on evals 2 and 4.** Same beat sheet, same bible, two runs each. Count orphan seams in the no-skill output with the audit, and count threads the no-skill output closed that the beat kept open. If the no-skill run passes both, the skill isn't earning its context.
2. **A blind read.** Two scenes from eval 2, one from each run, anonymised, to three model families and one person, asked which one loses its thread. Judges never see the skill.
3. **The trigger.** Evals 6 and 7 are near-misses (a synopsis, a load-test report). Twenty prompts in that shape, half of which should trigger, would measure whether the description is pushy in the right direction.

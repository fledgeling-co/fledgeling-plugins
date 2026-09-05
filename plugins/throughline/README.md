# throughline

Ask Claude for a chapter and you get the plot you asked for, told by someone who keeps forgetting what they wrote a paragraph ago. The characters are right. The outline is honoured. And the second paragraph of every scene reads as though it was written after a night's sleep, with the first one a vague memory. Readers feel it as the story losing its train of thought, and it's the reason a model's long fiction is easy to skim and hard to finish.

This skill is a way of writing stories where each paragraph has to take something from the one before it, and where a script checks that it did.

## Why it happens

Three deep-research reports were bought on this question (the reports are in `docs/deep-research/`, all read in full, with 21 claims traced in `skills/throughline/references/evidence.md`). They agree on four causes, and each one gets a mechanical counter rather than a paragraph of instructions.

**The whole manuscript is in the room.** When a model can see everything it has written, the early chapters pull on every sentence it writes, and the link to the paragraph it just finished gets diluted. It's the same reason a person can't proofread a book by re-reading the whole thing every time they add a line. Counter: the drafter never sees the manuscript. A script builds its entire input from the story bible, the state at the end of the last scene, the beat card for this one, and the last two paragraphs written. That's the window, and because a script builds it, nobody widens it by hand.

**A paragraph is a self-contained idea.** Models learned from the web, where paragraphs usually are. So each new paragraph gets treated as a fresh start that fits the theme without following from the last one. Counter: the drafting brief says the rule in one sentence, and the transition audit reads every seam and fails a scene where a paragraph shares nothing with the one before it.

**Everyone makes up too early.** A study of 1,200 model-written stories found a consistent pull toward reconciliation. A beat that asks for an argument to stay unresolved gets a paragraph where the characters hug. Counter: every scene ends with a written exit state (who's where, holding what, feeling what, and what's still open), and a check fails the scene if a thread the beat kept open has quietly closed.

**Thinking in the middle of writing flattens the prose.** Reasoning holds the plot together and makes the sentences stiff. Counter: planning happens in one place with thinking on, and drafting happens somewhere else with no instruction to plan, explain or reason at all.

## What you do

Say what you want written. *Write the next scene. Turn this outline into chapter two. This chapter keeps the plot but reads like every paragraph was written separately; fix the flow.*

The first time, you get a story bible and a beat sheet back and nothing else, because prose written from an unapproved outline is prose you'll throw away. Say the beats stand and the scenes get drafted one at a time. Each one is drafted by a fresh subagent that sees only its pack, gated by the audit, read by a second fresh subagent that's never seen the drafting conversation, and closed when two scripts both exit clean. The prose lands on disk; the reply is six lines saying what closed and what didn't.

If you're the author, say so. The skill routes to your voice skill (`create-luke-content:create-luke-content` for Luke) for the voice rules and runs that skill's lint on every scene as well as its own. It owns what connects to what; your voice skill owns how it reads.

## What's in the box

```
story/
  bible.md          voice, world, cast, and what's excluded
  beats.json        one card per scene: goal, the one change, how it ends
  scenes/<id>.md    the prose
  state/<id>.json   what's true at the end of that scene
  packs/<id>.md     exactly what the drafter was shown
  critique/<id>.md  what the fresh reader found
```

Three scripts, each with a self-test:

- `context_pack.py` builds the drafter's whole input and refuses to include more.
- `transition_audit.py` reads each paragraph seam for a pronoun, a connective, a shared name, a shared word or a spoken line, and fails on none. It also fails on a word count outside the beat's band, first-person leaks in a third-person scene, em dashes, and five stock tells (*a testament to*, *tapestry*, *delve*, *little did they know*, *in a world where*).
- `story_state.py` validates the bible's shapes, and fails a scene whose exit contradicts its beat card.

## What it won't do

- **It won't write from the whole manuscript**, even if you ask. If a scene needs more context, the fix is a bible section named on the beat card, not a wider window.
- **It won't rewrite prose in the main session.** Edits go back to the drafter with the sentences quoted, for the same reason.
- **It won't claim a scene is coherent.** The audit is a tripwire with named heuristics, and the research is clear that no measure of paragraph-level coherence exists yet. A scene can pass and still drift in a way only a reader catches, and the reply says so when a scene closes with warnings.
- **It won't write outlines, synopses or reports.** Those are documents, and other skills own them.

## Honest limits

Nothing has measured whether this beats asking Claude for the chapter with no skill at all. The scripts are proven to fire on deliberately bad prose and to pass a fixture, the design rests on three reports and 21 traced claims, and the comparison that matters hasn't been run. `EVALS.md` says exactly what was and wasn't verified, and records that the name and the icon were chosen without the user in the room.

The window width is a judgement. The reports disagree between two paragraphs, 500 words and 2,000 tokens; the default is two paragraphs and it's a flag, not a law.

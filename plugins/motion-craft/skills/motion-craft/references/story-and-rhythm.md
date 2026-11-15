# Story and rhythm

A film can be right in every frame and still be boring. Boring has a recognisable shape: one event every four or five seconds, the same move in every scene, one shot scale throughout, every ease a soft 0.6-0.8 s, and music idling until a single hit at the end. Nothing is wrong, so nothing gets fixed. This file designs the opposite on purpose, before any code.

Skip it for a short single-idea piece (one kinetic line, a logo sting, an overlay), where the request is the story. Follow the user's own script, storyboard or reference film when they gave one.

## 1. The one thing and the spine

- **What it is**, in one line: "You can now …" for a launch; the one idea the viewer must understand for an explainer; what changed and why it matters for a changelog.
- **One viewer doing one real task**, from the moment they need it to the result. One real piece of data (a query, a file, a prompt, a number) travels through it from the hook to the payoff. An explainer's spine is one concrete example worked through.
- **Facts stay apart from creative choices.** Every claim on screen traces to the source: the site, the docs, the data, the user's words. Never derive a claim the source did not make ("40 min to 2 min" is not "20× faster"); mark an illustrative number as illustrative.

## 2. Beats

A common shape for a launch film of about 35 s (HyperFrames `story.md` §4); scale it, and let the storyline's device bend it:

| Beat | Share of length | Job |
|---|---|---|
| Hook | ~8 % | the world and the need, or the feature already working |
| Tension | ~12 % | the old way failing on screen |
| Reveal | ~8 % | the product or idea named, about 20-30 % in |
| Proof | ~40 % | the real task in the real UI as 3-6 verbs (paste, pick, watch it build, ship), one shot each |
| Payoff | ~20 % | the output arrives already moving: the biggest moment, once, 60-80 % in |
| Claim | ~8 % | the one thing, in one line |
| End card | ~8 % | the mark carried in, the name and the call to action land and hold 2-3 s |

An explainer is narration-led instead: the script comes first and sets the timing, each picture appears on the spoken word it illustrates, and a scene changes when the idea changes (explainroo). A data story earns one number per scene and makes the key number physical before the claim. A logo sting is three beats: a deliberate entrance, the completion, a clean hold of at least 1.5 s.

**The proof beats show the product doing its job, not a metaphor for it.** The real interface acting on real material, its real output, and the evidence (a number, a before and after, a command a viewer can run). A brand mark, a mascot or an abstract device may carry the hook, the transitions and the end card; it never stands in for the proof. A film whose middle is the logo performing an idea reads as beautiful and empty, and blind judges preferred a plainer film that showed the work (`evidence.md` §6).

**The problem is shown, not named.** When the hook is the problem the product solves, put the problem itself on screen: the generic output, the broken state, the slow way. A caption naming it ("The rut.") over the brand mark asks the viewer to imagine what the film should have shown. In the second blind round the skill's launch film did exactly that and lost specificity and story 4-0 to a plain film that opened on twelve identical dark cards (`evidence.md` §6).

In each proof beat keep only what the cursor touches and what proves the line; delete the rest of the screen. The process runs fast; the payoff plays at normal speed.

## 3. The hook and frame 0

Frame 0 is the poster that feeds and players show before the film plays: the subject is already in it, never a black frame, an empty ground or a lone logo. The hook lands within 3 s: a clear onset, the first cut, or the feature visibly working on something recognisable (14 of 21 launch films measured by huashu-motion had an onset or cut inside 3 s). It does not have to be frantic; most measured films opened well under their peak loudness.

Good openers: the result first; a real moment that creates the need; a question with the input inside it; a sentence whose last word becomes the picture (the owner's reference film opens on a full sentence whose nouns turn into product chips, `references/evidence.md` §3). Typing into an empty prompt box as the opener is the tell of a generated film; a few seconds in, as a story step, it is fine.

## 4. Choose the route

| Route | What carries the eye | Hard cuts | Fits |
|---|---|---|---|
| Continuous | one world, a camera moving through it, objects carried from shot to shot | 0-2 | precise and calm brands, mechanisms, one product UI |
| Montage | the beat: every cut lands on it and every frame reads at once | many, on the beat | hype, hardware, games, "look how much it does" |
| Hybrid | a continuous spine broken open by one or two montage bursts | bursts only | most launch films that should feel energetic |

Measured with `hyperframes measure cuts`: Anthropic's Claude Motion launch has 8 hard cuts in 82 s with one unbroken 32-second stretch (continuous with few cuts); the owner's reference film has 20 cuts in 95 s, an unbroken 20.6-second opening, then nine cuts between 24 and 37 s and six between 42 and 58 s (hybrid); music-driven launch films averaged a shot every 1.8-3.5 s (huashu-motion, 21 films, October 2026). Whatever the route, every cut is motivated: carried by an object or landed on a beat.

## 5. Draw the energy curve

Before the beat map, score each stretch of a few seconds from 0 to 10 and check the shape:

- **Hook within 3 s.**
- **Climb in steps you can name** (the kick enters, the camera starts travelling, the cuts double), not a slope nobody can see.
- **A burst near the middle**: 5-8 cuts in five seconds, about one per beat, at 30-60 % of the length (median about 37 % in the measured films).
- **The hero moment on the strongest musical point**, usually after the burst.
- **A stop when it earns its place**: 0.5-1.6 s of near stillness and near silence, then picture and sound land on the same frame.
- **Resolve** to one idea, held.

Shapes that read as boring: a flat line with a hit at the end; a slow build that peaks in the last two seconds; the same energy in every scene. Two drops (a small one at a third, the big one at three quarters) work for films over 30 s.

## 6. Density: events per bar

An event is anything the eye or ear registers as new: a cut, an element landing, a camera move starting or stopping, a word, a hit. Count them per bar of four beats:

| Stretch | Events per bar | Shot or move length |
|---|---|---|
| Hook | 2-4 | moves of 0.25-0.5 s |
| Build | 2-4, rising | 1-2 beats per move |
| Stop | 0-1 | hold 1-2 beats |
| Peak or montage | 4-8 | ½-1 beat per shot |
| Resolve, mark | 1-2 | hold ≥ 1.5 s on the mark |

Underneath it: nothing stays unchanged for longer than about two bars (roughly 3-4 s) except a planned stop. Something new every 2-4 s across the film; a new layout every bar when there is music. In long-form talking-head work, a professional editor's rule of thumb is a change every 1-3 s (IFL9MLPDN_U).

## 7. Contrast schedule

Change at least two of these at every section boundary, and all of them at the drop:

- **Shot scale**: extreme close-up ↔ wide. Open on a detail and pull out hard; punch in on a number as it lands. The owner's reference film cuts from the whole window to one toolbar button and back.
- **Speed**: 0.25 s hard moves against a 2 s glide; speed ramps inside one move.
- **Ease family**: hard ease-out for arrivals, springs only for physical things.
- **Camera**: still ↔ travelling ↔ whipping.
- **Density**: one object ↔ a grid of nine.
- **Ground colour**: a flood to the brand colour, a flip to dark.
- **Music texture**: half-time ↔ full beat ↔ stop ↔ drop.

## 8. Montage bursts

A montage is a run of shots each a beat or shorter, cut exactly on the beat, each readable at a glance. Build it from real material (the product's outputs, real user stories, real numbers); invented filler makes a montage read as stock footage. Give it one spine: an anchor held in place while the world behind it changes, one framing stepped through scales, or a label slammed in with each shot. Accelerate inside it (two beats per shot, then one, then half, then stop). Every new shot enters already moving, and each cut gets a hit or tick in the sound.

## 9. Write it down: the rhythm sheet and the continuity chain

Add both to `SPEC.md` before writing scenes.

```text
stretch    bars   energy  events/bar  moves                                   music
hook       1-2    7       3           ECU on the dot, hard pull-out on beat 3 kick and hats from bar 1
build      3-6    5→7     3           cards land on beats, camera tracks      half-time, bass enters bar 5
stop       7      1       0           freeze on one word                      tape stop, reverse cymbal
peak       8-11   9       6           3x3 grid slams on eighths, punch-ins    full band, impact
resolve    12-13  4       1           pull back to the mark, hold             motif on the logo, ring
```

The continuity chain is one line per transition naming the object or colour that carries the eye from shot N to N+1 (`send button → orange card → colour flood → phone`). A link you cannot name is a cut; keep it only if the cut is the point. Scenes that replace each other with nothing carried across read as slides however smooth each one is.

Check the sheet before code: a hook inside 3 s, a burst of 5-8 cuts in five seconds, the hero on the strongest musical point, at least two changes at every boundary, and no stretch over two bars with nothing new.

## 10. Copy on screen

- Titles carry at most 6 words a line, one line on screen at a time, no trailing full stop; an explainer's lines may run to about 10 words.
- Show, do not list: no bullet slides, no three-card rows. When similar things repeat, each gets its own idea and layout.
- Real numbers only, from the source. The first line is never "Introducing", "Meet" or the logo; after the pain, "Introducing X" is fine.
- Never "unlock", "seamless", "supercharge", "game-changer", "revolutionize", "effortless", or "in seconds" unless measured.
- Read the lines alone: a stranger gets the pitch. Watch the pictures with the words covered: they tell the same story.
- With narration, the screen never repeats the spoken sentence word for word.
- The brand lands once, with weight, usually on the end card, carried in rather than placed; before that it shows only inside the product. The accent colour is rationed to one highlighted word, the payoff and the end card.

# Direction: from a one-line request to a film only this subject could have

Read this before building any new film. Most generated motion fails here rather than in the code: the request was one line, the model filled every gap with its defaults, and the result looks like every other agent's film (`references/evidence.md` §1: RSe268YFglA, Cft-TBQv_Y4, v1Gwa1KyUaI all show the one-line version and the directed version side by side).

The output of this stage is four files in the project: `BRIEF.md`, `materials/` with `materials.md`, `STORYLINES.md`, and `SPEC.md`. Nothing is built before `SPEC.md` exists, except the hardest shot used to test a direction.

## 1. Read the subject before asking anything

Collect, in this order, and write one line each into `BRIEF.md`:

1. **What it is**, in the user's words, and the one thing the viewer must remember after the film ends, in the viewer's words rather than a slogan.
2. **Where it plays**, which fixes the canvas: 16:9 1920×1080 for a site, YouTube or a keynote; 9:16 1080×1920 for Reels, TikTok and Shorts; 4:5 1080×1350 or 1:1 for a feed; a seamless loop for a landing-page hero or README GIF; a transparent overlay for footage.
3. **Length as a range**, from the story (a feature launch is usually 15-45 s, a logo sting 3-8 s, an overlay 4-10 s, an explainer 30-90 s). A length in the request is a ceiling, never padding.
4. **Sound mode**: sound-led (music and hits; narration only if asked), or must-read-muted (feeds autoplay silent; every line readable without sound).
5. **Narration**: none, a voice the user records, or generated speech. Settle it once; the default is none.
6. **Real material**, gathered before any design (step 2).
7. **What the film must carry**: the 3-5 facts a viewer must leave knowing, each traced to the source. For a launch, what the product does for the viewer, the evidence that it works (a number, an output, a before and after) and how to get it; for a data story, every headline figure of the data (the total, the peak, the change, and any second metric the data carries) unless the user narrowed it. Write them as a numbered list in `BRIEF.md`. This list exists because of a measured failure: in this skill's own first blind evaluation, both films built under it lost overall to plain no-skill films that simply carried more of the information, one a launch film that made its subject's logo perform an idea instead of showing what the product does, the other a data clip that dropped two of the data's four headline figures.

Ask only what you cannot find or infer, in one message with your defaults written in, so the user can answer "yes" or correct one line. Use the `AskUserQuestion` tool when the harness has it. In an autonomous run, write the defaults as stated assumptions and continue.

## 2. Real material first

A film about a product is made of the product. Before any direction, fill `materials/` and list every file in `materials.md` with its source:

- The real logo file, never redrawn. A logo rebuilt from shapes is "pretty close but never actually the exact logo" (cDb-wPq0Iyk).
- Screenshots or a screen recording of the real interface with real data, captured at the size the film needs. When the film needs the interface to move (typing, a list scrolling, a card lighting up), rebuild it in HTML traced from the capture at the same size with its real text, colours, type and icons, and compare the two side by side.
- The brand's colours and typefaces as values read from its site or code, and the font files themselves in `assets/fonts/`.
- Real numbers with their source; for a data story, the CSV or dashboard itself.
- Photos, avatars and thumbnails that appear inside the film: the project's own first, then openly licensed images (record source and licence), never grey boxes.
- **The signature device**: the one graphic or gesture only this subject has, read from its site, app or past campaigns. In the 21 films motionflare.ai made from product websites, each was built on one: Stripe's gradient ribbon sweeps through the film and returns on the end card, Raycast's diagonal red light bars are the ground of every shot, Cal.com's keycap grid backs each scene, Midjourney opens on its own `/imagine` command, Notion's illustrated characters pop in beside each feature, Caruso sets its interface over fine-art paintings. Write the device into `materials.md` with where you saw it; it becomes the ground, the carrier or the hook (`looks.md` §1). A subject with no device of its own gets one from its product's core gesture (the tap, the drag, the command it is used through), never from a stock motif.

Material you cannot get becomes a visibly labelled placeholder on the replacement list, and the gap is named in the first message. Screenshots from someone's machine can show private names and messages: crop or mask them.

## 3. Find the shape of the message

The message's shape picks the film's language more than the product category does (huashu-motion `director.md` §2):

| Shape | Sounds like | Language that fits | Wrong choice |
|---|---|---|---|
| Claim | "Introducing X" | kinetic type, one hero object, a sting | a UI tour |
| Workflow | "Type this, get that" | cursor demo in the real UI, continuous morph | abstract shapes with no product |
| Mechanism | "Here is why it works" | a system diagram or object the camera tours | a fast cut reel |
| Evidence | "Signups doubled" | a data story; one number earned, then made physical | numbers flashing by unread |
| List | "Five new things" | one object becoming each item, or kinetic chapters | five equal slides |
| Transformation | "Before and after" | the old way churning, the new way calm | a cut between two stills |
| Story | "A small agent wakes up" | a character, a hand-drawn world, a day in someone's life | bullet points |

Then score the subject's personality on five sliders from −2 to +2, each with the evidence you read it from (its site's type, copy and colours): precise ↔ playful (moves easing and shape language), calm ↔ energetic (moves cutting and tempo), premium ↔ accessible (moves density and type contrast), technical ↔ human (moves code and diagrams versus photos and faces), established ↔ new (moves restraint versus surprise). Write the result as one sentence, for example "precise, calm, premium, technical, new: Linear-like". For a launch film, keep the energy up whatever the brand: the calm of a brand sets the palette, type and eases, not the cutting (huashu-motion measured a calm brand's film rebuilt at a faster rhythm scoring 80 against 60 with the same user).

## 4. Three storylines, then one

Write three storylines into `STORYLINES.md`. They are three films, not three palettes: each has its own **device** (what the story is), **form** (how the camera and cuts carry it) and **world** (where it happens). Generate them per `ideas.md`: widen the request, freeze the default film, diverge through `trawl:trawl` or eight or more one-line pairings drawn from its device bank, and keep the three that beat the default and differ most; make one of them the bold one you would not have picked first.

Devices: a moment in someone's day; a character or cursor does the work; the feature happening to a recognisable image in the first half second; the result first, then pull back to where it came from; one object travelling across apps; life before and after; type carrying the argument; one number earned and made physical; a question with the input inside it ("What if you could make a video from your ⟨website⟩?"); the object is the explanation.

Forms: one continuous take; an object-to-object chain where every shot ends on the thing that opens the next; an endless zoom into a detail that becomes the next world; a flight through one world; cut on the beat; match cuts on one held shape; split screen collapsing to one pane; one frame that keeps rebuilding itself.

Each storyline says, in at most nine lines: its name and a real reference it resembles ("a Linear changelog", "an Apple bumper", "Kurzgesagt"), never adjectives; the first two seconds exactly; its beats in one line; its **carrier**, the one shape, object or colour that is on screen at every seam and that each transition hands over (one button that morphs through a dozen interface states, one photograph that travels from a grid to a lock screen to a print on a wall, Stripe's ribbon, an orange dot that becomes a graph and then a circle); its look in one line (ground, type, the one material, the palette with where each colour came from, or an entry from `looks.md`); its route (continuous, montage or hybrid, see `story-and-rhythm.md`); and its risk ("needs real UI captures"). The carrier is what the best-received films share: on prompt-motion.com the second most-liked film is one shape that never cuts (12,103 likes), and the most-liked launch film is one continuous take of one photograph (`evidence.md` §9). At most one of the three is a 3D direction, so the user always has depth to choose and always has something else. Every storyline carries every must-carry fact from step 1; a storyline that can only work by leaving facts out is a mood piece, and loses to a plain film that says more.

Put your recommendation first with its reason in one clause. When the user is there, stop until they pick; users often mix by layer ("A's composition with C's feeling"), so keep look, structure and rhythm as separate lines that can recombine. When they asked for the file or for no stops, take your recommendation, build it, and name the other two in one line each at handover.

When a direction depends on a drawn character or mascot, make that object first, alone, at full size; one weak object sinks every direction built on it.

## 5. The spec: every adjective becomes a number

Adjectives are where the default look lives. Write `SPEC.md` from the picked storyline before writing any scene (HyperFrames `spec.md`):

```text
GOAL:    what the viewer feels or does at the end, one sentence
OUTPUT:  W x H, fps, length range, MP4 | transparent WebM/MOV | GIF
TIME:    seconds x fps = frames; BPM and frames per beat (fps x 60 / BPM) when there is music
LOOK:    ground (hex, texture and amount), ink, one accent and where it may appear;
         display face + weight + size in px + tracking; body face the same;
         the medium (paper, product UI, glass, clay, 3D studio, photographs) with its numbers;
         light: shadow offset, blur and opacity; grain %, vignette %
CARRY:   the numbered must-carry facts from BRIEF.md, each mapped to the shot that shows it and its hold
CARRIER: the one shape, object or colour handed across every seam, and what it becomes in each shot
SIGNATURE: the subject's signature device from materials.md and where it appears (ground, carrier, hook, end card)
OBJECTS: every thing the viewer must recognise, with the details that make it read without a label
MOTION:  eases by role as named curves; springs as damping ratio; durations and staggers in frames
FINISH:  motion blur shutter, grain %, depth layers, light, fps (craft.md §9)
SHOTS:   one line per shot: frame range, the one hero move, what the viewer reads and for how long,
         the sound, the object that carries the eye into the next shot, and why the shot exists
BANNED:  the defaults below, plus anything this film must not become
QA:      the frames to check and what each must show
```

A shot whose "why" you cannot write in a clause does not belong in the film; cut it rather than decorate it (prompt-motion's fix guide: "If Claude can't say why a beat exists, the beat doesn't belong").

Turning words into numbers: **premium** becomes a material with numbers (satin paper with 2 % grain, a product on a seamless sweep with a 0.55-opacity contact shadow); **modern** becomes a camera and a type system (a 30-frame push on one ease, a display face at 9 % of frame height with −2 % tracking); **clean** becomes a grid and a ration (12 columns, 96 px margins, the accent on one word per shot); **dynamic** becomes cuts on the beat and a layout change every bar; **playful** becomes springs at damping ratio 0.45-0.6 on position and scale only; **cinematic** becomes a lens and a light (a 35 mm framing, key light upper left, rim from behind, 6 % vignette).

### BANNED by default

These are where generated video lands when nothing else is decided. Each is banned unless the brand's own material or the user's reference uses it, and then only as they use it:

- a black or dark-navy void with small elements floating in its middle;
- glow, bloom, neon, lens flares, glowing orbs and rings, floating decorative particles, shockwave rings, RGB split, camera shake, grid floors and flashing backgrounds; glow is allowed on a thing that is light in the story (a beam, a screen, a sun), where it explains rather than decorates;
- purple or blue gradients, mesh gradients, glass cards;
- the cream or off-white paper ground with a serif display, italic accent words, numbered "01 / 02" labels, small monospace caps labels and pill-shaped chips; Anthropic's Opus 5.5 prompting guide names this exact set as the model's default look;
- the showreel default: an off-white or near-black ground flooded in turn with saturated orange, cobalt and lime, a giant heavy grotesk in capitals, a lone dot motif and small readouts in every corner; AI-Video-Factory's director policy names it "the common AI look", and all five runs of the gallery's most-copied 26-word prompt sampled for this skill land on it;
- everything centred; everything fading in at once; every element fading and sliding up;
- text that moves while it is read; titles that keep drifting after they land;
- cross-dissolves between scenes (cDb-wPq0Iyk: "it looks cheap");
- corner labels, frame borders, corner brackets and HUD readouts as decoration;
- a highlight box behind a word, which reads as a text selection; mark the word with colour or weight instead;
- motion that is not connected to anything on screen: a burst, sweep or ring that comes from nothing and goes nowhere;
- three cards in a row, KPI grids, a title over a dimmed screenshot;
- a typing prompt box as the opening shot with nothing else on screen;
- the logo docked small in a corner, and a frame 0 that is black, empty or a lone logo.

On prompt-motion.com, the 16 of 230 prompts that carried a banned list like this one included four of the 20 most-liked videos, and their median was 56 likes against 7 for the gallery. People who write banned lists also write longer prompts, so the list alone does not explain the gap.

After the first render, name every default it used anyway, from this list or not, add each to the film's BANNED line, and fix them before anything else. The guide's own advice for the same problem is to "check which styles the first result used instead, and extend the list".

A look holds together when it is the rules of one medium rather than a palette. Write the look as its parts, what each part may carry, and how the medium itself moves: paper is cut and lifted, ink is printed plate by plate, glass refracts, clay is pressed. A risograph look, for example, is one flat paper colour with fibre noise, one ink for everything read, one fluorescent ink for the single focus per frame, a third colour where they overprint with the second plate 3 px off register, and every gradient rendered as halftone dots.

## 6. Steering after the first render

Users rarely say what they want before they see it, and the first render is usually plain (Cft-TBQv_Y4). Read their notes as layer changes and apply the smallest one:

| They say | Change |
|---|---|
| "too fast" | slow every zoom and pan to 0.7× its speed, nothing else |
| "speed this up" | shorten the beats and the content by the same amount; later beats move up |
| "the titles move" | land them, then hold them dead still until they leave |
| "it feels like slides" | enter the next scene through an object already on screen; cut a move mid-flight |
| "boring" | redraw the energy curve (`story-and-rhythm.md` §3): a burst, a stop, a peak |
| "I couldn't read that" | hold 0.5 s + 0.3 s per word; cut words before shrinking type |
| "make it more premium" | one material with numbers, fewer elements, more shot-scale contrast |
| "it looks cheap" or "amateur" | apply the finish in `craft.md` §9 (motion blur, grain, depth, light), then check the look against `looks.md` |
| "it feels static" | a 3-5 % camera push through every hold, carried into the next shot's starting zoom (`craft.md` §5) |
| "the transitions feel off" | name the second and the two shapes, then hand one shape across the seam (`craft.md` §6) |

When a fix needs to give something up (a line shortened, a shot dropped), say what was given up.

# Ideas: many different films from a little context

Read this at step 2 of every new film, and whenever the user asks for ideas, options, "something different" or "surprise me". Most requests arrive as one line and a name. The film every agent makes from that line is the same film (`direction.md` §5's defaults), and asking the model again for "something creative" gives a reworded copy of it: in the research behind `trawl:trawl`, about 95 % of 4,000 ideas sampled from one model were duplicates of each other. Different ideas come from structure: a frozen picture of the default to move away from, isolated frames that cannot see each other, a bank of devices that real films have proved, and a test that the ideas differ in mechanism rather than in wording.

The output is `STORYLINES.md` with three films that differ, each traced to the device it borrows and the material it uses.

## 1. Widen the little you were given

Before generating anything, turn the one line into a page of facts the ideas can grip, in `BRIEF.md`:

- **The subject's world**: who uses it, at what moment, with what object in their hand or on their screen. A bookkeeping app's world is a shoebox of receipts and a quarter-end Sunday; a trading terminal's is a second-by-second number.
- **Its signature device** (`direction.md` §2) and **its core gesture**: the tap, the drag, the command, the upload it is used through.
- **Its message shape** (`direction.md` §3) and the 3-5 facts the film must carry.
- **The everyday images the audience already owns** for the problem: a full inbox, a red spreadsheet cell, a stack of paper, a spinner.
- **What was made before.** List the storylines and looks of earlier films in this project and its siblings (`STORYLINES.md` and `REVIEW.md` in earlier film folders) so the new ideas can differ from them. Consecutive films that look alike are a defect.

## 2. Freeze the default

Write, in 2-4 sentences, the film a competent agent makes from this request with no direction: for most products, the logo on a dark or cream ground, a headline fading up, three feature cards, a stat, the logo again. Name its native stack too (HyperFrames scenes, GSAP, the brand's captured interface). This paragraph does two jobs, both taken from `trawl:trawl`: every idea must differ from it in cause, intervention point or assumption, and in §5 each finalist has to beat it on the stated ask.

## 3. Diverge

**With `trawl:trawl`, when the session lists it.** Hand it the problem ("concepts for a <length> <format> film about <subject>"), the widened brief from §1, the must-carry facts, the frozen default as its baseline, and the native stack. Run its any% tier by default (2 frames, about 3-4 agent calls); run its standard tier (5 frames, about 8-14 calls) when the user asks for more options, for a launch film, or when the first three ideas came back alike. Frames that fit films:

| Trawl seat | A film frame |
|---|---|
| Ordinary stakeholder | the viewer at the moment they need the product, in their own room, with their own object |
| Operational constraint | one shot and no cut; six seconds; type only; one colour; the product's interface and nothing else |
| Adversary or inversion | the old way failing on screen; the competitor's film, inverted |
| Cross-domain mechanism | another medium or genre with a named mechanism: a recipe card, a nature documentary, a game's level-up screen, a receipt printer, a train window, shadow theatre |
| Wild seat | anything that looks wrong for the brief, exempt from fit until §5 |

Keep the branches isolated, as trawl requires: showing one frame another's ideas measurably reduces diversity. Translate every surviving idea back into HyperFrames scenes and the subject's real material before it reaches the shortlist.

**Without it**, do the same inline: write 8-12 one-line pairings, at least one from each of six families in §4, then take a second pass that rewrites the list to be bolder and removes any two that share a mechanism.

## 4. The device bank

Devices measured in shipped and community films (`evidence.md` §7 and §9). Borrow the mechanism, never the trade dress, and combine freely: a family is a starting move, not a template.

**A. One thing, never cut.** One button morphs through a dozen interface states with a cursor driving each change (prompt-motion's second most-liked film, 12,103 likes); an orange dot leaves a toggle, becomes the dot on an "i", traces a spring graph, floods the frame and returns on the end card; a white ball travels between components and presses the keys that type the text; one photograph goes from a grid to a lock screen to a print hanging on a real wall (the gallery's most-liked launch film); Stripe's ribbon sweeps through every chapter.

**B. The product's own gesture is the film.** Midjourney opens on its `/imagine` command and its prompts become the wall the logo forms from; Raycast opens on the ⌥ key; a "Reduce Motion" toggle is clicked and its letters bend until only "Motion" remains; two labelled cursors type the closing tagline (Claude's films); a wordmark squeezes into its own full stop, which becomes the pill the film grows from.

**C. A process from empty to done.** A Negroni built from an empty glass with each measure labelled as it pours (1,028 likes on a 65-word prompt); a trust deed uploaded, its parties verified one by one, a person approving the task (Caruso); a nursery that furnishes itself as a progress ring goes from 0 to 100 % (Enxovaly); one black shape that becomes Ordered, Printing, On its way and Delivered; the finished object shown first, then rebuilt from nothing (`saas-films.md` §4).

**D. The problem, shown.** Twelve identical dark cards of generic output (the plain film that out-argued this skill's launch film in round two of its evaluation); a wall of baby-product icons under "a thousand lists, a thousand doubts" (Enxovaly); "You have 47 tasks due today" over browser tabs multiplying (Caruso); "$15 Trillion" typed, then a red spreadsheet cell, a stack of paper and an old desktop window (Caruso); the user's own complaints typed with their typos (Claude).

**E. A number made physical.** A city of bike docks that empties by 8:15 (Claude Motion's launch); "global GDP running on Stripe" ticking live; a row of three figures from the site; one large number over a logo marquee; a stat count that is the point because it is live, never one counted through false values.

**F. Form as the idea.** Recursion explained in a different video style each time it recurses; a film remade shot for shot in a reference's rhythm beside the original; a loop whose last frame is its first; a poster that breaks out of its own frame; what happens in one second; a headline that keeps its sentence and swaps one word ("Scale", "Ship", "Think").

**G. A medium as the world.** Engraving-style art painted over photographs (an ad for Claude); risograph plates printed one by one; paper cut-out, claymation, chalkboard, blueprint, pixel art, oscilloscope traces (`looks.md`, motion-educator's templates); fine-art paintings behind white interface cards (Caruso).

**H. The mechanism, drawn.** White light through a prism, a molecule, blue arriving at the eye (motion-educator); a photon's journey out of the Sun; a request moving through a token bucket; the yellow first-down line drawn on a broadcast; what goes in, what it meets, what comes out, where it ends up.

**I. A montage of real output.** A curved wall of real vertical clips (an ad tool's promo); images switching on sixteenth notes into the drop (an image model's launch); nine images flying into a grid and circling the result.

**J. A character or a small world.** A plush mascot beside a phone demo (Muse); sketchbook animals that come alive; a Scrabble-tile character's story; shadow theatre in a living room; the seasons passing outside one train window.

**K. The work and the human.** An agent narrated by a status pill above one card that changes state, then a person's tap (Caruso); a typed request, a two-second status tile, the result with a number (`saas-films.md` §3); a human choosing among generated variants, paid off by a tagline that splits the work ("Claude makes it. You steer it.").

## 5. Converge on three that differ

1. **Merge by mechanism.** Two ideas with different words and the same device are one idea.
2. **Floors, not scores.** An idea stays only if it carries every must-carry fact, uses the subject's real material, can be built in code at the length, and answers the stated ask. Novelty never rescues a floor failure: this skill's first blind evaluation lost to plain films that said more.
3. **Beat the default.** For each survivor, compare it blind against the frozen default as Option A and Option B, on one question: which would a stranger understand the product from and send to someone? Keep the ones that beat it or tie.
4. **Pick three that differ on at least three of five axes**: device family (§4), carrier, route and form, world and look, and the first two seconds. Make one of them the literal film (the product doing its job, families B, C or K), one a reframe (D, E, F or H), and one the bold film you would not have picked first. At least two of the three come from families the earlier films in this project did not use.
5. **Write them into `STORYLINES.md`** per `direction.md` §4, each with its family and the film it borrows the mechanism from. When the user is there and the film is longer than about 15 s, offer one still per storyline before building: prompt-motion's test runs priced three ideas with a still each at about $3 against about $14 for a whole 30 s film.

## 6. When the user steers

Users mix by layer ("A's world with C's opening"), so keep each storyline's device, carrier, look and rhythm as separate lines that recombine. When the user rejects all three, add what they rejected to the frozen default, so the next round moves away from it rather than circling back, and run the divergence again with a different frame in the wild seat.

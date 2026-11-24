# SaaS product films: what good looks and sounds like

Read this for any film about a software product: a launch or feature film, a walkthrough, a presenter-led explainer or tutorial, a short announcement, or a customer story. It is measured from 48 product films that the owner picked as good examples, studied on 2026-11-16: 24 from Claude (Anthropic), 19 from Harvey and 5 from Muse, 82 s median length (19-290 s), 84 minutes in total. Each film was downloaded, transcribed, sampled at one frame every 2 s (2,512 frames, 1,752 opened at full resolution), read at native frame rate around 400 on-screen events, cropped at 2x or more for 284 type and interface readings, measured for hard cuts, holds and loudness, and judged by one analyst per film using be-my-witness's looking protocol. The method and the per-film findings are in `docs/research/saas-film-corpus/` at the plugin root; a bracketed id such as [kuxha-8IHCQ] is a YouTube id with its own findings file there.

Numbers are medians with the middle half of the corpus in brackets. These films are good, not perfect: §10 lists what even they get wrong, and where a corpus habit misses a delivery spec (loudness, type size) the spec wins.

## 1. Choose the film type first, because the rhythm follows from it

The skill's launch-film cadence (a cut every 1.8-3.5 s and a burst of 5-8 cuts at 30-60 % of the length) describes music-cut hype films. Most SaaS product films are paced differently, by change inside the shot rather than by cuts:

| Type | Films | Length | Cuts a minute | Median shot | Longest shot as share of length | Interface on screen |
|---|---|---|---|---|---|---|
| Narrated explainer or tutorial (presenter or voiceover) | 19 | 177 s (90-232) | 5.9 (2.9-9.2) | 4.8 s (4.5-8.9) | 28 % | 75 % of runtime |
| Music-led feature film, no voice | 18 | 77 s (58-83) | 5.4 (3.9-8.7) | 4.2 s (3.5-5.8) | 41 % | 69 % |
| Short announcement, 45 s or less | 7 | 32 s (26-40) | 3.1 (3.0-8.7) | 9.5 s (3.0-17.8) | 71 % | 68 % |
| Customer story, interviews and a demo | 4 | 82 s (61-104) | 11.7 (8.6-14.8) | 2.6 s (1.9-3.2) | 35 % | 51 % |

Across all 48 the longest unbroken shot runs 31 s (22-42), and runs of 40-116 s inside a screen recording are common [yUuFvL1lK4k, ydIT4EdLK54, _f_rtbW_uFM]. What keeps those shots alive is a change on screen: the median hold between on-screen events is 1.3 s (1.0-1.5), and the longest stretch of 2-second samples with under 2 % of pixels changing is 6 s (4-10). So for every type except the customer story:

- **Pace by change, not by cuts.** Something on screen changes every 1-3 s: a zoom, a typed line, a state change, a card landing, a cursor arriving. A shot may run 20 s or more while that holds. Treat 4 s with no change as the ceiling outside a planned stop.
- **Cut for a cause.** Hard cuts follow a cursor click, a topic change in the voice, or a change of world, and they cluster at chapter seams [idJQMJwHtyM puts 4 of its 5 cuts in the first 10 s].
- **A burst is optional.** Only 7 of 48 films have 5 or more cuts inside 5 s, and they sit anywhere from 8 % to 78 % of the length. When a burst exists it has a reason on screen: one cut per spoken list item [kuxha-8IHCQ, 5 cuts in 4.2 s on "RSVPs, vendors, invoices, emails"], one per typed letter [mTzRvY38xGw, 8 cuts in 2.9 s], or a run of steps before the payoff [COJAZQM1aeQ, 7 cuts at 75 %]. Keep the 30-60 % burst for a film whose brief is energy.

The customer story is the exception: interview films cut on phrase boundaries every 1.4-3 s [XO244jk7xH4 runs a 1.4 s median shot for two minutes], and a demo inside them may still hold one long take [kuxha-8IHCQ holds the phone for 28 s].

## 2. Frame 0 and the first 3 seconds

What frame 0 shows across the 48:

| Opening | Films | Example |
|---|---|---|
| A title or claim card with the subject in it, often already typing | 14 | "Legal AI moves fast" typed in 0.4 s [vlwlzyBqgvc]; the question the product answers on one card [xDiG-MN7GzU] |
| The product or its output already working | 10 | a rolling counter on the dashboard [S9IJ1GgAAxE]; the user's own messages, typos included [5qt_aGyAsKk]; the finished 3D output [en0GuyhieQk] |
| A presenter mid-sentence, often with a lower third | 7 | [mQZB0l-rhxE, yUuFvL1lK4k] |
| A lone wordmark on a blank ground | 13 | every one of them Harvey's |
| Other: a motif, an icon, live-action scenery | 4 | [bOeWJRfYWWY, XO244jk7xH4] |

Binding rule 1 holds. The wordmark openers are the house style of one brand, and they work only when the product or the claim arrives within about 1.5-2 s [ydIT4EdLK54 cuts to its data map at 2.0 s]; the one that waited 21.7 s lost its hook [B87ICNnr_GQ]. The first hard cut lands at 4.8 s (2.2-8.4), so the hook is motion inside the first shot, not a cut: a headline typing, a counter rolling, a character walking in within 0.7 s [LrXnOKCr0mo].

Openers that showed the problem rather than naming it: the user's typed complaints on a dark ground [5qt_aGyAsKk]; a named colleague's message arriving inside the product at 2-4 s [G3vwVsh9RtU]; a product name struck through and replaced at 2 s [wzrBFx0ONZg].

## 3. The shape of the film

- **Demo beats carry the film.** Of 563 beats the analysts marked, 195 are demo or proof beats, each taking 10-11 % of the length. Hook beats take 4 %, the end card 5 %.
- **The hero moment sits at 56 % of the length (35-71 %).** It is usually the finished output arriving, not a transition.
- **One invented scenario, carried everywhere.** Films that used invented interface made it read as real work by running one business, named people and one set of numbers across every screen: Huckleberry and Teo on tiles, board, chat and Gantt [YUYeHMsqbmY]; 58,500 and 6,500 in both heading and chart [YewAJPawE7I]; one repo, one bug and PR #128 through a four-minute tutorial [-OH1y7CjIew]. Use one scenario with names and numbers that recur on at least four surfaces.
- **The agent action in three beats.** A typed request on screen, a status tile of about 2 s naming the work ("Analyzing data…"), then the result with a specific number [YUYeHMsqbmY, G3vwVsh9RtU]. Without voiceover, the status label is the narration [We8BTITLvb4 changes one present-tense chip every 2-3 s].
- **One card, narrated by a status pill.** Caruso's agent loops (getcaruso.com, recorded 2026-11-24) keep one card in place and let a pill above it narrate in present tense, a new phrase about every 1.5 s: "Picking an agent…", "Trust Onboarding", "Adding related parties…", "Screening parties…", "Added task". The card changes state underneath it: a trust deed uploaded, its details with a PENDING chip, three related parties stacking in, each gaining a green VERIFIED chip with a spinner on the one still running, then a task "Approve Thompson Family Trust" assigned to a named person, whose Approve button the cursor presses and which turns green. One entity and its named people run through the whole loop, and grey skeleton bars stand in for everything the story does not need.
- **A human decision in the middle of the machine's work**, paid off by the tagline: "i like D" among generated variants [5qt_aGyAsKk]; a person steering a running task once, on screen [tYOI-WoLS_o]. Claude's taglines then name the split: "Claude makes it. You steer it." [To5nrYqvR44, bVXiNb9RyyI, en0GuyhieQk].
- **Chapters as cards.** Long films restart attention with a text-only card of 1-5 words before each product area, held 2-4 s [ydIT4EdLK54, tYOI-WoLS_o], sometimes previewed as a numbered index first [Jw6l1jgNVw8]. A music-led film without voice can repeat one title template as a chorus: "AI that ___ for you", six times [We8BTITLvb4].
- **Bookends.** Close on, or rhyme with, the opening frame: the same flip [4tlIHJqGiRc], the same lockup move [_Qxh2NZcWuY], the opening card reached by a fade through grey [TVbOAMAxC4Y], the same dark wordmark frame at 0 s and 99 s [arDCe_F8vfk].

## 4. Proof: show the product working on something specific

The proof devices that recurred, each a picture rather than a claim:

- a fail state then a pass state in the same interface with one number changed ($4.50 to $9.00; layout shift 0.19 to 0.00) [mQZB0l-rhxE];
- the same input in two windows, cut to the result when the faster side finishes [jKRl_CSVxyI];
- the counter-case before the advice: medium effort misses a field, high effort finds it [jKRl_CSVxyI];
- one tiny flagged object fixed, then the same counters at full scale (0 errors, 0 warnings) [lCR9epzSNGc];
- the product checking itself ("Mostly.", with arguments for and against) [SkFmiMHDN38];
- a limit proved as well as a claim: the masked email, then the command that still uses the real one [yUuFvL1lK4k];
- each branch of a workflow run and shown producing different output [fFQM0LHOGBc];
- the finished object shown for 5-6 s, then rebuilt from empty, so a long build has a destination [fFQM0LHOGBc];
- the real wait left on screen (a spinner, 47 s, 1 min 21 s) and the result swapped in a single frame [lCR9epzSNGc], with a "sped up" pill wherever time is compressed [jKRl_CSVxyI].

A claim spoken with no picture was the commonest story weakness the analysts named [kuxha-8IHCQ says "I just tell Muse and it makes the change" over a dashboard scrolling back to the top]. Put a picture on screen for every claim the voice makes.

## 5. Showing the interface

The product is on screen for 70 % of the runtime (55-80 %): as a real capture in 29 films, floating interface cards in 21, a redrawn simplified interface in 20, a device mockup in 13. A real cursor appears in 25.

**Legibility is where even these films fail.** Analysts rated the interface fully legible at phone width in 1 film of 48; in the other 47 the wide shots carry 5-14 px text on a 720-pixel frame, which reads as texture. The films that read well all did the same thing:

- **Zoom to the control being used.** Push 1.5-3x onto the panel the voice or cursor is on, so working text reaches at least 2.6 % of the frame's short side (19 px at 720p; 25 px or more for a prompt [idJQMJwHtyM]). Show the whole window only to orient, for 2-4 s [B87ICNnr_GQ, _f_rtbW_uFM, arDCe_F8vfk].
- **Make the click target visible.** A target under about 2 % of the frame's width gets a crop that makes it about 5 % wide with the cursor in shot [C-5wF6tkQ2Q]. On a phone, a tap ripple and a push of about 1.27x until the new page lands [kuxha-8IHCQ].
- **Echo small facts at readable size.** When real interface text has to stay small, repeat its fact as a chip of 20 px or more beside it and highlight the matching spot [xDiG-MN7GzU], or grey a long paragraph down to three black key phrases that then become the next layout's labels [7M5TXyoJ-Jc].
- **Type the prompt on screen as it is spoken**, punched in about 2x, and hold it for the reading time (about 4 s for 18 words) [COJAZQM1aeQ, YewAJPawE7I]. One film typed the first letters at two thirds of the frame's height [mTzRvY38xGw].
- **Dim the rest.** Zoom about 3x on the one token being named and drop everything else to about a quarter contrast [yUuFvL1lK4k].
- **Let the product animate itself.** Named cursors typing at once show collaboration better than narration about it [SkFmiMHDN38, YewAJPawE7I]; the product's own editing gestures (select, bold, drag) can be the transitions [COJAZQM1aeQ, bVXiNb9RyyI].

Seven more from a production run reviewed frame by frame by other models (`evidence.md` §8). Each fixes a fault that passed every automated check:

- **Show the whole card, then push in.** Hold a card or panel whole for about 1 s, at a size where its headline reads, before pushing in on the part that matters. A run of crops that never shows the whole leaves the viewer rebuilding the card from pieces, and reviewers from four model families flagged exactly that.
- **Keep chrome off the line that carries the point.** In a pushed-in shot, a composer bar, toolbar, pinned header or the caption band covers live text. Before rendering, list every line in a capture that carries a must-carry fact, and confirm that some frame shows it whole and uncovered.
- **Give a decision time to read.** Keep the control on screen at least 1.5 s before the tap, show the press (a ripple or a pressed state), and hold the result before the camera moves. A tap 0.6 s after the buttons appeared read as no decision at all.
- **Veil the pane you leave.** On a foldable, a split view or two windows side by side, cover the pane the camera is not on with the ground colour at about 80 % opacity, so the text the frame edge cuts reads as background rather than as a cropping fault.
- **Fade system sheets in fast.** A passkey, Touch ID or permission sheet should be fully opaque within about 0.15 s; a slower fade leaves frames where the page shows through, which reads as a rendering fault.
- **Use the product's real mark in system chrome.** Notifications, connector chips and tool lines that stand for the product carry its real mark, never a generic glyph, or the notification reads as another app's.
- **Open on content, not an empty app.** A chat or editor that starts nearly empty and fills over 2-3 s makes frame 0 mostly blank screen. Start with the earlier messages already there.

## 6. Type on screen

From 144 `hyperframes measure ink` readings:

| Element | Height as share of frame | Source |
|---|---|---|
| Titles and claim cards | 7.3 % (5.7-9.4) | all films |
| Chapter titles beside an interface | 4.4-6 % | [_f_rtbW_uFM, TVbOAMAxC4Y] |
| Closing statements and product names | 9-11 % | [YUYeHMsqbmY, bOeWJRfYWWY] |
| Stat numerals beside the subject | 5-7 % | [lCR9epzSNGc, _Qxh2NZcWuY] |
| Lower thirds | 4-6 % | [XO244jk7xH4] |
| Running captions, one fixed position | about 3.6 % | [_Qxh2NZcWuY] |

Titles run 5 words a line at most (4-6), which confirms binding rule 3. How they move:

- **Built word by word, then still.** Six words in 0.77 s [_f_rtbW_uFM]; 0.04-0.16 s a word [7-1tNo8HAwk, wzrBFx0ONZg]; a 19-character claim typed in 0.4 s [vlwlzyBqgvc]. The landed line does not move.
- **Out in reading order**, word by word, in about 0.35 s, shorter than the entrance [mQZB0l-rhxE].
- **A title rail.** The title lands, slides to a left rail and holds there for about 10 s while only the interface beside it changes [Jw6l1jgNVw8, wzrBFx0ONZg].
- **Two accents worth adding to the one-accent-word rule:** a second line in pale grey that darkens to black over about 0.5 s [wzrBFx0ONZg], and a headline that changes one word at a time ("faster" to "smarter") [bOeWJRfYWWY, xDiG-MN7GzU].
- **The reading hold is the commonest type miss**: 7-9-word openers held 1.1-1.9 s where binding rule 2 asks 2.6-3.2 s [7-1tNo8HAwk, 5qt_aGyAsKk, o5PmFp8HYTM]. Hold every line for 0.5 s plus 0.3 s a word, counted from when its last word lands.
- **Running captions in a film without a voice.** Start each caption on a beat in `timeline.json` and hold it until the next. In the production run, three or four captions carried a 30 s film after seven or eight had run on a 3 s clock that ignored the picture. Each caption names the actor and the verb and says what the frame does not already show; a caption that repeats the card it sits under spends the viewer's reading time twice (`evidence.md` §8).

## 7. Motion and transitions

Each film uses 4 kinds of transition (4-5), which confirms binding rule 7's 3-5. By how many films use them: hard cut 46, interface state change 46, morph or shared element 25, continuous camera move 25, push or slide 16, fade through a colour 15, zoom through 13, cross-dissolve 10, mask or wipe 7, match cut 6, whip 2.

- **Hard cuts are the main seam in these films, and that works when each has a cause** (a click, a topic change, a change of world). For a walkthrough or explainer, judge a hard cut by its cause rather than by binding rule 7's one-third share.
- **Flip the ground between worlds.** White interface to a black claim card on a hard cut, instead of a dissolve; four times in 81 s [4tlIHJqGiRc], and as bookends around a light middle [Jw6l1jgNVw8, arDCe_F8vfk].
- **Travel inside one recording** with a blur-to-sharp zoom between two views of it [B87ICNnr_GQ].
- **Hand over with an object:** a drawn outline that fills with the next screen [_f_rtbW_uFM]; the old device sliding out in 0.25 s as the next rises [XNbc2HhL7J4]; one accent stroke carried through 30 s of abstract scenes [S9IJ1GgAAxE]; the chosen chip staying as the next scene's subject [xDiG-MN7GzU].
- **Dissolves stay short or stay out.** The 10 films with cross-dissolves use them for 1-3 frames between a presenter and graphics, or to clear a title card in reading order over about 0.7 s before cutting to the product [-OH1y7CjIew, C-5wF6tkQ2Q]. None dissolves between two scenes of content.

## 8. Ground and colour

Light grounds dominate: the median film has 85 % light frames in Claude's set, 91 % in Harvey's and 80 % in Muse's. Colour is rationed to one accent with one meaning: coral only on Claude-owned buttons, amber for the problem and teal for the contrast [en0GuyhieQk]; teal for memory [xDiG-MN7GzU]; purple only for the live recording state [Bn9Vv8e_WPk]. A pale film can make one saturated screen its reveal, cut to at about a third of the length [LrXnOKCr0mo]. Harvey's films run near-monochrome (saturation 0.015) and let product icons and outputs carry the colour [7M5TXyoJ-Jc].

Claude's own films use the cream ground and serif display that `direction.md` §5 bans by default. That is the brand's own material, which the BANNED list exempts; for any other brand the ban stands.

## 9. Sound

- **Voice.** 25 films are music-only; 23 carry speech (11 presenters on camera, 8 voiceovers, 3 customer testimonials, 1 presenter with voiceover). Narrated films run at 167 words a minute (151-178). Two voice-led tutorials carry no music bed at all [-OH1y7CjIew, mQZB0l-rhxE].
- **Cuts follow the story, not the beat.** In 36 of 46 measurable films, the share of cuts landing within 0.12 s of a strong sound onset is less than 0.10 above what chance would give. Where picture and music meet, it is at a music section change: a reveal on the return of section B [XNbc2HhL7J4], cuts on section boundaries [dUIuvfP2j2c], a zoom-out at a section change [mTzRvY38xGw]. Put the reveal and the hero on a section change of the track.
- **A silent tail.** 23 films end with at least 1 s of silence, the music stopping 1.2-2.5 s before the end under the logo [YewAJPawE7I, XNbc2HhL7J4]. A silent tail pulls integrated loudness down: one film's −13.6 LUFS short-term peak measured −15.4 integrated [YUYeHMsqbmY], so master the whole file, tail included.
- **Loudness is not a reference here.** Integrated loudness runs −15.8 LUFS (−17.2 to −14.1), from −25.7 to −11.2; 15 films sit within a decibel of −14; true peak exceeds −1 dBTP in 18 and 0 dBTP in 9. Keep the binding loudness rule in SKILL.md (−14 LUFS, true peak at or below −1 dBTP) as the delivery spec and treat these masters as the miss to avoid.

## 10. Endings

- **A line, then the mark, held still.** The mark holds 3.8 s (2.8-5.0) on a plain ground; Harvey holds longer (4.1 s) than Claude (3.3 s). The last line holds at least 2 s; the best hold 4-5 s [7M5TXyoJ-Jc, ydIT4EdLK54].
- **The tagline as a demo.** Typed, selected and trimmed [COJAZQM1aeQ]; one word retyped by a labelled cursor ("Sync", "Sort", "Work") [YUYeHMsqbmY]; the first word swapped under a selection highlight [YewAJPawE7I]; typed by the film's own two named cursors [To5nrYqvR44, SkFmiMHDN38].
- **Two short sentences that split the work** close 7 of Claude's 24 films ("Run by Claude. Led by you." [S9IJ1GgAAxE]); Harvey closes on one brand line, "AI Tailored for Law", in 7.
- **The ask is usually missing.** Only 12 of 48 put an action or availability on screen (a URL, store badges, an install command, "Coming soon"); 12 more end with no line of their own on the end card, two of them speaking the ask without showing it. Put the ask on the end card as text: a URL, a command [yUuFvL1lK4k: `/plugin install hide-email@my-mods`] or store badges [kuxha-8IHCQ].

## 11. What even these films get wrong

Check every film against these, in this order, because each appeared in the owner's chosen examples:

1. Interface text a viewer must read sits under 2.6 % of the short side in wide shots (47 of 48). Zoom per §5.
2. The master misses −14 LUFS or the −1 dBTP true-peak ceiling (33 of 48 outside ±1 LU; 18 over the ceiling).
3. A line meant to be read is held under 0.5 s plus 0.3 s a word, most often the opening line.
4. No ask on screen at the end (36 of 48).
5. Frame 0 is a lone wordmark and the product arrives late (13 open on a wordmark; 1 waits 21.7 s).
6. A claim is spoken with no picture of it (§4).
7. A stretch with nothing changing outruns 4 s: the longest static run is 6 s at the median and reaches 30 s.
8. A must-carry line inside the interface never reaches a frame whole: pushed past, or under a composer bar or the caption band (§5, from the production run in `evidence.md` §8).

## 12. Five house styles

Borrow the method, never the trade dress (`reference-films.md` §3).

| | Claude | Harvey | Muse | Caruso | motionflare.ai |
|---|---|---|---|---|---|
| Ground | warm cream, terracotta and sage fields; warmth +6 | white and near-black in alternation; saturation 0.015 | white studio and pale gradients; the most saturated (0.20) | warm off-white; fine-art paintings of architecture behind interface cards; dark teal heroes | the brand's own motif, moving (ribbon, light bars, keycap grid) |
| Type | serif display, one coral accent, hand-drawn underlines | serif wordmark, word-by-word headlines on blank ground | humanist sans titles beside a plush mascot | serif display, one lavender accent word, chapter words typed with a caret | flush-left 2-3-line headline beside the product |
| Device | presenter plus product, labelled cursors, one invented business | left-rail title with interface beside it, ground flips, an orbit motif | customer interviews around one phone demo | one agent card narrated by a status pill, skeleton filler, a human approval | one continuous take of feature chapters, a stat row from the site |
| Pace | 8.1 cuts a minute | 3.9 cuts a minute, long continuous takes | 10 cuts a minute | 0.8-2.1 cuts a minute; still for 74-78 % of the runtime | median 2 cuts a film; 15 or 30 s at 60 fps |
| Close | two-sentence tagline, typed; mark held 3.3 s | "AI Tailored for Law" and the wordmark; held 4.1 s | icon, wordmark and store badges on black; held 3.9 s | one claim line, then the wordmark on lavender, then on dark | mark, line, the product's own two buttons and the URL; held about 3 s |

Caruso's calm suits a finance audience, but its homepage films stand still for 7.0 s and 4.5 s at a stretch, past the 4 s ceiling in §1; borrow its register and keep a slow push or the next row arriving through every hold.

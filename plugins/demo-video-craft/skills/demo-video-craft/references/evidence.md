# Evidence

Where each rule in this skill comes from. Three sources, cited below as [run], [corpus] and [build].

**[run] The source run.** A series made on 24-25 November 2026 for an AI connector that works inside Claude and
ChatGPT, aimed at one US advisory firm (not named here). Five rounds of owner notes over two days, ending with one
overview of 1:41 and nine shorts of 21-25 s, each delivered muted and voiced, published on a small video site with
a menu page, an overview page, a shorts modal and an interactive features page; the last round moved every screen
onto a real US-listed company's public filings. The whole session transcript (about 12,300 lines before three
compactions) was read in fifteen slices by fifteen agents, each writing the owner's notes, the exact specs, the
failures and proposed changes; those findings are not committed, because they quote a client engagement, and the
quotes below have names removed.

**[corpus]** motion-craft's study of 48 shipped SaaS product films (24 Claude, 19 Harvey, 5 Muse; 84 minutes),
in `docs/research/saas-film-corpus/` of the motion-craft plugin: `digest.md` for the statistics,
`findings/<id>.md` for each film. motion-craft's `references/saas-films.md` is its readable form.

**[build]** Measurements made while building this skill, on the source run's finished files and on the starter kit's
example series (two films built, checked, and one rendered and gated).

## Rules and their sources

| Rule | Source |
|---|---|
| One source per thing that appears in several places | [run] the lockup fixed on the pages stayed wrong in the films ("the video versions of the logo … is still wrong"); the share image still showed round 1 after three rewrites; a corrected voice line kept playing from cache |
| Overview 80-110 s, shorts 20-25 s | [run] overview 1:24, 1:31, then 1:41 with its end slide; owner: shorts "extended to at least 20-25 seconds". [corpus] music-led feature films 77 s median (58-83) |
| Overview ≤ 130 words; a short is one line of 24-35 words | [run] round 2 halved round 1's 250 words to 124; the colleague's note "its quite verbose"; round 3's lines of 30-32 words, round 5's of 31-35 (9.6-12.0 s) |
| Second person, active, outcome first | [run] owner: "the narration needs to be in active tense - i.e. you can do this / achieve this outcome" |
| Hold 0.5 s + 0.3 s a word; hold after typing | [corpus] the commonest type miss is an opener held 1.1-1.9 s against 2.6-3.2 s; motion-craft's binding rule. [run] owner: "pause after typing has occurred so that the user can read what's put" |
| Text ≥ 2.6 % of the short side | [corpus] wide shots failed it in 47 of 48 films; HyperFrames' `text_below_floor` check at 28 px on 1080 |
| Something changes every 1-3 s; nothing still past 4 s | [corpus] median hold between on-screen events 1.3 s; longest static run 6 s at the median |
| Pace factor, start at 1.2-1.3; per-op motion capped at 1.25x, travel at 1.2x, the opener at 1.15 | [run] round 2 "pick up the pace", round 3 "very fast, they were hard to keep track of what was going on"; approved at 1.3 (overview) and 1.22 (shorts); the pace function in the source's film table |
| Frame 0 complete, never mid-type-on | [run] owner: "The first (main) video also starts partway through a text animation". [corpus] frame 0 carries the subject in 35 of 48 |
| Overview ends on an end slide with the ask as text | [run] owner: "the top video is missing any kind of end slide". [corpus] the ask was missing in 36 of 48; logo hold 3.8 s median (2.8-5.0) |
| Shorts end on their result, no repeated end card | [run] owner: "End on a useful product result and remove the closing screen that repeats the opening headline"; "Remove the repeated … end card from the short clips" |
| Keep the films inside the host app | [run] "the AI tools you already use" was the product's lead line; [corpus] interface on screen for 70 % of runtime |
| No serif in product mockups | [run] owner, twice: "Remove Times New Roman from the Claude mockup"; "make sure that none of the demos have times new roman font" |
| Live HTML of the product's kit, not screenshots | [run] round 1 onward; pushes of 2-3x stayed sharp, and copy fixes were text edits |
| Blur-in arrivals, navy cursor with press ring, growth from source | [run] owner: "Take more of the motion animation feel and effects and use of mouse from the [reference] film"; measured from that film's frames |
| The lockup measured from the brand's site by pixel rows | [run] the first pass put the mark high with a washed-out front colour; owner: "did you even look at this?" |
| One fictional company, figures on ≥ 4 surfaces | [corpus] the invented-scenario films [YUYeHMsqbmY, YewAJPawE7I, -OH1y7CjIew]. [run] a fictional Nasdaq-listed company, name and ticker checked free in SEC's ticker file |
| Show only what is built; owner overrides recorded | [run] one short re-scripted because its feature was partly built; the owner chose to show rules a round earlier held back |
| No timing or percentage claims without a measurement | [run] no measure of time saved existed in the product record; the owner's "in minutes" kept as an open claims item |
| Respell only the voice input, specific rules first, for the voice's accent | [run] owner: "it should sound like "clord""; "Clord" was replaced by "Clawd" before anyone listened, because a US voice says every r; a two-word name said as a possessive; the first attempt fixed the brand alone and the possessive never fired on one line |
| Delivery tags are direction, not words | [run] Scribe transcription of 27 tagged lines: 0 tags spoken |
| Pronunciation needs a listener | [run] Scribe returns its own spelling of a respelled name, so a transcript cannot confirm it |
| Bed 0.28, ducked to 0.10; voice about 11 dB over; measure the separation, not the mix | [run] the first mix with paid beds, 0.55 ducked to 0.30: voice about 1 dB over the bed while the mixed file's loudness looked normal (-14.1 against -13.5); after: -23 against -34 LUFS before mastering |
| Merge dips for lines under about 0.9 s apart | [build] the source run's duck logic let the bed creep back up under a line when the next line started within 0.9 s; `duck.py --self-test` case "no swell in a 0.8 s gap" |
| -14 LUFS ± 0.5, true peak ≤ -1 dBTP | [corpus] 33 of 48 masters outside ±1 LU and 18 over -1 dBTP, kept as the miss to avoid. [build] the source run's 20 files: -14.0 LUFS, true peak -1.1 to -2.6 dBTP |
| One render, one remux | [run] the muted/voiced switch kept its place (2.95 s to 4.35 s, still playing) only because the pictures were identical. [build] `delivery.py check`: 10 of 10 pairs share one video stream |
| Never rename a published file; version every URL | [run] owner: "Any new videos published should use identical file names as they may be linked to"; the cached voice line. [build] `site_urls.py check` on the live site found the share image and the menu poster unversioned, then 70 of 70 current after the fix |
| A password gate blocks your own checks | [run] every live request answered 401 while the gate stood; playback was verified locally |
| Range requests for the switch | [run] Python's `http.server` answered 200 and reset the position; `npx serve@14.2.4` answered 206 |
| Real click for sound-on autoplay | [run] a scripted `.click()` played nothing on the live site; a driver's real click played |
| Focus the modal wrapper, not the video | [run] with focus on the video, the arrow keys seeked instead of stepping shorts |
| Leave internal apparatus off prospect pages | [run] owner: "Determine what else likely shouldn't be shown to a potential client", after removing requirement counts, status and assistant lists |
| Read the whole queue before rendering | [run] four rounds gained a note mid-task |
| Say what nobody checked | [run] every round's report: nobody had listened to the sound or watched at full speed |
| Lengthen the scene's hold when a line outruns its frame | [run] owner: "What the narrator/voiceover says doesn't align/line up with what's on screen in the overview"; fixed by four offsets and the intro growing from 8.6 to 11.5 s |
| A line may run at most 0.1 s past its scene | [run] round 5's v2 ran 0.09 s into the next scene with the next line well clear, accepted; anything larger was a re-placement |
| Start from the kit, not from prose | [run] round 1 built from descriptions measured 12-16 px text and a 54 s scene; [build] the kit's example rendered at 1080p60, 0 `hf.sh check` errors, 0 pops and 0 still runs, `delivery: PASS 1/1` |
| Camera fills 0.62 / 0.7 / 0.9, 0.92 height cap, 3.2x, full-frame stage | [run] contact sheets of round 2 "frames too small" while the stage still reserved a 180 px caption band; after: about 27 px body text at 1080p |
| Typing 52 cps, hold 0.6 s; a prompt present at scene open is written whole | [run] 34 cps with a 1.5 s hold drew "Cut … long typing animations"; contact sheets showed frame 0 mid-type |
| Highlight as a multiply tint parented to its row | [run] owner: "some of the highlighting needs to be improved"; a boxed outline replaced by `rgba(31,63,166,.13)` multiply, padded 2 px sideways |
| Lengthen a short by one more step, not a longer hold | [run] owner: "these perhaps can be extended to at least 20-25 seconds"; nine shorts went from about 15 s to 21-25 s by saving, opening or correcting the result |
| Align a lockup with neighbouring text on the baseline | [run] owner: "this alignment is bad" (a page header); measured inside the text, the wordmark sat 6.7 px above the links on one page and 4.4 px on the others, and about 5 px below the button text in every short's lockup bar; after: within 0.1 px |
| GSAP owns transforms | [run] `gsap.set(…, { xPercent: 0 })` cancelled the bar's `translateX(-50%)`: every short's lockup bar sat with its left edge at the frame's centre for two rounds, found only while checking the alignment note |
| Stage, gate, then publish | [run] the render loop copied each film live as it finished and continued past a failed render; [build] `delivery.py publish` refused a staged set with K07 at +1.3 dBTP and published 9/9 after the limiter |
| Read an exit code on its own line | [run] `delivery.py check … \| tail` printed FAIL 9/10 beside rc=0; `films.py \| tail && build.py` hid a SyntaxError and built ten films from stale plans |
| A demo yields only to a press of its own controls | [run] owner: "when i hover over the first demo on the features page or click it, the animation stops"; wheel and empty clicks had handed it back |
| A prospect page has a length and layout budget, and no vendor apparatus | [run] owner: "this is inanely complex to handover", "this layout looks terrible. revise all sections", then removals of stats rows, feedback buttons, Pilot/Later badges, the assistants list and the status section; 6,313 words became 1,959 |
| One English variant, no switch | [run] a UK/US switch was asked for, shipped, and removed about 40 minutes later: "Remove the english toggle … just stick to us english" |
| A real company: every figure sourced, nothing invented, `SOURCES.md` first | [run] owner: "Update the videos and website to use a real company"; demos built on an invented acquisition and a "said privately" line were rebuilt around public facts; the sources file was written last, after the screens |
| Ask before a real company goes on a public page | [run] the owner chose "Keep it public" against a recommendation to gate it |
| Compare files before re-voicing | [run] "still says "Diologue Guardian""; the live and local files had identical SHA-1s, and the browser was replaying a copy cached under `max-age=86400` |

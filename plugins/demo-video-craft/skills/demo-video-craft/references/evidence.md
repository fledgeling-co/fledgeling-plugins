# Evidence

Where each rule in this skill comes from. Three sources, cited below as [run], [corpus] and [build].

**[run] The source run.** A series made on 24-25 November 2026 for an AI connector that works inside Claude and
ChatGPT, aimed at one US advisory firm (not named here). Four rounds of owner notes over two days, ending with one
overview of 1:41 and nine shorts of 21-25 s, each delivered muted and voiced, published on a small video site with
a menu page, an overview page and a shorts modal. Its notes were digested in four parts from the session
transcript. They are not committed, because they quote a client engagement; the quotes below have names removed.

**[corpus]** motion-craft's study of 48 shipped SaaS product films (24 Claude, 19 Harvey, 5 Muse; 84 minutes),
in `docs/research/saas-film-corpus/` of the motion-craft plugin: `digest.md` for the statistics,
`findings/<id>.md` for each film. motion-craft's `references/saas-films.md` is its readable form.

**[build]** Measurements made while building this skill, on the source run's finished files.

## Rules and their sources

| Rule | Source |
|---|---|
| One source per thing that appears in several places | [run] the lockup fixed on the pages stayed wrong in the films ("the video versions of the logo … is still wrong"); the share image still showed round 1 after three rewrites; a corrected voice line kept playing from cache |
| Overview 80-110 s, shorts 20-25 s | [run] overview 1:24, 1:31, then 1:41 with its end slide; owner: shorts "extended to at least 20-25 seconds". [corpus] music-led feature films 77 s median (58-83) |
| Overview ≤ 130 words; a short is one line of 24-34 words | [run] round 2 halved round 1's 250 words to 124; the colleague's note "its quite verbose"; round 3's lines of 24-34 words |
| Second person, active, outcome first | [run] owner: "the narration needs to be in active tense - i.e. you can do this / achieve this outcome" |
| Hold 0.5 s + 0.3 s a word; hold after typing | [corpus] the commonest type miss is an opener held 1.1-1.9 s against 2.6-3.2 s; motion-craft's binding rule. [run] owner: "pause after typing has occurred so that the user can read what's put" |
| Text ≥ 2.6 % of the short side | [corpus] wide shots failed it in 47 of 48 films; HyperFrames' `text_below_floor` check at 28 px on 1080 |
| Something changes every 1-3 s; nothing still past 4 s | [corpus] median hold between on-screen events 1.3 s; longest static run 6 s at the median |
| Pace factor, start at 1.2-1.3 | [run] round 2 "pick up the pace", round 3 "very fast, they were hard to keep track of what was going on"; approved at 1.3 (overview) and 1.22 (shorts) |
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
| Respell only the voice input, specific rules first | [run] Claude respelled so it is said "clord"; a two-word name said as a possessive; the first attempt fixed the brand alone and the possessive never fired on one line |
| Delivery tags are direction, not words | [run] Scribe transcription of 27 tagged lines: 0 tags spoken |
| Pronunciation needs a listener | [run] Scribe returns its own spelling of a respelled name, so a transcript cannot confirm it |
| Bed 0.28, ducked to 0.10; voice about 11 dB over | [run] first mix: voice about 1 dB over the bed; after: -23 against -34 LUFS before mastering |
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

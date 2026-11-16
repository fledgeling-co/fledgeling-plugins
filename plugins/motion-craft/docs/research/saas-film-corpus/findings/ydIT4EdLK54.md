# Harvey Platform Overview (ydIT4EdLK54), 231.6 s

## Hook and structure

Frame 0 is a centred black serif "Harvey" on near-white (f0001.jpg; `frames.frame0.contentfulCells` 0.031), so the poster holds no product. A hard cut at t=2.0 s (strips/window-01-1.933s.jpg) lands on a grey world map whose countries shade dark while the narrator says "Over 74,000 lawyers at 700 organizations in 58 countries" (f0004.jpg, transcript 00:00-00:07). The hook is therefore a proof statement at 2 s, not a problem.

The film runs as a feature explainer, one chapter per product area. Proof stats come first (map, "24" then "25 Hours Saved", f0007.jpg, sheet-01; four badges SOC2 II, CCPA, ISO 27001, GDPR at t=24, f0013.jpg). The Assistant demo follows as one 77.8 s capture from 30.4 to 108.2 s (`rhythm.longest_shot`, 33.6% of runtime). Word and Outlook take 108-142 s, Vault 142-158 s, review tables 158-190 s and Workflows 190-218 s. Hero moment: "96% Accuracy vs. 89% Contract Attorneys" over a blurred table at t=190 s (sheet-06), share 0.82. The close is "651 Deployments" on black (f0110.jpg), a 2x2 customer-stat grid (f0112.jpg) and "AI Tailored for Law" with the wordmark, static in f0115.jpg and f0116.jpg for about 5.5 s.

## Rhythm

`metrics.json` gives 11 hard cuts, 2.85 cuts per minute, a median shot of 8.95 s and six shots over 10 s. Cuts cluster in the first 30 s (2.0, 7.23, 9.67, 22.97, 30.4 s) and then thin out: 108.23, 131.5, 141.97, 144.53, 218.13, 220.97 s. `rhythm.bursts` is empty. Inside the long captures, change comes from the interface: median hold 1.73 s, longest 7.87 s, and a 14 s static run ending at 158 s (`longest_static_run_s`). That run is where the film is slowest (country-list scroll at f0046.jpg and f0049.jpg, sheet-02).

## Look and type

Ground is near-white (luma 239.4; `light_share` 0.983) with pale grey-green and off-white tiles, and two near-black cards at t=142 s and t=218 s (f0110.jpg). Saturation is 0.008 and `bw_share` 0.67: no brand accent. Colour appears only inside real UI (red strike-through edits in f0055.jpg, status dots in the playbook, partner logos).

Headlines are a large serif, sub-labels a small sans (crops/stat-sub2.png reads "saved per contract on review, summarization, analysis, and translation"). `$HF measure ink` on six lines gives 5.4-8.3% of the 720 px frame: "Harvey" 50 px (6.9%), "Accelerate Expertise" 39 px (5.4%), "24" 52 px (7.2%), "7 Hours" 60 px (8.3%), "7 Hours" in the grid 48 px (6.7%), "AI Tailored for Law" 51 px (7.1%). Every title is one line of at most 4 words.

## Product interface

About 74% of runtime shows product (my estimate from the 2 s samples). It is real capture with a real arrow cursor: the sources menu (f0022.jpg), the typed prompt with "Complaint.PDF" and "Web search" chips (f0061.jpg), the agent flowchart (f0037.jpg, crops/flowbox.png: "EXTRACTION Get the strongest pieces of evidence", "ITERATIVE DOCUMENT SEARCH Deeply search through documents"), the editor with "Show edits" and "Version 2" (crops/editor-toolbar.png), and Word and Outlook add-in panes (f0058.jpg, f0067.jpg). A desktop browser plus a phone mockup appears at t=20.9 s (strips/window-12-19.7s.jpg).

Legibility is partial. Crops such as crops/prompt-ui.png ("Remove all the materially non-conforming terms you identified...") are crisp at 1280 px, but the Outlook window (f0067.jpg), the review table (f0082.jpg) and the Vault grid have 8-10 px text and would not survive a phone.

## Motion and transitions

Four kinds appear. Hard cuts (11) land on a new subject, for example "Accelerate Expertise" to a grey-green tile grid at 9.67 s, with tiles entering by 9.73 s (strips/window-04-9.6s.jpg). UI state changes carry most of the film: menus open, a PDF chip drops into the prompt (f0052 sheet-02), checkboxes tick (f0085.jpg), columns generate, a progress bar fills (f0049 sheet-05). A cut at 19.77 s takes the H logo to a browser that scales to reveal a phone (window-12). A fade through colour at 144.3-144.8 s brightens a dark "Vault" card to white (strips/window-57-144.3s.jpg). Other seams: a dark card with a shrinking circle logo at 141.97 s (strips/window-56-141.9s.jpg) and a Word-to-Outlook hard cut at 131.5 s (strips/window-52-131.433s.jpg). I did not tally every seam, so the hard-cut share is not checked.

Typed prompts appear character by character (f0043.jpg shows "...strongest pieces of evidence in o"). The workflow prompt highlights key phrases (f0106.jpg), then the same phrases become nodes (f0109.jpg).

## Copy on screen

Cards carry 1-5 words and hold 2-6 s: "Accelerate Expertise" 2.4 s, "25 Hours Saved" about 4 s, "Matters Documents Research" about 4 s, "Workflows" about 2 s. All clear the 0.5 s plus 0.3 s a word rule. The last line, "AI Tailored for Law", holds about 5.5 s. Stats come in two forms: a single number with a label ("651 Deployments", f0110.jpg) and a 2x2 grid with a logo, number and subtext ("60% Reduction in NDA review times", "96% Adoption of Harvey across the legal department"; f0112.jpg). The on-screen copy mirrors the narration (transcript 00:11 "up to 25 hours each month", 03:04 "96% accuracy").

## Sound

The audio is narration over a music bed. `audio.json` tags: speech 0.82, music 0.628, keyboard_musical 0.328, synthesizer 0.285, percussion 0.213, piano 0.135 (below 0.2, not named). There is no steady beat (confidence 0.028). Auto-captions give 468 words, about 121 words a minute. Integrated loudness is -14.1 LUFS, true peak -0.2 dBTP (above a -1 ceiling), loudness range 2.9 LU, short-term max -10.6 LUFS: flat dynamics. `cuts_on_strong_onset_share` is 0.091 against `chance_share` 0.06, a 0.031 gap, so the cuts are not locked to the sound; they follow the sentences. Silence covers the last 1.55 s from 230 s. I did not hear the film; no sound-effect tag scored above 0.2.

## What to steal

1. A text-only chapter card of 1-3 words before each product area, held 2-4 s (Harvey / Microsoft, Matters Documents Research, Workflows).
2. A customer-proof grid: logo, serif number near 7% of frame height, one or two lines of subtext, on alternating tiles (f0112.jpg).
3. Turn typed text into structure by highlighting phrases, then showing them as diagram boxes (f0106.jpg to f0109.jpg).
4. A narrated explainer can let a 77.8 s real-UI take run if the screen changes about every 1.7 s and a cursor leads the eye.
5. Close on a tagline and wordmark held 5 s or more.
6. Avoid: a lone wordmark at frame 0, 8-10 px UI text in wide shots, and a true peak above -1 dBTP.

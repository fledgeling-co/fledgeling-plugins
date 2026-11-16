# Harvey Workflow Builder (fFQM0LHOGBc), findings

## Hook and structure

This is a 177 s narrated screen recording, not a launch film. Frame 0 (f0001.jpg) is a near-black card; the serif word "Harvey" is absent at t=0.15s and faint by t=0.2s (strips/window-01-0.15s.jpg), so frame 0 carries the brand but no product (metrics frames.frame0 contentfulCells 0.075). At t=1.4s a hard cut brings a white card reading "Workflow Builder" (f0002.jpg), and at t=3.6s a fade through grey lands on the finished two-branch canvas (strips/window-03-3.55s.jpg, f0003.jpg). The product is therefore on screen at 3.6s, just past the 3s hook window. The film then shows the answer first: the completed File upload, Selection list, Conditional, and Prompt/Response branches sit on screen until t=9.8s. A black "Build" card (f0007.jpg, t=10-11s) restarts from an empty canvas with one "Add step" button (f0010.jpg). The build runs in narration order: details modal (19.5s), file upload (28-51s), selection list and conditional (51-60s), buyer prompt (60-91s), supplier prompt (91-115s), a black frame at t=118 (f0060.jpg), the test run (120-154s), access (154-161s), publish (161-168s), the Workflows library (f0085.jpg) and a fade to the wordmark (f0088.jpg). The hero moment is the supplier output with its comparison table at t=150s (f0076.jpg, share 0.849).

## Rhythm

metrics.json reports 24 hard cuts, 8.15 cuts a minute, median shot 3.51s and mean 7.07s, with 3 shots over 10s and no burst (bursts: []). The longest shot is 53.1s (t=85.5-138.6, 30% of runtime). The numbers hide two modes: title cards and the access section cut quickly (cuts at 28.25, 28.35, 28.75, 28.78 and 154.57-155.98 are clusters), while the build runs in long takes. 33% of sampled intervals are static (intervals_static_share 0.333) and the longest static run is 14s, ending at 106s, where only a typing caret changes. Pace is carried by the narration at 181.6 words a minute (535 caption words) rather than by editing.

## Look and type

Three kinds of ground: near-black title cards, one white title card, and the product window floating over a desaturated plant-texture backdrop (f0003.jpg). look.json gives luma 209.5, saturation 0.013 and bw_share 0.77, so the film is nearly monochrome. There is no brand accent colour; the only colour is the product's pastel block icons and a green tick on the published dialog (f0082.jpg). Titles are in a high-contrast serif and measured with `hf measure ink`: "Harvey" 114 px of 720 (15.8%) at t=0.5s, "Workflow Builder" 83 px (11.5%) at t=2.5s, "Build" 83 px (11.5%) at t=10.6s. These are about twice the binding 4-9% range. Every title is one or two words. Everything else is the product's own interface type.

## Product interface

The product is on screen for about 95% of runtime and is a real capture with a real hand cursor (f0013.jpg, f0034.jpg). The film does not redraw it. Legibility depends on zoom: the full-window frame (f0003.jpg) has node labels around 9-12 px, too small for a phone, while the zoomed frames read cleanly (crops/prompt-typing.png reads "You will be provided with a Supply Agreement. Identify the top 10 red flags for the buyer…"; crops/summary-table.png reads "Raw Materials … Indemnity" rows with citation numbers 24-36). The prompt is typed live with a character counter at 66, 194 and 413 of 4000 (f0034.jpg, f0037.jpg, f0040.jpg). The branch structure (crops/branch-nodes.png) shows "Buyer" and "Supplier" labels over two Prompt/Response stacks, so the logic is visible without being narrated.

## Motion and transitions

Camera moves are digital zooms with directional blur on a recorded screen: strips/window-06-19.517s.jpg (full window to modal in about 0.6s), window-13-28.167s.jpg (modal to canvas to Add step menu), window-27-51.084s.jpg and window-34-59.117s.jpg (panel to canvas). Each is caused by the next narrated action. The title-to-product change at 3.6s is a 0.45s fade through white and grey (window-03-3.55s.jpg). The 9.8s seam is a hard cut to black (window-04-9.8s.jpg). Most seams are UI state changes: menus open, panels slide in, the chat answer streams (f0064.jpg, f0067.jpg). Strips beyond 100s were not generated, so motion after 100s is read from 2s samples only.

## Copy on screen

Overlay copy is three words in total: "Harvey" (hold about 1.2s), "Workflow Builder" (about 2.2s) and "Build" (about 1.3s). Each meets the 0.5s plus 0.3s a word reading rule. There is no problem caption, no benefit line and no CTA card. The story is told by narration (transcript.md, auto-generated captions) and by the product's own labels. The closing line, "If you can define the process, you can build the workflow", is spoken near 2:50 and never shown as text; f0088.jpg shows only the wordmark fading in.

## Sound

The audio is speech over a quiet music bed: audio.json describe tags speech 0.835, music 0.697, keyboard_musical 0.397, synthesizer 0.308; percussion 0.194 and piano 0.19 are below the 0.2 bar, so no drum or piano claim is made. There is no steady beat (confidence 0.13). Integrated loudness is -24.2 LUFS, short-term max -22.1, true peak -5.4 dBTP, loudness range 2.8 LU, roughly 10 LU quieter than the -14 LUFS social target. cuts_on_strong_onset_share is 0.042 against a chance_share of 0.086, so the cuts are not locked to the sound. Sound effects for clicks cannot be confirmed from the evidence.

## What to steal

1. Show the finished object for 5-6s, then rebuild it from empty (f0003.jpg to f0010.jpg), so a long build has a destination.
2. Zoom the camera to the active panel and use the full window only to orient; zoomed text stays legible, full-window text does not.
3. Type text live with a caret and counter instead of pasting it (f0034.jpg to f0040.jpg).
4. Prove branching by running each branch and showing different output (f0068.jpg, f0076.jpg).
5. Bookend with one- or two-word serif cards, each held 1.2s or longer, fading through grey into the product.
6. Fix what this film skips: bring the product into the first 3s, master loudness to -14 LUFS, and end on a visible call to action.

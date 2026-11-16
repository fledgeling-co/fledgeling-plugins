# Introducing Claude Whiteboards, Sheets, and Data (YewAJPawE7I)

## Hook and structure

The film opens on an off-white frame holding one small grey "New in" chip (strips/window-01-0s.jpg, frame 0; `frames.frame0.contentfulCells` 0.0625). A Claude-labelled cursor types "Artifact" with a caret by 1.3 s, and at 2 s four line icons (doc, deck, sheet, palette) sit beside the leftover "cts" (f0002.jpg). So frame 0 is nearly empty and the subject builds inside the first 1.3 s.

Fifty-eight seconds then run as three chapters, each opened by a title card: Whiteboards at t=5-8 s (f0004.jpg), Sheets at t=22 s (f0012.jpg), Data at t=32 s (f0017.jpg). Each is followed by a staged demo. The hero moment is the finished pie-launch whiteboard at t=20 s with four collaborator cursors, a heart and a "Perfect!" tag (f0011.jpg, 0.346 of runtime). The Sheets table at t=30 s (f0016.jpg) and the dashboard at t=36 s are the other two payoffs. The ending is the tagline cycling "Plan / Share / Work at the speed of thought" (t=48-55 s, f0025-f0027.jpg), then a starburst and the Claude wordmark from about t=55.5 s (f0029.jpg). There is no URL or button.

## Rhythm

`metrics.json` reports one hard cut, at 45.79 s, 1.04 cuts per minute and a median shot of 28.89 s. The first shot runs 45.79 s, which is 79% of runtime, and `bursts` is empty. Rhythm comes from animation inside the shot instead: 42 strip windows, 10 appear events and 52 change events (`events.counts`), with a new element or state roughly every 2 seconds. Two shots are over 10 s. This contradicts the skill's 1.8-3.5 s cut cadence for launch films and its burst rule, while the film still feels busy because something moves on screen all the time.

## Look and type

The ground is warm off-white throughout (`look.luma` 242.1, `saturation` 0.035, `light_share` 1.0). Type is a high-contrast serif: a light first line and a bold second line, as in "Plan it out with / Claude Whiteboards" (crops/title-whiteboards.png). UI text uses a grotesque sans. Each chapter takes one icon colour (blue doc, brown deck, green sheet, purple palette, crimson chart, f0003.jpg), and Claude's terracotta marks its cursor and starburst.

Title ink heights, measured against a 720 px frame: "Plan it out with" 48 px (6.7%, t=6.7 s), "Holiday Pies: Pre-order Sales" 64 px (8.9%, t=41 s) and the "Claude" wordmark 78 px (10.8%, t=56 s). The measurement at t=49 s returned 63 px (8.75%) but the region may include a cursor tip. Title lines carry at most 6 words ("Plan at the speed of thought"). The large serif is well inside the skill's 4-9% band at the low end and above it for the logo.

## Product interface

The interface is on screen for about 62% of runtime by my estimate from the contact sheets (an estimate, not a measurement). It shows a whiteboard with illustrated sticky notes (f0010.jpg), a chat-plus-spreadsheet window (f0015.jpg), and a four-tile dashboard with line and bar charts (f0019.jpg). Content is one invented business, GeeGolly Good Pies, and the numbers agree across surfaces: 58,500 pre-orders, +17%, 6,500 boxes left (f0019.jpg, f0021.jpg, crops/dashboard-title.png).

Legibility is mixed. Big numbers and titles survive a phone, but sheet cells and chart axes are small (crops/sheet-table.png at 2x is readable, the 720p frame is marginal), so I rate phone-width legibility "partly". I cannot tell from frames whether the UI is a real capture or a redraw.

## Motion and transitions

Titles tumble in rotated and settle in about 1.5 s (strips/window-05-4.917s.jpg). Prompts type character by character with a caret (f0006-f0007.jpg). Claude's cursor draws the whiteboard in over t=14-19 s while the view zooms out (strips/window-14-14.875s.jpg). Chapter changes use a slide or a blur: the Sheets card defocuses as the prompt bubble pulls ahead (strips/window-22-26.959s.jpg, f0014.jpg), and the Data card slides left as the dashboard enters (f0018.jpg).

Near the end the camera pushes into the Share button (f0023.jpg, strips/window-36-45.459s.jpg) and then hard-cuts at 45.79 s to a cloud of integration logos (Airtable, Excel, Grafana; f0024.jpg). The logos blur out into the tagline. The cut is the only one, so the seam share is 100% hard cuts of a total of one seam, and it follows a UI push; the other six or so seams are slides, blurs and morphs.

## Copy on screen

Verbatim from crops and full frames: "New in", "Artifacts", "Plan it out with Claude Whiteboards", "@Claude Lay out an illustrated timeline for the Huckleberry Pie launch, from locking the flavor to holiday delivery.", "Build it with Claude Sheets", "Draft a forecast for pre-orders. Reference last year's numbers from the Historical tab.", "You got it.", "Share a story with Claude Data", "Plan / Share / Work at the speed of thought". The "Share a story" and "Work at" wording is from f0017.jpg and f0027.jpg.

Holds are estimated from the 2 s samples. Six-word titles hold roughly 2-3 s against a 2.3 s reading floor, so most pass. The closing wordmark holds about 1.8 s, under the 2 s last-line floor. No caption names a problem; the user's request is typed instead.

## Sound

The film has no voice. The caption track covered 28% of runtime and local whisper returned a single sentence repeated across the film, so I recorded source `none`. `audio.json` classifies it as music. Describe tags: keyboard_musical 0.507, synthesizer 0.451, percussion 0.326, piano 0.292, plucked_string_instrument 0.284. The bpm estimate of 185.7 has beat confidence 0.44, so I do not trust the tempo.

Loudness is -15.5 LUFS integrated, -13.1 short-term max, true peak -1.1 dBTP, loudness range 7.1 LU. That misses the -14 LUFS target by 1.5 LU but meets the -1 dBTP ceiling. The three sections are A 0-15.6 s, B 15.6-51.9 s, C 51.9-57.8 s, with silence from 56.62 s. The cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.0 against a chance share of 0.216, from one cut. I did not check sound effects; no tag above 0.2 supports any.

## What to steal

- Run chapters as one connected take with title cards of identical structure, so three features read as one product (f0004, f0012, f0017).
- Make collaboration visible with named, coloured cursors that touch the content and return in the tagline (f0004, f0011, f0027).
- Keep one invented business and one set of numbers across every surface.
- Type the prompt on screen and hold it long enough to read (about 4 s for 18 words, t=10-14 s).
- Rebuild the tagline live by swapping its first word with a selection highlight (f0025-f0027).
- End with the music stopping about 1.2 s before the end under the wordmark, but hold the logo for at least 2 s.
- Fix the weak points: put something recognisable in frame 0, enlarge chart text for a phone, and add a call to action.

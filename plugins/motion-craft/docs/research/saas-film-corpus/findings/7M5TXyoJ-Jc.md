# Create and Edit Files in Harvey (7M5TXyoJ-Jc, 53.92 s)

## Hook and structure

The film opens on a blank white frame (frame0 contentful cells 0.05, blank 0.95 in `metrics.json`). The serif "Harvey" wordmark pops in at 0.33 s (`strips/window-01-0.266s.jpg`) and is measured at 60 px, 8.3 % of the 720 px frame. By 2.1 s the headline "Create and Edit Files" has arrived, and from 2.5 s a grey panel slides in carrying Word, Excel and PowerPoint icons (`strips/window-03-2.133s.jpg`, `f0002.jpg`). The hook is therefore a title plus three app icons, not a product shot, and it lands inside 3 s.

The structure is a single prompt followed by three results. The prompt types at 4 to 6.8 s (`f0003.jpg`, `crops/prompt.png`), three phrases are picked out at 7 to 9.7 s (`f0005.jpg`), and three chips take over at 10 to 13.8 s (`f0006.jpg`). Three demos follow: Documents 14 to 24.5 s, Spreadsheets 25 to 33.5 s, Presentations 34 to 41.8 s. A recap runs 42 to 45.5 s, then "All in one place." at 46 s, "Available in Early Access" at 47.6 s and an end card from 49.47 s. I take the hero moment as the finished fee table at t=32 s (`f0017.jpg`, share 0.593).

## Rhythm

There is one hard cut, at 49.47 s (`cut_times_s`), so the first shot lasts 49.47 s, which is 0.917 of the runtime. Cuts per minute 1.11; median shot 26.96 s; bursts none (`metrics.json` rhythm). Pace comes from state changes inside that shot: median hold 1.33 s, longest 3.03 s, longest static run 4 s ending at 48 s. 19.2 % of sampled intervals are static and 3.8 % show a new composition. The three demos each take about 8 to 10 s and run the same sequence of log, skeleton, result, which makes the film easy to follow without cuts.

## Look and type

The ground is white, then warm grey with a white right panel; 92.6 % of sampled frames are light and saturation is 0.024 (`look.json`). Colour comes only from the Office icons and the generated files. Type is a serif for the brand lines and a bold grotesque for "Create and Edit Files" and the chips. Measured ink heights (`$HF measure ink`): "Harvey" 60 px (8.3 %, t=1 s), "Create and Edit Files" 40 px (5.6 %, t=3 s), "All in one place." 35 px (4.9 %, t=46 s), "Available in Early Access" 63 px (8.8 %, t=48.5 s), "AI Tailored for Law" 50 px (6.9 %, t=51 s). Chip labels measure 23 to 29 px, about 3.2 to 4 %. No title runs past four words. Density is sparse: `frames.median_contentful_cells` is 0.144.

## Product interface

Product UI is on screen from about 4 s to 44 s, roughly 72 % of runtime by my reading of the sheets. It looks like real Harvey screens with invented legal content, and a real cursor clicks send at 6 s (`f0004.jpg`). The camera never moves: each result appears in a right pane that occupies about 40 % of the frame width (`f0008.jpg`, `f0016.jpg`, `f0021.jpg`). Crops show readable file names ("Crestview V - Comment Memo - Commonwealth Health_v1.docx" in `crops/memo.png`), a legible spreadsheet title "Management Fee Model - Net Economic Impact Analysis" (`crops/sheet.png`) and a navy deck slide "Crestview Opportunities Fund V, L.P" with an agenda panel (`crops/deck.png`). The Answering log text is about 12 px high and the redlined memo body is unreadable at 1280 px (`f0007.jpg`, `f0013.jpg`), so legibility at phone width is partial.

## Motion and transitions

Transitions are caused by something on screen. The grey panel slides in at 2.5 s (`window-03-2.133s.jpg`); the phrases drop into rows and the chips slide in from the left at 10.7 s (`window-08-10.1s.jpg`); each chip's spinner turns to a green tick when its file is ready (`f0012.jpg`). The right pane slides off at 42.3 to 42.9 s to expose the recap (`window-24-42.333s.jpg`), about 0.6 s, shorter than the multi-second builds it follows. Inside the right pane, the log fades in line by line, the memo skeleton resolves into a redlined document (`window-13-20.033s.jpg`), the grid fills top to bottom (`f0016.jpg`) and "Generating Deck..." thumbnails scroll sideways (`window-22-37.7s.jpg`). The one hard cut at 49.47 s moves from pale grey to a dark end card (`window-27-49.4s.jpg`). Kinds of transition: ui-state-change, slide, wipe, hard-cut, four in all.

## Copy on screen

The prompt is the main copy: "I've uploaded 10 anchor LP comment memos and the corresponding Fund IV memos - update each memo for Fund V ..." (`crops/prompt.png`). It runs about 60 words and is held about 3 s, far below the 0.5 s + 0.3 s a word reading rule, so the film does not expect it to be read. At 7.4 s it greys out and three phrases stay black: "update each memo", "generate a spreadsheet", "prepare a slide deck" (`f0005.jpg`). Those ten words hold about 2.6 s, then reappear on the chip layout for about 3.3 s and again in the recap for about 2.2 s. Closing lines: "All in one place." 4 words, about 1.6 s; "Available in Early Access" 4 words, about 1.8 s; "AI Tailored for Law" 4 words, 4.4 s, over the 2 s floor. The wordmark appears again below it. There is no spoken copy and no caption.

## Sound

The film is music only. Kind is music; describe tags are keyboard_musical 0.864, synthesizer 0.779, piano 0.539 and electric_piano 0.533, so a keyboard and synth bed is supported. Percussion scores only 0.142, so I name no drums. Tempo is 82.1 BPM with beat confidence 0.456, which is weak. Sections run A 0 to 18.6 s, B 18.6 to 45.4 s, C 45.4 to 53.9 s. Integrated loudness is -14.0 LUFS, short-term max -11.6, loudness range 4.5 LU and true peak -0.6 dBTP, above the -1 dBTP ceiling. The one cut lands on a strong onset share of 0.0 against chance 0.173, so the cut is not locked to the sound, though with a single cut that is thin evidence. I cannot say whether typing or click sound effects exist.

## What to steal

- Reduce a long prompt to three read phrases by greying the rest, then reuse them as row labels (`f0005.jpg` to `f0006.jpg`).
- Keep one status chip with spinner then tick on the left and swap the demo on the right, repeating it per feature.
- Show each output as a specific real-looking file with a readable name, not a generic card.
- Echo the early chip layout as a recap at about 80 % of runtime before the tagline (43 s of 53.9 s).
- Close with large, quiet, word-by-word lines, then a dark card held 4.4 s.
- Fix before copying: keep log and prompt type above the 2.6 % floor and hold true peak below -1 dBTP.

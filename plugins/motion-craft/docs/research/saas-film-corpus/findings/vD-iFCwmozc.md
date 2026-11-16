## Hook and structure

Frame 0 is the word Harvey in a serif, centred on off-white (`f0001.jpg`). `frame0.contentfulCells` is 0.031, so it is a lone wordmark, not a poster with the product in it. The tagline "Legal Work, On the Move." types in word by word from 1.54 s to 1.75 s (`strips/window-01-1.459s.jpg`), then a hard cut at 3.0 s lands on a dark phone with an H on it (`strips/window-02-2.75s.jpg`). The product UI first appears at 3 s. The film runs in ten beats: logo, tagline, phone, attach menu (`f0005.jpg`, t=8 s), typed prompt (`f0008.jpg`, t=14 s), drafted email on the phone (`f0009.jpg`, t=16 s), Outlook window (`f0011.jpg`, t=20 s), Send button, Harvey / Microsoft lockup (`f0016.jpg`, t=30 s), then "Coming Soon" and "AI Tailored for Law" (`f0019.jpg`). I take the hero moment as t=26 s (share 0.648), when the Outlook email is mid-rewrite (`f0014.jpg`), though nothing in the sound marks it.

## Rhythm

`metrics.json` gives 1 hard cut, 1.5 cuts per minute and a median shot of 20.05 s. The longest shot is 37.1 s (92.5 % of the runtime) and there are no bursts. The film is continuous, not montage: the prompt card turns into a phone at 16.1 to 16.8 s (`strips/window-07-15.417s.jpg`), and the phone becomes the Outlook window at 18.9 to 19.6 s (`strips/window-08-18.459s.jpg`). Static stretches are long: `intervals_static_share` is 0.579 and the longest static run is 10 s, ending at 14 s. This contradicts the launch-film cut cadence of rules 8 and 10. It works here because a single object keeps changing, but no burst gives the film a high point.

## Look and type

The ground is flat off-white (mean luminance 0.978, `light_share` 1.0), with no gradient, grain or depth beyond the phone bezel and soft card shadows. Colour is held back: black type, purple on the send and stop buttons (`f0006.jpg`), Outlook blue on the title bar (`f0011.jpg`), and Microsoft's logo colours at 30 s. Titles are a high-contrast serif, centred, one line, with no accent word. I measured ink heights with `hf measure ink`: Harvey 50 px (6.9 % of 720) at t=1 s, "Legal Work, On the Move." 64 px (8.9 %) at t=2.5 s, "Coming Soon" 51 px (7.1 %) at t=34 s, "AI Tailored for Law" 51 px (7.1 %) at t=37 s, and the closing Harvey wordmark 38 px (5.3 %) at t=38 s. The first two ROIs clip at the region width and include descenders, so they are upper bounds. All titles sit inside rule 3's 4 to 9 % band, and the longest line is 5 words.

## Product interface

UI is on screen about 68 % of the runtime (3 s to about 30 s). It is a redrawn, simplified Harvey app and a faithful Outlook-style window, shown through a phone mockup and floating cards. The cursor is a real arrow, visible at 22 s (`crops/sidebar.png`). The crops are clean and readable: the attach menu lists "Scan document", "Upload from Vault", "Upload from phone files", "Web search" and "Knowledge source" (`crops/menu.png`). The prompt card shows the attached "24 Sept 2025 Meeting Notes" chip above "Draft an email summarizing the attached meeting notes" (`crops/prompt.png`). The Outlook panel reads "Harvey for Outlook", "Make this email more concise", "Edit / Ask", and the two Workflows "Summarize email" and "Send to Vault project" (`crops/sidebar.png`). Legibility at phone width is partial. In the wide Outlook shots (`f0011.jpg`, `f0014.jpg`) the body text is about 9 px high, so it only reads once the camera zooms at 22 to 24 s (`f0012.jpg`).

## Motion and transitions

Text enters word by word, each word fading from grey to black. This shows in the tagline strip and in "Draft an email summarizing the attached meeting notes", where the last word "notes" is still grey at t=14 s (`crops/prompt.png`). Transitions are almost all dissolves and morphs: the phone fades to a bare input bar by 5.6 s (`strips/window-04-4.959s.jpg`), and the Send button turns into the "Harvey / Microsoft" lockup at 30.1 to 30.3 s through a half-formed "H…soft" frame (`strips/window-12-30.042s.jpg`). The lockup is replaced by Outlook, SharePoint and Word icons at 31.7 s (`strips/window-13-31.459s.jpg`), and "Coming Soon" becomes "AI Tailored for Law" at 35.8 s with Harvey fading in underneath (`strips/window-16-35.25s.jpg`). The camera acts by scale: a zoom to the sidebar at about 22 to 24 s and a pull-back at 26 s. Each transition has a visible cause (a sent prompt, a Send click), which agrees with rule 7's "caused by something on screen". The dissolves between phone and bare input bar are close to the cross-dissolve rule 7 forbids, but they are same-object dissolves, not between worlds.

## Copy on screen

All the copy is on screen and the film has no spoken voice (transcript source `none`; whisper returned the typed prompt text and a hallucinated "Thank you."). Eight lines carry the film: "Legal Work, On the Move." (5 words, held about 1.25 s), "24 Sept 2025 Meeting Notes", "Draft an email summarizing the attached meeting notes" (8 words), "Post-Meeting Summary and Required Next Steps", "Make this email more concise", "Harvey / Microsoft", "Coming Soon", and "AI Tailored for Law". Hold times: the tagline falls short of rule 2's 0.5 s plus 0.3 s a word (2.0 s) at about 1.25 s. "Coming Soon" holds about 1.9 s, and the last line holds about 4.1 s, above the 2 s minimum. The problem is never named; the viewer watches a lawyer's task done by the tool.

## Sound

The sound is music only (`audio.json` kind music; describe tag music 0.884). Instrument tags above 0.2 are orchestra 0.512, keyboard_musical 0.478, plucked_string_instrument 0.406, bowed_string_instrument 0.402, piano 0.316, zither 0.309 and mandolin 0.3. Tempo is about 94 BPM but beat confidence is only 0.201. The five sections (A 0 to 6.3 s through E 32.4 to 40.1 s) are near equal in length. Integrated loudness is -13.6 LUFS, short-term max -12.2, loudness range 4.4 LU, and true peak is +0.3 dBTP. That peak is above rule 9's -1 dBTP ceiling, and the integrated level is close to -14. Silence runs from 38.6 s. Cuts are not locked to the sound: `cuts_on_strong_onset_share` is 0.0 against `chance_share` 0.048, from a single cut. I could not hear the film, so I can say nothing about sound effects on clicks or typing.

## What to steal

- Carry the whole film on one object that scales, dissolves and morphs into the next view. This film has one hard cut and still changes scene every 3 to 8 s.
- Let the last action cause the brand reveal: the Send button becomes the partner lockup (t=30 s).
- Show the capability with a believable two-step interaction, a typed prompt and then an edit prompt, not a feature label.
- After any wide window shot, zoom to the panel in use within 2 s. The full-window text here (about 9 px) fails the phone-width check.
- Hold the final line still for about 4 s (t=36 s to 40.1 s).
- Give the tagline a longer hold than 1.25 s, and give a calm film one bright burst or sound peak as its high point, which this one lacks.

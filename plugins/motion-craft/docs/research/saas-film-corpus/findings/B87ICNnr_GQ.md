# Harvey’s Legal AI Is Now Inside Microsoft 365 (B87ICNnr_GQ)

## Hook and structure

Frame 0 is the word "Harvey" in black serif at the centre of a near-white ground (`f0001.jpg`); `frames.frame0` reports 3 % contentful cells. The brand is present and the product is not. At t=3.4–3.8 s "Microsoft" fades in beside it (`strips/window-01-3.417s.jpg`), and the first product UI arrives at t=21.7 s, which is also `rhythm.first_cut_s`. So the opening 21.7 s, 14 % of the 151 s runtime, is logos and title cards only. The structure is: promise (0–21 s), SharePoint chapter (21.7–32 s), Outlook (33–58 s), Word editing and workflows (59–107 s), playbook review (108–127 s), a six-card close (128–140 s) and a logo hold (140–151 s). I placed the hero moment at t=110 s (share 0.73), where the playbook Summary panel reads "Review complete 17 of 17 rules" above a green, yellow and red bar (`crops/rules.png`). There is no call to action or URL at the end.

## Rhythm

`metrics.json` gives 10 hard cuts, 3.97 cuts a minute, a median shot of 4.62 s and a mean of 13.73 s, with five shots over 10 s. The longest shot runs 34.8 s from t=116.25 s to the end (23 % of runtime). `rhythm.bursts` is empty. Hard cuts cluster at 21.7–27.7 s (four cuts) and 109–116 s (three cuts); between them the film runs on long recorded takes where movement comes from zooms and UI state changes, not from editing. `frames.intervals_static_share` is 0.29, and the longest static run is 22 s, ending at 150 s: the closing cards.

## Look and type

The ground is near-white (`look.luma` 232, saturation 0.012). Title type is a high-contrast serif, Title Case, centred, one or two lines, at most three words a line. I measured it with `hf measure ink`: "Harvey" at t=0.5 s is 51 px tall (7.1 % of 720 px), "Access Institutional" 47 px (6.5 %) and "Knowledge" 56 px with its descender (7.8 %) at t=18 s, and "No Lost Context" and "In Sync" 44 px (6.1 %) at t=132 s and 138 s. That gives `title_height_pct` of 6.1–7.8. The crops at `crops/title-access.png` and `crops/title-nolost.png` show clean, unanimated glyphs. Colour comes only from third-party logos and the product itself: Microsoft's four-colour mark (`crops/lockup.png`), Outlook's blue bar (`f0014.jpg`) and the rule bar. There is no brand accent colour. UI windows sit on a warm grey ground with a soft shadow and a small black H mark at bottom right (`f0013.jpg`).

## Product interface

Real recorded UI covers about 70 % of runtime (t=21.7–127 s). It is the Vault file picker, Outlook for Mac with the Harvey pane, and Word with the "Harvey for Word" side pane, with a real arrow and hand cursor. Zoomed shots read well even at small size: the Save Email dialog (`crops/save-email.png`) shows "Name", "Folder: NDAs" and "Email Attachments", and the toast says "Files saved / Email saved as Re NDA Review Request – Acme Co..eml" (`f0029.jpg`). The wide window shots do not: at `f0040.jpg`, `f0061.jpg` and `f0064.jpg` body text is under 7 px glyph height. Legibility at phone width is "partly". The Playbook tooltip, "Highlight clauses in the document that are covered by playbook rules", is readable only because the camera has pushed in (`crops/tooltip.png`).

## Motion and transitions

Title cards fade in and out in place, over about 0.3 s. The strip at `strips/window-06-21.167s.jpg` shows "Access Institutional Knowledge" dissolving to white (t=21.17–21.27 s) before the Create project dialog fades up from white and a cursor appears (t=21.3–21.4 s). That is the one place where the film crosses worlds with a dissolve. In `strips/window-02-10.284s.jpg` the Microsoft lockup vanishes at t=10.33 s, a dot appears at 10.35 s, grows into the SharePoint icon by 10.47 s, and the label fades in; the icon is caused by what came before it. Inside the recordings, cuts land on a new dialog (`strips/window-09-25.3s.jpg`: the Select click at 25.3–25.38 s, then Create project at 25.4 s). Movement between views uses digital zoom with heavy motion blur that settles sharp: the Save Email dialog blurs at 56.08–56.18 s and resolves to the "Files saved" toast by 56.6 s (`strips/window-32-56.034s.jpg`). At t=29.55 s a toast expands into a panel on click (`strips/window-13-29.334s.jpg`). Word edits animate as real UI: 30 suggestions are queued and apply one at a time in the term-sheet task (`strips/window-60-91.317s.jpg`). I did not measure ease curves.

## Copy on screen

On-screen words are minimal: "Quality at Speed" (t≈14 s), "Work Without Interruption" (16 s), "Access Institutional Knowledge" (18–21 s), then the closing six cards "No Switching Apps" (128 s), "No Copying Files" (130), "No Lost Context" (132), "One Connected Workflow" (134), "Drafts" (136), "In Sync" (138). All are verbatim from the sheets and frames. Each is held about 2 s at the 2 s sample step, which is above the reading-rule minimum for 2–4 words (1.1–1.7 s). The cards echo the narration: the transcript has "No switching apps, no copying files, no lost context" at 2:09–2:11 and "just one connected workflow that keeps your documents, drafts, and communication in sync" at 2:11–2:16. The product does the explaining; the cards only name the benefit. The final "Harvey" holds about 5 s (t=146–151 s), above the 2 s minimum.

## Sound

The film is a voiceover. `audio.json` kind is "voice" and the top describe tag is speech at 0.915. Music scores 0.078, no beat is detected (`beats.count` 0, confidence 0.012), and the captions carry no music tag, so I name no music. Click (0.082) and tick (0.059) are too weak to claim UI sound effects; the "insect" tag at 0.203 is more likely a speech artefact. Integrated loudness is -14.7 LUFS with a 4.4 LU range and short-term max -11.3 LUFS. True peak is +0.2 dBTP, which is over the -1 dBTP ceiling. The auto-captions give 335 words, about 136 a minute, with short pauses at 33.0–34.3 s, 64.6–66.0 s and 73.5–75.0 s that fall on section changes. `cuts_on_strong_onset_share` is 0.10 against a chance share of 0.098, so the cuts are not locked to the sound. The only sync is semantic: closing cards follow phrases in the voice.

## What to steal

Name the integrations on one card with their logos, then show them in that order (`f0007.jpg`, t=10.3 s). Zoom each recording onto the panel being narrated and keep wide shots to short orientation beats. End on one phrase per card, 2–3 words, about 2 s each. Keep titles at 6–8 % of frame height; this film's measure 6.1–7.8 %. Use blur-to-sharp zoom travel between views of one recording and keep the white fade for the title-to-UI switch.

What not to copy: opening on a wordmark for 21.7 s before any product, since that breaks the 3 s hook rule; ending without a call to action; wide-shot text that cannot be read on a phone; and a mix that peaks at +0.2 dBTP. Because the film reaches its 34.8 s final shot and 3.97 cuts a minute without a cut burst, it also shows that a narrated feature walkthrough does not need rule 8's burst. It needs a UI event on screen at every sentence.

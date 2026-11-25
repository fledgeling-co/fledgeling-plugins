# Rounds

Step 9, and every owner note. A demo series is rarely finished in one pass: the source run took four rounds over two
days, and three of its notes reversed an earlier one. This file covers reading a note, finding everything it
touches, and reporting a round.

## 1. Read the whole queue first

Notes arrive while you work, as several messages. Before rendering, re-read every message since the last render.
In the source run four separate rounds gained a note mid-task (a reference film to study, a pronunciation, an
opening that started mid-animation, a whole new brief), and a render started before reading them would have
targeted asks that no longer stood.

Turn the notes into a numbered list in `ROUNDS.md`, each with what changes and where. Ask through `clarify:clarify`
only about what the notes leave open.

## 2. Find every place a note lives

The owner reviews by watching and by screenshot, and quotes the exact words on screen or in the voice. So:

- **Search the whole series for the quoted string**: `lines.json`, `respell.json`, the voice cache, the film
  plans, the page sources, the built pages. A wrong spoken word can live in the respelling rules, in the cached
  voice file, or in the browser's cached copy of the video (`site.md` §5); look at all three before re-voicing.
- **"Still wrong" means a second place.** When a note comes back, assume the fix landed in one copy and the thing
  lives in another: the films as well as the pages, the poster and share image as well as the video, the menu page
  as well as the overview page. In the source run the lockup was fixed on the pages, then "the video versions of
  the logo + guardian text is still wrong" sent the fix into the films, and only a URL check found the menu poster
  and the share image still showing the old one.
- **Check the result where the viewer sees it**: a crop of a rendered frame, the live page after deploy, the
  share image itself. A changed stylesheet is not a changed video.

## 3. Expect reversals, and build for them

Three reversals from the source run, each answered by a knob that existed before the note:

| Earlier note | Later note | The knob |
|---|---|---|
| "pick up the pace" | "very fast, … hard to keep track" | the pace factor in the film table |
| narration and captions | "remove the narrator and subtitles", then "with and without voiceover" | picture-first build, muted master plus a remux |
| labels added for clarity | "remove all text that says … illustrative workflow" | the label switch |

When a note reverses an earlier one, make the change and say in one line that it reverses round N's note, so the
owner sees the trade and can keep it.

## 4. What usually comes back

Notes that recurred, so check them before the owner has to say them:

- The opening starts mid-animation, or on an empty app.
- The narration does not line up with the picture (`voice-and-music.md` §4).
- A name is pronounced wrong.
- The end of the overview has no end slide, or a short ends on a card instead of its result.
- Text is too small, or highlights sit off their text.
- The page reads as a vendor's internal notes (`site.md` §6).
- An earlier round's videos or images are still on the site.

## 5. Reporting a round

- Inside a `~/Dev` project, invoke `status-update:status-update` and reply in its two lines.
- Otherwise reply in 3-6 lines through `agent-voice:agent-voice`'s work-report register: what changed, where it is
  live, the measured results (`delivery: PASS 10/10`, `urls: PASS 70/70`, the loudness range), and what is open.
- Always say what nobody checked. Loudness and still-frame numbers are not a listen or a viewing at full speed.
- Name every reversal and every claim made on the owner's say-so, so they are decisions on record rather than
  surprises in review.
- Confirm a deploy happened before saying something is live. The owner in the source run asked "its deployed
  though, right?"; the answer should already have been in the report.

# Rounds

Step 9, and every owner note. A demo series is rarely finished in one pass: the source run took five rounds over two
days, and five of its notes reversed an earlier one. This file covers reading a note, finding everything it
touches, and reporting a round.

## 1. Read the whole queue first

Notes arrive while you work, as several messages, and not always where you expect them: appended to a tool result
("The user sent a new message while you were working") or queued as attachments. Before writing a plan or a runtime,
and again before rendering, re-read everything since the last render, tool results included. In the source run five
rounds gained a note mid-task (a reference film to study, a pronunciation, an opening that started mid-animation, a
whole new brief, a lockup still wrong in the videos), and a whole stage-only plan was written and discarded within one
turn because a note had already ruled it out. When digesting a past session, extract the queued attachments as well
as the user messages.

When the owner's notes are screenshots saying a page "looks terrible", revise the whole page to the layout budget
(`site.md` §1) rather than patching the pictured sections; the next screenshot is of the section you did not touch.
Before replanning a round, reread the findings for the reference films the owner chose and judge the plan against
their numbers, not only against the gates.

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
  the logo + [product] text is still wrong" sent the fix into the films, and only a URL check found the menu poster
  and the share image still showing the old one.
- **Check the result where the viewer sees it**: a crop of a rendered frame, the live page after deploy, the
  share image itself. A changed stylesheet is not a changed video.
- **A note about one surface covers its twins.** "None of the demos" covers the films, the page's animated demos and
  the posters. When the owner flags an alignment on the site, check the same element in the films: the source run's
  header note ("this alignment is bad") led to the shorts' lockup bar, which had sat off centre and off baseline in
  all nine for two rounds.
- **Before re-voicing a line the owner says is still wrong, compare files**: `shasum` the live file and the local
  one. If they match, the viewer is hearing a cached copy (`site.md` §5) and a re-voice changes nothing.
- **When a value retires, sweep for it**: a colour, a size, a name. `series_lint.py retired --term <old>` over every
  kit, generator, screen builder, page and site build must find nothing before the re-render; the source run's old
  front colour lived in a JS helper, two inline SVG fills and the per-placement CSS.

## 3. Expect reversals, and build for them

Seven reversals from the source run, each answered by a knob that existed before the note, or should have:

| Earlier note | Later note | The knob |
|---|---|---|
| "pick up the pace" | "very fast, … hard to keep track" | the pace factor in the film table |
| narration and captions | "remove the narrator and subtitles", then "with and without voiceover" | picture-first build, muted master plus a remux |
| labels added for clarity | "remove all text that says … illustrative workflow" | the label switch |
| narration-first timing, shorts stretched with `atempo` to 29.9 s | "remove the narrator", then "with and without voiceover" | picture-first scenes, voice at offsets |
| a UK/US spelling switch on the page | "remove the english toggle … just stick to us english" | the English variant, fixed once in `BRIEF.md` |
| a voiced/muted switch on every player | "disable the voice toggle and just have the voice version playing" | the player's source list |
| an "Animated demos" switch on the features page | "remove the animations toggle (which should default to on)" | reduced motion as the only off |

Before building a page-wide switch, ask whether the brief's own setting is what is changing: two of these switches
lived for one round each.

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
  Report loudness from the encoded files only: the WAVs run lower (-2.1 against -1.7 dBTP on the worst file).
- List every scope call under "Calls I made", with what the other reading would have changed ("the longer video"
  applied to the overview only, not the shorts).
- Name every reversal and every claim made on the owner's say-so, so they are decisions on record rather than
  surprises in review.
- Confirm a deploy happened before saying something is live. The owner in the source run asked "its deployed
  though, right?"; the answer should already have been in the report.
- End a republish with a commit that names what changed in the videos, the posters and the share image, with the gate
  lines (`delivery: PASS 10/10`, `urls: PASS 70/70`).
- A round's written record, when one is kept, goes in `REVIEW.md` under: Built; Calls made; Measured; Looked at, not
  measured; Not checked; Weakest shots (with times and the measured text size, which pre-empts the next notes); and
  what would replace them.
- When the repository's own status file holds another session's uncommitted work, write the series' record in the
  series folder and say so.

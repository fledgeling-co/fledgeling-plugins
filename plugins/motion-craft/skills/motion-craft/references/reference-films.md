# Reference films and taste

The strongest single input to a film is a picture of what the user likes. Screenshots of a film or site they admire beat any adjective (qZqZ02AsYiA: "screenshots of what you want animated" were "really powerful"; Cft-TBQv_Y4's best title card came from one screenshot of a website with huge type and floating 3D objects). This file covers three jobs: borrowing a look, borrowing a rhythm, and copying a specific motion.

## 1. Ask for references, then look

In the first message, ask for two to five references: frames, a film, a site, a Pinterest board, a folder of saved screenshots. Never make them a precondition. When there are none and Mobbin's MCP is connected, use `search_sections` or `search_screens` for the closest shipped screens of the subject's category, and once for something deliberately outside it; open the images, never just the titles.

For each reference, write three observations a frame could confirm: how many type sizes are in play, where the focal object sits and what isolates it, how the ground and the accent are used, how dense the frame is, what moves and what holds still. Then one line naming what the references share. That line goes into `SPEC.md` under LOOK, and the direction must answer it or say why it departs.

## 2. Borrow a rhythm: "steal the rhythm, not the footage"

When the user hands over a film whose pacing they want (RSe268YFglA did this with a movie trailer), study its structure and build new content on it. Never copy its footage, copy, logo or signature effect.

```bash
<skill>/scripts/hf.sh measure probe ref/film.mp4 --json            # size, frame rate, duration, sound
<skill>/scripts/hf.sh measure cuts ref/film.mp4 --json > ref/cuts.json   # hard cuts, shots, and fast moves listed apart
<skill>/scripts/hf.sh measure events ref/film.mp4 --json           # appears, disappears, holds, flashes
<skill>/scripts/hf.sh measure curve ref/film.mp4 --help            # one element's move: duration, overshoot, closest GSAP ease
mkdir -p ref/frames && ffmpeg -v error -i ref/film.mp4 -vf "fps=1,scale=320:-2,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x4:padding=4" ref/frames/sheet-%02d.png
```

Use `measure cuts` rather than ffmpeg's scene score: on the owner's reference film the scene score above 0.28 found 11 cuts where the frame-difference measure found 20, because it misses cuts between similar frames. Open every sheet. From them and `cuts.json`, write into `SPEC.md`: the number of hard cuts and their times, the median shot length, where the bursts are, the route (continuous, montage or hybrid), the opening frame, the hero moment's position as a share of the length, how titles enter and how long they hold, and the transitions by type. Build the new film's rhythm sheet to those numbers, and check the sheets for dissolves and whips the cut list reports as fast moves rather than cuts.

When the reference is a YouTube link, download it into a fresh empty folder with `yt-dlp` at 720p or lower; when the download is refused, ask the user for the file or a screen recording and continue with everything else meanwhile.

## 3. Borrow a look

A look is the rules of one medium (`direction.md` §5). From the reference frames, name the medium and its parts (ground, inks, texture, light, type system, corner and rule language) as values, and write them into LOOK. Then design the new subject's own compositions in that medium; the reference's layouts, characters and objects are not a template. A look lifted wholesale with only the nouns swapped is imitation, and for a brand reference it is someone else's trade dress.

## 4. Copy a specific motion exactly

When the user wants one animation reproduced ("make the title do what theirs does"), use reanimate's method (NiazMorshed2007/reanimate, MIT); when the reanimate skill is installed, invoke it by the exact identifier the session lists:

1. Capture the reference frame by frame at a fixed rate (`ffmpeg -vf fps=30` on a video; for a live site, record the element at a fixed viewport).
2. Write a motion spec with one row per element per property: trigger, start, duration, delay or stagger, from → to, easing, and whether it overshoots. Read the easing from the middle frames, not only the first and last.
3. Build it, capture your version with the same size, crop and frame rate, and compare the two side by side at the same timestamps.
4. Change the smallest thing the comparison points at and re-capture. Expect 2-5 rounds; if a row still fails after five, report it with its numbers and the reason rather than lowering the bar.

Motion-faithful is the default (timing within about 80 ms, the same easing family, the same direction and relative distance); pixel-faithful only when the user asks for an exact match.

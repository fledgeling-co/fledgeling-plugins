# Sound

A film over about 15 s that tells something ships with music and sound on its visible actions unless the user asked for silence; most generated motion graphics are silent, and sound is what makes a piece feel produced (claude-motion `sound-design`; cDb-wPq0Iyk shows the same clip with and without). A transparent overlay ships silent.

You cannot hear. Never write that a sound "fits", "lands" or "feels right"; report what you measured (loudness, peak, where each hit sits against its beat) and say that nobody listened.

## 1. Order of work

- **Narrated film: voice first.** The script sets the timing for everything else (explainroo). Write `script.md`, get the voice file (a recording the user gives, or generated speech when the session has a speech tool and the user approved it), get word timings, then tie each picture to the spoken word it illustrates. Word timings come from the speech tool's own timestamps when it returns them, or from a local Whisper run (`whisper --word_timestamps True`, or `faster-whisper`) when one is installed; name which in REVIEW.md. With no timing source, place pictures on sentence boundaries measured from the waveform and say so.
- **Music-led film: tempo first, picture on the grid.** Pick a BPM (100-125 for an energetic launch, 80-100 for calm or ambient), put scene labels on beats, and mark hit points while you animate. Mix the sound after picture lock: changing the animation after sound design moves the sync (cDb-wPq0Iyk tip 6). Marking cues during animation and mixing after lock are compatible: the cue sheet reads the same timeline file, so a retime moves the sound with it.
- **Supplied track**: find its beats and drop with a beat tracker (librosa's `beat_track` when installed; otherwise ask the user for the BPM and the drop time), then lay the picture's grid on it and put the hero moment on the drop.
- **Voiceover written to a finished cut**: when the picture is locked at a fixed length (a 15 s or 30 s spot), write the voiceover to fit that length rather than generating speech first and hoping (cDb-wPq0Iyk tip 10).

## 2. The bundled sound engine

`scripts/sfx/` is claude-motion's procedural sound engine (MIT, by whaleyxbt; licence in `scripts/sfx/LICENSE-claude-motion.txt`): pure Python standard library, no samples, no licences to clear, identical output on every run, mastered automatically to a loudness target.

```bash
cd <skill>/scripts && python3 -m sfx --list            # the generators and what each is for
PYTHONPATH=<skill>/scripts python3 -m sfx <project>/sound/cues.py \
  --timeline <project>/timeline.json --out <project>/assets/sound.wav
```

A cue sheet is a Python file with a `score(mix, tl)` function; every time in it comes from the timeline file, never a typed number, so retiming the picture retimes the sound. `scripts/sfx/cues/example_effort.py` is a complete real example (129 sounds and a pad bed). The essentials:

```python
from sfx.synth import whoosh, pop, chime, impact, riser, pad, envelope

TARGET_LUFS = -14.0

def score(mix, tl):
    s = tl["scenes"]
    mix.put(s["hook"]["title"], whoosh(0.4, 500, 2400, peak=0.45), 0.12)
    for i, t in enumerate(s["proof"]["steps"]):
        mix.put(t, pop(900 + i * 150, 400), 0.3, pan=-0.4 + i * 0.3)
    mix.put(s["payoff"]["hit"] - 1.0, riser(1.0), 0.2)
    mix.put(s["payoff"]["hit"], impact(), 0.32)
    mix.typing(s["proof"]["typeStart"], s["proof"]["typeEnd"], chars=28)
```

`timeline.json` must carry a top-level `"duration"` in seconds; the rest of its shape is yours, as long as the composition and the cue sheet read the same keys.

## 3. Which event gets which sound

| On screen | Generator | Notes |
|---|---|---|
| Typing | `mix.typing()` | humanised per keystroke |
| Word or line reveal | `whoosh()`, `blip()` on the landing | short and airy |
| Badge, chip or card pops in | `pop()` | raise the pitch across a sequence |
| Control snaps to a step | `click()` + `blip()` in key | |
| Sketch or draw-on | `scratch()` | |
| Build-up | `riser()` | ends exactly on the hit; one big riser per film |
| Success or arrival | `chime()` | a chord in the film's key |
| Hero transition | `whoosh()` in, `impact()` on the hit | one impact per film |
| Montage cut | a short hit or tick per cut | gives the burst weight |
| Under everything | `pad()` with an `envelope()` | duck it about 65 % under the hero transition |

Accent, do not narrate: continuous motion (drift, grain, rotation) stays silent. Aim for a hit on every landing that matters, roughly 8-15 in 30 s (huashu-motion). Levels: hero hits gain 0.25-0.35, supporting sounds 0.08-0.2, the pad about 0.03. Pan follows on-screen position (−1 left to +1 right). Keep every tonal sound in one key, rising with progress and resolving on the payoff.

Three rules from motlab's mixer and earshot's launch kit keep a dense cue sheet from smearing:

- **Spacing**: ticks at least 66 ms apart, keystrokes 87 ms, pops 114 ms; closer than that they blur into one sound.
- **Variation**: a repeated sound climbs in pitch across its run (0.90, 1.00, 1.10, 1.20) and alternates pan; never the same file or generator settings five times in a row.
- **A bed in three layers**: two to four quiet beds (a soft tonal pad, a high airy layer, a faint texture) that lift towards the reveal; soft whooshes 26-33 dB below full scale under camera and object moves; then the hits.

## 4. Recorded effects

Recorded effects sound richer than synthesized ones, and the best-received long prompts on prompt-motion.com ask for "a downloaded SFX for every event, never synthesized, each placed by its measured peak". Use them when the user has a sound library, or when the film will be published and the engine's sounds read as plain:

- **Source**: the user's own library first; otherwise openly licensed sounds, CC0 from Openverse (`https://api.openverse.org/v1/audio/?q=soft+whoosh&license=cc0`) or a library whose licence allows commercial use. Record each file's source and licence in `materials.md`; CC BY needs a credit line.
- **Anchor each sound on its beat by the right point.** A struck sound (a click, a pop, a hit) goes on at the moment it becomes audible, past the 30-150 ms of near silence most library files start with; a whoosh at its loudest point, in the middle of the move; a riser at its end, on the reveal. Placing a file by its first sample makes it sound late.
- **Levels by role**, as the cue's peak in dBFS (Clipwing's real-sfx levels, via motlab): hit −4, whoosh −9, riser −12, click, UI, pop, tap, keystroke and tick −14, ambience −24.
- Place them from the cue sheet with `scripts/sfx/samples.py`: `place(mix, t, load("sound/sfx/click.wav"), anchor="onset", peak_db=-14)` (anchor `"peak"` for a whoosh, `"end"` for a riser). The same `timeline.json` times them and the engine still masters to −14 LUFS; convert other formats first with `ffmpeg -i in.mp3 -ac 1 -ar 48000 out.wav`. On a test sheet, three clicks with 120 ms of silence at the head of the file measured onsets at 0.495, 1.495 and 2.495 s against cues at 0.5, 1.5 and 2.5 s.

## 5. Music beyond the engine

The engine makes effects and beds, not songs. For a full music track:

- a track the user supplies (mix it under the effects; place the drop on the hero moment);
- a track generated by a music tool the session has (Suno, ElevenLabs music), only with the user's approval because these are paid: ask for the exact length in seconds and the BPM in the prompt so it fits the cut (cDb-wPq0Iyk);
- licensed sound-effect packs the user owns, placed by filename on the timeline.

Record each track's source and licence in `materials.md`.

## 6. Loudness and delivery

- Social and web masters: integrated −14 LUFS ±1, true peak ≤ −1 dBTP. Shipped product films do not reliably meet this: of 48 measured on 2026-11-16, 15 sit within ±1 LU of −14, the median is −15.8 LUFS, and 18 exceed the true-peak ceiling (`saas-films.md` §9). Master to the spec rather than to a reference film. The engine masters to −14 LUFS with the true peak at or under −2 dBFS, leaving room for AAC overshoot.
- **When the renderer lowers the mix.** If the render log says `Audio lowered by N dB to stay under −1 dBTP`, one transient, usually an impact or a sharp click, overshoots once the score is encoded to AAC, and the renderer turns the whole film down to protect the ceiling. Lower that one cue and render again rather than shipping a quiet master: on one film an impact at gain 0.30 cost 3.5 dB across the mix (−17.5 LUFS), and at 0.18 the film rendered at −14.0 with nothing lowered. Find the cue by encoding `assets/sound.wav` to AAC and reading the true peak one second at a time.
- A mix of mostly short hits with silence between cannot reach −14 LUFS without crushing; add sustained sound (a pad, longer tails) rather than forcing the gain. The engine says when it came out quieter.
- Place the mastered WAV in the composition so the render carries it: `<audio id="score" class="clip" src="assets/sound.wav" data-start="0" data-duration="<film length>" data-volume="1"></audio>` inside the root of `index.html`. A voice file is a second `<audio>` with its own `id`. Check the rendered file has an audio stream (`ffprobe -v error -show_entries stream=codec_type -of csv=p=0 out/<name>.mp4` prints `audio`); a render whose `<audio>` tag is missing or malformed comes out silent with no error.

## 7. Checking sound you cannot hear

1. Loudness of the file you will actually deliver: the same `hf.sh audio` JSON carries `loudness.lufsIntegrated` and `loudness.truePeakDb`; quote both. Without HyperFrames, `ffmpeg -hide_banner -i film.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12` gives the same two numbers.
2. Sync: `<skill>/scripts/hf.sh audio out/<name>.mp4 --json` lists the onsets (`onsets.events[].t`) and loudness of the rendered file. Compare each hero onset with its beat in `timeline.json`: a transient more than 2 frames early, or more than 100 ms late, is a note, and a hit between beats means a hardcoded time or a stale WAV. Measured on a test film, three cues at 0.30, 1.40 and 3.20 s produced onsets at 0.310, 1.395 and 3.195 s.
3. A spectrogram for the eye: `ffmpeg -i assets/sound.wav -lavfi showspectrumpic=s=1600x400 out/spectrum.png`, then open it and check that the hits are where the beat map says and nothing masks the voice.
4. When the earshot tool is installed (Leonxlnx/earshot), use its `timeline` and `critique` commands for a listening transcript and per-cut sync; quote its numbers.

REVIEW.md always carries the line "sound measured, not heard".

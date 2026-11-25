# Voice and music

Steps 3 and 5. The words come from the brand's voice skill; this file covers the register a demo series needs, how
the audio is made through Vercel AI Gateway, and how it is mixed through motion-craft's sound engine.

## 1. The narration register

- **Second person, active, outcome first.** "You can …", "Your … is ready", "Draft responses checked against what
  you have already said". The owner in the source run asked for exactly this after a round of third-person
  description.
- **The picture carries the specifics.** Names, figures, times and which assistant is open are on screen; the
  narration does not repeat them. A line that reads out what the frame already shows spends the viewer's attention
  twice.
- **Budgets.** The overview: at most 130 spoken words, roughly half what a first draft runs to. A short: one line
  of 24-34 words, about 10-13 s, placed so it ends before the result's hold does.
- **Claims.** Nothing beyond `CLAIMS.md`. No percentages, no timing claims unless measured, no rule or compliance
  findings the product's record does not support for that market.
- **Delivery tags.** ElevenLabs v4 reads a leading tag such as `[upbeat]` as direction, not words. In the source
  run Scribe transcribed 27 tagged lines and found 0 tags spoken. Keep tags in `lines.json`; `gateway_audio.py`
  strips them from the caption text it records.

## 2. Choosing the voice

Audition three or four voices on the lead line, in the accent the audience expects, and let the user pick by
listening. Record the voice id in `lines.json`. ElevenLabs keys may lack the `voices_read` permission; pick by known
voice ids and audition through the gateway instead.

## 3. Generating the lines

Export the key without echoing it. From a dotenv file:

```bash
set -a; . <(grep -E '^AI_GATEWAY_API_KEY=' .env.local); set +a
python3 scripts/gateway_audio.py lines --script lines.json --out-dir voice --respell respell.json
python3 scripts/gateway_audio.py lines --script lines.json --out-dir voice --respell respell.json --only K03
```

Per line it writes the MP3, a 48 kHz mono WAV for the sound engine, word timings from Scribe v2, and a cache key.
A re-run regenerates only lines whose spoken text, voice or model changed, and prints the characters sent and the
cost. The source run's re-voice of 18 lines sent 1,653 characters, about US$0.13.

## 4. Placing the lines

- Each line sits at `[line, scene, offset]` in the film table. Choose the offset by the frame it describes: the
  line about the citation starts as the citation lands, not when its scene starts. The owner's note in the source
  run, "what the narrator says doesn't line up with what's on screen", was fixed by moving four offsets between
  0.7 s and 3.55 s, with no picture change.
- After any pace change, re-check every line's span against its scene: a line must end before its scene does.
- Word timings let a beat reference a word (`o3.word:figures+0.2`). A beat naming a word the line does not contain
  fails the build, which is the check doing its job.

## 5. Music beds

One bed per family: one at the overview's length and one at the shorts' length, which each short cuts to its own
length and fades. Write the prompt for the audience, and keep it instrumental with room for a voice. The prompt
that served a finance audience in the source run:

> Instrumental background music for a product film made for investor relations professionals and chief financial
> officers. Calm, confident and modern: a warm felt piano motif, soft analog synth pads, a gentle pulsing bassline
> and light, crisp electronic percussion with brushed textures, around 100 BPM in a major key. Quietly optimistic
> and focused. Steady energy with no big drops, no risers, no vocals and no choir, leaving space for a narrator.

Add the shape per bed: for the overview "opens softly, settles into a steady groove by fifteen seconds, and resolves
on a warm, simple chord in the final eight seconds"; for the shorts "starts already moving … resolves in the final
four seconds".

```bash
python3 scripts/gateway_audio.py music --prompt "$(cat bed-overview.txt)" --seconds 106 --out music/overview.mp3
```

music-v2.5 costs about US$0.0025 a second, so two beds of 106 s and 27 s cost about US$0.33. Show that and wait
for a yes before generating.

## 6. The mix

Score through motion-craft's sound engine (`PYTHONPATH=<motion-craft>/scripts python3 -m sfx cues.py --timeline
timeline.json --out assets/sound.wav`). Each film gets two mixes from the same cue sheet:

- **`sound.wav`, for the muted master**: the bed at 0.28 throughout, plus effects.
- **`sound_vo.wav`, for the voiced cut**: the bed ducked to 0.10 under each line by `scripts/duck.py`, the voice
  at full level, plus the same effects.

```python
from duck import duck_points, gain_at          # scripts/duck.py, on PYTHONPATH
pts = duck_points([(l['start'], l['end']) for l in lines], duration)
gain = [gain_at(pts, i / SR) for i in range(n)]
```

Those levels put the voice about 11 dB over the bed. At the first mix in the source run the bed sat at full level
and the voice was about 1 dB over it. Effects come from beat-name prefixes: `pop_` for a card landing, `click_` for
a press, `whoosh_` for a change of world, `chime_` for a check passing, `rise_` into a beat. Leave out typing sounds:
one owner called them out as noise. Master both mixes to -14 LUFS with true peak at or below -1 dBTP;
`delivery.py check` measures it on the finished files.

## 7. What the numbers cannot tell you

Loudness, peak and duck depth say nothing about whether the music suits the product, whether a name is said
right, or whether the voice sounds bored. Say in every report whether anyone listened at full speed on speakers,
and who.

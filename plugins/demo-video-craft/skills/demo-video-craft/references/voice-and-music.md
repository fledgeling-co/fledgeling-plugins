# Voice and music

Steps 3 and 5. The words come from the brand's voice skill; this file covers the register a demo series needs, how
the audio is made through Vercel AI Gateway, and how it is mixed through motion-craft's sound engine.

## 1. The narration register

- **Second person, active, outcome first.** "You can …", "Your … is ready", "Catch the figure that doesn't match before
  your CFO says it on the call." The owner in the source run asked for exactly this after a round of third-person
  description. With a real client on screen, the possessive works: "your client's outlook".
- **The picture carries the specifics.** Names, figures, times and which assistant is open are on screen; the line
  does not repeat them. Each line names the on-screen card that proves it; a line with no card is cut or reworded.
  Give the voice skill each short's full picture list, so the line describes the outcome rather than the screen.
- **Budgets.** The overview: at most 130 spoken words, about nine lines of 15-21 words. A short: one line of 24-35
  words (the source run's last round ran 31-35 words, 9.6-12.0 s), placed 0.5-3 s in so it ends well before the
  result's hold does. ElevenLabs v4 speaks 155-177 words a minute with about 0.10 s of silence before speech and
  0.18 s after, so 130 words is about 50 s and 30 words about 11 s. Expect a first draft at about four times the
  budget.
- **Read the brand lint's advisories as spoken-register signals.** A contraction rate or sentence-length variance far
  outside the corpus band (3.97 against 1.36 in round 1) is how a script sounds read aloud; fix it before paying for
  the voice.
- **Claims.** Nothing beyond `CLAIMS.md`. No percentages, no timing claims unless measured, no rule or compliance
  findings the product's record does not support for that market.
- **Delivery tags.** ElevenLabs v4 reads a leading tag such as `[upbeat]` as direction, not words. In the source run
  Scribe transcribed 27 tagged lines and found 0 tags spoken. Keep tags in `lines.json`; `gateway_audio.py` strips them
  from the caption text it records.

## 2. Choosing the voice

The owner picks the voice by listening; the agent picks none. Audition three or four voices on the lead line, in the
accent the audience expects, and hand over the files to play. The source run's voice, the first one to audition
for a US finance audience: `cgSgspJ2msm6clMCkdW9` on `elevenlabs/eleven-v4`, with `[upbeat]` on the short lines.
ElevenLabs keys may lack `voices_read`; audition by known voice ids through the gateway.

A series without `gateway_audio.py` reaches the same models: speech is `POST https://ai-gateway.vercel.sh/v4/ai/speech-model`
with headers `ai-gateway-protocol-version: 0.0.1`, `ai-speech-model-specification-version: 4` and `ai-model-id`, body
`{text, voice, outputFormat: "mp3"}`, base64 `audio` back; word timings are `/v4/ai/transcription-model` with
`elevenlabs/scribe-v2`; music is the speech endpoint with `elevenlabs/music-v2.5` and
`providerOptions.elevenlabs.{musicLengthMs, forceInstrumental}`.

## 3. Generating the lines

Find the key by its variable name without printing it, then check the balance and the price before scripting:

```bash
grep -rl --include='.env*' '^AI_GATEWAY_API_KEY=' . 2>/dev/null      # which files hold it; the value is never printed
set -a; . <(grep -E '^AI_GATEWAY_API_KEY=' <that file>); set +a
curl -s https://ai-gateway.vercel.sh/v1/credits -H "Authorization: Bearer $AI_GATEWAY_API_KEY"    # the balance
python3 scripts/gateway_audio.py lines --script lines.json --out-dir voice --respell respell.json [--only K03]
```

Per line it writes the MP3, a 48 kHz mono WAV, word timings from Scribe v2 and a cache key, regenerates only lines
whose spoken text, voice or model changed, and prints the characters and the cost. On 24-25 Nov 2026: speech US$0.08
per 1,000 characters, Scribe US$0.000061 a second, music US$0.0025 a second; `GET /v1/models` lists the current ids
and prices. A nine-line re-voice of shorts cost about US$0.14.

- **Respell for the voice's accent.** The owner's "clord" is non-rhotic; a US voice says every r it is given, so
  "Clord" became "Clawd". Order rules specific first ("Diolog Guardian" → "Dialogue's Guardian" before "Diolog" →
  "Dialogue").
- **Read the brand name back from Scribe's words** and flag where it merges with what follows: Scribe heard a
  possessive as "Dialogues view". Scribe writes back what it expects to hear, so it cannot confirm a pronunciation;
  ask for a listen of one line per respelling and record who listened.
- **Fit narration with `atempo` at most 1.08**, set per film as `tempo`; `build.py` divides the word timings by the
  same factor. Past that, shorten the line.

## 4. Placing the lines

- Each line sits at `[line, scene, offset]`. Choose the offset by the frame it describes: the line about the citation
  starts as the citation lands. Offsets scale with the scene's pace factor; the narration's tempo does not.
- **When a line outruns the frame it describes, lengthen that scene's hold**, not only the offset. The owner's "what
  the narrator says doesn't line up with what's on screen" was fixed by moving four offsets (0.7-3.55 s) and growing
  the overview's intro from 8.6 to 11.5 s so the headline holds until its line ends.
- `build.py` fails when a line starts within 0.2 s of the previous line's end, runs more than 0.1 s past the end of
  its scene (the source run accepted one at 0.09 s, with the next line well clear), or ends within 0.6 s of the film's
  end.
- **Read the sync table and the alignment sheet** after any pace change, scene insert or new offset, before the owner
  watches: `sync_table.py films/<id>` prints each line beside the on-screen events inside it, and `delivery.py sheet
  --file <id>-vo.mp4 --lines films/<id>/timeline.json` gives one frame 1 s into each line, stamped, to open.

## 5. Music beds

One bed per family: one at the overview's length and one at the shorts' length, which each short cuts to its own
length and fades. Write the prompt for the audience, instrumental with room for a voice. The prompt that served a
finance audience in the source run:

```text
Instrumental background music for a product film made for investor relations professionals and chief financial
officers. Calm, confident and modern: a warm felt piano motif, soft analog synth pads, a gentle pulsing bassline
and light, crisp electronic percussion with brushed textures, around 100 BPM in a major key. Quietly optimistic
and focused, polished like a financial technology brand film. Steady energy with no big drops, no risers, no vocals
and no choir, leaving space for a narrator.
```

Add the shape per bed: for the overview "opens softly, settles into a steady groove by fifteen seconds, and resolves
on a warm, simple chord in the final eight seconds"; for the shorts "starts already moving … resolves in the final
four seconds". Two beds of 106 s and 27 s cost about US$0.33; show that and wait for a yes.

```bash
python3 scripts/gateway_audio.py music --prompt "$(cat bed-overview.txt)" --seconds 106 --out music/overview.mp3
ffmpeg -i music/overview.wav -af ebur128=metadata=1,ametadata=print:key=lavfi.r128.S -f null - 2>&1 | grep r128.S | awk 'NR%30==1'
```

Nobody has heard a new bed, so read its short-term loudness every 3 s (the second command): find gaps and dips, and
check the decay lands inside the end slide (the source's overview bed fell from -17 to -44 LUFS over its last 6 s, on
the slide). When the owner declines paid music, the fallback is a procedural bed from motion-craft's synth: 112 BPM,
I-V-vi-IV, drums entering after two bars, silent over the last 1.2 s.

## 6. The mix

`build.py` writes a cue sheet per film that motion-craft's sound engine renders twice from the same beats:

- **`sound.wav`, for the muted master**: the bed at 0.28 throughout, plus effects.
- **`sound_vo.wav`, for the voiced cut**: the bed ducked to 0.10 under each line by `scripts/duck.py`, the voice at
  full level, the same effects.

`duck.py`'s constants: the dip starts 0.25 s before a line over a 0.3 s ramp, holds to 0.35 s after it and recovers
over 0.6 s; two lines under 0.9 s apart share one dip, or the bed swells between them; the bed fades in over 0.25 s and
out over the last 1.6 s. Those levels are an 8.9 dB duck (20 log10 of 0.28 / 0.10) and put the voice about 11 dB over
the bed; the first mix with the paid beds, 0.55 ducked to 0.30 (5.3 dB), left the voice about 1 dB over it. Compute
the depth from the curve before mixing and keep it at 8.5 dB or more.

**Measure the separation, not the mix.** At the source run's first mix the integrated loudness of the mixed file
looked normal (-14.1 against -13.5 for the bed alone) while the voice sat 1 dB over the bed; only measuring the voice
WAV alone and the bed slice times its gain with `ebur128` showed it. Effects come from beat prefixes: `pop` for a card
landing, `click` for a press, `whoosh` for a change of world, `chime` for a check passing. Leave out typing sounds:
one owner called them noise.

Master both mixes to -14 LUFS with true peak at or below -1 dBTP, and measure on the encoded files: motion-craft masters
to a -2.0 dB ceiling, and the AAC encode still added up to 0.9 dB, once taking a -2.4 dBTP mix to +1.3 dBTP.
`delivery.py remux --limit 0.6` puts a limiter ahead of the encoder (that file then measured -3.5 dBTP at -14.3 LUFS);
record which films need it in `SERIES.md`, because the next re-render needs it again.

## 7. What the numbers cannot tell you

Loudness, peak and duck depth say nothing about whether the music suits the product, whether a name is said right, or
whether the voice sounds bored. Say in every report whether anyone listened at full speed on speakers, and who.

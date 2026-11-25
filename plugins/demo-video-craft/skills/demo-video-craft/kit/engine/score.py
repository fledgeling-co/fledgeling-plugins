"""The film's score: the series' music bed, ducked beneath the narration when the timeline carries lines (the voiced
cut) and at full bed level when it does not (the muted master), with soft effects on named beats and a whoosh at each
change of scene. Every time comes from timeline.json, which build.py writes. Run by motion-craft's sound engine:

    PYTHONPATH=<motion-craft>/scripts python3 -m sfx films/<id>/sound/cues.py --timeline timeline.json --out sound.wav

Beat names pick their sound by prefix: pop_* (a card lands), click_* (a press), whoosh_* (a change of world),
chime_* (a check passing or a figure fixed). No typing sound: an owner called it noise.

The bed is series.json "beds": a WAV path per family (the ElevenLabs bed gateway_audio.py music writes), "procedural"
for the no-spend groove below (the source series' round 2 bed: 112 BPM, I-V-vi-IV in D, a soft kick, offbeat hats, a
backbeat clap, a picked bass and a plucked arpeggio over a pad, drums from bar 3, silent over the last 1.2 s), or null
for effects only.
"""
import math
import random
import struct
import wave
from pathlib import Path

from duck import BED, duck_points, gain_at
from sfx.dsp import saw, svf
from sfx.samples import load
from sfx.synth import SR, chime, click, envelope, pad, pop, whoosh

TARGET_LUFS = -14.0
POPS = [880.0, 987.77, 1108.73, 1174.66, 1318.51]
BPM = 112.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
PROG = [[146.83, 220.0, 293.66, 369.99], [110.0, 164.81, 220.0, 277.18], [123.47, 185.0, 246.94, 293.66], [98.0, 146.83, 196.0, 246.94]]
ROOTS = [73.42, 55.0, 61.74, 49.0]                  # D2 A1 B1 G1
_rng = random.Random(7)


def _kick():
    n, out, ph = int(0.26 * SR), [], 0.0
    for k in range(n):
        t = k / SR
        ph += 2 * math.pi * (48 + 110 * math.exp(-t / 0.035)) / SR
        out.append(math.sin(ph) * math.exp(-t / 0.11) * min(1, t / 0.002))
    return out


def _noise_hit(dur, fc, tau, mode='hp'):
    return svf([(_rng.random() * 2 - 1) * math.exp(-(k / SR) / tau) for k in range(int(dur * SR))], fc, q=0.8, mode=mode)


def _pluck(freq, dur, cutoff, tau):
    n = int(dur * SR)
    env = [math.exp(-(k / SR) / tau) * min(1, k / (0.004 * SR)) for k in range(n)]
    return svf([a * b for a, b in zip(saw(freq, n), env)], lambda k: cutoff * (0.35 + 0.65 * math.exp(-(k / SR) / (tau * 0.6))), q=0.9)


def procedural_bed(mix, dur, pts):
    """The no-spend groove, ducked by the same curve as a paid bed (pts from duck_points)."""
    put = mix.put
    g = lambda t: gain_at(pts, t) / BED            # noqa: E731  1.0 between lines, about 0.36 under the voice
    end = dur - 1.2
    chords = [(i * BAR, PROG[i % 4]) for i in range(int(end / BAR) + 1)] + [(end, PROG[0])]
    vol = envelope(sorted([(0.0, 0.0), (0.5, 0.9), (max(0.6, dur - 1.9), 0.8), (end, 0.0), (dur, 0.0)]))
    mix.put_stereo(0, *pad(dur, chords, volume=vol, tremolo=0.12), gain=0.035)
    kick, hat, clap, bass, plk = _kick(), _noise_hit(0.05, 7500, 0.012), _noise_hit(0.16, 1600, 0.045, mode='bp'), {}, {}
    beat_i, t = 0, 0.0
    while t < end:
        bar, pos = divmod(beat_i, 4)
        chord, root, gg = PROG[bar % 4], ROOTS[bar % 4], g(t)
        if t >= 2 * BAR:
            put(t, kick, 0.30 * gg)
            put(t + BEAT / 2, hat, 0.05 * gg, -0.25 if beat_i % 2 else 0.25)
            if pos in (1, 3):
                put(t, clap, 0.09 * gg, 0.1)
        for off in ((0,) if pos in (0, 2) else (0, 0.5)):
            if t + off * BEAT < end and t >= BAR:
                f = root * (2 if (pos == 3 and off) else 1)
                bass.setdefault(f, _pluck(f, 0.32, 520, 0.16))
                put(t + off * BEAT, bass[f], 0.20 * gg)
        for half in (0, 1):
            note = (chord + [chord[1] * 2, chord[2] * 2])[[1, 2, 3, 4, 3, 2][(pos * 2 + half) % 6]] * 2
            plk.setdefault(note, _pluck(note, 0.28, 3400, 0.09))
            put(t + half * BEAT / 2, plk[note], 0.045 * gg * (0.6 if t < 2 * BAR else 1.0), -0.4 if half else 0.4)
        beat_i += 1
        t = beat_i * BEAT


def _stereo(path):
    with wave.open(str(path), 'rb') as w:
        if w.getnchannels() != 2 or w.getsampwidth() != 2 or w.getframerate() != SR:
            raise SystemExit(f'{path} must be 16-bit stereo at {SR} Hz (gateway_audio.py music writes one)')
        raw = w.readframes(w.getnframes())
    vals = struct.unpack('<%dh' % (len(raw) // 2), raw)
    return [v / 32768.0 for v in vals[0::2]], [v / 32768.0 for v in vals[1::2]]


def score(mix, tl):
    dur, put = tl['duration'], mix.put
    lines = sorted(tl['lines'].items(), key=lambda kv: kv[1]['start'])
    for lid, ln in lines:
        put(ln['start'], load(str(Path(tl['voiceDir']) / f'{lid}.wav')), 1.0)

    pts = duck_points([(ln['start'], ln['end']) for _, ln in lines], dur)
    if tl.get('bed') == 'procedural':
        procedural_bed(mix, dur, pts)
    elif tl.get('bed'):
        left, right = _stereo(tl['bed'])
        n = min(len(left), int(dur * SR))
        g = [gain_at(pts, i / SR) for i in range(n)]
        mix.put_stereo(0, [left[i] * g[i] for i in range(n)], [right[i] * g[i] for i in range(n)], gain=1.0)

    starts = sorted(v['start'] for v in tl['scenes'].values())
    for i, s in enumerate(starts[1:]):
        put(max(0, s - 0.12), whoosh(0.45, 600, 2800, peak=0.5), 0.04, -0.3 + 0.2 * (i % 4))
    npop = 0
    for name, tt in sorted(tl['beats'].items(), key=lambda kv: kv[1]):
        if name.startswith('pop'):
            put(tt, pop(POPS[npop % len(POPS)], POPS[npop % len(POPS)] * 0.5), 0.07, 0.1)
            npop += 1
        elif name.startswith('click'):
            put(tt, click(2000), 0.11)
        elif name.startswith('whoosh'):
            put(tt, whoosh(0.45, 600, 2800, peak=0.5), 0.04)
        elif name.startswith('chime'):
            put(tt, chime([739.99, 880.0, 1108.73], dur=1.6, tau=0.55), 0.06)

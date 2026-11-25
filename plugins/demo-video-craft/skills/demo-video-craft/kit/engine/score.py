"""The film's score: the series' music bed, ducked beneath the narration when the timeline carries lines (the voiced
cut) and at full bed level when it does not (the muted master), with soft effects on named beats and a whoosh at each
change of scene. Every time comes from timeline.json, which build.py writes. Run by motion-craft's sound engine:

    PYTHONPATH=<motion-craft>/scripts python3 -m sfx films/<id>/sound/cues.py --timeline timeline.json --out sound.wav

Beat names pick their sound by prefix: pop_* (a card lands), click_* (a press), whoosh_* (a change of world),
chime_* (a check passing or a figure fixed). No typing sound: an owner called it noise.
"""
import struct
import wave
from pathlib import Path

from duck import duck_points, gain_at
from sfx.samples import load
from sfx.synth import SR, chime, click, pop, whoosh

TARGET_LUFS = -14.0
POPS = [880.0, 987.77, 1108.73, 1174.66, 1318.51]


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

    if tl.get('bed'):
        left, right = _stereo(tl['bed'])
        n = min(len(left), int(dur * SR))
        pts = duck_points([(ln['start'], ln['end']) for _, ln in lines], dur)
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

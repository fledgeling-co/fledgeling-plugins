#!/usr/bin/env python3
"""The music bed's gain curve: full between narration lines, ducked under each one, faded at both ends.

    from duck import duck_points, gain_at          # in a motion-craft sound/cues.py
    duck.py --spans 2.9:14.2,16.0:20.5 --duration 23.2      # prints the (time, gain) points as JSON
    duck.py --self-test

The defaults are the levels measured on a delivered series: bed 0.28, ducked to 0.10 under the voice, which put the
narration about 11 dB over the bed (-23 against -34 LUFS before mastering). At the first mix the bed sat at full
level and the voice was only about 1 dB over it. The muted master uses the same bed with no spans, so it plays at
0.28 throughout.

The dip starts 0.25 s before a line and recovers 0.35 s after it over 0.6 s, so the bed never swells between two
lines closer than about a second. The bed fades in over 0.25 s and out over the last 1.6 s.
"""
import json
import sys

BED, UNDER_VOICE = 0.28, 0.10


def duck_points(spans, duration, bed=BED, under=UNDER_VOICE, lead=0.25, tail=0.35, recover=0.6, fade_in=0.25,
                fade_out=1.6):
    """(time, gain) points for a piecewise-linear curve. spans: [(start, end)] of narration, in film seconds."""
    # Two lines closer than a full dip-and-recover share one dip; otherwise the bed creeps back up under the first.
    merged = []
    for a, b in sorted((s - lead, e + tail) for s, e in spans):
        if merged and a - merged[-1][1] < recover + 0.3:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    end = duration - 0.05
    pts = [(0.0, 0.0), (fade_in, bed)]
    for a, b in merged:
        a = max(a, fade_in + 0.35)
        pts += [(a - 0.3, bed), (a, under), (b, under), (b + recover, bed)]
    pts = [p for p in pts if p[0] < end]
    if pts[-1][0] < duration - fade_out:
        pts.append((duration - fade_out, pts[-1][1]))
    pts.append((end, 0.0))
    return pts


def gain_at(points, t):
    if t <= points[0][0]:
        return points[0][1]
    for (t0, g0), (t1, g1) in zip(points, points[1:]):
        if t0 <= t <= t1:
            return g0 if t1 == t0 else g0 + (g1 - g0) * (t - t0) / (t1 - t0)
    return points[-1][1]


def self_test():
    spans = [(2.9, 14.2), (15.0, 20.5)]
    p = duck_points(spans, 23.2)
    cases = [
        ('ducked in the middle of a line', abs(gain_at(p, 8.0) - UNDER_VOICE) < 1e-9),
        ('no swell in a 0.8 s gap between lines', gain_at(p, 14.6) <= UNDER_VOICE + 0.06),
        ('full bed before the first line', abs(gain_at(p, 1.5) - BED) < 1e-9),
        ('silent at the very end', gain_at(p, 23.2) == 0.0),
        ('silent at frame 0', gain_at(p, 0.0) == 0.0),
        ('the muted master stays at full bed', abs(gain_at(duck_points([], 23.2), 10.0) - BED) < 1e-9),
        ('times only increase', all(a[0] < b[0] for a, b in zip(p, p[1:]))),
    ]
    failed = [n for n, ok in cases if not ok]
    print(f'self-test: {len(cases) - len(failed)}/{len(cases)} passed' +
          (f'; failed: {", ".join(failed)}' if failed else ''))
    sys.exit(1 if failed else 0)


def main():
    a = sys.argv[1:]
    if '--self-test' in a:
        self_test()
    if '--spans' in a and '--duration' in a:
        raw = a[a.index('--spans') + 1]
        spans = [tuple(float(x) for x in s.split(':')) for s in raw.split(',') if s]
        print(json.dumps(duck_points(spans, float(a[a.index('--duration') + 1]))))
        return
    print(__doc__.split('\n\n')[0], file=sys.stderr)
    sys.exit(2)


if __name__ == '__main__':
    main()

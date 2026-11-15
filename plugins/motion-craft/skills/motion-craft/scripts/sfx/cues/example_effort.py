"""Sound design for EffortVideo. Every time comes from timeline.json.

    python3 -m sfx sfx/cues/effort.py
"""

from sfx.synth import blip, chime, click, envelope, impact, pad, pop, riser, scratch, whoosh

TIMELINE = "timeline.json"
OUT = "public/sfx.wav"
TARGET_LUFS = -14.0

PROMPT_1 = "redesign the /config menu"
PROMPT_2 = "build an HTML sanitizer"

# D major: the bed moves from Dmaj7(add9) to D6/9 on the iris hit.
BED_A = [146.83, 220.0, 293.66, 369.99, 554.37]
BED_B = [146.83, 220.0, 293.66, 440.0, 587.33, 739.99]
STEP_NOTES = [659.25, 739.99, 880.0, 987.77]
POP_NOTES = [1046.5, 1318.5, 1568.0, 2093.0]


def score(mix, tl):
    s1, s2, s3, s4 = tl["s1"], tl["s2"], tl["s3"], tl["s4"]
    dur = tl["duration"]
    put = mix.put

    duck, lift = s4["merge"], s4["irisOut"]
    volume = envelope([
        (0, 0), (1.4, 1), (duck, 1), (duck + 0.3, 0.35),
        (lift, 0.35), (lift + 0.5, 1.15), (dur - 1.2, 1.15), (dur, 0),
    ])
    mix.put_stereo(0, *pad(dur, [(0, BED_A), (lift, BED_B)], volume=volume), gain=0.028)

    # scene 1: title, prompt bar, typing, flip
    put(s1["spark"], chime([1318.5, 1975.5, 2637.0], dur=1.6, tau=0.5), 0.10)
    put(s1["spark"], whoosh(0.9, 200, 1400, peak=0.3), 0.10)
    for i, w in enumerate([s1["line1"], s1["line1"] + 0.09, s1["line2"], s1["line2"] + 0.09]):
        put(w, whoosh(0.28, 500, 2400, peak=0.45), 0.10, -0.3 + i * 0.2)
        put(w + 0.12, blip(98 if i < 2 else 110, dur=0.3, tau=0.08), 0.22)
    put(s1["bar"], pop(420, 180), 0.25)
    put(s1["sparkDock"], whoosh(0.5, 2600, 700, peak=0.5), 0.12, -0.4)
    put(s1["sparkDock"] + 0.48, click(2400), 0.18, -0.5)
    mix.typing(s1["typeStart"], s1["typeEnd"], len(PROMPT_1))
    put(s1["exit"], whoosh(0.42, 600, 3200, peak=0.4), 0.16)
    put(s1["flipStart"], whoosh(s1["flipEnd"] - s1["flipStart"], 400, 2200, peak=0.55), 0.2, 0.2)

    # scene 2: sketch draws on, slider notches through every level
    put(s2["drawOn"] + 0.05, scratch(1.2), 0.12, 0.1)
    for i, st in enumerate(s2["steps"]):
        put(st, click(1600 + i * 250), 0.28, -0.1 + i * 0.07)
        put(st + 0.01, blip(STEP_NOTES[i], dur=0.5, tau=0.14), 0.16, -0.1 + i * 0.07)
        if i in (1, 2):
            put(st + 0.08, whoosh(0.5, 1800, 7000, peak=0.35, q=0.5), 0.07)
    put(s2["steps"][3] + 0.2, chime([987.77, 1479.98, 1975.53], dur=1.8, tau=0.6), 0.16, 0.1)
    for i, c in enumerate(s2["callouts"]):
        put(c, pop(900 + i * 180, 380 + i * 80), 0.32, [0.4, -0.5, 0.3][i])
    put(s2["exit"], whoosh(0.5, 3000, 500, peak=0.45), 0.2)

    # scene 3: rewind, retype, 1/5 at low, climb to 5/5 at xhigh
    for k in range(6):
        put(s3["rewind"] + k * 0.035, click(2600 - k * 260, dur=0.03), 0.14 * (1 - k * 0.1), 0.3 - k * 0.1)
    mix.typing(s3["retypeStart"], s3["retypeEnd"], len(PROMPT_2), gain=(0.14, 0.22), jitter=0.004)
    for i in range(5):
        put(s3["enter"] + 0.15 + i * 0.06, click(900 + i * 60, dur=0.04), 0.06, (i - 2) * 0.3)
    put(s3["lowResult"], pop(1200, 520), 0.3, -0.5)
    put(s3["lowResult"] + 0.02, blip(880, dur=0.4), 0.1, -0.5)
    for i in range(1, 5):
        put(s3["lowResult"] + 0.1 + i * 0.05, blip(146.8, dur=0.2, tau=0.05), 0.2, (i - 2) * 0.3)
    put(s3["climb"] - 0.05, riser(s3["arrive"] - s3["climb"] + 0.05), 0.22)
    for i, c in enumerate(s3["chips"]):
        put(c, pop(1500 + i * 120, 900), 0.14, -0.4 + i * 0.27)
    put(s3["arrive"], click(2000), 0.22)
    for i, pp in enumerate(s3["pops"]):
        put(pp, pop(POP_NOTES[i] * 0.9, POP_NOTES[i] * 0.45), 0.34, -0.25 + i * 0.25)
        put(pp + 0.005, blip(POP_NOTES[i] / 2, dur=0.4, tau=0.12), 0.1, -0.25 + i * 0.25)
    put(s3["pops"][3] + 0.08, chime([523.25, 783.99, 1046.5, 1318.5], dur=2.0, tau=0.8), 0.14)

    # iris transition and finale: the only impact in the mix
    put(s4["merge"] - 0.05, whoosh(0.3, 3500, 800, peak=0.8), 0.18)
    put(s4["irisIn"], whoosh(s4["irisOut"] - s4["irisIn"] + 0.05, 300, 4200, peak=0.85, q=0.7), 0.32)
    put(s4["irisOut"] - 0.01, impact(), 0.34)
    put(s4["irisOut"], whoosh(0.7, 5000, 300, peak=0.15, q=0.6), 0.14)
    for i in range(4):
        put(s4["setup"] + i * 0.07 + 0.1, blip(220 * (1.5 if i % 2 else 1), dur=0.25, tau=0.05), 0.08)
    for line, (note, tick) in zip((s4["line1"], s4["line2"]), ((73.4, 900), (82.4, 1100))):
        put(line + 0.12, blip(note, dur=0.7, tau=0.25), 0.35)
        put(line + 0.12, click(tick), 0.08)
    put(s4["mini"], pop(700, 350), 0.14)
    put(s4["miniTravel"], riser(s4["miniArrive"] - s4["miniTravel"], 600, 3800), 0.1)
    put(s4["miniArrive"], chime([587.33, 880.0, 1174.66, 1479.98], dur=1.1, tau=0.5), 0.2)
    put(s4["miniArrive"], click(2200), 0.2)
    put(s4["footer"], pop(1100, 600), 0.1, -0.6)

"""Recorded sound files for the cue sheet: load a WAV and find the point to anchor on its beat.

Not part of the vendored claude-motion engine; written for motion-craft (MIT, like the plugin).
Standard library only. Convert other formats first:
    ffmpeg -i whoosh.mp3 -ac 1 -ar 48000 sound/sfx/whoosh.wav

    from sfx.samples import load, place
    w = load("sound/sfx/whoosh.wav")
    place(mix, s["hook"]["title"], w, anchor="peak", peak_db=-9)    # a whoosh peaks mid-move
    place(mix, s["proof"]["tap"], load("sound/sfx/click.wav"), anchor="onset", peak_db=-14)
"""

import math
import struct
import wave

from .synth import SR


def load(path):
    """A WAV file as mono floats in [-1, 1] at the engine's sample rate."""
    with wave.open(path, "rb") as w:
        ch, width, rate, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    if width == 2:
        vals = struct.unpack("<%dh" % (len(raw) // 2), raw)
        scale = 32768.0
    elif width == 3:
        vals = [int.from_bytes(raw[i:i + 3], "little", signed=True) for i in range(0, len(raw), 3)]
        scale = 8388608.0
    elif width == 4:
        vals = struct.unpack("<%di" % (len(raw) // 4), raw)
        scale = 2147483648.0
    elif width == 1:
        vals = [b - 128 for b in raw]
        scale = 128.0
    else:
        raise ValueError(f"{path}: unsupported sample width {width}")
    mono = [sum(vals[i:i + ch]) / (ch * scale) for i in range(0, len(vals), ch)]
    if rate == SR:
        return mono
    step = rate / SR  # linear resample; fine for effects, convert music with ffmpeg instead
    out_n = int(len(mono) / step)
    out = []
    for k in range(out_n):
        x = k * step
        i = int(x)
        f = x - i
        a = mono[i]
        b = mono[i + 1] if i + 1 < len(mono) else a
        out.append(a + (b - a) * f)
    return out


def onset(samples, below_peak_db=30.0):
    """Index where the sound becomes audible: the first sample within below_peak_db of its peak.
    Library files often start with 30-150 ms of near silence, so placing by sample 0 sounds late."""
    pk = max((abs(s) for s in samples), default=0.0)
    if pk == 0:
        return 0
    floor = pk * 10 ** (-below_peak_db / 20)
    for i, s in enumerate(samples):
        if abs(s) >= floor:
            return i
    return 0


def peak_index(samples, window=480):
    """Index of the loudest 10 ms (at 48 kHz) of the sound: a whoosh's middle."""
    best, best_i, acc = 0.0, 0, 0.0
    sq = [s * s for s in samples]
    for i, v in enumerate(sq):
        acc += v
        if i >= window:
            acc -= sq[i - window]
        if acc > best:
            best, best_i = acc, max(0, i - window // 2)
    return best_i


def place(mix, t, samples, anchor="onset", peak_db=-14.0, pan=0.0):
    """Put a recorded sound on the mix so its anchor lands at t seconds and its peak sits at peak_db dBFS.
    anchor: "onset" for struck sounds, "peak" for whooshes, "end" for risers that end on the reveal."""
    if not samples:
        return
    if anchor == "onset":
        a = onset(samples)
    elif anchor == "peak":
        a = peak_index(samples)
    elif anchor == "end":
        a = len(samples)
    else:
        raise ValueError(f"unknown anchor {anchor!r}")
    pk = max(abs(s) for s in samples) or 1.0
    gain = (10 ** (peak_db / 20)) / pk
    mix.put(max(0.0, t - a / SR), samples, gain=gain, pan=pan)

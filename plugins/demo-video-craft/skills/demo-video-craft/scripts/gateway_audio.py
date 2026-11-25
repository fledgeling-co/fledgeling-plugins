#!/usr/bin/env python3
"""Narration, word timings and music beds through Vercel AI Gateway's ElevenLabs models.

    gateway_audio.py lines   --script lines.json --out-dir voice/ [--respell respell.json] [--only O K02] [--dry-run]
    gateway_audio.py speech  --voice ID --text "..." --out line.mp3 [--model elevenlabs/eleven-v4] [--respell r.json]
    gateway_audio.py words   --audio line.mp3 --out line.json
    gateway_audio.py music   --prompt "..." --seconds 27 --out bed.mp3 [--model elevenlabs/music-v2.5] [--dry-run]
    gateway_audio.py respell --rules respell.json "Diolog Guardian works in Claude"
    gateway_audio.py --self-test

The key is read from AI_GATEWAY_API_KEY and never printed or written anywhere. Every paid call prints what it
bought, so the cost is known before the next one: speech is US$0.08 per 1,000 characters, Scribe v2 US$0.000061
a second and music-v2.5 US$0.0025 a second (Vercel AI Gateway price list, 24-25 Nov 2026; re-read it before a
large run).

`lines` is the batch form. lines.json is {"voice": {"id": ..., "model": ...}, "lines": [{"id", "film", "text"}]}.
For each line it writes <id>.mp3, <id>.wav (48 kHz mono, for motion-craft's sound engine), <id>.json (word timings,
duration, the script text and the spoken text) and <id>.txt (the cache key). A line is regenerated only when its
spoken text, voice or model changes, so re-running after editing one line costs one line.

Respelling changes what the voice is sent, never what the captions or pages say. Rules apply in file order, so put
the specific rule before the general one: "Diolog Guardian" -> "Dialogue's Guardian" has to run before
"Diolog" -> "Dialogue", or the possessive never fires.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GATEWAY = 'https://ai-gateway.vercel.sh/v4/ai'
SPEECH_MODEL = 'elevenlabs/eleven-v4'
MUSIC_MODEL = 'elevenlabs/music-v2.5'
WORDS_MODEL = 'elevenlabs/scribe-v2'
PRICE_PER_1K_CHARS = 0.08
PRICE_PER_MUSIC_SECOND = 0.0025
PRICE_PER_SCRIBE_SECOND = 0.000061
TAG = re.compile(r'\s*\[[a-z][a-z \-]*\]\s*', re.I)   # ElevenLabs v4 audio tags such as [upbeat]


def _key():
    k = os.environ.get('AI_GATEWAY_API_KEY', '')
    if not k:
        sys.exit('AI_GATEWAY_API_KEY is not set. Export it from wherever the project keeps it, without printing it.')
    return k


def _post(kind, model, body, spec_header, timeout):
    req = urllib.request.Request(
        f'{GATEWAY}/{kind}', data=json.dumps(body).encode(),
        headers={'Authorization': 'Bearer ' + _key(), 'ai-gateway-protocol-version': '0.0.1',
                 spec_header: '4', 'ai-model-id': model, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'gateway {e.code} from {kind} ({model}): {e.read().decode(errors="replace")[:600]}')


def load_rules(path):
    if not path:
        return []
    rules = json.loads(Path(path).read_text())
    if not isinstance(rules, list) or not all(isinstance(r, list) and len(r) == 2 for r in rules):
        sys.exit(f'{path}: expected a list of [pattern, replacement] pairs')
    return rules


def respell(text, rules):
    """The text the voice is sent. Rules are regular expressions applied in order."""
    for pat, rep in rules:
        text = re.sub(pat, rep, text)
    return text


def caption_text(text):
    """The text a caption or page shows: delivery tags removed, real spellings kept."""
    return TAG.sub(' ', text).strip()


def speech(voice, text, out, model=SPEECH_MODEL):
    res = _post('speech-model', model, {'text': text, 'voice': voice, 'outputFormat': 'mp3'},
                'ai-speech-model-specification-version', 180)
    audio = base64.b64decode(res.get('audio') or '')
    if not audio:
        sys.exit(f'no audio returned for {out}: {json.dumps(res)[:400]}')
    Path(out).write_bytes(audio)
    return len(text)


def words(audio, out):
    body = {'audio': base64.b64encode(Path(audio).read_bytes()).decode(), 'mediaType': 'audio/mpeg'}
    res = _post('transcription-model', WORDS_MODEL, body, 'ai-transcription-model-specification-version', 180)
    meta = (res.get('providerMetadata') or {}).get('elevenlabs') or {}
    ws = [{'w': w['text'], 'start': w['start'], 'end': w['end']} for w in meta.get('words', []) if w.get('type') == 'word']
    if not ws:
        sys.exit(f'no word timings for {audio}: response keys {",".join(res)}')
    data = {'text': res.get('text', ''), 'words': ws}
    Path(out).write_text(json.dumps(data, indent=1))
    return data


def music(prompt, seconds, out, model=MUSIC_MODEL):
    body = {'text': prompt, 'outputFormat': 'mp3',
            'providerOptions': {'elevenlabs': {'musicLengthMs': int(seconds * 1000), 'forceInstrumental': True}}}
    res = _post('speech-model', model, body, 'ai-speech-model-specification-version', 600)
    audio = base64.b64decode(res.get('audio') or '')
    if not audio:
        sys.exit(f'no music returned for {out}: {json.dumps(res)[:400]}')
    Path(out).write_bytes(audio)
    wav = Path(out).with_suffix('.wav')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(out), '-ac', '2', '-ar', '48000', str(wav)], check=True)
    return seconds


def _duration(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                                check=True, capture_output=True, text=True).stdout)


def cache_key(voice, model, spoken):
    return f'{voice}|{model}|{spoken}'


def lines(script, out_dir, rules, only, dry_run=False):
    d = json.loads(Path(script).read_text())
    voice, model = d['voice']['id'], d['voice'].get('model', SPEECH_MODEL)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    jobs, skipped, cached = [], 0, 0
    for ln in d['lines']:
        if only and ln.get('film') not in only:
            skipped += 1
            continue
        spoken = respell(ln['text'], rules)
        key = cache_key(voice, model, spoken)
        base = out / ln['id']
        if base.with_suffix('.txt').exists() and base.with_suffix('.txt').read_text() == key \
                and base.with_suffix('.mp3').exists() and base.with_suffix('.json').exists():
            if not base.with_suffix('.wav').exists():
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(base.with_suffix('.mp3')), '-ac', '1',
                                '-ar', '48000', str(base.with_suffix('.wav'))], check=True)
            cached += 1
            continue
        jobs.append((ln, spoken, key, base))
    if dry_run:
        # speech is priced by character; Scribe by second, estimated at 14 spoken characters a second
        chars = sum(len(sp) for _, sp, _, _ in jobs)
        est = chars * PRICE_PER_1K_CHARS / 1000 + chars / 14 * PRICE_PER_SCRIBE_SECOND
        for ln, sp, _, _ in jobs:
            print(f'{ln["id"]:8} {len(sp):4} chars  would be generated')
        print(f'dry run: {len(jobs)} lines to generate, {cached} cached, {skipped} skipped by --only; {chars} characters, '
              f'about US${est:.2f}. Nothing was sent.')
        return

    def run(job):
        ln, spoken, key, base = job
        n = speech(voice, spoken, base.with_suffix('.mp3'), model)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(base.with_suffix('.mp3')), '-ac', '1', '-ar',
                        '48000', str(base.with_suffix('.wav'))], check=True)
        w = words(base.with_suffix('.mp3'), base.with_suffix('.json'))
        dur = _duration(base.with_suffix('.wav'))
        w.update({'duration': dur, 'script': caption_text(ln['text']), 'spoken': spoken})
        base.with_suffix('.json').write_text(json.dumps(w, indent=1))
        base.with_suffix('.txt').write_text(key)
        return ln['id'], n, dur

    chars = secs = 0.0
    with ThreadPoolExecutor(6) as ex:
        for lid, n, dur in ex.map(run, jobs):      # a running total, so a failure part-way still says what was bought
            chars += n
            secs += dur
            spent = chars * PRICE_PER_1K_CHARS / 1000 + secs * PRICE_PER_SCRIBE_SECOND
            print(f'{lid:8} {n:4} chars {dur:6.2f}s   spent so far about US${spent:.2f}')
    cost = chars * PRICE_PER_1K_CHARS / 1000 + secs * PRICE_PER_SCRIBE_SECOND
    print(f'{len(jobs)} lines generated, {cached} cached, {skipped} skipped by --only, {int(chars)} characters sent, '
          f'about US${cost:.2f}')


def self_test():
    rules = [[r'\bDiolog Guardian\b', 'Dialogue’s Guardian'], [r'\bDiolog', 'Dialogue'], [r'\bClaude\b', 'Clawd']]
    cases = [
        ('specific rule before general', respell('Diolog Guardian works in Claude.', rules),
         'Dialogue’s Guardian works in Clawd.'),
        ('reversed order loses the possessive', respell('Diolog Guardian', list(reversed(rules))), 'Dialogue Guardian'),
        ('a word containing the name is untouched', respell('Claudette', rules), 'Claudette'),
        ('captions drop tags and keep real names', caption_text('[upbeat] Diolog Guardian works in Claude.'),
         'Diolog Guardian works in Claude.'),
        ('a spoken-text change changes the cache key',
         cache_key('v', 'm', 'a') != cache_key('v', 'm', 'b'), True),
    ]
    failed = [name for name, got, want in cases if got != want]
    env = {k: v for k, v in os.environ.items() if k != 'AI_GATEWAY_API_KEY'}
    with tempfile.TemporaryDirectory() as t:
        r = subprocess.run([sys.executable, __file__, 'speech', '--voice', 'x', '--text', 'hi', '--out',
                            str(Path(t) / 'x.mp3')], env=env, capture_output=True, text=True)
    if r.returncode == 0 or 'AI_GATEWAY_API_KEY is not set' not in r.stderr:
        failed.append('a missing key stops before any request')
    total = len(cases) + 1
    print(f'self-test: {total - len(failed)}/{total} passed' + (f'; failed: {", ".join(failed)}' if failed else ''))
    sys.exit(1 if failed else 0)


def main():
    if '--self-test' in sys.argv:
        self_test()
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('lines')
    p.add_argument('--script', required=True)
    p.add_argument('--out-dir', required=True)
    p.add_argument('--respell')
    p.add_argument('--only', nargs='*', default=[])
    p.add_argument('--dry-run', action='store_true', help='print what would be generated and its cost; send nothing')
    p = sub.add_parser('speech')
    p.add_argument('--voice', required=True)
    p.add_argument('--text', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--model', default=SPEECH_MODEL)
    p.add_argument('--respell')
    p = sub.add_parser('words')
    p.add_argument('--audio', required=True)
    p.add_argument('--out', required=True)
    p = sub.add_parser('music')
    p.add_argument('--prompt', required=True)
    p.add_argument('--seconds', type=float, required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--model', default=MUSIC_MODEL)
    p.add_argument('--dry-run', action='store_true', help='print the cost; send nothing')
    p = sub.add_parser('respell')
    p.add_argument('--rules', required=True)
    p.add_argument('text')
    a = ap.parse_args()
    if a.cmd == 'lines':
        lines(a.script, a.out_dir, load_rules(a.respell), set(a.only), a.dry_run)
    elif a.cmd == 'speech':
        spoken = respell(a.text, load_rules(a.respell))
        n = speech(a.voice, spoken, a.out, a.model)
        print(f'{a.out}: {n} characters sent, about US${n * PRICE_PER_1K_CHARS / 1000:.3f}')
    elif a.cmd == 'words':
        w = words(a.audio, a.out)
        print(f'{a.out}: {len(w["words"])} words')
    elif a.cmd == 'music' and a.dry_run:
        print(f'dry run: {a.seconds:.0f} seconds of {a.model}, about US${a.seconds * PRICE_PER_MUSIC_SECOND:.2f}. Nothing was sent.')
    elif a.cmd == 'music':
        s = music(a.prompt, a.seconds, a.out, a.model)
        print(f'{a.out}: {s:.0f} seconds bought, about US${s * PRICE_PER_MUSIC_SECOND:.2f}')
    elif a.cmd == 'respell':
        print(respell(a.text, load_rules(a.rules)))


if __name__ == '__main__':
    main()

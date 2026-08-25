#!/usr/bin/env python3
"""Deterministic signals over Claude Code session transcripts.

Every signal is countable and carries a citable location (file + line + verbatim
span), so a later reader can check the claim rather than take it. Nothing here
judges quality; it counts things a judge would otherwise have to eyeball.
"""
import json, os, re, sys, collections

GLYPH = '\U0001FAE5'   # the session-marker probe

# A sentence that asserts a check happened. Kept narrow on purpose: a claim in
# the future or conditional tense is not an assertion that something ran.
CLAIM_RE = re.compile(
    r'(?:^|[.!?)\]]\s|\n\s*[-*]\s*|\n#+\s*)'
    r'([^.!?\n]{0,200}?\b(?:'
    r'all (?:\d+\s+)?(?:tests?|checks?|specs?|assertions?|suites?)\s+(?:pass|passed|are passing|green)'
    r'|(?:tests?|suite|build|lint|typecheck|gate)\s+(?:passes|passed|is green|are green|succeeded)'
    r'|(?:I|we)\s+(?:ran|verified|confirmed|validated|tested|measured|checked)'
    r'|verified\s+(?:that|the|it|by)'
    r'|100%\s+(?:pass|passing|coverage|of)'
    r'|exit(?:ed|s)?\s+(?:code\s+)?0'
    r'|(?:no|zero)\s+(?:errors?|failures?|regressions?|warnings?)'
    r'|screenshot(?:s|ted|ed)?\s+(?:confirm|show|verif)'
    r')[^.!?\n]{0,200})', re.I)

DONE_RE = re.compile(
    r'\b(?:complete(?:d|ly)?|done|finished|shipped|ready to (?:merge|ship)|'
    r'production[- ]ready|fully (?:implemented|working|functional)|'
    r'all (?:items?|tasks?|features?|requirements?) (?:are )?(?:complete|done|implemented))\b', re.I)

# Human correction / dissatisfaction, used as ground truth on output quality.
CORRECT_RE = re.compile(
    r"(?:you (?:didn'?t|did not|failed to|haven'?t|have not|never)"
    r"|that'?s (?:wrong|not right|incorrect|not what)"
    r"|(?:doesn'?t|does not|isn'?t|is not) work"
    r"|still (?:broken|failing|not|doesn'?t|wrong)"
    r"|no[,.]? (?:it|that|you)"
    r"|why (?:didn'?t|did'?nt|isn'?t|aren'?t|haven'?t|are you not|is it not)"
    r"|nothing happen"
    r"|(?:it'?s|its) (?:broken|blank|empty|missing)"
    r"|(?:i )?told you"
    r"|(?:read|follow) the (?:skill|instructions?|rules?)"
    r"|didn'?t (?:you|it) (?:read|run|follow|check)"
    r"|(?:you )?(?:lied|made (?:that|it) up|fabricat)"
    r"|(?:not|never) (?:actually|really) (?:ran|run|tested|checked)"
    r")", re.I)

STOPWORDS = set('the a an and or of to in for with on at by is are be run using cd git python3 node npm pnpm bash sh echo cat ls'.split())

def script_tokens(text):
    """Named executables / scripts a claim points at, e.g. build-catalogue.mjs."""
    return set(re.findall(r'[\w./-]+\.(?:py|mjs|js|sh|ts|rb)\b', text)) | \
           set(re.findall(r'\b(?:pytest|jest|vitest|playwright|xcodebuild|swiftc|cargo|turbo|eslint|tsc|obscura|spctl|codesign)\b', text, re.I))

def scan(path):
    d = dict(path=path, turns=0, user_turns=0, assistant_text_turns=0,
             glyph_ok=0, glyph_miss=0, glyph_first_miss=None,
             tools=collections.Counter(), tool_errors=collections.Counter(),
             bash_cmds=[], skills=collections.Counter(),
             claims=[], done_claims=0, corrections=[], todo_writes=0,
             models=collections.Counter(), repeats=0, longest_repeat=0,
             file_writes=collections.Counter(), commits=[], first='', last='')
    last_sig = None; run = 0
    prev_tool_input = collections.Counter()
    with open(path, errors='replace') as f:
        for ln, line in enumerate(f, 1):
            try: o = json.loads(line)
            except Exception: continue
            ts = o.get('timestamp','')
            if ts:
                if not d['first']: d['first']=ts[:19]
                d['last']=ts[:19]
            t = o.get('type')
            if t == 'user':
                d['user_turns'] += 1
                m = o.get('message') or {}
                c = m.get('content')
                txt = c if isinstance(c,str) else ' '.join(
                    b.get('text','') for b in (c or []) if isinstance(b,dict) and b.get('type')=='text')
                if txt and not o.get('isSidechain'):
                    for mt in CORRECT_RE.finditer(txt[:4000]):
                        s=max(0,mt.start()-90); d['corrections'].append(
                            dict(line=ln, quote=' '.join(txt[s:mt.end()+110].split())))
                # tool results
                for b in (c or []) if isinstance(c,list) else []:
                    if isinstance(b,dict) and b.get('type')=='tool_result' and b.get('is_error'):
                        d['tool_errors']['<err>'] += 1
            elif t == 'assistant':
                d['turns'] += 1
                msg = o.get('message') or {}
                mdl = msg.get('model') or ''
                if mdl: d['models'][mdl]+=1
                blocks = msg.get('content') or []
                texts = [b.get('text','') for b in blocks if isinstance(b,dict) and b.get('type')=='text']
                text = '\n'.join(texts).strip()
                if text:
                    d['assistant_text_turns'] += 1
                    if not o.get('isSidechain'):
                        if text.startswith(GLYPH): d['glyph_ok'] += 1
                        else:
                            d['glyph_miss'] += 1
                            if d['glyph_first_miss'] is None:
                                d['glyph_first_miss'] = dict(line=ln, quote=' '.join(text[:110].split()))
                    for mt in CLAIM_RE.finditer(text):
                        d['claims'].append(dict(line=ln, quote=' '.join(mt.group(1).split())[:230]))
                    d['done_claims'] += len(DONE_RE.findall(text))
                for b in blocks:
                    if not (isinstance(b,dict) and b.get('type')=='tool_use'): continue
                    name = b.get('name','?'); inp = b.get('input') or {}
                    d['tools'][name] += 1
                    sig = (name, json.dumps(inp, sort_keys=True)[:400])
                    if sig == last_sig:
                        run += 1; d['repeats'] += 1
                        d['longest_repeat'] = max(d['longest_repeat'], run+1)
                    else: run = 0
                    last_sig = sig
                    if name == 'Skill': d['skills'][inp.get('skill','?')] += 1
                    elif name == 'TodoWrite': d['todo_writes'] += 1
                    elif name == 'Bash':
                        cmd = (inp.get('command') or '')[:600]
                        d['bash_cmds'].append(cmd)
                        if re.search(r'\bgit\s+commit\b', cmd): d['commits'].append(dict(line=ln, cmd=' '.join(cmd.split())[:200]))
                    elif name in ('Write','Edit','NotebookEdit'):
                        d['file_writes'][os.path.basename(inp.get('file_path','?'))] += 1
    # fabrication check: a claim naming a script/binary that no Bash command ever ran
    allbash = '\n'.join(d['bash_cmds'])
    unsupported = []
    for c in d['claims']:
        toks = script_tokens(c['quote'])
        toks = {t for t in toks if t.lower() not in STOPWORDS}
        if not toks: continue
        missing = [t for t in toks if os.path.basename(t) not in allbash and t not in allbash]
        if missing:
            unsupported.append(dict(**c, missing=missing))
    d['unsupported_claims'] = unsupported
    d['bash_count'] = len(d['bash_cmds'])
    d['bash_cmds'] = d['bash_cmds'][:0]   # drop bulk
    for k in ('tools','tool_errors','skills','file_writes','models'):
        d[k] = dict(collections.Counter(d[k]).most_common(25))
    return d

if __name__ == '__main__':
    corpus = json.load(open(sys.argv[1]))
    out=[]
    for r in corpus:
        try:
            m = scan(r['path']); m['proj']=r.get('proj','?'); m['gem']=r.get('gem',0)
            m['frac']=r.get('frac',0); m['size']=r.get('size',0); m['cwd']=r.get('cwd','')
            out.append(m)
        except Exception as e:
            print('ERR', r['path'], e, file=sys.stderr)
    json.dump(out, open(sys.argv[2],'w'), indent=1)
    print(f"scanned {len(out)}")

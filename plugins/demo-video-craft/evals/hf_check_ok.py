"""Exit 0 when a saved `hf.sh check --json` output reports ok with no errors in any section."""
import json
import sys

t = open(sys.argv[1]).read()
d, _ = json.JSONDecoder().raw_decode(t[t.find('{'):])
errs = sum(d[k]['errorCount'] for k in ('lint', 'runtime', 'layout', 'contrast'))
warns = sum(d[k]['warningCount'] for k in ('lint', 'runtime', 'layout', 'contrast'))
print(f'{sys.argv[1]}: ok={d["ok"]} errors={errs} warnings={warns}')
sys.exit(0 if d['ok'] and errs == 0 else 1)

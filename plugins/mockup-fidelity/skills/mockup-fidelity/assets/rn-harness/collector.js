// Local sink for the RN fidelity harness. Writes each POSTed snapshot to
// <workspace>/<screen>/target.snapshot.json. Run: node collector.js [workspaceDir] [port]
const http = require('http'), fs = require('fs'), path = require('path');
const OUT = process.argv[2] || process.cwd() + '/.mockup-fidelity';
const PORT = +(process.argv[3] || 8799);
fs.mkdirSync(OUT, { recursive: true });
http.createServer((req, res) => {
  if (req.method === 'POST') {
    let b = ''; req.on('data', c => (b += c));
    req.on('end', () => {
      try {
        const screen = new URL(req.url, 'http://x').searchParams.get('screen') || 'latest';
        fs.writeFileSync(path.join(OUT, '_latest.json'), b);
        if (screen !== 'latest') { const d = path.join(OUT, screen); fs.mkdirSync(d, { recursive: true }); fs.writeFileSync(path.join(d, 'target.snapshot.json'), b); }
        let n = 0; try { n = JSON.parse(b).length; } catch (e) {}
        process.stdout.write(`${new Date().toISOString()} ${screen} ${n} nodes\n`);
        res.writeHead(200); res.end('ok');
      } catch (e) { res.writeHead(500); res.end(String(e)); }
    });
  } else { res.writeHead(200); res.end('rn-harness collector'); }
}).listen(PORT, () => console.log(`collector on :${PORT} -> ${OUT}`));

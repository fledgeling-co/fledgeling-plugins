// mfserve.js — tiny CORS-enabled static file server for the staged MODE-A JSON captures.
//
// WHY: analyze.js v2.0.0's RESPONSIVE pass needs the reference + target analyses keyed by width
// (390/768/1280) injected onto the page before the MODE-B run. Those maps are multi-MB and EXCEED
// the shell's ARG_MAX (1 MB on macOS), so they cannot be passed inline via `obscura fetch --eval
// "$(cat …)"` — the shell errors with "argument list too long". The reliable injection path is to
// serve the captures over a CORS-enabled localhost server and fetch() them in a small setref eval
// (the fetch call fits in argv; the payload does not). The same applies to any single reference
// above a few hundred KB. capture.mjs, which drives CDP directly, has no argv limit and injects
// the reference inline instead — this server is for the shell-driven path.
//
// Usage:  node mfserve.js <dir> [port]      (default port 8799)
// Then in the page:  await fetch('http://localhost:8799/<slug>-ref-1280.json')
// Obscura must be run with --allow-private-network to reach this server at all, and it will not
// reach it from a page loaded over file:// with the default CORS policy — serve the mock too.
// (JSON.parse twice if the capture was written double-encoded; `obscura fetch --output` is not.)
const http = require('http');
const fs = require('fs');
const path = require('path');
const DIR = path.resolve(process.argv[2] || '.');
const PORT = +(process.argv[3] || 8799);
http
  .createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    const rel = decodeURIComponent((req.url || '/').replace(/^\//, '').split('?')[0]);
    const f = path.join(DIR, rel);
    if (!f.startsWith(DIR) || !fs.existsSync(f)) {
      res.statusCode = 404;
      return res.end('not found');
    }
    res.setHeader('Content-Type', 'application/json');
    fs.createReadStream(f).pipe(res);
  })
  .listen(PORT, () => console.error('mfserve on', PORT, 'dir', DIR));

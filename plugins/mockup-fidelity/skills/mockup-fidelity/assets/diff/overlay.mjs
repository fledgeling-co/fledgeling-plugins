// overlay.mjs — visual pixel-overlay diff (improvement #3), zero dependencies.
//
// Measurement is necessary but blind to some things (a missing standalone icon, a
// reflowed grid, a z-order/overlap problem). The fastest way to SEE "this region is
// structurally wrong" is to lay the reference screenshot over the target and look at
// where they disagree. This script reads two PNGs (reference + target) and writes a
// self-contained `overlay.html` that shows three views with NO external deps:
//   1. side-by-side
//   2. a `mix-blend-mode: difference` overlay (identical pixels → black; any
//      divergence → bright edges — a missing icon / shifted card lights up instantly)
//   3. an opacity slider to fade the reference in/out over the target
// The agent opens it in the browser and screenshots it — use it as the TRIGGER to go
// measure a region, never as the proof of a match (frontier vision recall is too low).
//
//   node overlay.mjs --ref ref.png --app target.png [--out .mockup-fidelity/diff/overlay.html]
//   obscura fetch "file://$PWD/.mockup-fidelity/diff/overlay.html" --screenshot overlay.png

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const args = Object.fromEntries(
  process.argv.slice(2).reduce((a, v, i, arr) => {
    if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1]?.startsWith('--') ? true : arr[i + 1]]);
    return a;
  }, []),
);
if (!args.ref || !args.app) {
  console.error('usage: node overlay.mjs --ref <ref.png> --app <target.png> [--out overlay.html]');
  process.exit(2);
}
const OUT = args.out || '.mockup-fidelity/diff/overlay.html';
const b64 = (p) => 'data:image/png;base64,' + readFileSync(resolve(p)).toString('base64');
const refSrc = b64(args.ref);
const appSrc = b64(args.app);

const html = `<!doctype html><meta charset=utf8><title>overlay diff</title>
<style>
  body{margin:0;background:#0b1020;color:#cdd6e8;font:13px system-ui;padding:16px}
  h2{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#7d8aa6;margin:18px 0 8px}
  .row{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}
  .col{flex:1;min-width:360px}
  img{width:100%;display:block;border:1px solid #243049;border-radius:6px}
  .stack{position:relative}
  .stack img{position:absolute;inset:0}
  .stack .base{position:static}
  .diff{background:#000;border-radius:6px;overflow:hidden}
  .diff .over{mix-blend-mode:difference}
  .controls{display:flex;gap:14px;align-items:center;margin:8px 0}
  input[type=range]{width:280px}
  .legend{color:#7d8aa6}
</style>
<h2>1 · Difference (identical → black; bright edges = divergence)</h2>
<div class="diff stack"><img class="base" src="${appSrc}"><img class="over" src="${refSrc}"></div>
<h2>2 · Fade reference over target</h2>
<div class="controls"><span class="legend">target</span><input id="op" type="range" min="0" max="100" value="50"><span class="legend">reference</span></div>
<div class="stack" id="fadeWrap"><img class="base" src="${appSrc}"><img id="fade" src="${refSrc}" style="opacity:.5"></div>
<h2>3 · Side by side — reference (left) · target (right)</h2>
<div class="row"><div class="col"><img src="${refSrc}"></div><div class="col"><img src="${appSrc}"></div></div>
<script>
  const f=document.getElementById('fade'), w=document.getElementById('fadeWrap');
  // size the absolute-stack wrappers to the image height once loaded
  function fit(el){const img=el.querySelector('.base'); const set=()=>el.style.height=img.clientHeight+'px'; img.complete?set():img.addEventListener('load',set); addEventListener('resize',set);}
  document.querySelectorAll('.stack').forEach(fit);
  document.getElementById('op').addEventListener('input',e=>f.style.opacity=e.target.value/100);
</script>`;

mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, html);
console.log(`overlay → ${OUT}  (open file://${resolve(OUT)} and screenshot)`);

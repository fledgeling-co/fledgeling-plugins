#!/usr/bin/env node
// audit_page.mjs — check a built status-and-decision page in a real browser.
//
//     node scripts/audit_page.mjs <page.html> [--shots <dir>]
//
// Exit 0 clean, 1 on any error. Warnings never block.
//
// Three of these checks exist because the defect they catch is invisible in the
// source and invisible in a screenshot:
//
//   * the export. The page's whole purpose is the JSON that comes out of it, and
//     the only honest way to check it is to click real options in a real browser
//     and read the payload back through the audit seam — not to assert on a
//     fixture the auditor wrote itself.
//   * confirmation on re-click. Selecting the option that is ALREADY selected
//     must register as a decision, because agreeing with the recommendation is
//     the most common answer on the page. A `change`-only binding passes every
//     visual review and silently exports that agreement as "left as found".
//   * the reading half without JavaScript. The report must be legible with
//     scripting off, so the check re-fetches the raw HTML and looks for the item
//     text in the source rather than in the DOM.

import fs from 'node:fs';
import path from 'node:path';
import { open } from './lib/harness.mjs';

const file = process.argv[2];
const shotsIx = process.argv.indexOf('--shots');
const shotDir = shotsIx > -1 ? process.argv[shotsIx + 1] : null;
if (!file) { console.error('usage: node scripts/audit_page.mjs <page.html> [--shots <dir>]'); process.exit(2); }

const errors = [];
const warnings = [];
const err = m => errors.push(m);
const warn = m => warnings.push(m);

const raw = fs.readFileSync(path.resolve(file), 'utf8');

// ── static, no browser needed ───────────────────────────────────────────────
// A subresource the page LOADS breaks the no-network guarantee. A link a person
// CLICKS does not: the page has already opened, and an <a> to the record a
// question came from is how a reader gets the history without the page carrying
// it. So the check is per element rather than per attribute, and it still catches
// the classic violation — a font or stylesheet pulled in from a CDN by CSS.
const external = [];
for (const m of raw.matchAll(/<([a-z0-9-]+)\b([^>]*)>/gi)) {
  if (m[1].toLowerCase() === 'a') continue;
  const hit = m[2].match(/(?:src|srcset|href|data|poster)\s*=\s*["'](https?:)?\/\/[^"']+/i);
  if (hit) external.push(hit[0]);
}
for (const m of raw.matchAll(/url\(\s*["']?(https?:)?\/\/[^)"']+/gi)) external.push(m[0]);
if (external.length) err(`${external.length} external reference(s) — the page must open with no network: ${external[0].slice(0, 90)}`);

for (const tag of ['<h1', '<main', 'lang=']) {
  if (!raw.includes(tag)) err(`missing ${tag} — basic document structure`);
}
if (!/prefers-reduced-motion/.test(raw)) warn('no prefers-reduced-motion rule');
if (!/@media print/.test(raw)) err('no print styles — this page gets printed and annotated');

const page = await open(file, { width: 1280, height: 900, dpr: 2, settleMs: 400 });

try {
  // ── the model, and both directions of the link ────────────────────────────
  const model = await page.ev('JSON.stringify(window.__wl ? window.__wl.model : null)');
  if (!model) { err('no audit seam on the page — was it built by build_page.py?'); throw new Error('stop'); }

  const links = await page.ev(`(() => {
    const bad = [];
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      if (!document.getElementById(a.getAttribute('href').slice(1))) bad.push(a.getAttribute('href'));
    });
    return JSON.stringify(bad);
  })()`);
  for (const href of JSON.parse(links)) err(`dead in-page link ${href} — a blocked item pointing at a question that is not here`);

  const orphans = await page.ev(`(() => {
    const out = [];
    document.querySelectorAll('.item').forEach(it => {
      if (it.dataset.owner === 'you' && !it.querySelector('a.wait')) out.push(it.id);
    });
    return JSON.stringify(out);
  })()`);
  for (const id of JSON.parse(orphans)) warn(`${id} is yours to decide but links to no question`);

  // ── every question is labelled and reachable ──────────────────────────────
  const a11y = JSON.parse(await page.ev(`(() => {
    const out = { unlabelled: 0, noLegend: 0, tinyTargets: 0 };
    document.querySelectorAll('textarea').forEach(t => {
      const id = t.id;
      if (!id || !document.querySelector('label[for="' + CSS.escape(id) + '"]')) out.unlabelled++;
    });
    document.querySelectorAll('fieldset').forEach(f => { if (!f.querySelector('legend')) out.noLegend++; });
    document.querySelectorAll('.opt').forEach(l => { if (l.getBoundingClientRect().height < 40) out.tinyTargets++; });
    return JSON.stringify(out);
  })()`));
  if (a11y.unlabelled) err(`${a11y.unlabelled} textarea(s) with no label — a placeholder is not a label`);
  if (a11y.noLegend) err(`${a11y.noLegend} fieldset(s) with no legend`);
  if (a11y.tinyTargets) warn(`${a11y.tinyTargets} option row(s) under 40px tall`);

  // ── a question the reader owns pre-selects nothing ────────────────────────
  const owned = JSON.parse(await page.ev(`(() => {
    const out = [];
    document.querySelectorAll('.q[data-policy="none"], .q[data-policy="forced"]').forEach(q => {
      if (q.querySelector('input[name="answer"]:checked')) out.push(q.dataset.q);
    });
    return JSON.stringify(out);
  })()`));
  for (const id of owned) err(`${id} pre-selects an option on a question whose default policy is not \`recommended\``);

  // ── every question offers an explicit way to put it off ───────────────────
  const noDefer = JSON.parse(await page.ev(`(() => {
    const out = [];
    document.querySelectorAll('.q[data-kind="single"], .q[data-kind="multi"]').forEach(q => {
      if (!q.querySelector('input[value="__defer__"]')) out.push(q.dataset.q);
    });
    return JSON.stringify(out);
  })()`));
  for (const id of noDefer) err(`${id} offers no way to defer — a skipped question would export as the default nobody read`);

  // ── re-clicking the pre-selected option counts as confirming it ───────────
  const reclick = JSON.parse(await page.ev(`(() => {
    const q = document.querySelector('.q[data-policy="recommended"][data-kind="single"]');
    if (!q) return JSON.stringify({ skipped: true });
    const checked = q.querySelector('input[name="answer"]:checked');
    if (!checked) return JSON.stringify({ error: 'no pre-selected option on a recommended question' });
    checked.click();
    const a = window.__wl.payload().answers.find(x => x.id === q.dataset.q) || {};
    return JSON.stringify({
      confirmed: q.dataset.confirmed === 'yes',
      state: a.state, origin: a.answerOrigin, id: q.dataset.q
    });
  })()`));
  if (reclick.error) err(reclick.error);
  else if (!reclick.skipped) {
    if (!reclick.confirmed) err(`re-selecting the already-selected option on ${reclick.id} did not mark it reviewed — bind click, not only change`);
    if (reclick.state !== 'confirmed') err(`${reclick.id} exports as "${reclick.state}" after being actively re-selected`);
    if (reclick.origin !== 'accepted-recommendation') err(`${reclick.id} exports origin "${reclick.origin}" after the recommendation was accepted`);
  }

  // ── a note raises the caveat lock unless its author clears it ─────────────
  const caveat = JSON.parse(await page.ev(`(() => {
    const q = document.querySelector('.q[data-kind="single"]');
    if (!q) return JSON.stringify({ skipped: true });
    const f = document.forms['q-' + q.dataset.q];
    const ta = f.elements['note'];
    ta.value = 'Only for the Australian entity.';
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    const a = window.__wl.payload().answers.find(x => x.id === q.dataset.q) || {};
    const row = f.querySelector('.qual');
    return JSON.stringify({ blocks: a.blocksAutomation, visible: row ? !row.hidden : false, id: q.dataset.q });
  })()`));
  if (!caveat.skipped) {
    if (!caveat.blocks) err(`a note on ${caveat.id} did not set \`blocksAutomation\` — a qualified answer is not the answer its label says`);
    if (!caveat.visible) err(`the "this note changes the answer" control stayed hidden after ${caveat.id} was annotated`);
  }

  // ── the export itself ─────────────────────────────────────────────────────
  const payload = JSON.parse(await page.ev('JSON.stringify(window.__wl.payload())'));
  for (const k of ['schema', 'project', 'slug', 'reportGeneratedAt', 'exportedAt', 'states', 'answers', 'counts']) {
    if (!(k in payload)) err(`export is missing \`${k}\``);
  }
  if (!Array.isArray(payload.answers) || !payload.answers.length) err('export carries no answers');
  for (const a of payload.answers || []) {
    for (const k of ['id', 'title', 'kind', 'answer', 'state', 'note', 'blocksAutomation']) {
      if (!(k in a)) err(`answer ${a.id} is missing \`${k}\``);
    }
    if (!['confirmed', 'as-found', 'deferred', 'unanswered'].includes(a.state)) err(`answer ${a.id} has state "${a.state}"`);
    if (a.defaultPolicy !== 'recommended' && a.state === 'as-found') {
      err(`${a.id} exported as "as-found" with policy "${a.defaultPolicy}" — it has no default to fall back to`);
    }
    if (a.kind !== 'text' && !('optionConsequences' in a)) {
      err(`answer ${a.id} exports labels without consequences — whatever acts on it can read more into a label than it meant`);
    }
  }
  if (!payload.states || !payload.states['as-found']) {
    err('the export does not say what its own states mean — a reader downstream will guess');
  }

  // ── the report reads with scripting off ───────────────────────────────────
  const firstPlain = await page.ev(`(() => { const p = document.querySelector('.item .plain'); return p ? p.textContent.trim().slice(0, 40) : ''; })()`);
  if (firstPlain && !raw.includes(firstPlain.slice(0, 30).replace(/&/g, '&amp;'))) {
    err('item text is not in the served HTML — the report half depends on JavaScript');
  }
  const optCount = (raw.match(/class="opt"/g) || []).length;
  if (!optCount) err('no options in the served HTML — the questionnaire is JavaScript-only');

  // ── contrast, against each element's EFFECTIVE background ─────────────────
  // Measuring every colour against `body` is the mistake that passes muted text
  // sitting on a tinted card. Walk up until a non-transparent background is found.
  const contrast = JSON.parse(await page.ev(`(() => {
    const lum = c => {
      const [r, g, b] = c.match(/[\\d.]+/g).slice(0, 3).map(Number).map(v => {
        v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };
    const bgOf = el => {
      for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
        const c = getComputedStyle(n).backgroundColor;
        if (c && !/rgba\\(0, 0, 0, 0\\)|transparent/.test(c)) return c;
      }
      return getComputedStyle(document.body).backgroundColor;
    };
    const out = [];
    document.querySelectorAll('.plain, .oconsequence, .why, .row dd, .olabel, .privacy, .gnote, .tally small, .top li span').forEach(el => {
      const size = parseFloat(getComputedStyle(el).fontSize);
      const bold = parseInt(getComputedStyle(el).fontWeight, 10) >= 700;
      const need = (size >= 24 || (size >= 18.66 && bold)) ? 3 : 4.5;
      const a = lum(getComputedStyle(el).color), b = lum(bgOf(el));
      const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
      if (ratio < need) out.push({ cls: el.className || el.tagName, ratio: Math.round(ratio * 100) / 100, need });
    });
    const seen = new Set();
    return JSON.stringify(out.filter(o => !seen.has(o.cls) && seen.add(o.cls)).slice(0, 8));
  })()`));
  for (const c of contrast) err(`${c.cls} is ${c.ratio}:1 on its own background — needs ${c.need}:1`);

  // ── overflow at phone width ───────────────────────────────────────────────
  await page.send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  const over = await page.ev('document.scrollingElement.scrollWidth - window.innerWidth');
  if (over > 2) err(`page scrolls sideways by ${over}px at 390px wide`);

  if (shotDir) {
    fs.mkdirSync(shotDir, { recursive: true });
    await page.shot(path.join(shotDir, 'mobile.png'), { x: 0, y: 0, w: 390, h: 1200 });
    await page.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 900, deviceScaleFactor: 2, mobile: false });
    await page.shot(path.join(shotDir, 'top.png'), { x: 0, y: 0, w: 1280, h: 1100 });
    const qy = await page.ev(`Math.round(document.querySelector('#decisions').getBoundingClientRect().top + window.scrollY)`);
    await page.shot(path.join(shotDir, 'questions.png'), { x: 0, y: qy, w: 1280, h: 1100 });
    const iy = await page.ev(`Math.round(document.querySelector('.item').getBoundingClientRect().top + window.scrollY)`);
    await page.shot(path.join(shotDir, 'items.png'), { x: 0, y: iy, w: 1280, h: 900 });
    console.log(`shots → ${shotDir}`);
  }
} catch (e) {
  if (e.message !== 'stop') err(`audit threw: ${e.message}`);
} finally {
  await page.close();
}

for (const w of warnings) console.log(`warn  ${w}`);
for (const e of errors) console.log(`ERROR ${e}`);
console.log(`\n${errors.length} error(s), ${warnings.length} warning(s)`);
process.exit(errors.length ? 1 : 0);

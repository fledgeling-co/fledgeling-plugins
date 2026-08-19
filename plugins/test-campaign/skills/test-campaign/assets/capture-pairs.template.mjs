/* ============================================================================
 * capture-pairs.template.mjs — photograph the build AND its design of record,
 * as pairs, so something can compare them.
 * ----------------------------------------------------------------------------
 * Copy into the project's own harness and fill in MOCKS.
 *
 * ── WHY PAIRS, AND WHY THIS FILE EXISTS ────────────────────────────────────
 * Phase 8 measures the build against its design of record on structure, style,
 * vocabulary and geometry — all read from the DOM. None of that sees what a
 * person sees. `be-my-witness` does, but it needs two images: the shot and the
 * reference. Campaigns kept producing the first and never the second, so the
 * comparison never happened and nothing said so.
 *
 * Measured across twelve campaigns on 18 Aug 2026: eleven had no mock captures
 * at all, and one had 22 build captures that were never attached to anything.
 *
 * ── WHAT A MOCK IS, HERE ───────────────────────────────────────────────────
 * Whatever the project treats as the design of record, in this order:
 *   1. a rendered mock file      docs/ui-mockups/dashboard.html
 *   2. a design-system story     storybook iframe.html?id=pages-dashboard--default
 *   3. a served prototype        http://design.local/dashboard
 * A surface with none is recorded as `mock: null` WITH a reason, because a
 * missing reference and an unexamined match look identical in a report.
 *
 * ── THE TRAP THIS AVOIDS ───────────────────────────────────────────────────
 * Capturing both at different viewports, themes or scroll positions produces
 * differences that are entirely the capture's fault, and a judge then reports
 * them as design drift. So both halves of a pair are taken at the SAME viewport
 * and device scale, both are given the same settle, and the pair records those
 * settings — a comparison whose conditions are not written down is not evidence.
 */

import { test } from '@playwright/test';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

/** Fill this in: surface id → where its design of record lives. */
const MOCKS = {
  // 'SURF-001': { kind: 'file',    at: 'docs/ui-mockups/dashboard.html' },
  // 'SURF-002': { kind: 'story',   at: 'http://localhost:6007/iframe.html?id=pages-inbox--default' },
  // 'SURF-003': { kind: 'none',    reason: 'no mock was ever drawn for this surface' },
};

/** Both halves of every pair are taken under exactly these conditions. */
const VIEWPORT = { width: 1440, height: 900 };
const SETTLE_MS = 1200;
const OUT = process.env.CAMPAIGN_SHOTS ?? 'evidence/shots';

const pairs = [];

/* ── captures.json — WHAT EACH PICTURE DEPICTS ─────────────────────────────
 * pairs.json says a shot and a reference belong together. It does NOT say what
 * the shot is OF, and that turns out to be the claim readers actually rely on.
 * A campaign published 20 surface captures of three unrelated documents and
 * passed every gate it had, because the only thing binding a picture to a
 * surface was its filename.
 *
 * So every shoot() records its own subject and the target the channel was
 * actually pointed at. This has to happen HERE, at capture time: a manifest
 * written afterwards records what somebody believed, and `capture-lineage.py`
 * reports that as reconstructed rather than as provenance.
 */
const captures = [];

async function shoot(page, url, file, subject) {
  await page.setViewportSize(VIEWPORT);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 6000 }).catch(() => {});
  await page.waitForTimeout(SETTLE_MS);
  mkdirSync(path.dirname(file), { recursive: true });
  await page.screenshot({ path: file, fullPage: false });
  if (subject) {
    captures.push({
      path: file,
      subject,
      target: page.url(),          // where the browser ENDED UP, not where it was sent:
                                   // a redirect to a login page is exactly the capture
                                   // that would otherwise be filed as the dashboard
      channel: `playwright/${test.info().project.name ?? 'default'}`,
      derivedFrom: null,
      sha256: createHash('sha256').update(readFileSync(file)).digest('hex'),
      capturedAt: new Date().toISOString(),
      conditions: {
        viewport: [VIEWPORT.width, VIEWPORT.height],
        dpr: page.viewportSize()?.deviceScaleFactor ?? 1,
        settleMs: SETTLE_MS,
      },
    });
  }
  return file;
}

export function definePairCaptures(surfaces) {
  for (const s of surfaces) {
    test(`CAPTURE ${s.id} ${s.name}`, async ({ page }) => {
      const built = await shoot(page, s.route, path.join(OUT, `${s.id}.png`), s.id);

      const mock = MOCKS[s.id];
      if (!mock || mock.kind === 'none') {
        pairs.push({
          surface: s.id, name: s.name, shot: built, reference: null,
          reason: mock?.reason ?? 'no design of record is mapped for this surface',
          viewport: VIEWPORT, settleMs: SETTLE_MS,
        });
        return;
      }

      const url = mock.kind === 'file' ? `file://${path.resolve(mock.at)}` : mock.at;
      // The reference is the DESIGN, not the build — it gets no subject entry,
      // because it depicts what the surface should look like rather than what it does.
      const ref = await shoot(page, url, path.join(OUT, 'mock', `${s.id}.png`), null);
      pairs.push({
        surface: s.id, name: s.name, shot: built, reference: ref,
        reason: null, viewport: VIEWPORT, settleMs: SETTLE_MS,
      });
    });
  }

  test.afterAll(() => {
    mkdirSync(OUT, { recursive: true });
    writeFileSync(path.join(OUT, 'pairs.json'), JSON.stringify(pairs, null, 1));
    writeFileSync(path.join(OUT, 'captures.json'), JSON.stringify(captures, null, 1));
    const withRef = pairs.filter((p) => p.reference).length;
    // eslint-disable-next-line no-console
    console.log(
      `\nCAPTURE PAIRS  surfaces=${pairs.length}  with a reference=${withRef}  ` +
        `without=${pairs.length - withRef}\n` +
        `Every pair carries the viewport and settle it was taken at. Hand pairs.json to\n` +
        `be-my-witness; a pair with reference:null is an UNCOMPARED surface, not a passing one.\n` +
        `captures.json records what each shot DEPICTS and where the channel was pointed.\n` +
        `Gate it with capture-lineage.py before publishing: without it the wall rests on\n` +
        `filenames, which is how 20 captures of three unrelated documents once passed.\n`,
    );
  });
}

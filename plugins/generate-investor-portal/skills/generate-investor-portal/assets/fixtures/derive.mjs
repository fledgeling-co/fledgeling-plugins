// Derives the fail-* and peer fixtures from pass-minimal.json, so each failing fixture is
// "the passing record plus exactly one defect" and cannot drift into failing for a second
// reason nobody intended. Run from the assets/ directory: node fixtures/derive.mjs
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const clone = (o) => JSON.parse(JSON.stringify(o));
const base = JSON.parse(readFileSync(join(HERE, 'pass-minimal.json'), 'utf8'));
const write = (rel, obj) => { mkdirSync(dirname(join(HERE, rel)), { recursive: true }); writeFileSync(join(HERE, rel), JSON.stringify(obj, null, 2) + '\n'); };

// ── the fabrication channel ────────────────────────────────────────────────
const fig = clone(base);
fig._fixture = 'FAIL, deliberately. Two defects, both of them the fabrication channel: a plausible figure arrives in the hero as PROSE (no asAt, no source, no provenance marker, and indistinguishable on the page from a disclosed one), and one facts row lost its `from`, which used to default to `record` and so made an omission silently assert the strongest claim available. Derived from pass-minimal.json — the only differences are the defects.';
fig.pages[0].sections[0].sub = 'Northbridge Rail maintains and renews rail infrastructure across the eastern seaboard, with $412 million in contracted revenue and 1,180 people on site.';
delete fig.pages[0].sections[1].props.rows[0].from;
write('fail-fabricated-figure.json', fig);

// ── the refusal that must fire before the spend ────────────────────────────
const pub = clone(base);
pub._fixture = 'FAIL, deliberately. status is already `published` and --republish was not passed. Derived from pass-minimal.json — the only difference is the status. This is the check that has to fire BEFORE the crawl: reached at the write, it has already cost two crawls and an image budget.';
pub.status = 'published';
write('fail-published-no-republish.json', pub);

// ── the published peer, because sameness is a property of a pair ───────────
const peer = clone(base);
peer._fixture = 'A PUBLISHED PEER, for the three collision keys. Note the consequence, because it looks like a bug: this peer is a clone of pass-minimal, so pass-minimal ALSO collides with it. The self-test therefore runs pass-minimal with no peer set and fail-collides-with-peer with one. If you run `record-gate.mjs fixtures/pass-minimal.json --peers fixtures/peers` by hand you will get two collision blocks, and they are correct. Same archetype, same page paths, same per-page section-kind order, same canvas vector and the same "/" headings as pass-minimal: a different company wearing the same portal. Every per-tenant gate is green on both.';
peer.companyId = 'fixture-eastcoast-freight';
peer.slug = 'eastcoast-freight-free';
peer.status = 'published';
peer.identity = { legalName: 'Eastcoast Freight Limited', tradingName: 'Eastcoast Freight', listingCode: 'ASX: ECF' };
peer.title = 'Eastcoast Freight Limited (ASX:ECF) - Investor portal';
peer.theme.primary = '#8A1F3D';
peer.theme.focusRing = '#8A1F3D';
peer.generation.brandPrimaryStated = '#8A1F3D';
peer.canvas = { preset: 'pointField', palette: 'accentOnDark', density: 1, figure: 'planar', stroke: 'solid', accentRation: 'standard', intensity: 'standard' };
write('peers/eastcoast-freight-free.json', peer);

const coll = clone(base);
coll._fixture = 'FAIL, deliberately. Structurally, motionally and verbally identical to the published peer in fixtures/peers — the previous company’s portal in a new palette. Every per-tenant check on this record passes; only a pairwise one can see it. Derived from pass-minimal.json plus the canvas vector the peer also carries.';
coll.canvas = { preset: 'pointField', palette: 'accentOnDark', density: 1, figure: 'planar', stroke: 'solid', accentRation: 'standard', intensity: 'standard' };
write('fail-collides-with-peer.json', coll);

// ── the levy evasion, because a check an incidental string satisfies has measured nothing ──
const levy = clone(base);
levy._fixture = 'FAIL, deliberately. The governance and disclosure PAGES are gone and only footer links still carry the words, which is exactly what an earlier version of the levy check accepted: it matched the whole record as one string, so a footer link reading "Governance" satisfied a gate that is supposed to ask whether a governance SURFACE exists. Derived from pass-minimal.json.';
levy.pages = levy.pages.filter((pg) => pg.path === '/');
levy.chrome.footer.columns = [{ heading: 'Corporate', links: [
  { label: 'Governance', href: '/' },
  { label: 'Disclosures', href: '/' },
  { label: 'Share registry', href: '/' },
] }];
write('fail-levy-evasion.json', levy);

console.log('fixtures derived from pass-minimal.json');


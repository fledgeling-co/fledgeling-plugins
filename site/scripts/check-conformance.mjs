#!/usr/bin/env node
/**
 * Check every plugin against the standard this marketplace publishes for itself.
 *
 * `build-catalogue.mjs` is the build gate: it asserts the four things that would
 * break the site (a SKILL.md, a 256px icon, a banner, agreeing versions) and it
 * has to stay fast because it runs before every `next dev`. This script is the
 * conformance gate. It asserts the rest of what
 * `create-skill/references/brand-and-docs.md` and the repo's CLAUDE.md actually
 * require, and it exists because an audit on 2026-08-18 found that ten
 * dimensions of that standard were being enforced by prose alone. Nothing was
 * checking them, so all ten had drifted: 315 em dashes across READMEs and EVALS
 * files, two install blocks pointing at repositories that were wrong or
 * missing, a plugin that was rebuilt and never registered, and a root README
 * advertising 16 skills against a roster of 35.
 *
 * The lesson that shaped this file is in CLAUDE.md already, twice: a warning is
 * not a gate. `should-compact` shipped with no README and the site could not
 * build; the root-README row was a warning until a real pipeline run skipped it
 * and nothing objected. So every dimension here fails the build, and an
 * accepted exception is a name and a date in DEBT below, which shows up in
 * review. Adding a name is a deliberate act. Removing one is the fix.
 *
 * Usage:
 *   node site/scripts/check-conformance.mjs           # everything
 *   node site/scripts/check-conformance.mjs --quick   # skip the icon audit sheets
 *   node site/scripts/check-conformance.mjs --json    # machine-readable
 */

import { readFileSync, existsSync, readdirSync, statSync, openSync, readSync, closeSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const SITE_DIR = dirname(dirname(fileURLToPath(import.meta.url)));
const REPO_DIR = dirname(SITE_DIR);
const PLUGINS_DIR = join(REPO_DIR, "plugins");
const MARKETPLACE = join(REPO_DIR, ".claude-plugin", "marketplace.json");
const ROOT_README = join(REPO_DIR, "README.md");

const AUDIT_SHEET = join(
  PLUGINS_DIR, "create-mac-icon", "skills", "create-mac-icon", "scripts", "audit_sheet.py",
);

const SHELF_CHECK = join(
  PLUGINS_DIR, "create-mac-icon", "skills", "create-mac-icon", "scripts", "shelf_check.py",
);

const MARKETPLACE_SLUG = "fledgeling-co/fledgeling-plugins";
const MARKETPLACE_NAME = "fledgeling-plugins";

/**
 * The banner the whole family ships: a 1600x520 composition rendered at
 * deviceScaleFactor 2 by create-skill's scripts/render_banner.py.
 *
 * This is asserted rather than merely documented because three banners had
 * already drifted without anything noticing. resume-session shipped at
 * 1600x520, which is the layout size at scale 1, so it was half resolution on
 * every retina display. test-campaign and whats-left render 3200x840 from a
 * 1600x420 layout. All three passed every assertion render_banner.py makes,
 * because none of them is about the family agreeing with itself.
 */
const BANNER_W = 3200;
const BANNER_H = 1040;

/**
 * skill-creator, which create-skill's Phase 2 says to invoke and follow, states
 * "Keep SKILL.md under 500 lines; if you're approaching this limit, add an
 * additional layer of hierarchy", and adds that its counts "are approximate and
 * you can feel free to go longer if needed".
 *
 * create-skill's own prose says "under ~300 lines", which is stricter than the
 * authority it cites and gives no reason for being stricter. Against 300, 15
 * files breach; against 500, five do. 500 is the number with an argument behind
 * it, so it is the number enforced here.
 */
const SKILL_MAX_LINES = 500;

/**
 * Directories under plugins/ that are deliberately not plugins. The three
 * *-workspace directories are eval scratch: blind-panel bundles, unblinding
 * keys and run output. .gitignore has covered `plugins/*-workspace/` since
 * before the audit, and plugins/report/EVALS.md documents them as unversioned,
 * but dossier-report-workspace had been committed before that rule existed and
 * stayed tracked for 72 files. It is untracked now.
 */
const NOT_PLUGINS = /-workspace$/;

/**
 * Named, dated exceptions. Same contract as build-catalogue.mjs's BANNER_DEBT:
 * a name here is a decision somebody made on a date, visible in review, not a
 * silent carve-out. `why` is required because a debt entry with no argument is
 * indistinguishable from a check somebody switched off.
 */
const DEBT = [
  {
    plugin: "report", dimension: "banner", since: "2026-08-18",
    why: "Its banner has no icon at all. The right side is a related illustration of document cards rather than the icon tile every sibling carries beside its wordmark, so brand-and-docs' \"the real icon asset beside a set wordmark\" is unmet by composition rather than by a stale render. Fixing it is a layout change, not a re-render, so it is owed a deliberate pass.",
  },
  {
    plugin: "test-campaign", dimension: "banner", since: "2026-08-18",
    why: "3200x840 from a 1600x420 layout against the family's 520, and its wordmark is set in Iowan Old Style with no web font linked, so it is unreproducible on another machine. Both need a recomposition at the family height rather than a re-render, and squeezing that in beside nine icon commissions is how the 420 got there.",
  },
  {
    plugin: "resume-session", dimension: "banner", since: "2026-08-18",
    why: "Rendered at 1600x520, which is the layout size at deviceScaleFactor 1, so it is half resolution and soft on every retina display. A straight re-render at scale 2 is most of the fix, but its composition also runs the wordmark into the decorative swoosh, so it wants a look rather than a command.",
  },
  {
    plugin: "whats-left", dimension: "banner", since: "2026-08-18",
    why: "3200x840 like test-campaign, wordmark in Iowan Old Style with nothing linked, and its icon is being rebuilt as this list is written, so the banner would be stale the moment it was rendered. Owed once the icon lands.",
  },
  ...["clarify", "dossier-report", "generate-investor-portal", "proctor", "report"].map(
    (plugin) => ({
      plugin, dimension: "skill", since: "2026-08-19",
      why: "Over the 500-line ceiling, held rather than split, on a referral rather than a preference. fable-5 was given the fork and named the asymmetry that decides it: a reference is read only if the model chooses to read it, so moving a mandatory step into references/ converts a guaranteed instruction into a probabilistic one whose failure is silent. Length costs tokens on every trigger, which is a spend argument; splitting control flow costs compliance. There is no published evidence that a 600-900 line SKILL.md degrades instruction-following, and Anthropic's own 500 is explicitly approximate. So ordered steps, refusals and gates stay inline, and only taxonomy, rationale and worked examples are candidates to move. clarify was inspected line by line against that rule and is rules interleaved with the evidence that makes them stick, 16 lines over a proxy threshold, with references/evidence.md already carrying the depth: shaving it would be cosmetic. The other four additionally have uncommitted edits from concurrent sessions as of 2026-08-19, so touching them would collide. Revisit by capping non-procedural inline material rather than total lines.",
    }),
  ),
  {
    plugin: "test-campaign", dimension: "skill", since: "2026-08-20",
    why: "704 lines against the 500-line ceiling, held on the same referral as the 2026-08-19 entries above rather than on a preference. Inspected against that rule: lines 61-500 are one ordered campaign procedure, and everything after it is gates (What counts as done), refusals (Standing rules) and the manifests of its 13 references, 8 scripts and assets. That is the category the referral says stays inline, and the depth that could move has already moved, since references/ carries 13 files. Splitting it would convert the campaign's ordered steps into a reference the runner may or may not open. Revisit by capping non-procedural inline material rather than total lines.",
  },
  {
    plugin: "geminify", dimension: "banner", since: "2026-08-18",
    why: "Sets its wordmark in Rockwell, a local face, on purpose. Its assets/build_banner.py records the reason: it renders through rsvg, which resolves system fonts and ignores webfonts, the reverse of the browser here. Unlike the other two the web-font check catches, it ships assert_font_resolves() and a dotless-i comparison, so a missing Rockwell fails loudly instead of silently substituting. Machine-dependent with a guard is a different thing from machine-dependent by accident.",
  },
];

const debtFor = (plugin, dimension) =>
  DEBT.find((d) => d.plugin === plugin && d.dimension === dimension);

/**
 * The voice gate brand-and-docs.md has always prescribed, and which this script
 * originally could not run.
 *
 * The audit that commissioned this file reported that no `voice_lint.py` existed
 * anywhere in the repo, so the em-dash count below was a hand proxy for its one
 * hard check. That was wrong in substance. The script exists and works; it just
 * does not live here. It ships with the installed `create-luke-content` plugin,
 * and both create-skill and improve-skill cite it as a bare relative path with
 * no owner named, which reads as the citing skill's own `scripts/` directory.
 * That is the real defect, and it is exactly the failure mode mac-craft's
 * SKILL.md documents and writes its paths out in full to avoid.
 *
 * Resolved dynamically because a cache path carries a version number, so pinning
 * one here would rot. When the plugin is not installed the em-dash check still
 * runs and the report says the fuller lint was skipped, rather than passing
 * quietly as though it had run.
 */
function findVoiceLint() {
  const cache = join(process.env.HOME || "", ".claude", "plugins", "cache", "diolog-plugins", "create-luke-content");
  if (!existsSync(cache)) return null;
  const versions = readdirSync(cache).filter((v) => /^\d/.test(v)).sort().reverse();
  for (const v of versions) {
    const candidate = join(cache, v, "skills", "create-luke-content", "scripts", "voice_lint.py");
    if (existsSync(candidate)) return candidate;
  }
  return null;
}

const VOICE_LINT = findVoiceLint();

// ---------------------------------------------------------------------------

const args = new Set(process.argv.slice(2));
const QUICK = args.has("--quick");
const AS_JSON = args.has("--json");

const failures = [];
const excused = [];

const fail = (plugin, dimension, message) => {
  const debt = debtFor(plugin, dimension);
  if (debt) excused.push({ plugin, dimension, message, ...debt });
  else failures.push({ plugin, dimension, message });
};

const read = (p) => (existsSync(p) ? readFileSync(p, "utf8") : null);

/**
 * PNG dimensions straight out of the IHDR chunk, so this script needs no image
 * library. Width and height are big-endian uint32 at byte offsets 16 and 20.
 */
function pngSize(path) {
  if (!existsSync(path)) return null;
  const buf = Buffer.alloc(24);
  const fd = openSync(path, "r");
  try {
    if (readSync(fd, buf, 0, 24, 0) < 24) return null;
  } finally {
    closeSync(fd);
  }
  if (buf.toString("ascii", 1, 4) !== "PNG") return null;
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

const countEmDashes = (text) => (text.match(/—/g) || []).length;

/**
 * Every published README and EVALS.md, and nothing else. The em-dash ban is a
 * voice check on what a reader is shown, so it stops at the plugin's own two
 * documents. Nested READMEs inside evals fixtures, render directories and
 * bundled harnesses are technical notes rather than published copy, and sweeping
 * them would be churn with no reader on the other end.
 */
function voiceSurfaces(dir) {
  const out = [];
  const readme = join(dir, "README.md");
  if (existsSync(readme)) out.push(readme);
  for (const candidate of [join(dir, "EVALS.md"), join(dir, "evals", "EVALS.md")]) {
    if (existsSync(candidate)) out.push(candidate);
  }
  return out;
}

function findFirst(dir, matcher, depth = 4) {
  if (depth < 0 || !existsSync(dir)) return null;
  let entries;
  try { entries = readdirSync(dir, { withFileTypes: true }); } catch { return null; }
  for (const entry of entries) {
    if (entry.name === "node_modules" || entry.name.startsWith(".")) continue;
    const full = join(dir, entry.name);
    if (entry.isFile() && matcher(entry.name)) return full;
    if (entry.isDirectory()) {
      const hit = findFirst(full, matcher, depth - 1);
      if (hit) return hit;
    }
  }
  return null;
}

// ---------------------------------------------------------------------------

const marketplace = JSON.parse(readFileSync(MARKETPLACE, "utf8"));
const registered = new Map(marketplace.plugins.map((p) => [p.name, p]));
const rootReadme = readFileSync(ROOT_README, "utf8");

/**
 * The row index of the first entry under "## The skills". That one entry does
 * not need a preceding <br clear="left" />, because the heading itself breaks
 * the float; every entry after it does.
 */
const firstRowIndex = [...registered.keys()]
  .map((n) => rootReadme.indexOf(`### [${n}](plugins/${n}/README.md)`))
  .filter((i) => i !== -1)
  .sort((a, b) => a - b)[0];

const dirs = readdirSync(PLUGINS_DIR)
  .filter((name) => statSync(join(PLUGINS_DIR, name)).isDirectory())
  .filter((name) => !NOT_PLUGINS.test(name))
  .sort();

for (const name of dirs) {
  const dir = join(PLUGINS_DIR, name);
  const manifestPath = join(dir, ".claude-plugin", "plugin.json");

  // --- registration -------------------------------------------------------
  // A plugin directory that is not in marketplace.json is not installable, and
  // nothing else in the repo notices. mockup-fidelity was rebuilt on
  // 2026-08-18 with a 474-line SKILL.md, a README and 53 tracked files, was
  // already listed in build-catalogue's GROUP_OF, and had no marketplace entry,
  // no root-README row and an empty assets/ directory. Four sibling skills
  // routed to it by name and resolved to a superseded copy in another
  // marketplace instead.
  if (!existsSync(manifestPath)) {
    fail(name, "manifest", `plugins/${name}/ has no .claude-plugin/plugin.json. If it is not a plugin, it does not belong under plugins/.`);
    continue;
  }

  const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  const entry = registered.get(name);

  for (const field of ["name", "description", "version", "author"]) {
    if (!manifest[field]) fail(name, "manifest", `plugin.json has no "${field}".`);
  }
  if (manifest.name !== name) {
    fail(name, "manifest", `plugin.json name "${manifest.name}" does not match its directory.`);
  }
  if (!entry) {
    fail(name, "registration", `not in .claude-plugin/marketplace.json, so it cannot be installed. Add { "name": "${name}", "source": "./plugins/${name}", "version": "${manifest.version}", "category": ... }.`);
  } else if (entry.version !== manifest.version) {
    fail(name, "registration", `plugin.json says ${manifest.version}, marketplace.json says ${entry.version}.`);
  }

  // --- root README row ----------------------------------------------------
  // build-catalogue checks the row exists. It cannot check the <br clear> that
  // has to precede it: the icon is floated left, so a row without one floats up
  // beside the previous entry's paragraph and renders as an overlapping mess.
  // That reads to a human as "my plugin isn't in the README" and no script has
  // ever caught it.
  const rowAnchor = `plugins/${name}/README.md`;
  const rowIndex = rootReadme.indexOf(`### [${name}](${rowAnchor})`);
  if (rowIndex === -1) {
    fail(name, "root-readme", `no "### [${name}](${rowAnchor})" row under "## The skills" in the root README.`);
  } else {
    const preceding = rootReadme.slice(Math.max(0, rowIndex - 400), rowIndex);
    if (rowIndex !== firstRowIndex && !preceding.includes('<br clear="left" />')) {
      fail(name, "root-readme", `its row is missing the <br clear="left" /> that must precede every entry after the first, so it will render overlapping the row above.`);
    }
    if (!preceding.includes(`plugins/${name}/assets/icon-256.png`)) {
      fail(name, "root-readme", `its row does not point at assets/icon-256.png. One filename for the shipped icon, so the README and the site cannot disagree.`);
    }
  }

  // --- icons --------------------------------------------------------------
  const iconSizes = { "icon.png": 1024, "icon-256.png": 256, "icon-128.png": 128 };
  for (const [file, expected] of Object.entries(iconSizes)) {
    const size = pngSize(join(dir, "assets", file));
    if (!size) fail(name, "icons", `assets/${file} is missing.`);
    else if (size.w !== expected || size.h !== expected) {
      fail(name, "icons", `assets/${file} is ${size.w}x${size.h}, expected ${expected}x${expected}.`);
    }
  }

  // --- icon audit sheet ---------------------------------------------------
  if (!QUICK) {
    if (!existsSync(join(dir, "assets", "audit.html"))) {
      fail(name, "audit-sheet", `no assets/audit.html. The sheet is the record of which takes were considered and why one shipped; without it the icon has no provenance.`);
    } else {
      try {
        execFileSync("python3", [AUDIT_SHEET, "check", join(dir, "assets")], { stdio: "pipe" });
      } catch (error) {
        const output = `${error.stdout || ""}${error.stderr || ""}`;
        const problems = output.split("\n").filter((line) => line.startsWith("FAIL")).map((l) => l.replace(/^FAIL\s+/, ""));
        fail(name, "audit-sheet", `audit_sheet.py check exits nonzero: ${problems.length ? problems.join(" | ") : output.trim().slice(0, 300)}`);
      }
    }
  }

  // --- banner -------------------------------------------------------------
  const bannerPath = join(dir, "assets", "banner.png");
  const bannerSize = pngSize(bannerPath);
  if (!bannerSize) {
    fail(name, "banner", `no assets/banner.png. Compose assets/banner-src.html and render it with create-skill's scripts/render_banner.py.`);
  } else if (bannerSize.w !== BANNER_W || bannerSize.h !== BANNER_H) {
    fail(name, "banner", `assets/banner.png is ${bannerSize.w}x${bannerSize.h}, and the family ships exactly ${BANNER_W}x${BANNER_H} (a 1600x520 layout at deviceScaleFactor 2).`);
  }
  if (bannerSize && !existsSync(join(dir, "assets", "banner-src.html")) && !existsSync(join(dir, "assets", "banner-src.svg"))) {
    fail(name, "banner", `has a rendered banner but no assets/banner-src, so it can never be edited again.`);
  }

  // --- banner reproducibility ---------------------------------------------
  // A banner is reproducible only when its wordmark face arrives with the
  // document. whats-left and test-campaign set theirs in Iowan Old Style
  // and Avenir Next, which are local macOS faces with nothing linked, so
  // re-rendering either on another machine or in CI silently substitutes a
  // different face and produces a different banner that still passes every
  // size and overflow assertion. The full 12-point rubric lives in
  // create-skill's scripts/banner_sheet.py; this is the subset a build can
  // decide without a person looking.
  const LOCAL_ONLY_FACES = /\b(Iowan Old Style|Palatino|Avenir|Segoe UI|Helvetica Neue|Lucida|Baskerville|Optima|Futura|Gill Sans)\b/i;
  const bannerSrc = [join(dir, "assets", "banner-src.html"), join(dir, "assets", "banner-src.svg")]
    .map((p) => read(p)).find(Boolean);
  if (bannerSrc) {
    const linksWebFont = /fonts\.googleapis\.com/.test(bannerSrc)
      || (/@font-face/.test(bannerSrc) && /url\(\s*['"]?data:/.test(bannerSrc));
    if (!linksWebFont) {
      const named = bannerSrc.match(LOCAL_ONLY_FACES);
      fail(name, "banner", `its banner-src links no web font${named ? ` and sets ${named[0]}` : ""}, so the wordmark is whatever the rendering machine happens to have installed. Link the face or inline it as a data URI.`);
    }
  }

  // --- README -------------------------------------------------------------
  const readmePath = join(dir, "README.md");
  const readme = read(readmePath);
  if (!readme) {
    fail(name, "readme", `no README.md.`);
  } else {
    const head = readme.split("\n").slice(0, 12).join("\n");
    if (!/banner\.(png|svg)/i.test(head)) {
      // A plugin whose banner is on the dated debt list cannot open with one, so
      // reporting the README separately double-counts a single accepted decision
      // and buries the eleven real README defects under nine consequences of it.
      // The banner entry is the debt; this follows it.
      if (debtFor(name, "banner")) {
        excused.push({
          plugin: name, dimension: "readme",
          message: "no banner image in the first 12 lines",
          ...debtFor(name, "banner"),
          why: `Follows the banner debt: ${debtFor(name, "banner").why}`,
        });
      } else {
        fail(name, "readme", `no banner image in the first 12 lines. Every README in this marketplace opens with one.`);
      }
    }
    if (!/img\.shields\.io/.test(readme.split("\n").slice(0, 24).join("\n"))) {
      fail(name, "readme", `no badges near the top.`);
    }
    if (!readme.includes(`/plugin marketplace add ${MARKETPLACE_SLUG}`)) {
      fail(name, "install", `install block does not read "/plugin marketplace add ${MARKETPLACE_SLUG}". A wrong owner here is a dead end for every reader who follows it.`);
    }
    if (!readme.includes(`/plugin install ${name}@${MARKETPLACE_NAME}`)) {
      fail(name, "install", `install block does not read "/plugin install ${name}@${MARKETPLACE_NAME}". Without the suffix the name is ambiguous when more than one marketplace is added.`);
    }
  }

  // --- evals --------------------------------------------------------------
  if (!findFirst(dir, (f) => /^evals.*\.json$/.test(f))) {
    fail(name, "evals", `no evals.json anywhere. The standard asks for 6 to 8 prompts with checkable assertions, including one adversarial case.`);
  }
  if (!findFirst(dir, (f) => f.toLowerCase() === "evals.md")) {
    fail(name, "evals", `no EVALS.md. If the evals have not been run, that file still ships and opens by saying so, listing what was verified mechanically and naming the tasks that would settle the rest. An unevaluated skill with that section is honest; one that omits the subject reads as though the pipeline ran.`);
  }

  // --- voice --------------------------------------------------------------
  for (const surface of voiceSurfaces(dir)) {
    const shown = surface.replace(`${REPO_DIR}/`, "");
    const count = countEmDashes(readFileSync(surface, "utf8"));
    if (count > 0) {
      fail(name, "voice", `${shown} carries ${count} em dash${count === 1 ? "" : "es"}. The ban covers body text, headings, alt text and table cells.`);
    }
    if (VOICE_LINT) {
      try {
        execFileSync("python3", [VOICE_LINT, "--format", "marketing", surface], { stdio: "pipe" });
      } catch (error) {
        const out = `${error.stdout || ""}${error.stderr || ""}`;
        const hard = out.split("\n").filter((l) => /^(fail|error)/i.test(l.trim())).slice(0, 4);
        fail(name, "voice", `${shown} fails voice_lint --format marketing: ${hard.length ? hard.join(" | ") : out.trim().slice(0, 200)}`);
      }
    }
  }

  // --- SKILL.md -----------------------------------------------------------
  // Two layouts in the repo: skills/<name>/SKILL.md for most, and SKILL.md at
  // the plugin root for braindump. The site indexes exactly one per plugin.
  const skillPath = [join(dir, "skills", name, "SKILL.md"), join(dir, "SKILL.md")].find((p) => existsSync(p));
  if (!skillPath) {
    fail(name, "skill", `no skills/${name}/SKILL.md.`);
  } else {
    // A newline-terminated file ends with an empty final element, which is a line
    // terminator rather than a line. Counting it reported a 500-line SKILL.md as 501
    // and failed a file that sat exactly on the ceiling.
    const lines = readFileSync(skillPath, "utf8").replace(/\n$/, "").split("\n").length;
    if (lines > SKILL_MAX_LINES) {
      fail(name, "skill", `${skillPath.replace(`${REPO_DIR}/`, "")} is ${lines} lines against a ${SKILL_MAX_LINES}-line ceiling. Push depth into references/ rather than trimming substance.`);
    }
  }
}

// --- repo-level -------------------------------------------------------------

/**
 * Whether any two icons read as each other on a shelf. This is a set property, so
 * no per-plugin rubric can see it: the 12-point icon rubric scores the tile in
 * front of you and never asks whether that tile already exists, which is how
 * better-loop and better-goal both scored 11/12 as the same cream dial.
 *
 * shelf_check carries its own DECIDED list of pairs somebody has looked at and
 * ruled on, so this fails only on a collision nobody has judged yet.
 */
if (!QUICK && existsSync(SHELF_CHECK)) {
  try {
    execFileSync("python3", [SHELF_CHECK, REPO_DIR], { stdio: "pipe" });
  } catch (error) {
    const out = `${error.stdout || ""}${error.stderr || ""}`;
    const pairs = out.split("\n").filter((l) => l.includes("FLAG")).map((l) => l.trim().replace(/\s+/g, " "));
    failures.push({
      plugin: "(set)", dimension: "shelf",
      message: `icons read as each other at 16px and nobody has ruled on it: ${pairs.join("; ") || out.trim().slice(0, 300)}. Look at each pair side by side, then either differentiate one or add it to shelf_check's DECIDED list with the reason.`,
    });
  }
}


const rootEmDashes = countEmDashes(rootReadme);if (rootEmDashes > 0) {
  failures.push({ plugin: "(root)", dimension: "voice", message: `README.md carries ${rootEmDashes} em dashes.` });
}

const badgeMatch = rootReadme.match(/badge\/skills-(\d+)-/);
if (!badgeMatch) {
  failures.push({ plugin: "(root)", dimension: "root-readme", message: `no "skills-N" badge found.` });
} else if (Number(badgeMatch[1]) !== registered.size) {
  failures.push({
    plugin: "(root)", dimension: "root-readme",
    message: `the badge says ${badgeMatch[1]} skills and marketplace.json registers ${registered.size}. This is the first number a visitor reads.`,
  });
}

for (const name of registered.keys()) {
  if (!dirs.includes(name)) {
    failures.push({ plugin: name, dimension: "registration", message: `registered in marketplace.json with no plugins/${name}/ directory.` });
  }
}

// --- report -----------------------------------------------------------------

if (AS_JSON) {
  console.log(JSON.stringify({ plugins: dirs.length, registered: registered.size, failures, excused }, null, 2));
} else {
  const byPlugin = new Map();
  for (const f of failures) {
    if (!byPlugin.has(f.plugin)) byPlugin.set(f.plugin, []);
    byPlugin.get(f.plugin).push(f);
  }

  for (const [plugin, items] of [...byPlugin].sort((a, b) => b[1].length - a[1].length)) {
    console.error(`\n${plugin}  (${items.length})`);
    for (const item of items) console.error(`  ${item.dimension.padEnd(13)} ${item.message}`);
  }

  if (excused.length) {
    console.log(`\nExcused by the dated debt list (${excused.length}):`);
    for (const item of excused) {
      console.log(`  ${item.plugin.padEnd(26)} ${item.dimension.padEnd(8)} owed since ${item.since}`);
    }
  }

  const clean = dirs.length - byPlugin.size + (byPlugin.has("(root)") ? 1 : 0);
  console.log(`\ncheck-conformance: ${dirs.length} plugins, ${registered.size} registered, ${clean} fully conformant, ${failures.length} failures across ${byPlugin.size} names, ${excused.length} excused.`);
  console.log(VOICE_LINT
    ? `  voice: em dashes plus voice_lint --format marketing (${VOICE_LINT.replace(process.env.HOME || "", "~")})`
    : `  voice: em dashes only. voice_lint.py was not found, so the fuller lint brand-and-docs.md prescribes did NOT run. It ships with the create-luke-content plugin.`);
}

process.exit(failures.length ? 1 : 0);

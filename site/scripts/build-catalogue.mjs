#!/usr/bin/env node
/**
 * Build the skill catalogue from the repository itself.
 *
 * Runs before `next dev` and `next build`. Reads ../.claude-plugin/marketplace.json
 * as the source of truth (never `ls ../plugins` — the two `*-workspace` scratch
 * directories would otherwise read as plugins), then pulls each plugin's manifest,
 * SKILL.md, README and icon, and writes:
 *
 *   lib/catalogue.json     the typed catalogue every page and the search route reads
 *   public/icons/<n>.png   the 256px icons, copied because Next can't serve files
 *                          from above the app root
 *
 * It throws on a missing SKILL.md, a missing icon, or a missing banner (except
 * for the named BANNER_DEBT list). All of those fail silently
 * today — CLAUDE.md documents the broken-image case as a known trap — so this turns
 * them into a red build.
 */

import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { parse as parseYaml } from "yaml";

const SITE_DIR = dirname(dirname(fileURLToPath(import.meta.url)));
const REPO_DIR = dirname(SITE_DIR);
const MARKETPLACE = join(REPO_DIR, ".claude-plugin", "marketplace.json");
const ROOT_README = join(REPO_DIR, "README.md");
const OUT_CATALOGUE = join(SITE_DIR, "lib", "catalogue.json");
const OUT_ICONS = join(SITE_DIR, "public", "icons");
const OUT_BANNERS = join(SITE_DIR, "public", "banners");

const MARKETPLACE_NAME = "fledgeling-plugins";

/**
 * Facets. marketplace.json gives every plugin `category: "development"`, which
 * groups nothing, so the browse axis is defined here instead: what you are trying
 * to do, not what kind of artifact the skill is.
 *
 * A plugin missing from this map still ships — it lands under "Uncategorised" and
 * warns — because the site auto-indexing a newly added skill matters more than the
 * facet being complete on day one.
 */
const GROUPS = [
  { id: "making", label: "Making something",
    blurb: "Design it, write it, or build it from nothing." },
  { id: "checking", label: "Checking it before anyone sees it",
    blurb: "Catch the problems while they are still cheap to fix." },
  { id: "backlog", label: "Handing over a pile of work",
    blurb: "Give Claude a list and let it work through it on its own." },
  { id: "standing", label: "Knowing where things stand",
    blurb: "What is finished, what is not, and what nobody has actually checked." },
  { id: "long-runs", label: "Keeping a long job alive",
    blurb: "For work that outlasts one sitting, one usage limit, or one crash." },
  { id: "asking", label: "Fewer interruptions",
    blurb: "When Claude should ask you, which AI answers, and what it all costs." },
  { id: "authoring", label: "Making your own skills",
    blurb: "Turn something you do often into a skill you can reuse." },
  { id: "sending", label: "Sending things to people",
    blurb: "Work that leaves your machine and reaches somebody." },
  { id: "machine", label: "Looking after your Mac",
    blurb: "Stop it grinding to a halt while all this is running." },
];

const GROUP_OF = {
  // Making something.
  "design-craft": "making", "ux-craft": "making", "mac-craft": "making", "tui-craft": "making",
  "deck-craft": "making", "create-mac-icon": "making", "agent-voice": "making",
  "generate-investor-portal": "making", "create-swe-project": "making", "launch-craft": "making",
  eli5: "making",

  // Checking it before anyone sees it.
  "design-review": "checking", "be-my-witness": "checking", "mockup-fidelity": "checking",
  "code-review": "checking", "test-campaign": "checking", warrant: "checking",
  proctor: "checking", vouch: "checking", tailings: "checking",

  // Handing over a pile of work.
  shipyard: "backlog", "ship-feature": "backlog", "ship-fleet": "backlog",
  "ship-armada": "backlog", flagship: "backlog", "armada-sync": "backlog",
  "anvil-errand": "backlog", "atlas-publish": "backlog",

  // Knowing where things stand.
  reckon: "standing", "whats-left": "standing", stocktake: "standing", report: "standing",
  "dossier-report": "standing", trawl: "standing", positioning: "standing",

  // Keeping a long job alive.
  "better-goal": "long-runs", "better-loop": "long-runs", "should-compact": "long-runs",
  "resume-session": "long-runs", "recover-claude-code": "long-runs", braindump: "long-runs",

  // Fewer interruptions.
  clarify: "asking", defer: "asking", discipline: "asking",

  // Making your own skills.
  "create-skill": "authoring", "improve-skill": "authoring", geminify: "authoring",

  // Sending things to people.
  "email-digest": "sending", "mac-design-digest": "sending",

  // Looking after your Mac.
  harbourmaster: "machine", "mac-doctor": "machine",
};

const UNCATEGORISED = {
  id: "uncategorised",
  label: "Uncategorised",
  blurb: "Added to the marketplace but not yet placed on the browse axis.",
};

// --------------------------------------------------------------------- utils --

function fail(message) {
  console.error(`\n  build-catalogue: ${message}\n`);
  process.exit(1);
}

function readIfExists(path) {
  return existsSync(path) ? readFileSync(path, "utf8") : null;
}

/**
 * Does this skill hand work to another model through `defer`?
 *
 * Matched on the routing idioms rather than the English word, because "defer to
 * a human", "defers to it" and Swift's `defer:` are all common in these files
 * and none of them is a model lane. A wrong pill is a false claim on a public
 * page, so this is deliberately narrow: it wants defer's own script, its slash
 * form, its skills path, or the skill named in backticks.
 */
function usesDefer(dir, name) {
  if (name === "defer") return false; // it IS the lane; a pill would be circular
  const skillsDir = join(dir, "skills");
  if (!existsSync(skillsDir)) return false;
  const NEEDLES = [/lane_pick\.py/, /\/defer:defer/, /`defer`/, /skills\/defer/];
  const walk = (dir) => {
    for (const item of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, item.name);
      if (item.isDirectory()) {
        if (walk(full)) return true;
        continue;
      }
      if (!/\.(md|py|sh|mjs|js|ts)$/.test(item.name)) continue;
      const body = readFileSync(full, "utf8");
      if (NEEDLES.some((n) => n.test(body))) return true;
    }
    return false;
  };
  return walk(skillsDir);
}

function countFiles(dir) {
  if (!existsSync(dir)) return 0;
  let total = 0;
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    total += statSync(full).isDirectory() ? countFiles(full) : 1;
  }
  return total;
}

/**
 * Split YAML frontmatter off a markdown file.
 *
 * Strict YAML first, because 4 of the 16 descriptions are folded block scalars
 * (`description: >`) spanning many lines and a regex would mangle them. But at
 * least one SKILL.md (trawl) carries a plain scalar containing `: ` — "Tier
 * flags: --any (cheap)" — which YAML 1.2 does not allow, so a strict parse
 * throws on a file Claude Code itself loads happily. Falling back to a
 * line-oriented reader keeps the build honest about what is in the repo rather
 * than failing on it.
 */
function splitFrontmatter(source, label) {
  if (!source.startsWith("---")) return { data: {}, body: source };
  const end = source.indexOf("\n---", 3);
  if (end === -1) return { data: {}, body: source };
  const raw = source.slice(source.indexOf("\n") + 1, end);
  const body = source.slice(source.indexOf("\n", end + 1) + 1);
  try {
    return { data: parseYaml(raw) ?? {}, body };
  } catch {
    return { data: parseLooseFrontmatter(raw, label), body };
  }
}

/**
 * Tolerant `key: value` reader for frontmatter YAML rejects. Splits on the first
 * `: ` of each unindented line so a colon inside the value is just text, and
 * gathers indented continuations under a `>` or `|` block scalar.
 */
function parseLooseFrontmatter(raw, label) {
  const data = {};
  const lines = raw.split("\n");
  let key = null;
  let buffer = [];

  const flush = () => {
    if (key) data[key] = buffer.join(" ").replace(/\s+/g, " ").trim();
    key = null;
    buffer = [];
  };

  for (const line of lines) {
    if (/^\s/.test(line) || line.trim() === "") {
      if (key) buffer.push(line.trim());
      continue;
    }
    flush();
    const separator = line.indexOf(":");
    if (separator === -1) continue;
    key = line.slice(0, separator).trim();
    const value = line.slice(separator + 1).trim();
    buffer = value === ">" || value === "|" || value === ">-" || value === "|-" ? [] : [value];
  }
  flush();

  looseParses.push(label);
  return data;
}

/** Files whose frontmatter needed the tolerant reader — reported at the end. */
const looseParses = [];

/**
 * Pull the example invocations out of a trigger description.
 *
 * Every SKILL.md description quotes the phrases that make the skill fire —
 * "set a goal to ship the rest of the backlog", "my UI looks AI-generated",
 * "/report". They are the author's own words for what a person would say, which
 * makes them the honest source of example prompts: nothing here is written for
 * the website.
 */
function extractExamplePrompts(trigger) {
  const quoted = [...trigger.matchAll(/["“‘]([^"”’]{4,90})["”’]/g)].map((match) => match[1].trim());

  const seen = new Set();
  const prompts = [];

  for (const phrase of quoted) {
    // Scare quotes around a single word ("just", "quick") are not invocations.
    const words = phrase.split(/\s+/).length;
    if (words < 2 && !phrase.startsWith("/")) continue;
    // Nor are parenthetical asides or fragments that only make sense in context.
    if (/^(and|or|but|not|use)\b/i.test(phrase)) continue;

    const key = phrase.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    prompts.push(phrase);
  }

  return prompts.slice(0, 6);
}

/**
 * Pull the boundary clause out of a SKILL.md trigger description.
 *
 * Nine of the sixteen end with an explicit "NOT for X (use Y)". It is the most
 * disambiguating sentence each skill owns and nothing renders it today — not the
 * README, not the marketplace, not the plugin manager. It also yields the
 * near-neighbour graph for free, including the cases where the named alternative
 * lives in a different marketplace and cannot be installed from here.
 */
function extractBoundary(trigger) {
  const match = trigger.match(/((?:NOT|Not)\s+(?:for|a\b|to\b)[\s\S]*)$/);
  if (!match) return null;

  // Take to the end of the sentence, tolerating the parenthesised "(use X)"
  // asides that carry the referrals.
  let text = match[1];
  let depth = 0;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (char === "(") depth += 1;
    else if (char === ")") depth -= 1;
    else if (char === "." && depth === 0) {
      text = text.slice(0, index + 1);
      break;
    }
  }

  const referrals = [...text.matchAll(/\buse\s+([a-z][a-z0-9-]*(?:-[a-z0-9]+)*)/gi)].map((m) => m[1]);
  return { text: text.trim(), referrals: [...new Set(referrals)] };
}



/**
 * Pull the paragraph the root README writes under each skill's heading. It is the
 * best-written one-liner in the repo — better than both the plugin.json capability
 * blurb and the SKILL.md trigger description — so it becomes the card copy.
 */
function blurbsFromRootReadme(source) {
  const blurbs = {};
  // Trailing content after the link is allowed so a row can carry a marker
  // (e.g. "· **Uses multiple models**") without becoming invisible to the gate.
  const heading = /^### \[([^\]]+)\]\(plugins\/[^)]+\).*$/gm;
  let match;
  while ((match = heading.exec(source)) !== null) {
    const rest = source.slice(match.index + match[0].length);
    // Everything up to the next entry's separator, image anchor or heading.
    // `##` matters as much as `###`: the last entry in a group is followed by
    // the next GROUP heading, and without it that entry's blurb swallowed the
    // heading, its blurb, and (for the final entry) the whole page footer. It
    // stayed invisible while descriptions were long enough for the extra to
    // look like more of the same paragraph.
    const stop = rest.search(/\n(?:<br clear="left" \/>|<a href=|#{2,3} )/);
    const paragraph = (stop === -1 ? rest : rest.slice(0, stop)).trim();
    if (paragraph) blurbs[match[1]] = paragraph.replace(/\s+/g, " ");
  }
  return blurbs;
}

/**
 * Strip the header chrome from a plugin README so the detail page renders the
 * prose only. The page already shows the icon, name, version and blurb; repeating
 * the banner, the h1 and the shields row would say all of it twice.
 *
 * The shapes vary across the 16 (centred vs left h1, `<h1><img>` vs `# name`,
 * badges in a `<p align="center">` vs a bare `<p>`), so this trims known chrome
 * from the top rather than pattern-matching one layout.
 */
function stripReadmeChrome(source) {
  const lines = source.split("\n");
  let cursor = 0;

  const isChrome = (line) => {
    const trimmed = line.trim();
    if (trimmed === "" || trimmed === "---") return true;
    if (/^<\/?p[\s>]/.test(trimmed)) return true;
    if (/^<img\s/.test(trimmed)) return true;
    if (/^<h1[\s>]/.test(trimmed) || /^<\/h1>/.test(trimmed)) return true;
    if (/^#\s/.test(trimmed)) return true;
    if (/^<a\s/.test(trimmed) || trimmed === "</a>") return true;
    // A lone paragraph made only of shields.io badges.
    if (/^!?\[?[^\]]*\]?\(?https:\/\/img\.shields\.io/.test(trimmed)) return true;
    return false;
  };

  // Consume chrome until the first line of real prose, then stop — a `---` or an
  // `<img>` deeper in the document is content, not a header.
  while (cursor < lines.length && isChrome(lines[cursor])) cursor += 1;

  // If the first prose line is immediately followed by more badge chrome (the
  // "tagline then shields" layout), skip that block too.
  let lookahead = cursor;
  while (lookahead < lines.length && !/^##\s/.test(lines[lookahead].trim())) {
    if (lines[lookahead].includes("img.shields.io")) {
      lookahead += 1;
      while (lookahead < lines.length && isChrome(lines[lookahead])) lookahead += 1;
      cursor = lookahead;
      continue;
    }
    lookahead += 1;
    if (lookahead - cursor > 12) break;
  }

  return lines.slice(cursor).join("\n").trim();
}

/**
 * Replace mermaid blocks with a pointer to the rendered diagram.
 *
 * Eight of the sixteen READMEs carry exactly one mermaid flowchart. GitHub
 * renders those; a markdown renderer without the library shows the source, which
 * is forty lines of `A --> B` a reader cannot use. Shipping mermaid to draw two
 * diagrams costs more than the diagrams are worth here, so the block becomes a
 * link to where it does render.
 */
function replaceMermaid(markdown, pluginName) {
  const readme = `https://github.com/fledgeling-co/fledgeling-plugins/blob/main/plugins/${pluginName}/README.md`;
  return markdown.replace(
    /```mermaid\n[\s\S]*?\n```/g,
    `> **A flow diagram sits here.** It needs a renderer this page deliberately does not ship — [see it drawn on GitHub](${readme}).`,
  );
}

/** Rewrite repo-relative links so they resolve on GitHub rather than 404 here. */
function absolutiseLinks(markdown, pluginName) {
  const base = `https://github.com/fledgeling-co/fledgeling-plugins/blob/main/plugins/${pluginName}/`;
  const raw = `https://raw.githubusercontent.com/fledgeling-co/fledgeling-plugins/main/plugins/${pluginName}/`;
  return markdown
    .replace(/!\[([^\]]*)\]\((?!https?:|\/)([^)]+)\)/g, (_m, alt, href) => `![${alt}](${raw}${href})`)
    .replace(/\[([^\]]*)\]\((?!https?:|#|\/)([^)]+)\)/g, (_m, text, href) => `[${text}](${base}${href})`)
    .replace(/<img\s+src="(?!https?:|\/)([^"]+)"/g, (_m, src) => `<img src="${raw}${src}"`)
    // GitHub's alert syntax renders as a literal "[!NOTE]" outside GitHub. Turn
    // the marker into the bold lead-in it is actually standing in for.
    .replace(/^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$/gim, (_m, kind) => {
      const label = kind.charAt(0) + kind.slice(1).toLowerCase();
      return `> **${label}**`;
    });
}

// --------------------------------------------------------------------- build --

function build() {
  const marketplaceRaw = readIfExists(MARKETPLACE);
  if (!marketplaceRaw) fail(`${MARKETPLACE} not found — is the site still inside the plugins repo?`);
  const marketplace = JSON.parse(marketplaceRaw);

  const rootReadme = readIfExists(ROOT_README);
  if (!rootReadme) fail("root README.md not found");
  const blurbs = blurbsFromRootReadme(rootReadme);

  mkdirSync(OUT_ICONS, { recursive: true });
  mkdirSync(OUT_BANNERS, { recursive: true });
  mkdirSync(dirname(OUT_CATALOGUE), { recursive: true });

  const warnings = [];
  const skills = marketplace.plugins.map((entry) => {
    const name = entry.name;
    const dir = join(REPO_DIR, entry.source.replace(/^\.\//, ""));

    if (!existsSync(dir)) fail(`${name}: marketplace points at ${entry.source}, which does not exist`);

    // --- manifest -----------------------------------------------------------
    const manifestRaw = readIfExists(join(dir, ".claude-plugin", "plugin.json"));
    if (!manifestRaw) fail(`${name}: missing .claude-plugin/plugin.json`);
    const manifest = JSON.parse(manifestRaw);
    if (manifest.version !== entry.version) {
      fail(
        `${name}: version mismatch — plugin.json says ${manifest.version}, marketplace.json says ${entry.version}`,
      );
    }

    // --- SKILL.md -----------------------------------------------------------
    // Two layouts in the repo: skills/<name>/SKILL.md for fifteen of them, and
    // SKILL.md at the plugin root for braindump.
    const skillCandidates = [join(dir, "skills", name, "SKILL.md"), join(dir, "SKILL.md")];
    const skillPath = skillCandidates.find((candidate) => existsSync(candidate));
    if (!skillPath) {
      fail(`${name}: no SKILL.md at skills/${name}/SKILL.md or the plugin root`);
    }
    const { data: frontmatter } = splitFrontmatter(readFileSync(skillPath, "utf8"), name);
    const trigger = typeof frontmatter.description === "string" ? frontmatter.description.replace(/\s+/g, " ").trim() : "";
    if (!trigger) fail(`${name}: SKILL.md has no description in its frontmatter`);

    // --- icon ---------------------------------------------------------------
    // One filename, no candidates. This used to prefer create-skill's
    // icon-c1-256.png, on the belief that it was that plugin's published icon
    // because the root README pointed at it. Both were wrong: create-skill's own
    // assets/icon-notes.md scores take A (the layered icon.svg) at 11/12 and
    // "ships", and take C1 at 9/12, failing check #10 as, in its words, "a flat
    // raster is failure mode #10 by construction, whatever it scores". So the
    // special case made the site serve a losing take, and the README agreed with
    // it rather than with the audit sheet. If a plugin's winning take is a
    // raster, promote it to icon-256.png rather than teaching this loader a
    // second filename.
    const iconPath = join(dir, "assets", "icon-256.png");
    if (!existsSync(iconPath)) fail(`${name}: no assets/icon-256.png — the card would render a broken image`);
    copyFileSync(iconPath, join(OUT_ICONS, `${name}.png`));

    // --- email banner derivatives -------------------------------------------
    // Optional, and served rather than generated here: this script has no image
    // library, and the source banner is 3200x1040 at ~660KB, which is a fine web
    // asset and a bad email one. A plugin that wants to appear with imagery in a
    // digest ships assets/banner-email-<width>.png alongside its banner, made
    // with email-digest's scripts/email_assets.py. Absent one, the digest simply
    // renders that item without a banner, which every tier already supports.
    for (const width of [1072, 720]) {
      const src = join(dir, "assets", `banner-email-${width}.png`);
      if (existsSync(src)) copyFileSync(src, join(OUT_BANNERS, `${name}-${width}.png`));
    }

    // The same argument one size down. A digest's tail carries an icon per row,
    // and pointing eighteen of those at the 256px card icon costs the recipient
    // most of a megabyte to render a 24px square. The 48px derivative is ~3KB.
    const iconEmail = join(dir, "assets", "icon-email-48.png");
    if (existsSync(iconEmail)) copyFileSync(iconEmail, join(OUT_ICONS, `${name}-48.png`));

    // --- banner -------------------------------------------------------------
    // Every plugin README in this marketplace opens with assets/banner.png, and
    // until this check existed nothing anywhere verified it. tui-craft shipped
    // with a complete icon set, an audit sheet, a README, a root-README row and
    // no banner at all: the catalogue built, the site deployed, and the only
    // symptom was a README that opened on a heading. The registration checklist
    // in the repo's CLAUDE.md does not contain the word "banner" either, which
    // is why prose was never going to catch this.
    //
    // BANNER_DEBT is a named, dated list rather than a silent exemption.
    // Adding a name here is a deliberate act that shows up in review. Removing
    // one is the fix, and on 2026-08-19 the list emptied: the two names that
    // predated the check and all six of the diolog-plugins migration plugins now
    // ship composed banners with signed verdicts. It is kept, empty, because the
    // mechanism is what stops the next missing banner being invisible, and
    // because an empty list is a stronger statement than a deleted one.
    const BANNER_DEBT = new Set([]);
    const bannerPath = join(dir, "assets", "banner.png");
    if (!existsSync(bannerPath)) {
      if (BANNER_DEBT.has(name)) {
        warnings.push(`${name}: no assets/banner.png — on the named banner-debt list`);
      } else {
        fail(`${name}: no assets/banner.png — every plugin README in this ` +
             `marketplace opens with one, and a missing banner is invisible ` +
             `to every other check. Compose assets/banner-src.html and render ` +
             `it with create-skill's scripts/render_banner.py, which asserts ` +
             `the 3200x1040 size, that the web font loaded, and that no ` +
             `artwork silently failed to load.`);
      }
    }

    // --- README -------------------------------------------------------------
    const readmeRaw = readIfExists(join(dir, "README.md"));
    if (!readmeRaw) fail(`${name}: missing README.md`);
    const readme = absolutiseLinks(replaceMermaid(stripReadmeChrome(readmeRaw), name), name);

    // The root-README row is a deliverable, not a nicety: it is the best-written
    // one-liner in the repo and it becomes the card copy. It was a warning until
    // 2026-08-18, and a warning is not a gate — a real pipeline run shipped a
    // complete plugin with no row and nothing objected, because the fallback to
    // plugin.json makes the omission invisible. Same shape as BANNER_DEBT above:
    // an existing offender is named with a date, a new one fails.
    const ROW_DEBT = new Set([
      // Empty on purpose. Every listed plugin had a row when this became a gate.
      // Add a name here with a date rather than reverting the check.
    ]);
    const blurb = blurbs[name];
    if (!blurb) {
      if (ROW_DEBT.has(name)) {
        warnings.push(`${name}: no entry under "## The skills" in the root README — on the named row-debt list, falling back to plugin.json`);
      } else {
        fail(`${name}: no entry under "## The skills" in the root README. ` +
             `Add a row — icon anchor, "### [${name}](plugins/${name}/README.md)", ` +
             `and one paragraph of card copy. Without it the catalogue falls ` +
             `back to plugin.json, so the omission renders as a plausible card ` +
             `and nothing else in this build notices.`);
      }
    }

    // --- signals ------------------------------------------------------------
    const skillRoot = skillPath === skillCandidates[0] ? join(dir, "skills", name) : dir;
    const evalsPath = [join(dir, "EVALS.md"), join(dir, "evals", "EVALS.md")].find((p) => existsSync(p));
    const referenceCount = countFiles(join(skillRoot, "references"));
    const hasScripts = existsSync(join(skillRoot, "scripts"));

    const group = GROUP_OF[name] ?? UNCATEGORISED.id;
    if (group === UNCATEGORISED.id) {
      warnings.push(`${name}: no group in GROUP_OF — showing under "Uncategorised"`);
    }

    return {
      name,
      version: entry.version,
      group,
      groupLabel: (GROUPS.find((g) => g.id === group) ?? UNCATEGORISED).label,
      // Capability prose, written for a catalogue reader.
      description: entry.description,
      // Trigger prose from SKILL.md — "Use this whenever…", "NOT for…". This is
      // the language a search query actually rhymes with.
      trigger,
      // The root README paragraph: the best short copy in the repo.
      blurb: blurb ?? entry.description,
      readme,
      license: frontmatter.license ?? manifest.license ?? "MIT",
      keywords: manifest.keywords ?? [],
      allowedTools: frontmatter["allowed-tools"] ?? null,
      // The trigger's own "NOT for X (use Y)" clause. Resolved against the
      // catalogue below, so the site can say which alternatives are installable
      // from here and which live in another marketplace.
      boundary: extractBoundary(trigger),
      // The author's own quoted trigger phrases — what a person actually says to
      // make this fire. Extracted, never written for the site.
      examplePrompts: extractExamplePrompts(trigger),
      icon: `/icons/${name}.png`,
      install: `/plugin install ${name}@${MARKETPLACE_NAME}`,
      repoUrl: `https://github.com/fledgeling-co/fledgeling-plugins/tree/main/plugins/${name}`,
      signals: {
        evals: Boolean(evalsPath),
        evalsUrl: evalsPath
          ? `https://github.com/fledgeling-co/fledgeling-plugins/blob/main/${evalsPath.slice(REPO_DIR.length + 1)}`
          : null,
        scripts: hasScripts,
        references: referenceCount,
        defer: usesDefer(dir, name),
      },
    };
  });

  const usedGroups = new Set(skills.map((skill) => skill.group));
  const groups = [...GROUPS, UNCATEGORISED]
    .filter((group) => usedGroups.has(group.id))
    .map((group) => ({ ...group, count: skills.filter((skill) => skill.group === group.id).length }));

  // Resolve each boundary's referrals now the whole catalogue is known. A skill
  // named as the alternative but absent from this marketplace is the case worth
  // flagging: installing the named skill from here is not possible, and a visitor
  // who does not learn that finds out when it fails to run.
  const known = new Set(skills.map((skill) => skill.name));
  const neighbours = new Map(skills.map((skill) => [skill.name, new Set()]));

  for (const skill of skills) {
    if (!skill.boundary) continue;
    skill.boundary.referrals = skill.boundary.referrals.map((target) => {
      const here = known.has(target);
      if (here) {
        neighbours.get(skill.name).add(target);
        neighbours.get(target).add(skill.name);
      }
      return { name: target, here };
    });
  }

  for (const skill of skills) {
    skill.neighbours = [...neighbours.get(skill.name)];
  }

  const withBoundary = skills.filter((skill) => skill.boundary).length;
  const elsewhere = new Set(
    skills.flatMap((skill) => (skill.boundary?.referrals ?? []).filter((r) => !r.here).map((r) => r.name)),
  );


  const catalogue = {
    marketplace: MARKETPLACE_NAME,
    repo: "fledgeling-co/fledgeling-plugins",
    generatedFrom: ".claude-plugin/marketplace.json",
    groups,
    skills,
  };

  writeFileSync(OUT_CATALOGUE, `${JSON.stringify(catalogue, null, 2)}\n`);

  for (const warning of warnings) console.warn(`  build-catalogue: ${warning}`);
  if (looseParses.length > 0) {
    console.warn(
      `  build-catalogue: frontmatter is not valid YAML in ${looseParses.join(", ")} — read with the tolerant parser`,
    );
  }
  console.log(
    `  build-catalogue: ${skills.length} skills, ${groups.length} groups, ${skills.length} icons -> public/icons/`,
  );
  console.log(
    `  build-catalogue: ${withBoundary} carry a "NOT for" boundary; ${elsewhere.size} referrals point outside this marketplace (${[...elsewhere].join(", ")})`,
  );
}

build();

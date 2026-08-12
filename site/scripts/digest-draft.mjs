/**
 * Write the email copy for any newly published skill.
 *
 * This is the half of the pipeline that cannot run on Vercel: the copy is
 * written by the Claude CLI through create-luke-content, so it runs here, on
 * push, against Luke's own subscription.
 *
 * A skill is "new" when the catalogue has it and this collection does not. The
 * unique index on `skill` is what makes that safe to run twice: a re-push, a
 * retried hook or a second terminal all collide on the index and write nothing
 * rather than queueing a duplicate announcement.
 *
 * Nothing here sends. Drafts wait for `pnpm digest:approve` until the first
 * issue has been approved, after which they go straight to `ready` and the
 * scheduled send picks them up at 10am Sydney time.
 */

import { spawnSync } from "node:child_process";
import {
  connect,
  items,
  readSettings,
  loadCatalogue,
  installLine,
  skillUrl,
  iconUrl,
  fail,
  REPO_DIR,
} from "./digest-lib.mjs";

const SCHEMA = JSON.stringify({
  type: "object",
  properties: {
    subject: {
      type: "string",
      description:
        "Email subject line for an announcement of this one skill. Catchy, and unmistakably about a new skill. Under 70 characters.",
    },
    headline: {
      type: "string",
      description:
        "A short line naming what this skill gets you. Under 60 characters. Not a restatement of the subject.",
    },
    body: {
      type: "string",
      description:
        "Two or three sentences on why this skill exists and what it does, grounded only in the supplied material. Luke's voice. Plain text, no markdown.",
    },
  },
  required: ["subject", "headline", "body"],
  additionalProperties: false,
});

// What create-luke-content's own lint needs, and nothing more. Bypassing
// permissions wholesale would let an unattended run touch anything on the disk;
// this lets it read the repo and run its Python linter.
const ALLOWED_TOOLS = "Read,Glob,Grep,Bash(python3:*),Bash(python3 *)";

function brief(skill) {
  return `/create-luke-content:create-luke-content Write the announcement copy for one newly published skill. Route as marketing.

This is a single section of a digest email that goes to people who asked to hear when a new skill lands on skills.fledgeling.app, Fledgeling's directory of SWE Skills for Claude Code, built and used daily by Luke. Return three fields through the structured output tool: subject, headline, body.

Ground everything in the material below and invent nothing. The point of the copy is the reason the skill exists, which is what the trigger and README already say; do not add a benefit, a statistic, a use case or an opinion that is not in there.

Site voice for reference: the hero reads "Skills built because a real workflow needed them." and "Each one exists because something kept going wrong, and each carries its own README, evals or references where the work justified them."

Constraints. The subject must be catchy and still leave no doubt the email is about a new skill; a reader scanning an inbox should know what it is without opening it. The headline is a different sentence from the subject, not a rewording. The body is two or three sentences, plain text, no markdown, no bullet list, no heading. This is chrome inside an email, not an article, so it stays tight. No hype, no salesy call to action, no em dash.

--- SKILL: ${skill.name} (v${skill.version}) ---

WHAT IT DOES (from marketplace.json):
${skill.description}

WHEN IT FIRES (the SKILL.md trigger, which is where the reason it exists usually lives):
${skill.trigger}

THE ONE-PARAGRAPH BLURB (the best short copy the repo has for it):
${skill.blurb}

README (truncated):
${(skill.readme ?? "").slice(0, 6000)}
--- END ---`;
}

function writeCopy(skill) {
  const result = spawnSync(
    "claude",
    [
      "--model",
      "claude-sonnet-5",
      "--effort",
      "high",
      "-p",
      brief(skill),
      "--allowedTools",
      ALLOWED_TOOLS,
      "--output-format",
      "json",
      "--json-schema",
      SCHEMA,
    ],
    { cwd: REPO_DIR, encoding: "utf8", maxBuffer: 32 * 1024 * 1024, stdio: ["ignore", "pipe", "pipe"] },
  );

  if (result.error) return { error: `could not run the claude CLI: ${result.error.message}` };
  if (result.status !== 0) {
    return { error: `claude exited ${result.status}: ${(result.stderr ?? "").trim().slice(0, 400)}` };
  }

  let envelope;
  try {
    envelope = JSON.parse(result.stdout);
  } catch {
    return { error: `claude returned something that is not JSON: ${result.stdout.slice(0, 200)}` };
  }
  if (envelope.is_error) return { error: `claude reported an error: ${envelope.result}` };

  const copy = envelope.structured_output;
  if (!copy) return { error: "claude returned no structured output" };

  for (const field of ["subject", "headline", "body"]) {
    const value = copy[field];
    if (typeof value !== "string" || value.trim().length === 0) {
      return { error: `the ${field} came back empty` };
    }
    // The voice skill's lint bans this and it is the rule Luke cares about
    // most, so it is checked again here rather than trusted.
    if (value.includes("—")) return { error: `the ${field} contains an em dash` };
  }

  // Sanity caps, not style limits. The template already sizes a long headline
  // down rather than truncating it, so a good long line is welcome; these only
  // catch a run that returned a paragraph where a line belongs.
  if (copy.subject.length > 140) return { error: `the subject is ${copy.subject.length} characters` };
  if (copy.headline.length > 130) return { error: `the headline is ${copy.headline.length} characters` };
  if (copy.body.length > 900) return { error: `the body is ${copy.body.length} characters` };

  return { copy, cost: envelope.total_cost_usd };
}

const catalogue = loadCatalogue();
const connection = await connect();

try {
  const collection = items(connection);
  await collection.createIndex({ skill: 1 }, { unique: true });

  const known = new Set((await collection.distinct("skill")) ?? []);
  const fresh = catalogue.skills.filter((skill) => !known.has(skill.name));

  if (fresh.length === 0) {
    console.log("\n  No new skills. Nothing to draft.\n");
    process.exit(0);
  }

  const { autoSend, seededAt } = await readSettings(connection);
  if (!seededAt) {
    fail(
      `The baseline has not been recorded, so all ${catalogue.skills.length} skills look new.\n  Run \`pnpm digest:seed\` first; it marks what is already published as announced.`,
    );
  }

  console.log(
    `\n  ${fresh.length} new skill${fresh.length === 1 ? "" : "s"}: ${fresh.map((s) => s.name).join(", ")}`,
  );
  console.log(`  Writing the copy with claude sonnet 5 (high effort). This takes a minute each.\n`);

  const written = [];
  const problems = [];

  for (const skill of fresh) {
    process.stdout.write(`  ${skill.name} ... `);
    const { copy, error, cost } = writeCopy(skill);
    if (error) {
      console.log(`failed`);
      problems.push({ skill: skill.name, error });
      continue;
    }

    const now = new Date();
    const status = autoSend ? "ready" : "draft";
    try {
      await collection.insertOne({
        skill: skill.name,
        version: skill.version,
        subject: copy.subject.trim(),
        headline: copy.headline.trim(),
        body: copy.body.trim(),
        blurb: skill.blurb ?? "",
        install: skill.install || installLine(skill.name),
        url: skillUrl(skill.name),
        iconUrl: iconUrl(skill.name),
        group: skill.group ?? "",
        status,
        draftedAt: now,
        readyAt: status === "ready" ? now : null,
        createdAt: now,
        updatedAt: now,
      });
    } catch (err) {
      // Someone else drafted it between the read and the write.
      if (err.code === 11000) {
        console.log("already queued by another run");
        continue;
      }
      throw err;
    }

    console.log(`done${cost ? ` ($${cost.toFixed(2)})` : ""}`);
    written.push({ ...copy, skill: skill.name, status });
  }

  for (const entry of written) {
    console.log(`\n  ── ${entry.skill} ─────────────────────────────`);
    console.log(`  subject:  ${entry.subject}`);
    console.log(`  headline: ${entry.headline}`);
    console.log(`  body:     ${entry.body}`);
  }

  if (problems.length > 0) {
    console.log(`\n  ${problems.length} failed and ${problems.length === 1 ? "was" : "were"} not queued:`);
    for (const p of problems) console.log(`    ${p.skill}: ${p.error}`);
    console.log(`  Re-run \`pnpm digest:draft\` to try those again.`);
  }

  if (written.length > 0) {
    console.log(
      autoSend
        ? `\n  Queued to send at the next 10am Sydney time.\n  Hold them instead with \`pnpm digest:hold\`.\n`
        : `\n  Held as drafts. Nothing sends until you run:\n\n    pnpm digest:approve\n`,
    );
  }
} catch (err) {
  fail(`Drafting failed: ${err.message}`);
} finally {
  await connection.close();
}

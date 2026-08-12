/**
 * Read the drafted copy, then release it.
 *
 * The user asked to read the first issue and then stop being asked, so this
 * does two things: it releases the drafts in front of it, and on the first ever
 * run it turns auto-send on. A flag that flips itself silently is a surprise
 * waiting to happen, so the flip is announced in full along with the command
 * that reverses it.
 *
 * The terminal shows the words; the rendered email lives behind the preview
 * route, because a template is a `.tsx` and this is plain node. That split is a
 * feature rather than a workaround: the preview then comes out of the same code
 * path that sends, so approving it means approving what actually goes.
 */

import { connect, items, readSettings, settings, fail, SITE_URL } from "./digest-lib.mjs";

const connection = await connect();

try {
  const collection = items(connection);
  const drafts = await collection.find({ status: "draft" }).sort({ draftedAt: 1 }).toArray();

  if (drafts.length === 0) {
    console.log("\n  No drafts waiting. Nothing to approve.\n");
    process.exit(0);
  }

  console.log(`\n  ${drafts.length} draft${drafts.length === 1 ? "" : "s"} waiting.\n`);
  if (drafts.length === 1) console.log(`  Subject:  ${drafts[0].subject}`);

  for (const item of drafts) {
    console.log(`\n  ── ${item.skill} ─────────────────────────────`);
    console.log(`  ${item.headline}`);
    console.log(`  ${item.body}`);
  }

  const secret = process.env.CRON_SECRET;
  const base = process.env.DIGEST_PREVIEW_URL ?? SITE_URL;
  if (secret) {
    console.log(`\n  Rendered, as it will actually send:`);
    console.log(`    ${base}/api/digest/preview?token=${encodeURIComponent(secret)}`);
    console.log(`    ${base}/api/digest/preview?part=text&token=${encodeURIComponent(secret)}`);
  } else {
    console.log(`\n  CRON_SECRET is not in site/.env.local, so the rendered preview is not reachable.`);
    console.log(`  Add it to read the email rather than only its words.`);
  }

  if (!process.argv.includes("--yes")) {
    console.log(`\n  Read that, then run:\n\n    pnpm digest:approve --yes\n`);
    process.exit(0);
  }

  const now = new Date();
  const released = await collection.updateMany(
    { status: "draft" },
    { $set: { status: "ready", readyAt: now, updatedAt: now } },
  );

  console.log(
    `\n  Released ${released.modifiedCount} item${released.modifiedCount === 1 ? "" : "s"}. They go out at the next 10am Sydney time.`,
  );

  const current = await readSettings(connection);
  if (!current.autoSend) {
    await settings(connection).updateOne({ key: "settings" }, { $set: { autoSend: true, updatedAt: now } });
    console.log(`\n  Auto-send is now ON.`);
    console.log(`  From here, a new skill's copy is written on push and queued without asking you.`);
    console.log(`  You will not see another draft unless you turn it back off:\n`);
    console.log(`    pnpm digest:hold\n`);
  } else {
    console.log("");
  }
} catch (err) {
  fail(`Approving failed: ${err.message}`);
} finally {
  await connection.close();
}

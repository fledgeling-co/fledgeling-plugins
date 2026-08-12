/**
 * Turn auto-send back off.
 *
 * The reverse of the flip that `digest:approve` makes on its first run. After
 * this, new copy is written on push as usual and then waits for you again.
 * Anything already released stays released; holding is about what happens next,
 * not a recall.
 */

import { connect, items, readSettings, settings, fail } from "./digest-lib.mjs";

const connection = await connect();

try {
  const current = await readSettings(connection);
  if (!current.autoSend) {
    console.log("\n  Auto-send is already off. New copy will wait for `pnpm digest:approve`.\n");
    process.exit(0);
  }

  await settings(connection).updateOne(
    { key: "settings" },
    { $set: { autoSend: false, updatedAt: new Date() } },
  );

  const pending = await items(connection).countDocuments({ status: "ready" });
  console.log("\n  Auto-send is off. New copy will wait for `pnpm digest:approve`.");
  if (pending > 0) {
    console.log(
      `\n  Note: ${pending} item${pending === 1 ? " is" : "s are"} already released and will still send at the next 10am Sydney time.`,
    );
    console.log("  This holds what comes next; it does not recall what is already queued.");
  }
  console.log("");
} catch (err) {
  fail(`Could not change the setting: ${err.message}`);
} finally {
  await connection.close();
}

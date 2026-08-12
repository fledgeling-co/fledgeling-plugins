/**
 * The baseline, run once.
 *
 * Twenty skills were already published when this pipeline shipped. Without a
 * baseline the first draft run would treat all twenty as new and the first
 * digest would be a twenty-item wall sent to a list that signed up to hear what
 * comes next. So they are recorded as `seeded`: present, never mailed, and
 * with no path to `ready`.
 *
 * Safe to run again. Existing rows are left exactly as they are, so a re-run
 * only ever records skills added since the last one.
 */

import { connect, items, readSettings, settings, loadCatalogue, fail } from "./digest-lib.mjs";

const catalogue = loadCatalogue();
const connection = await connect();

try {
  const collection = items(connection);
  await collection.createIndex({ skill: 1 }, { unique: true });

  const known = new Set((await collection.distinct("skill")) ?? []);
  const fresh = catalogue.skills.filter((skill) => !known.has(skill.name));

  if (fresh.length === 0) {
    console.log(`\n  Nothing to seed. All ${catalogue.skills.length} skills are already recorded.\n`);
  } else {
    const now = new Date();
    await collection.insertMany(
      fresh.map((skill) => ({
        skill: skill.name,
        version: skill.version,
        subject: "",
        headline: "",
        body: "",
        blurb: skill.blurb ?? "",
        install: skill.install ?? "",
        url: "",
        iconUrl: "",
        group: skill.group ?? "",
        status: "seeded",
        draftedAt: null,
        readyAt: null,
        createdAt: now,
        updatedAt: now,
      })),
    );
    console.log(`\n  Recorded ${fresh.length} skill${fresh.length === 1 ? "" : "s"} as already announced:`);
    for (const skill of fresh) console.log(`    ${skill.name}`);
    console.log("\n  Nothing was queued and nothing will be sent for these.\n");
  }

  const current = await readSettings(connection);
  if (!current.seededAt) {
    await settings(connection).updateOne(
      { key: "settings" },
      { $set: { seededAt: new Date(), updatedAt: new Date() } },
    );
  }
} catch (err) {
  fail(`Seeding failed: ${err.message}`);
} finally {
  await connection.close();
}

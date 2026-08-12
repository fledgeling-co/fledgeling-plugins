/**
 * Shared plumbing for the digest scripts.
 *
 * These run on Luke's machine, not on Vercel, because the copy is written by
 * the Claude CLI and a serverless function has no CLI. They talk to the same
 * database the site uses, through the native driver rather than the mongoose
 * models in lib/digest.ts: those are TypeScript and carry `server-only`, so a
 * plain node script cannot import them. The collection names below are the
 * contract between the two halves, and they are the only thing duplicated.
 */

import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import mongoose from "mongoose";

export const SITE_DIR = dirname(dirname(fileURLToPath(import.meta.url)));
export const REPO_DIR = dirname(SITE_DIR);

export const DIGEST_ITEMS = "digest_items";
export const DIGEST_SETTINGS = "digest_settings";

export const MARKETPLACE_NAME = "fledgeling-plugins";
export const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://skills.fledgeling.app";

export function fail(message) {
  console.error(`\n  ${message}\n`);
  process.exit(1);
}

export async function connect() {
  const uri = process.env.MONGODB_URI;
  if (!uri) {
    fail(
      "MONGODB_URI is not set.\n  These scripts read it from site/.env.local; check that the file exists and carries it.",
    );
  }
  mongoose.set("strictQuery", true);
  await mongoose.connect(uri);
  return mongoose.connection;
}

export function items(connection) {
  return connection.collection(DIGEST_ITEMS);
}

export function settings(connection) {
  return connection.collection(DIGEST_SETTINGS);
}

export async function readSettings(connection) {
  const existing = await settings(connection).findOne({ key: "settings" });
  if (existing) return existing;
  const doc = { key: "settings", autoSend: false, seededAt: null, createdAt: new Date(), updatedAt: new Date() };
  await settings(connection).insertOne(doc);
  return doc;
}

/**
 * The catalogue, rebuilt first.
 *
 * A hook fires before anything has run `next build`, so lib/catalogue.json can
 * be older than the marketplace entry that triggered the hook. Rebuilding also
 * inherits the repo's registration gate for free: a plugin missing its README,
 * icon or SKILL.md fails here rather than being announced and then 404ing.
 */
export function loadCatalogue({ rebuild = true } = {}) {
  if (rebuild) {
    const build = spawnSync(process.execPath, [join(SITE_DIR, "scripts", "build-catalogue.mjs")], {
      stdio: "inherit",
    });
    if (build.status !== 0) fail("build-catalogue.mjs failed, so the catalogue cannot be trusted.");
  }
  return JSON.parse(readFileSync(join(SITE_DIR, "lib", "catalogue.json"), "utf8"));
}

export function installLine(name) {
  return `/plugin install ${name}@${MARKETPLACE_NAME}`;
}

export function skillUrl(name) {
  return `${SITE_URL}/skills/${name}`;
}

export function iconUrl(name) {
  return `${SITE_URL}/icons/${name}.png`;
}

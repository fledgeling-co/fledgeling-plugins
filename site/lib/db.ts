import "server-only";
import mongoose from "mongoose";

/**
 * The database connection.
 *
 * Lifted from ~/Dev/hopper/apps/web/lib/db.ts, which is the house pattern for a
 * Next app on Vercel, and correct for two reasons that are easy to get wrong:
 *
 *   * the cached value is the PROMISE, not the resolved connection. Two
 *     concurrent cold invocations would otherwise both bootstrap a connection.
 *   * a rejection clears the cache. Caching a rejected promise wedges every
 *     later request on one transient network failure, and nothing recovers it
 *     short of a new instance.
 */

mongoose.set("strictQuery", true);
// Mongoose runs no validators on updates by default, so without this a $set
// could write past a maxlength or outside an enum. The caps in the schema are
// meant to hold on every path, not only on create.
mongoose.set("runValidators", true);

const globalForMongoose = globalThis as unknown as {
  _mongoose?: Promise<typeof mongoose>;
};

/** True when a database is configured at all. Callers degrade rather than throw. */
export function hasDatabase(): boolean {
  return Boolean(process.env.MONGODB_URI);
}

export function db(): Promise<typeof mongoose> {
  const uri = process.env.MONGODB_URI;
  if (!uri) throw new Error("MONGODB_URI is not set");
  globalForMongoose._mongoose ??= mongoose.connect(uri).catch((err: unknown) => {
    globalForMongoose._mongoose = undefined;
    throw err;
  });
  return globalForMongoose._mongoose;
}

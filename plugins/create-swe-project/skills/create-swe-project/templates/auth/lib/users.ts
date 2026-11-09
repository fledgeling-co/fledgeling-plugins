import 'server-only';
import { mongo } from 'mongoose';
import { db } from './db';
import { UserModel } from './models';

export type UserRef = { id: string; email: string; created: boolean };

async function upsert(email: string): Promise<UserRef> {
  const result = await UserModel.findOneAndUpdate(
    { email },
    { $setOnInsert: { email } },
    { upsert: true, returnDocument: 'after', includeResultMetadata: true },
  );
  const doc = result.value;
  if (!doc) throw new Error('user upsert returned no document');
  return { id: String(doc._id), email: doc.email, created: !result.lastErrorObject?.updatedExisting };
}

/**
 * Find-or-create in one atomic upsert against the unique email index
 * (CP §4 A07, §6.3). Two concurrent first sign-ins race to insert; the loser
 * gets E11000 and retries once, finding the winner's row.
 */
export async function findOrCreateUser(email: string): Promise<UserRef> {
  await db();
  const normalized = email.trim().toLowerCase();
  try {
    return await upsert(normalized);
  } catch (err: unknown) {
    if (err instanceof mongo.MongoServerError && err.code === 11000) return upsert(normalized);
    throw err;
  }
}

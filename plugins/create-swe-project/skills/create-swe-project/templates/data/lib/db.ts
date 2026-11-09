import 'server-only';
import mongoose from 'mongoose';
import { requireEnv } from './env';

// 'throw', not true: with true, Mongoose silently drops filter keys missing from
// the schema, so a misspelt { tenatId } becomes {} and matches every tenant's
// documents (BP §4).
mongoose.set('strictQuery', 'throw');

const globalForMongoose = globalThis as unknown as { _mongoose?: Promise<typeof mongoose> };

/**
 * One cached connection on globalThis, surviving dev hot reloads and serverless
 * reuse (BP §4). The PROMISE is cached so two concurrent cold starts don't both
 * connect (BP §16), and it is cleared on rejection so one failed connect can't
 * wedge every later request (CP §6.3).
 */
export function db(): Promise<typeof mongoose> {
  globalForMongoose._mongoose ??= mongoose.connect(requireEnv('MONGODB_URI')).catch((err: unknown) => {
    globalForMongoose._mongoose = undefined;
    throw new Error('MongoDB connection failed', { cause: err });
  });
  return globalForMongoose._mongoose;
}

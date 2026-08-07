import 'server-only';
import mongoose from 'mongoose';

// Single cached connection on globalThis — survives Next.js dev hot reloads and
// serverless function reuse (BP §4). Cache the PROMISE so two concurrent cold
// invocations don't both bootstrap (BP §16).
mongoose.set('strictQuery', true);

const globalForMongoose = globalThis as unknown as { _mongoose?: Promise<typeof mongoose> };

export function db(): Promise<typeof mongoose> {
  const uri = process.env.MONGODB_URI;
  if (!uri) throw new Error('MONGODB_URI is not set');
  globalForMongoose._mongoose ??= mongoose.connect(uri);
  return globalForMongoose._mongoose;
}

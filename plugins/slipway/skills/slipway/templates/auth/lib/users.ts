import 'server-only';
import { db } from './db';
import { UserModel } from './models';

export async function findOrCreateUser(email: string): Promise<{ id: string; email: string; created: boolean }> {
  await db();
  const normalized = email.trim().toLowerCase();
  const existing = await UserModel.findOne({ email: normalized }).lean<{ _id: unknown; email: string }>();
  if (existing) return { id: String(existing._id), email: existing.email, created: false };
  const created = await UserModel.create({ email: normalized });
  return { id: String(created._id), email: normalized, created: true };
}

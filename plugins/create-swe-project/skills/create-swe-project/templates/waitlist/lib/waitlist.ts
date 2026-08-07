import 'server-only';
import mongoose, { Schema, type InferSchemaType, type Model } from 'mongoose';
import { randomBytes } from 'node:crypto';
import { db } from './db';

// Waitlist with a referral loop — the research's most under-used pre-launch
// lever (bare email capture converts ~1-2%; referral-powered lists report far
// higher). Position = referral count first, then join order.
const waitlistSchema = new Schema(
  {
    email: { type: String, required: true, unique: true, index: true, lowercase: true, trim: true },
    refCode: { type: String, required: true, unique: true, index: true },
    referredBy: { type: String, default: null },
    referrals: { type: Number, default: 0, index: true },
  },
  { timestamps: true },
);

export type WaitlistDoc = InferSchemaType<typeof waitlistSchema>;

export const WaitlistModel: Model<WaitlistDoc> =
  (mongoose.models.Waitlist as Model<WaitlistDoc> | undefined) ??
  mongoose.model<WaitlistDoc>('Waitlist', waitlistSchema);

export type WaitlistStatus = { position: number; total: number; refCode: string; referrals: number };

async function status(entry: { refCode: string; referrals: number; createdAt?: Date }): Promise<WaitlistStatus> {
  const ahead = await WaitlistModel.countDocuments({
    $or: [
      { referrals: { $gt: entry.referrals } },
      { referrals: entry.referrals, createdAt: { $lt: entry.createdAt ?? new Date() } },
    ],
  });
  const total = await WaitlistModel.countDocuments();
  return { position: ahead + 1, total, refCode: entry.refCode, referrals: entry.referrals };
}

export async function joinWaitlist(email: string, referredBy?: string): Promise<WaitlistStatus> {
  await db();
  const normalized = email.trim().toLowerCase();
  const existing = await WaitlistModel.findOne({ email: normalized });
  if (existing) return status(existing);
  const entry = await WaitlistModel.create({
    email: normalized,
    refCode: randomBytes(6).toString('base64url'),
    referredBy: referredBy ?? null,
  });
  if (referredBy) {
    await WaitlistModel.updateOne({ refCode: referredBy }, { $inc: { referrals: 1 } });
  }
  return status(entry);
}

export async function waitlistStatus(refCode: string): Promise<WaitlistStatus | null> {
  await db();
  const entry = await WaitlistModel.findOne({ refCode });
  return entry ? status(entry) : null;
}

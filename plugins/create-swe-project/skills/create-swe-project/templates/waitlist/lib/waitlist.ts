import 'server-only';
import mongoose, { Schema, mongo, type InferSchemaType, type Model } from 'mongoose';
import { createHash, randomBytes } from 'node:crypto';
import { db } from './db';

// Waitlist with a referral loop, the research's most under-used pre-launch
// lever (bare email capture converts ~1-2%; referral-powered lists report far
// higher). Position = referral count first, then join order.
//
// Joining never reveals whether an address was already on the list (CP §6.1):
// every join gets the same response and a fresh opaque viewer token, and only
// the token minted with a real insert is stored. So the browser that created an
// entry can see its position and share link, and nobody else can, including
// someone who types an address they suspect joined.
const waitlistSchema = new Schema(
  {
    email: { type: String, required: true, unique: true, index: true, lowercase: true, trim: true },
    refCode: { type: String, required: true, unique: true, index: true },
    referredBy: { type: String, default: null },
    referrals: { type: Number, default: 0, index: true },
    viewerTokenHash: { type: String, required: true, unique: true, index: true, select: false },
  },
  { timestamps: true },
);

export type WaitlistDoc = InferSchemaType<typeof waitlistSchema>;

export const WaitlistModel: Model<WaitlistDoc> =
  (mongoose.models.Waitlist as Model<WaitlistDoc> | undefined) ??
  mongoose.model<WaitlistDoc>('Waitlist', waitlistSchema);

export type WaitlistStatus = { position: number; total: number; refCode: string; referrals: number };

/** A random 256-bit viewer token; only its hash is stored, never the token (CP §6.11). */
export function newViewerToken(): string {
  return randomBytes(32).toString('base64url');
}
const hashToken = (token: string): string => createHash('sha256').update(token).digest('hex');

async function status(entry: { refCode: string; referrals: number; createdAt?: Date | null }): Promise<WaitlistStatus> {
  const ahead = await WaitlistModel.countDocuments({
    $or: [
      { referrals: { $gt: entry.referrals } },
      { referrals: entry.referrals, createdAt: { $lt: entry.createdAt ?? new Date() } },
    ],
  });
  const total = await WaitlistModel.countDocuments();
  return { position: ahead + 1, total, refCode: entry.refCode, referrals: entry.referrals };
}

/**
 * Join in one atomic upsert on the unique email index (CP §6.3), so two
 * concurrent joins can't both insert or both credit the referrer. The viewer
 * token is stored only on a real insert, and only a real insert credits the
 * referral, never to the joiner's own code. Returns nothing on purpose: the
 * caller must not be able to tell a new address from a known one.
 */
export async function joinWaitlist(email: string, viewerToken: string, referredBy?: string): Promise<void> {
  await db();
  const normalized = email.trim().toLowerCase();
  const upsert = () =>
    WaitlistModel.findOneAndUpdate(
      { email: normalized },
      {
        $setOnInsert: {
          email: normalized,
          refCode: randomBytes(6).toString('base64url'),
          referredBy: referredBy ?? null,
          viewerTokenHash: hashToken(viewerToken),
        },
      },
      { upsert: true, returnDocument: 'after', includeResultMetadata: true },
    );
  let result;
  try {
    result = await upsert();
  } catch (err: unknown) {
    if (!(err instanceof mongo.MongoServerError && err.code === 11000)) throw err;
    result = await upsert();
  }
  const entry = result.value;
  if (!entry) throw new Error('waitlist upsert returned no document');
  if (!result.lastErrorObject?.updatedExisting && referredBy && referredBy !== entry.refCode) {
    await WaitlistModel.updateOne({ refCode: referredBy }, { $inc: { referrals: 1 } });
  }
}

/** The status of the entry this viewer token created, or null for any other token. */
export async function statusForViewer(viewerToken: string): Promise<WaitlistStatus | null> {
  await db();
  const entry = await WaitlistModel.findOne({ viewerTokenHash: hashToken(viewerToken) });
  return entry ? status(entry) : null;
}

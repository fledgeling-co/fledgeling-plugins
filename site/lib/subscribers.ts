import "server-only";
import mongoose, { Schema, type InferSchemaType, type Model } from "mongoose";
import { db } from "./db";

/**
 * One collection, one document per address.
 *
 * `cadence` carries the whole state, including "unsubscribed" as `none`. The
 * alternative — a separate `status` field beside a cadence — has a failure mode
 * where the two disagree about whether to send, and the only way to resolve it
 * is to guess which one the person meant. GitHub's newsletter preferences model
 * it the same way: None / Daily / Weekly is one control, not a switch and a
 * dial that can contradict each other.
 */

export const CADENCES = ["daily", "weekly", "paused", "none"] as const;
export type Cadence = (typeof CADENCES)[number];

export const DEFAULT_CADENCE: Cadence = "weekly";

const SubscriberSchema = new Schema(
  {
    email: {
      type: String,
      required: true,
      unique: true,
      // Stored lowercased and trimmed so "Luke@X.com " and "luke@x.com" are one
      // person rather than two rows that both get sent to.
      lowercase: true,
      trim: true,
      maxlength: 320,
    },
    cadence: { type: String, enum: CADENCES, default: DEFAULT_CADENCE, required: true },
    source: { type: String, maxlength: 120, default: "site" },
    unsubscribedAt: { type: Date, default: null },

    /**
     * Two watermarks, each answering one question, because one field cannot
     * answer both without being wrong about one of them.
     *
     * `lastDigestAt` decides *which items* are new to this person. It starts at
     * sign-up time, so somebody who joins today is never sent a backlog of
     * everything that shipped before they had heard of the site.
     *
     * `lastDigestOn` decides *whether today is a send day*, and it is a Sydney
     * calendar label rather than an instant. Comparing labels is what survives
     * the cron's ±59 minute jitter; comparing instants means a weekly send that
     * once ran late gets skipped entirely the following week.
     */
    lastDigestAt: { type: Date, default: null },
    lastDigestOn: { type: String, default: null, maxlength: 10 },
  },
  { timestamps: true, collection: "subscribers" },
);

// Every send starts by asking who is on a sending cadence at all.
SubscriberSchema.index({ cadence: 1 });

export type Subscriber = InferSchemaType<typeof SubscriberSchema> & { _id: mongoose.Types.ObjectId };

// Guarded because Next's dev server re-evaluates modules on hot reload, and
// mongoose throws on a second model registration under the same name.
const SubscriberModel: Model<Subscriber> =
  (mongoose.models.Subscriber as Model<Subscriber>) ??
  mongoose.model<Subscriber>("Subscriber", SubscriberSchema);

export type SubscribeOutcome = { subscriber: Subscriber; created: boolean; reactivated: boolean };

/**
 * Add an address, or return the one already there.
 *
 * Deliberately an upsert that reports success either way. A form that answers
 * "you are already subscribed" differently from "you are now subscribed" tells
 * anyone who asks whether a given address is on the list, and the person typing
 * their own address into a footer does not need that distinction anyway.
 */
export async function subscribe(email: string, source: string): Promise<SubscribeOutcome> {
  await db();
  const normalised = email.trim().toLowerCase();
  const existing = await SubscriberModel.findOne({ email: normalised });

  if (!existing) {
    // The digest watermark starts now, so the first email this address gets is
    // about something that shipped after they signed up. Backfilling the whole
    // catalogue to a new subscriber is the fastest way to be marked as spam.
    const subscriber = await SubscriberModel.create({
      email: normalised,
      source,
      lastDigestAt: new Date(),
    });
    return { subscriber, created: true, reactivated: false };
  }

  // Someone who left and came back is reactivated rather than left on `none`,
  // which would silently accept the address and then never send anything. The
  // watermark resets with them: they asked to hear what happens next, not to
  // receive everything they missed while they were off the list.
  if (existing.cadence === "none") {
    existing.cadence = DEFAULT_CADENCE;
    existing.unsubscribedAt = null;
    existing.lastDigestAt = new Date();
    await existing.save();
    return { subscriber: existing, created: false, reactivated: true };
  }

  return { subscriber: existing, created: false, reactivated: false };
}

export async function findById(id: string): Promise<Subscriber | null> {
  await db();
  if (!mongoose.Types.ObjectId.isValid(id)) return null;
  return SubscriberModel.findById(id);
}

export async function setCadence(id: string, cadence: Cadence): Promise<Subscriber | null> {
  await db();
  if (!mongoose.Types.ObjectId.isValid(id)) return null;
  return SubscriberModel.findByIdAndUpdate(
    id,
    { cadence, unsubscribedAt: cadence === "none" ? new Date() : null },
    { new: true },
  );
}

/** Everyone on a cadence that sends. `paused` and `none` are both excluded. */
export async function sendableSubscribers(): Promise<Subscriber[]> {
  await db();
  return SubscriberModel.find({ cadence: { $in: ["daily", "weekly"] } });
}

/**
 * Advance both watermarks, for the addresses the mailer actually accepted.
 *
 * Only the accepted ones, and only after the send: marking first would turn a
 * Resend outage into a silently skipped issue that nothing ever retries, since
 * the items it covered would then be behind every watermark.
 */
export async function markDigestSent(
  ids: mongoose.Types.ObjectId[],
  sentAt: Date,
  sydneyDate: string,
): Promise<number> {
  if (ids.length === 0) return 0;
  await db();
  const result = await SubscriberModel.updateMany(
    { _id: { $in: ids } },
    { lastDigestAt: sentAt, lastDigestOn: sydneyDate },
  );
  return result.modifiedCount;
}

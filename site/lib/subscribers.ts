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
  },
  { timestamps: true, collection: "subscribers" },
);

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
    const subscriber = await SubscriberModel.create({ email: normalised, source });
    return { subscriber, created: true, reactivated: false };
  }

  // Someone who left and came back is reactivated rather than left on `none`,
  // which would silently accept the address and then never send anything.
  if (existing.cadence === "none") {
    existing.cadence = DEFAULT_CADENCE;
    existing.unsubscribedAt = null;
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

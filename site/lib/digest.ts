import "server-only";
import mongoose, { Schema, type InferSchemaType, type Model } from "mongoose";
import { db } from "./db";
import { daysBetween } from "./sydney";
import type { Cadence } from "./subscribers";

/**
 * The digest queue.
 *
 * One document per skill, ever — announcing a skill is a one-time event, so the
 * unique index on `skill` is what makes the whole pipeline idempotent. A draft
 * script that runs twice, a hook that fires on a re-push, a retried CI job: all
 * of them collide on the index and write nothing rather than queueing a second
 * copy of the same announcement.
 *
 * Three states, and `seeded` is the load-bearing one. The twenty skills already
 * published when this shipped must never mail, so they are recorded here with
 * no copy and no path to `ready`. Without that the first cron run would send a
 * twenty-item digest to a list that signed up for what comes next.
 *
 * The copy fields are written once by `scripts/digest-draft.mjs`, which is the
 * only thing in the system that can call the Claude CLI. The send path reads
 * them and renders; it never generates.
 *
 * Catalogue values are denormalised on purpose. A digest describes the skill as
 * it was when it landed, and the catalogue is rebuilt on every deploy.
 */

export const DIGEST_ITEMS = "digest_items";
export const DIGEST_SETTINGS = "digest_settings";

export const ITEM_STATUSES = ["seeded", "draft", "ready"] as const;
export type ItemStatus = (typeof ITEM_STATUSES)[number];

const DigestItemSchema = new Schema(
  {
    skill: { type: String, required: true, unique: true, maxlength: 120 },
    version: { type: String, default: "", maxlength: 40 },

    // Written by the CLI. Empty on a seeded row, which is why none of them are
    // required — a seed must not have to invent copy to satisfy a validator.
    subject: { type: String, default: "", maxlength: 200 },
    headline: { type: String, default: "", maxlength: 200 },
    body: { type: String, default: "", maxlength: 1200 },

    // Denormalised from the catalogue at draft time.
    blurb: { type: String, default: "", maxlength: 2000 },
    install: { type: String, default: "", maxlength: 200 },
    url: { type: String, default: "", maxlength: 400 },
    iconUrl: { type: String, default: "", maxlength: 400 },
    group: { type: String, default: "", maxlength: 80 },

    status: { type: String, enum: ITEM_STATUSES, default: "draft", required: true },
    draftedAt: { type: Date, default: null },
    readyAt: { type: Date, default: null },
  },
  { timestamps: true, collection: DIGEST_ITEMS },
);

// Every send starts by asking for ready items newer than a watermark.
DigestItemSchema.index({ status: 1, readyAt: 1 });

export type DigestItem = InferSchemaType<typeof DigestItemSchema> & {
  _id: mongoose.Types.ObjectId;
};

const DigestSettingsSchema = new Schema(
  {
    key: { type: String, required: true, unique: true, default: "settings" },
    /**
     * False until the first issue is approved by hand.
     *
     * The user asked to read the first one and then stop being asked. A flag
     * that flips itself is a surprise waiting to happen, so the approve script
     * says out loud that it has flipped and prints the command to flip it back.
     */
    autoSend: { type: Boolean, default: false },
    seededAt: { type: Date, default: null },
  },
  { timestamps: true, collection: DIGEST_SETTINGS },
);

export type DigestSettings = InferSchemaType<typeof DigestSettingsSchema>;

// Guarded for the same reason as the Subscriber model: Next re-evaluates
// modules on hot reload and mongoose throws on a duplicate registration.
const ItemModel: Model<DigestItem> =
  (mongoose.models.DigestItem as Model<DigestItem>) ??
  mongoose.model<DigestItem>("DigestItem", DigestItemSchema);

const SettingsModel: Model<DigestSettings> =
  (mongoose.models.DigestSettings as Model<DigestSettings>) ??
  mongoose.model<DigestSettings>("DigestSettings", DigestSettingsSchema);

export async function getSettings(): Promise<DigestSettings> {
  await db();
  const existing = await SettingsModel.findOne({ key: "settings" });
  if (existing) return existing;
  return SettingsModel.create({ key: "settings" });
}

/** Ready items published after a watermark, oldest first. */
export async function readyItemsSince(since: Date): Promise<DigestItem[]> {
  await db();
  return ItemModel.find({ status: "ready", readyAt: { $gt: since } }).sort({ readyAt: 1 });
}

/** Everything in one state, oldest first. Used by the preview route. */
export async function itemsByStatus(status: ItemStatus): Promise<DigestItem[]> {
  await db();
  return ItemModel.find({ status }).sort({ draftedAt: 1 });
}

/**
 * Whether a subscriber is due today.
 *
 * Calendar days in Sydney, never elapsed milliseconds. Vercel's Hobby cron has
 * ±59 minutes of jitter, so a `>= 7 days` duration test drops a whole week the
 * first time one send lands at 10:59 and the next at 10:00.
 */
export function isDue(cadence: Cadence, lastDigestOn: string | null, today: string): boolean {
  if (cadence !== "daily" && cadence !== "weekly") return false;
  if (!lastDigestOn) return true;
  if (cadence === "daily") return lastDigestOn !== today;
  return daysBetween(lastDigestOn, today) >= 7;
}

/**
 * The subject line for one send.
 *
 * Composed rather than generated, because the copy is written per skill at
 * publish time and a digest's shape is only known when it goes out. A solo send
 * — the common case — uses the line the CLI wrote for it. A multi-skill send
 * keeps that catchy half and then says plainly what the email is, so the
 * subject never leaves someone guessing whether it is an announcement or a
 * newsletter.
 */
export function digestSubject(items: DigestItem[]): string {
  const newest = items[items.length - 1];
  if (items.length === 1) return newest?.subject || "A new Fledgeling skill";
  const lead = newest?.headline || newest?.subject || "A new Fledgeling skill";
  const rest = items.length - 1;
  return `${lead}, and ${rest} more new skill${rest === 1 ? "" : "s"}`;
}

export { ItemModel as DigestItemModel, SettingsModel as DigestSettingsModel };

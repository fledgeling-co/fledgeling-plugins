import { timingSafeEqual } from "node:crypto";
import { digestSubject, isDue, readyItemsSince } from "@/lib/digest";
import { sendDigestBatch, hasMailer, type DigestSend } from "@/lib/email";
import { getSkill } from "@/lib/skills";
import { hasDatabase } from "@/lib/db";
import { mintToken, hasTokenSecret } from "@/lib/subscribe-token";
import { markDigestSent, sendableSubscribers } from "@/lib/subscribers";
import { sydneyNow } from "@/lib/sydney";

/**
 * The scheduled send. 10am in Sydney, daily or weekly per subscriber.
 *
 * Two cron entries in vercel.json point here, at 23:00 and 00:00 UTC. That is
 * not redundancy for its own sake: Sydney is UTC+10 for half the year and
 * UTC+11 for the other half, and this account's Vercel plan allows a cron to
 * run only once a day, so no single UTC slot is 10am all year. One entry is
 * 10am in summer, the other is 10am in winter, and the hour gate below decides
 * which one is live today.
 *
 * The pair is also the retry story. If one invocation fails outright, the other
 * covers the same Sydney day, and the per-subscriber watermark makes a second
 * successful run a no-op rather than a duplicate.
 */

export const dynamic = "force-dynamic";
export const maxDuration = 60;

/** The hours in Sydney at which a send may happen. Vercel's Hobby cron drifts
 *  up to 59 minutes, so a run aimed at 10:00 can land at 10:59; 11 is the
 *  headroom for that, and the watermark stops it becoming a second send. */
const SEND_HOURS = new Set([10, 11]);

function authorised(request: Request): boolean {
  const expected = process.env.CRON_SECRET;
  if (!expected) return false;

  const header = request.headers.get("authorization") ?? "";
  const given = header.startsWith("Bearer ") ? header.slice(7) : "";

  const a = Buffer.from(given);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}

function json(body: unknown, status = 200): Response {
  return Response.json(body, { status });
}

export async function GET(request: Request): Promise<Response> {
  if (!authorised(request)) return new Response(null, { status: 401 });

  if (!hasDatabase() || !hasTokenSecret() || !hasMailer()) {
    return json({ skipped: "not configured" }, 503);
  }

  const url = new URL(request.url);
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? url.origin;

  // `?force=1` exists for driving this by hand during verification. It skips
  // the clock, never the watermark, so it cannot double-send to anybody.
  const forced = url.searchParams.get("force") === "1";
  const { date: today, hour } = sydneyNow();
  if (!forced && !SEND_HOURS.has(hour)) {
    return json({ skipped: "outside the send window", sydneyHour: hour, sydneyDate: today });
  }

  try {
    const subscribers = await sendableSubscribers();
    const due = subscribers.filter((s) => isDue(s.cadence, s.lastDigestOn ?? null, today));
    if (due.length === 0) {
      return json({ sydneyDate: today, sydneyHour: hour, due: 0, sent: 0 });
    }

    // Where this person's "new to me" starts. `lastDigestAt` is unset for
    // anyone who subscribed before the digest existed, and falling back to now
    // rather than to their sign-up would quietly send them nothing forever.
    const sinceFor = (s: (typeof due)[number]): Date =>
      s.lastDigestAt ?? s.createdAt ?? new Date(0);

    // The oldest watermark among the people due bounds how far back to read.
    const earliest = due.reduce<Date>((oldest, s) => {
      const since = sinceFor(s);
      return since < oldest ? since : oldest;
    }, new Date());
    const items = await readyItemsSince(earliest);

    /**
     * Only skills this deployment can actually show.
     *
     * The draft runs from a pre-push hook, so an item can be queued minutes
     * before the deploy that publishes its page. Asking the deployment's own
     * catalogue is exact where a timer would be a guess: if the skill is not
     * live here, the link would 404, so the item simply waits for tomorrow.
     */
    const live = items.filter((item) => getSkill(item.skill));
    const held = items.length - live.length;

    if (live.length === 0) {
      return json({ sydneyDate: today, sydneyHour: hour, due: due.length, sent: 0, held });
    }

    const sends: DigestSend[] = [];
    const recipients: typeof due = [];

    for (const subscriber of due) {
      const since = sinceFor(subscriber);
      const mine = live.filter((item) => item.readyAt && item.readyAt > since);
      // Nothing new for this person. No empty digest, and no watermark move.
      if (mine.length === 0) continue;

      const token = mintToken(String(subscriber._id));
      const preferencesUrl = `${siteUrl}/preferences/${token}`;
      const unsubscribeUrl = `${siteUrl}/api/unsubscribe?token=${token}`;

      sends.push({
        to: subscriber.email,
        subject: digestSubject(mine),
        preferencesUrl,
        unsubscribeUrl,
        props: {
          email: subscriber.email,
          cadence: subscriber.cadence,
          preferencesUrl,
          unsubscribeUrl,
          siteUrl,
          items: mine.map((item) => ({
            skill: item.skill,
            headline: item.headline,
            body: item.body,
            install: item.install,
            url: item.url || `${siteUrl}/skills/${item.skill}`,
            iconUrl: item.iconUrl || `${siteUrl}/icons/${item.skill}.png`,
          })),
        },
      });
      recipients.push(subscriber);
    }

    if (sends.length === 0) {
      return json({ sydneyDate: today, sydneyHour: hour, due: due.length, sent: 0, held });
    }

    const result = await sendDigestBatch(sends);

    // Only the accepted addresses. Marking everyone would turn a mailer failure
    // into an issue nothing ever retries, because its items would then sit
    // behind every watermark.
    const accepted = new Set(result.sent);
    const ids = recipients.filter((s) => accepted.has(s.email)).map((s) => s._id);
    await markDigestSent(ids, new Date(), today);

    if (result.failed.length > 0) {
      console.error("digest: some sends failed", result.failed);
    }

    return json({
      sydneyDate: today,
      sydneyHour: hour,
      due: due.length,
      sent: result.sent.length,
      failed: result.failed.length,
      held,
    });
  } catch (err) {
    console.error("digest send failed", err);
    return json({ error: "digest send failed" }, 500);
  }
}

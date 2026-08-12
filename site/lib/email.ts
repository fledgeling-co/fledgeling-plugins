import "server-only";
import { Resend } from "resend";
import { DigestEmail, digestText, type DigestEmailProps } from "@/emails/digest";
import { WelcomeEmail } from "@/emails/welcome";

/**
 * Sending, through Resend.
 *
 * Same shape as ~/Dev/hopper/apps/web/lib/email.ts: a client built per call
 * rather than at module load (so an unset key is a failure at send time, not an
 * import-time crash that takes the whole page down), a `from` read from env,
 * and one named export per template.
 */

function client(): Resend {
  const key = process.env.RESEND_API_KEY;
  if (!key) throw new Error("RESEND_API_KEY is not set");
  return new Resend(key);
}

const from = () => process.env.RESEND_FROM_EMAIL ?? "Fledgeling Skills <onboarding@resend.dev>";

export function hasMailer(): boolean {
  return Boolean(process.env.RESEND_API_KEY);
}

export async function sendWelcomeEmail(args: {
  to: string;
  cadence: string;
  preferencesUrl: string;
  siteUrl: string;
  unsubscribeUrl: string;
}): Promise<void> {
  await client().emails.send({
    from: from(),
    to: args.to,
    subject: "You're on the list for new Fledgeling skills",
    react: WelcomeEmail({
      email: args.to,
      cadence: args.cadence,
      preferencesUrl: args.preferencesUrl,
      siteUrl: args.siteUrl,
    }),
    // RFC 8058. Gmail and Yahoo's bulk-sender rules expect both headers, and a
    // list that omits them loses deliverability regardless of what it sends.
    // The POST target unsubscribes without the recipient visiting anything.
    headers: {
      "List-Unsubscribe": `<${args.unsubscribeUrl}>, <${args.preferencesUrl}>`,
      "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
    },
  });
}

export type DigestSend = {
  to: string;
  subject: string;
  preferencesUrl: string;
  unsubscribeUrl: string;
  props: DigestEmailProps;
};

export type DigestSendResult = {
  /** Addresses Resend accepted. Only these watermarks may advance. */
  sent: string[];
  failed: { to: string; reason: string }[];
};

/** Resend's batch endpoint takes 100 emails per call. */
const BATCH_SIZE = 100;

/**
 * One digest per subscriber, in batches.
 *
 * Every message is its own object rather than one message with many `to`
 * addresses: the unsubscribe link is a signature over that subscriber's id, so
 * they cannot share an envelope even before considering that a shared `to`
 * would show every recipient the whole list.
 *
 * `batchValidation: "permissive"` is the load-bearing option. Under the default
 * a single malformed address fails the entire call, which on a list of any size
 * means one dead mailbox silently costs everybody else their digest. Permissive
 * returns per-index errors instead, so the bad address is reported and the other
 * ninety-nine go out.
 */
export async function sendDigestBatch(sends: DigestSend[]): Promise<DigestSendResult> {
  const result: DigestSendResult = { sent: [], failed: [] };
  if (sends.length === 0) return result;

  const resend = client();

  for (let start = 0; start < sends.length; start += BATCH_SIZE) {
    const chunk = sends.slice(start, start + BATCH_SIZE);

    const payload = chunk.map((send) => ({
      from: from(),
      to: send.to,
      subject: send.subject,
      react: DigestEmail(send.props),
      // Written, not stripped from the HTML. Some clients and some filters want
      // a real text part, and a generated one reads worse than none.
      text: digestText(send.props),
      headers: {
        "List-Unsubscribe": `<${send.unsubscribeUrl}>, <${send.preferencesUrl}>`,
        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
      },
    }));

    const response = await resend.batch.send(payload, { batchValidation: "permissive" });

    if (response.error) {
      // The whole call failed, so nothing in this chunk was accepted.
      const reason = response.error.message ?? "batch send failed";
      for (const send of chunk) result.failed.push({ to: send.to, reason });
      continue;
    }

    const failedAt = new Map<number, string>();
    for (const error of response.data?.errors ?? []) {
      failedAt.set(error.index, error.message);
    }

    chunk.forEach((send, index) => {
      const reason = failedAt.get(index);
      if (reason) result.failed.push({ to: send.to, reason });
      else result.sent.push(send.to);
    });
  }

  return result;
}

import "server-only";
import { Resend } from "resend";
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

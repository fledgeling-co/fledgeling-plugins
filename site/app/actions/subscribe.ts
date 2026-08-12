"use server";

import { headers } from "next/headers";
import { z } from "zod";
import { hasDatabase } from "@/lib/db";
import { hasMailer, sendWelcomeEmail } from "@/lib/email";
import { callerKeyFromHeaders, check } from "@/lib/rate-limit";
import { hasTokenSecret, mintToken, verifyToken } from "@/lib/subscribe-token";
import { CADENCES, type Cadence, setCadence, subscribe } from "@/lib/subscribers";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://skills.fledgeling.app";

/**
 * Two Server Actions, not a REST endpoint.
 *
 * Next handles `<form action={…}>` natively, so both forms submit and work with
 * JavaScript switched off. That matters more than usual here: the footer form is
 * on every page including the ones people reach from search, and a subscribe box
 * that silently does nothing without JS is worse than no box at all.
 */

export type SubscribeState =
  | { status: "idle" }
  | { status: "ok"; email: string }
  | { status: "invalid" }
  | { status: "unavailable" }
  | { status: "error" };

// Deliberately permissive. Strict RFC 5322 rejects addresses that work, and the
// real check is whether the welcome email arrives.
const Email = z.string().trim().toLowerCase().min(3).max(320).email();

export async function subscribeAction(
  _prev: SubscribeState,
  formData: FormData,
): Promise<SubscribeState> {
  const parsed = Email.safeParse(formData.get("email"));
  if (!parsed.success) return { status: "invalid" };

  // A honeypot, not a captcha. Bots fill every field; people never see this one.
  if (String(formData.get("company") ?? "").length > 0) {
    return { status: "ok", email: parsed.data };
  }

  if (!hasDatabase() || !hasTokenSecret()) return { status: "unavailable" };

  const head = await headers();
  const verdict = check(callerKeyFromHeaders(head));
  if (!verdict.ok) return { status: "unavailable" };

  try {
    const source = String(formData.get("source") ?? "site").slice(0, 120);
    const { subscriber, created, reactivated } = await subscribe(parsed.data, source);

    // Only on the way in. Someone already subscribed who submits the form again
    // gets the same success state and no second email.
    if ((created || reactivated) && hasMailer()) {
      const token = mintToken(String(subscriber._id));
      try {
        await sendWelcomeEmail({
          to: subscriber.email,
          cadence: subscriber.cadence,
          preferencesUrl: `${SITE_URL}/preferences/${token}`,
          unsubscribeUrl: `${SITE_URL}/api/unsubscribe?token=${token}`,
          siteUrl: SITE_URL,
        });
      } catch (err) {
        // The address is saved. A mailer failure is not the subscriber's problem
        // and must not present as a failed sign-up, or they will submit again.
        console.error("welcome email failed", err);
      }
    }

    return { status: "ok", email: subscriber.email };
  } catch (err) {
    console.error("subscribe failed", err);
    return { status: "error" };
  }
}

export type CadenceState =
  | { status: "idle" }
  | { status: "saved"; cadence: Cadence }
  | { status: "error" };

export async function setCadenceAction(
  _prev: CadenceState,
  formData: FormData,
): Promise<CadenceState> {
  const token = String(formData.get("token") ?? "");
  const cadence = String(formData.get("cadence") ?? "");

  const id = verifyToken(token);
  if (!id) return { status: "error" };
  if (!CADENCES.includes(cadence as Cadence)) return { status: "error" };

  try {
    const updated = await setCadence(id, cadence as Cadence);
    if (!updated) return { status: "error" };
    return { status: "saved", cadence: updated.cadence };
  } catch (err) {
    console.error("cadence update failed", err);
    return { status: "error" };
  }
}

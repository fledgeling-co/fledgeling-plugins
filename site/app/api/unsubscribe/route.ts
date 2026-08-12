import { verifyToken } from "@/lib/subscribe-token";
import { setCadence } from "@/lib/subscribers";

/**
 * RFC 8058 one-click unsubscribe.
 *
 * A route handler rather than a Server Action, because the caller is a mail
 * client hitting the URL in the List-Unsubscribe header directly, and a Server
 * Action is not addressable that way.
 *
 * Answers 200 whatever happens to a well-formed request. A mail client that
 * gets an error surfaces it to the recipient as a failure to unsubscribe, which
 * is worse than a silent no-op on a token that was already spent.
 */

export const dynamic = "force-dynamic";

async function unsubscribe(token: string | null): Promise<Response> {
  if (!token) return new Response(null, { status: 400 });
  const id = verifyToken(token);
  if (!id) return new Response(null, { status: 400 });

  try {
    await setCadence(id, "none");
  } catch (err) {
    console.error("one-click unsubscribe failed", err);
    return new Response(null, { status: 500 });
  }
  return new Response(null, { status: 200 });
}

export async function POST(request: Request): Promise<Response> {
  const url = new URL(request.url);
  let token = url.searchParams.get("token");

  // Some clients post the RFC 8058 body rather than preserving the query string.
  if (!token) {
    try {
      const form = await request.formData();
      const value = form.get("token");
      if (typeof value === "string") token = value;
    } catch {
      // no body, or not a form; the query string was the only chance
    }
  }
  return unsubscribe(token);
}

/**
 * GET redirects to the preference page rather than unsubscribing. A link
 * prefetcher or a mail scanner following the URL must never remove someone from
 * a list, which is why the one-click path is POST-only.
 */
export async function GET(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const token = url.searchParams.get("token");
  if (!token || !verifyToken(token)) return new Response(null, { status: 400 });
  return Response.redirect(new URL(`/preferences/${token}`, url.origin), 302);
}

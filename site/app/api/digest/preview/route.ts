import { timingSafeEqual } from "node:crypto";
import { render } from "@react-email/components";
import { DigestEmail, digestHeading, digestText, type DigestItemView } from "@/emails/digest";
import { hasDatabase } from "@/lib/db";
import { itemsByStatus } from "@/lib/digest";

/**
 * Render whatever is queued, through the code that will send it.
 *
 * The approve script cannot do this itself: it is plain node and the template is
 * a `.tsx`, which node will not transform. Rendering here is the better answer
 * anyway, because the preview then comes out of the exact path a subscriber's
 * copy does rather than a second implementation that can drift from it.
 *
 * Guarded by CRON_SECRET, accepted in a header or a query parameter. A query
 * parameter ends up in request logs, which is a real cost; it is taken here
 * because a browser cannot set a header and the thing being protected is copy
 * that becomes public within the day.
 */

export const dynamic = "force-dynamic";

function authorised(request: Request, url: URL): boolean {
  const expected = process.env.CRON_SECRET;
  if (!expected) return false;

  const header = request.headers.get("authorization") ?? "";
  const given = header.startsWith("Bearer ") ? header.slice(7) : (url.searchParams.get("token") ?? "");

  const a = Buffer.from(given);
  const b = Buffer.from(expected);
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}

export async function GET(request: Request): Promise<Response> {
  const url = new URL(request.url);
  if (!authorised(request, url)) return new Response(null, { status: 401 });
  if (!hasDatabase()) return new Response("no database configured", { status: 503 });

  const status = url.searchParams.get("status") === "ready" ? "ready" : "draft";
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? url.origin;

  const queued = await itemsByStatus(status);
  if (queued.length === 0) {
    return new Response(`Nothing with status "${status}".`, {
      status: 404,
      headers: { "content-type": "text/plain; charset=utf-8" },
    });
  }

  const items: DigestItemView[] = queued.map((item) => ({
    skill: item.skill,
    headline: item.headline,
    body: item.body,
    install: item.install,
    url: item.url || `${siteUrl}/skills/${item.skill}`,
    iconUrl: item.iconUrl || `${siteUrl}/icons/${item.skill}.png`,
  }));

  const props = {
    email: "you@example.com",
    cadence: "weekly",
    items,
    preferencesUrl: `${siteUrl}/preferences/preview`,
    unsubscribeUrl: `${siteUrl}/api/unsubscribe?token=preview`,
    siteUrl,
  };

  const subject = items.length === 1 ? queued[0]?.subject : digestHeading(items);

  // `?part=text` shows the plain-text alternative, which is written by hand and
  // therefore has to be readable on its own rather than assumed correct.
  if (url.searchParams.get("part") === "text") {
    return new Response(`Subject: ${subject}\n\n${digestText(props)}`, {
      headers: { "content-type": "text/plain; charset=utf-8", "x-robots-tag": "noindex" },
    });
  }

  const html = await render(DigestEmail(props));
  return new Response(html, {
    headers: { "content-type": "text/html; charset=utf-8", "x-robots-tag": "noindex" },
  });
}

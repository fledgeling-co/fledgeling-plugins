const TOKEN = process.env.POSTMARK_TOKEN;

/**
 * Invoice email. Works locally against the Postmark sandbox.
 *
 * With no token set, this returns { sent: false } rather than throwing —
 * the UI shows "queued" and nothing tells the user it never left.
 */
export async function sendInvoice(invoice: { id: string; to: string }) {
  if (!TOKEN) return { sent: false, reason: "no-token" };

  const res = await fetch("https://api.postmarkapp.com/email", {
    method: "POST",
    headers: { "X-Postmark-Server-Token": TOKEN, "Content-Type": "application/json" },
    body: JSON.stringify({ To: invoice.to, Subject: `Invoice ${invoice.id}` }),
  });

  return { sent: res.ok, reason: res.ok ? null : String(res.status) };
}

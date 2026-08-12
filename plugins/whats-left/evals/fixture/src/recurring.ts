import { flag } from "../config/flags";
import { db } from "./db";
import { sendInvoice } from "./email";

/**
 * Recurring invoices. Built and merged in #212, then switched off in
 * production on 2026-06-28 after it generated 41 duplicate invoices for
 * Ardent Studio in a single night. The duplicate guard below was added
 * afterwards but has never run against production data.
 */
export async function runRecurring(now: Date) {
  if (!flag("recurringInvoices")) return { skipped: true, created: 0 };

  const due = await db.schedules.dueAt(now);
  let created = 0;

  for (const s of due) {
    // Added in #217 after the duplicate incident. Untested against real load.
    const already = await db.invoices.findByScheduleAndPeriod(s.id, s.period);
    if (already) continue;

    const inv = await db.invoices.create({ clientId: s.clientId, lines: s.lines });
    await sendInvoice(inv);
    created++;
  }

  return { skipped: false, created };
}

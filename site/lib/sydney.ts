/**
 * Sydney wall-clock time.
 *
 * The digest sends at 10am in Sydney, and Sydney is UTC+10 for half the year
 * and UTC+11 for the other half. Every date and hour that decides whether to
 * send is therefore computed in `Australia/Sydney` rather than in UTC, and
 * `Intl` is what knows when the changeover falls — a stored offset would be
 * wrong twice a year and correct in between, which is the hardest kind of bug
 * to notice.
 *
 * Not `server-only`: the cron route and the local scripts both need it.
 */

const ZONE = "Australia/Sydney";

const FORMAT = new Intl.DateTimeFormat("en-CA", {
  timeZone: ZONE,
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  hour12: false,
});

export type SydneyNow = {
  /** `YYYY-MM-DD` — the Sydney calendar day. */
  date: string;
  /** 0-23, Sydney local. */
  hour: number;
};

export function sydneyNow(at: Date = new Date()): SydneyNow {
  const parts = FORMAT.formatToParts(at);
  const get = (type: Intl.DateTimeFormatPartTypes) =>
    parts.find((part) => part.type === type)?.value ?? "";

  // en-CA gives 24-hour time, but "24" appears for midnight in some ICU
  // versions, which would read as hour 24 rather than hour 0.
  const hour = Number(get("hour")) % 24;
  return { date: `${get("year")}-${get("month")}-${get("day")}`, hour };
}

/**
 * Whole days between two `YYYY-MM-DD` strings.
 *
 * Parsed at UTC midnight deliberately: these are calendar labels, not instants,
 * so no timezone should be applied to them a second time. Comparing labels is
 * the point — an elapsed-milliseconds test would skip a week whenever one send
 * ran late and the next ran early, which the ±59 min cron jitter guarantees.
 */
export function daysBetween(from: string, to: string): number {
  const a = Date.parse(`${from}T00:00:00Z`);
  const b = Date.parse(`${to}T00:00:00Z`);
  if (Number.isNaN(a) || Number.isNaN(b)) return Number.POSITIVE_INFINITY;
  return Math.round((b - a) / 86_400_000);
}

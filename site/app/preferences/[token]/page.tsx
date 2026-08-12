import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { CadencePicker } from "@/components/cadence-picker";
import { verifyToken } from "@/lib/subscribe-token";
import { findById } from "@/lib/subscribers";
import styles from "./page.module.css";

/**
 * The preference page an email link lands on.
 *
 * Four options, not a toggle and a separate destructive flow: Daily, Weekly,
 * Pause, Leave. Leaving is one choice among four, which is how GitHub's
 * newsletter preferences model it, and it means nobody has to hunt for the
 * unsubscribe or pass through a confirmation dialog designed to talk them out
 * of it.
 *
 * No session. The token in the URL is the whole credential, which is why it is
 * signed and why this page is never indexed.
 */

export const metadata: Metadata = {
  title: "Email preferences · Fledgeling Skills",
  robots: { index: false, follow: false },
};

export const dynamic = "force-dynamic";

export default async function PreferencesPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;
  const id = verifyToken(token);
  if (!id) notFound();

  const subscriber = await findById(id);
  if (!subscriber) notFound();

  return (
    <main className={styles.page}>
      <div className="container">
        <p className={`eyebrow ${styles.eyebrow}`}>Fledgeling · Skills</p>
        <CadencePicker token={token} current={subscriber.cadence} email={subscriber.email} />
      </div>
    </main>
  );
}

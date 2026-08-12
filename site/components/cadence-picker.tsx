"use client";

import Link from "next/link";
import { useActionState } from "react";
import { setCadenceAction, type CadenceState } from "@/app/actions/subscribe";
import type { Cadence } from "@/lib/subscribers";
import styles from "./cadence-picker.module.css";

/**
 * Four cards, one submit per card.
 *
 * Each card is its own form so the whole thing works with JavaScript off: a
 * click posts that cadence and the page comes back with it saved. With
 * JavaScript, `useActionState` swaps in the confirmation without a reload.
 *
 * Leaving plays a short mark rather than a celebration. Every confirmation
 * screen in the reference set was plain centred text; a party at the moment
 * someone leaves reads as a company that has not listened.
 */

const OPTIONS: { value: Cadence; label: string; when: string; body: string }[] = [
  {
    value: "daily",
    label: "Daily",
    when: "The day it lands",
    body: "An email on any day a new skill lands. Quiet days stay quiet.",
  },
  {
    value: "weekly",
    label: "Weekly",
    when: "Once a week",
    body: "Anything new from the past seven days, in one email. This is the default, and it's what most people want.",
  },
  {
    value: "paused",
    label: "Pause",
    when: "Nothing for now",
    body: "You stay on the list and receive nothing. Come back and change it whenever.",
  },
  {
    value: "none",
    label: "Leave",
    when: "Take me off",
    body: "You're removed from the list for good. You can sign up again any time.",
  },
];

const INITIAL: CadenceState = { status: "idle" };

export function CadencePicker({
  token,
  current,
  email,
}: {
  token: string;
  current: Cadence;
  email: string;
}) {
  const [state, action, pending] = useActionState(setCadenceAction, INITIAL);
  const selected = state.status === "saved" ? state.cadence : current;
  const hasLeft = state.status === "saved" && state.cadence === "none";

  // The heading lives here rather than in the page so that leaving replaces it.
  // Left in the page, "How often would you like to hear?" and "whatever you pick
  // takes effect immediately" sat above a confirmation that there was nothing
  // left to pick.
  if (hasLeft) {
    return (
      <div className={styles.left} role="status">
        <span className={styles.mark} aria-hidden="true">
          <svg viewBox="0 0 48 48" width="48" height="48" fill="none">
            <circle className={styles.ring} cx="24" cy="24" r="20" strokeWidth="2.5" />
            <path className={styles.tick} d="M15 24.5l6.5 6.5L33 19" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </span>
        <h1 className={`display ${styles.leftTitle}`}>That&rsquo;s done, you&rsquo;re off the list.</h1>
        <p className={styles.leftBody}>
          Nothing else will go to {email}. The skills are all still on the site whenever you want a
          look.
        </p>
        <Link className={styles.leftLink} href="/">
          Back to the skills
        </Link>
      </div>
    );
  }

  return (
    <>
      <h1 className={`display ${styles.title}`}>How often would you like to hear?</h1>
      <p className={styles.lede}>
        You&rsquo;re changing the list for <strong>{email}</strong>. Whatever you pick takes effect
        immediately.
      </p>

      <div className={styles.grid}>
        {OPTIONS.map((option) => {
          const isCurrent = option.value === selected;
          return (
            <form key={option.value} action={action} className={styles.cardForm}>
              <input type="hidden" name="token" value={token} />
              <input type="hidden" name="cadence" value={option.value} />
              <button
                type="submit"
                disabled={pending}
                aria-current={isCurrent ? "true" : undefined}
                className={`${styles.card} ${isCurrent ? styles.cardCurrent : ""} ${
                  option.value === "none" ? styles.cardLeave : ""
                }`}
              >
                <span className={styles.cardHead}>
                  <span className={styles.cardLabel}>{option.label}</span>
                  {/* A word, not only a colour: the current choice has to be
                      legible to someone who cannot see the fill. */}
                  {isCurrent ? <span className={styles.cardState}>Current</span> : null}
                </span>
                <span className={styles.cardWhen}>{option.when}</span>
                <span className={styles.cardBody}>{option.body}</span>
              </button>
            </form>
          );
        })}
      </div>

      <p className={styles.status} role="status">
        {state.status === "saved"
          ? `Saved. You're on ${labelFor(state.cadence)}.`
          : state.status === "error"
            ? "That didn't save. The link may have expired; try the one in your most recent email."
            : " "}
      </p>
    </>
  );
}

function labelFor(cadence: Cadence): string {
  return OPTIONS.find((o) => o.value === cadence)?.label.toLowerCase() ?? cadence;
}

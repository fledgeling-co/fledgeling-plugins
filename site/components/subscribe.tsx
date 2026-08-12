"use client";

import { usePathname } from "next/navigation";
import { useActionState, useId } from "react";
import { subscribeAction, type SubscribeState } from "@/app/actions/subscribe";
import styles from "./subscribe.module.css";

/**
 * The subscribe field, in the footer of every page.
 *
 * Every state is designed rather than defaulted: idle, submitting, success,
 * invalid address, service unavailable, unexpected failure. The success state
 * echoes the address back with a way to correct it, which is the fix for the
 * dead end where someone mistypes their address, believes they subscribed, and
 * never hears anything.
 *
 * Progressive enhancement is not decorative here. `useActionState` posts the
 * form natively when JavaScript has not loaded, and this sits on pages people
 * arrive at cold from search.
 */

const INITIAL: SubscribeState = { status: "idle" };

/**
 * The footer mount.
 *
 * Suppressed on the preference pages. Someone who arrived there is already on
 * the list and is there to change or leave it; offering them a sign-up form
 * competes with the page's only job, and directly under "you're off the list"
 * it reads as an immediate re-solicitation.
 */
export function FooterSubscribe({ className }: { className?: string }) {
  const pathname = usePathname();
  // The wrapper goes with it, so the footer does not keep an empty padded band.
  if (pathname?.startsWith("/preferences")) return null;
  return (
    <div className={className}>
      <Subscribe source="footer" />
    </div>
  );
}

export function Subscribe({ source = "site" }: { source?: string }) {
  const [state, action, pending] = useActionState(subscribeAction, INITIAL);
  const fieldId = useId();
  const noteId = useId();

  if (state.status === "ok") {
    return (
      <div className={styles.wrap}>
        <p className={styles.heading}>You&rsquo;re on the list.</p>
        <p className={styles.done}>
          Subscribed as <strong>{state.email}</strong>.{" "}
          {/* A reload clears the action state and returns the form. */}
          <a className={styles.correct} href="">
            Not you? Use a different address.
          </a>
        </p>
      </div>
    );
  }

  const problem =
    state.status === "invalid"
      ? "That address doesn't look right. Worth a second look."
      : state.status === "unavailable"
        ? "Sign-up isn't working right now. Try again in a bit, or watch the repo on GitHub instead."
        : state.status === "error"
          ? "Something went wrong saving that. Try again in a moment."
          : null;

  return (
    <div className={styles.wrap}>
      <p className={styles.heading}>Hear when there&rsquo;s a new one</p>
      <p className={styles.blurb}>
        An email when a new skill lands. Nothing else goes out on this list, and you pick daily or
        weekly.
      </p>

      <form className={styles.form} action={action} noValidate>
        <input type="hidden" name="source" value={source} />
        {/* Honeypot. Hidden from sight and from assistive tech, filled by bots. */}
        <div className={styles.pot} aria-hidden="true">
          <label htmlFor={`${fieldId}-company`}>Company</label>
          <input id={`${fieldId}-company`} name="company" type="text" tabIndex={-1} autoComplete="off" />
        </div>

        <label className={styles.label} htmlFor={fieldId}>
          Your email address
        </label>
        <div className={styles.row}>
          <input
            id={fieldId}
            className={styles.input}
            name="email"
            type="email"
            inputMode="email"
            autoComplete="email"
            required
            placeholder="you@example.com"
            aria-describedby={problem ? noteId : undefined}
            aria-invalid={state.status === "invalid" || undefined}
          />
          <button className={styles.button} type="submit" disabled={pending}>
            {pending ? "Adding…" : "Subscribe"}
          </button>
        </div>

        {problem ? (
          <p className={styles.problem} id={noteId} role="status">
            {problem}
          </p>
        ) : null}
      </form>
    </div>
  );
}

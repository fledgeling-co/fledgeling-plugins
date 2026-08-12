"use client";

import { usePathname } from "next/navigation";
import { useActionState, useEffect, useId, useRef, useSyncExternalStore } from "react";
import { subscribeAction, type SubscribeState } from "@/app/actions/subscribe";
import styles from "./subscribe-bar.module.css";

/**
 * The always-visible signup.
 *
 * Shown from the first paint and never hidden by scroll position: this page is
 * ~6,300px tall, so anything that waits for a scroll or steps aside near the
 * bottom is a signup most visitors never meet.
 *
 * Because it is always on screen, the footer's own form would be a second copy
 * of itself at the bottom of every page. So this marks the document while it is
 * mounted and the footer block hides under that mark — exactly one form exists
 * at any moment. With JavaScript off nothing marks anything, the bar never
 * renders, and the footer form is the one that works.
 *
 * Dismissing is still possible and still permanent. A bar with no way out is
 * the thing people install blockers for, and closing it returns the footer
 * form, so the signup never actually disappears.
 */

const DISMISS_KEY = "fledgeling-skills:subscribe-bar-dismissed";
const INITIAL: SubscribeState = { status: "idle" };

/**
 * Dismissal lives in localStorage, which is an external store rather than React
 * state — so it is read through useSyncExternalStore. Reading it in an effect
 * and calling setState would either flash the bar at someone who already closed
 * it, or cascade a second render on every mount.
 *
 * The server snapshot is `true` (hidden), so nothing is ever sent in the HTML
 * that the client then has to take away.
 */
const listeners = new Set<() => void>();

function subscribeToDismissal(onChange: () => void) {
  listeners.add(onChange);
  window.addEventListener("storage", onChange);
  return () => {
    listeners.delete(onChange);
    window.removeEventListener("storage", onChange);
  };
}

function readDismissed(): boolean {
  try {
    return window.localStorage.getItem(DISMISS_KEY) === "1";
  } catch {
    return false; // storage blocked: show it rather than swallow the feature
  }
}

function setDismissed() {
  try {
    window.localStorage.setItem(DISMISS_KEY, "1");
  } catch {
    /* storage blocked; it stays closed for this page view */
  }
  dismissedThisView = true;
  listeners.forEach((l) => l());
}

let dismissedThisView = false;

export function SubscribeBar() {
  const pathname = usePathname();
  const [state, action, pending] = useActionState(subscribeAction, INITIAL);
  const fieldId = useId();
  const barRef = useRef<HTMLDivElement>(null);
  const dismissed = useSyncExternalStore(
    subscribeToDismissal,
    () => dismissedThisView || readDismissed(),
    () => true,
  );

  // Marks the document so the footer's copy of this form stands down, and
  // publishes the bar's own height so the page can make exactly that much room
  // at the bottom. Measured rather than hard-coded: the bar is taller when it is
  // showing an error, and shorter on a phone, and a fixed guess is how the last
  // line of the colophon ends up permanently behind it.
  useEffect(() => {
    if (dismissed) return;
    const root = document.documentElement;
    root.dataset.subscribeBar = "on";

    const el = barRef.current;
    const publish = () => {
      root.style.setProperty("--subscribe-bar-h", `${el?.offsetHeight ?? 0}px`);
    };
    publish();
    const ro = el ? new ResizeObserver(publish) : null;
    if (el && ro) ro.observe(el);

    return () => {
      ro?.disconnect();
      delete root.dataset.subscribeBar;
      root.style.removeProperty("--subscribe-bar-h");
    };
  }, [dismissed]);

  // Subscribing is its own dismissal — nobody needs the ask again.
  useEffect(() => {
    if (state.status === "ok") {
      const t = setTimeout(setDismissed, 4000);
      return () => clearTimeout(t);
    }
  }, [state.status]);

  if (pathname?.startsWith("/preferences")) return null;
  if (dismissed) return null;

  return (
    <div className={styles.bar} ref={barRef}>
      <div className={styles.inner}>
        {state.status === "ok" ? (
          <p className={styles.done} role="status">
            You&rsquo;re on the list. Confirmation is on its way to{" "}
            <strong>{state.email}</strong>.
          </p>
        ) : (
          <>
            <p className={styles.pitch}>
              <strong>Hear when there&rsquo;s a new one.</strong>{" "}
              <span className={styles.pitchRest}>
                An email when a new skill lands, daily or weekly.
              </span>
            </p>

            <form className={styles.form} action={action} noValidate>
              <input type="hidden" name="source" value="bar" />
              <div className={styles.pot} aria-hidden="true">
                <label htmlFor={`${fieldId}-company`}>Company</label>
                <input
                  id={`${fieldId}-company`}
                  name="company"
                  type="text"
                  tabIndex={-1}
                  autoComplete="off"
                />
              </div>

              <label className="visuallyHidden" htmlFor={fieldId}>
                Your email address
              </label>
              <input
                id={fieldId}
                className={styles.input}
                name="email"
                type="email"
                required
                autoComplete="email"
                placeholder="you@example.com"
                aria-invalid={state.status === "invalid" ? true : undefined}
              />
              <button className={styles.button} type="submit" disabled={pending}>
                {pending ? "Adding…" : "Subscribe"}
              </button>
            </form>
          </>
        )}

        <button
          className={styles.close}
          type="button"
          onClick={setDismissed}
          aria-label="Close the subscribe bar"
        >
          <svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true">
            <path
              d="M4 4l8 8M12 4l-8 8"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </div>

      {state.status !== "ok" && state.status !== "idle" ? (
        <p className={styles.problem} role="status">
          {state.status === "invalid"
            ? "That address doesn't look right."
            : state.status === "unavailable"
              ? "Sign-up isn't working right now. Try again in a bit."
              : "Something went wrong saving that. Try again in a moment."}
        </p>
      ) : null}
    </div>
  );
}

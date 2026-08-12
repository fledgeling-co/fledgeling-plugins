"use client";

import { usePathname } from "next/navigation";
import { useActionState, useEffect, useId, useState, useSyncExternalStore } from "react";
import { subscribeAction, type SubscribeState } from "@/app/actions/subscribe";
import styles from "./subscribe-bar.module.css";

/**
 * The always-visible signup.
 *
 * The footer block is the full pitch, but this page is ~6,300px tall, so on a
 * first visit the footer sits about 5,400px down and nobody meets it. This bar
 * is the same form as chrome instead of as content.
 *
 * Three rules keep it from being the thing everyone hates:
 *
 *  - It stays out of the hero. Nothing appears until the search field and the
 *    first band of the roster have scrolled away, so the page's actual job is
 *    never competing with an ask.
 *  - It retracts when the footer widget comes into view. Two identical forms on
 *    one screen reads as a bug, and the footer one is the better of the two.
 *  - Dismissing it is permanent, and remembered. A bar you have to close twice
 *    is worse than no bar.
 */

const DISMISS_KEY = "fledgeling-skills:subscribe-bar-dismissed";
const SHOW_AFTER_PX = 700;
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
  const [pastHero, setPastHero] = useState(false);
  const [footerInView, setFooterInView] = useState(false);
  const fieldId = useId();
  const dismissed = useSyncExternalStore(
    subscribeToDismissal,
    () => dismissedThisView || readDismissed(),
    () => true,
  );

  useEffect(() => {
    const onScroll = () => setPastHero(window.scrollY > SHOW_AFTER_PX);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Retract while the footer's own form is on screen.
  useEffect(() => {
    const footerForm = document.querySelector("footer form");
    if (!footerForm) return;
    const io = new IntersectionObserver(
      (entries) => setFooterInView(entries.some((e) => e.isIntersecting)),
      { rootMargin: "0px 0px -40px 0px" },
    );
    io.observe(footerForm);
    return () => io.disconnect();
  }, [state.status]);

  // Subscribing is its own dismissal — nobody needs the ask again.
  useEffect(() => {
    if (state.status === "ok") {
      const t = setTimeout(setDismissed, 4000);
      return () => clearTimeout(t);
    }
  }, [state.status]);

  if (pathname?.startsWith("/preferences")) return null;
  if (dismissed) return null;

  const open = pastHero && !footerInView;

  return (
    <div
      className={`${styles.bar} ${open ? styles.open : ""}`}
      // Out of the tab order and the a11y tree while it is off-screen, so a
      // keyboard user never tabs into a control they cannot see.
      aria-hidden={open ? undefined : true}
      inert={!open}
    >
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
                An email when a skill lands or changes, daily or weekly.
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

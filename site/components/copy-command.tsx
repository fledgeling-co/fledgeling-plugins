"use client";

import { useCallback, useEffect, useState } from "react";
import styles from "./copy-command.module.css";

/**
 * A command you can read and a button that copies it. The command is always
 * visible as text — a copy button that hides what it copies asks for trust it
 * has not earned, and it breaks for anyone whose clipboard permission is denied.
 */
export function CopyCommand({ command, label }: { command: string; label?: string }) {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!copied) return;
    const timer = setTimeout(() => setCopied(false), 2200);
    return () => clearTimeout(timer);
  }, [copied]);

  const copy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
    } catch {
      // Clipboard denied or unavailable. The command is on screen; select it.
      setCopied(false);
    }
  }, [command]);

  return (
    <div className={styles.wrap}>
      {label ? <span className={styles.label}>{label}</span> : null}
      <div className={styles.row}>
        <code className={styles.code}>{command}</code>
        <button type="button" className={styles.button} onClick={() => void copy()}>
          <span aria-hidden="true">{copied ? "Copied" : "Copy"}</span>
          <span className="visuallyHidden">
            {copied ? "Copied to clipboard" : `Copy ${command} to clipboard`}
          </span>
        </button>
      </div>
    </div>
  );
}

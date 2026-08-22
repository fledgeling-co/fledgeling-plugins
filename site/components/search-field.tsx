"use client";

import styles from "./search-field.module.css";

export type Lane = "browse" | "local" | "asking" | "ai" | "degraded";

type Props = {
  query: string;
  onQueryChange: (value: string) => void;
  onAsk: () => void;
  /** A suggestion click fills the field and runs immediately — never opens a dialog. */
  onSuggestion: (value: string) => void;
  onStop: () => void;
  onReset: () => void;
  lane: Lane;
  matchCount: number;
  total: number;
  note: string | null;
  suggestions: string[];
};

const MAX_QUERY = 200;

export function SearchField({
  query,
  onQueryChange,
  onAsk,
  onSuggestion,
  onStop,
  onReset,
  lane,
  matchCount,
  total,
  note,
  suggestions,
}: Props) {
  const asking = lane === "asking";

  return (
    <div className={styles.wrap}>
      <form
        className={styles.field}
        role="search"
        onSubmit={(event) => {
          event.preventDefault();
          if (!asking && query.trim()) onAsk();
        }}
      >
        <SearchGlyph />
        <label className="visuallyHidden" htmlFor="skill-search">
          Describe the problem you are trying to solve
        </label>
        <input
          id="skill-search"
          className={styles.input}
          type="search"
          name="q"
          value={query}
          maxLength={MAX_QUERY}
          autoComplete="off"
          spellCheck={false}
          placeholder="What are you trying to do?"
          onChange={(event) => onQueryChange(event.target.value)}
          onKeyDown={(event) => {
            // Escape is the way back from every lane, including while the AI
            // lane is still working. Without it the only exit was a text link
            // in the status line, and that line does not exist while asking.
            if (event.key === "Escape" && (query.length > 0 || lane !== "browse")) {
              event.preventDefault();
              onReset();
            }
          }}
        />
        {query.length > 0 && (
          <button
            type="button"
            className={styles.clear}
            onClick={onReset}
            aria-label="Clear the search and show every skill"
            title="Clear (Esc)"
          >
            <ClearGlyph />
          </button>
        )}
        {asking ? (
          <button type="button" className={styles.stop} onClick={onStop}>
            Stop
          </button>
        ) : (
          <button type="submit" className={styles.ask} disabled={query.trim().length === 0}>
            Ask
            <span className={styles.kbd}>⏎</span>
          </button>
        )}
        {asking && (
          <span className={styles.track} aria-hidden="true">
            <span className={styles.trackFill} />
          </span>
        )}
      </form>

      {lane === "browse" ? (
        <div className={styles.suggestions}>
          <span className={styles.suggestionsLabel}>Try</span>
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              className={styles.suggestion}
              onClick={() => onSuggestion(suggestion)}
            >
              {suggestion}
            </button>
          ))}
        </div>
      ) : (
        <p className={styles.status} aria-live="polite">
          <Status
            lane={lane}
            matchCount={matchCount}
            total={total}
            note={note}
            onReset={onReset}
          />
        </p>
      )}
    </div>
  );
}

function Status({
  lane,
  matchCount,
  total,
  note,
  onReset,
}: Pick<Props, "lane" | "matchCount" | "total" | "note" | "onReset">) {
  if (lane === "asking") {
    return (
      <>
        <span className={styles.pulse} aria-hidden="true" />
        <span className={styles.statusWorking}>Reading the catalogue</span>
        <span className={styles.note}>· all {total} stay on the page</span>
        <button type="button" className={styles.reset} onClick={onReset}>
          Clear
        </button>
      </>
    );
  }

  if (lane === "ai") {
    return (
      <>
        <span className={styles.statusAi}>Ranked by AI</span>
        <span>
          · {matchCount} of {total} matched
        </span>
        <button type="button" className={styles.reset} onClick={onReset}>
          Clear
        </button>
      </>
    );
  }

  if (lane === "degraded") {
    return (
      <>
        <span className={styles.statusMono}>Name match</span>
        <span>· {note ?? "The AI lane is unavailable, so this is a plain text match."}</span>
        <button type="button" className={styles.reset} onClick={onReset}>
          Clear
        </button>
      </>
    );
  }

  return (
    <>
      <span className={styles.statusMono}>Name match</span>
      <span>
        · {matchCount} of {total}
      </span>
      <span className={styles.note}>· press ⏎ to ask instead</span>
    </>
  );
}

function ClearGlyph() {
  return (
    <svg viewBox="0 0 16 16" width="13" height="13" fill="none" aria-hidden="true">
      <path
        d="M4 4l8 8M12 4l-8 8"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
    </svg>
  );
}

function SearchGlyph() {
  return (
    <svg
      className={styles.glyph}
      width="17"
      height="17"
      viewBox="0 0 17 17"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      aria-hidden="true"
    >
      <circle cx="7.2" cy="7.2" r="5.2" />
      <path d="M11 11l4 4" strokeLinecap="round" />
    </svg>
  );
}

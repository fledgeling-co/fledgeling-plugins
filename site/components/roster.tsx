"use client";

import { useCallback, useMemo, useRef, useState } from "react";
import type { Group, SkillSummary } from "@/lib/skills";
import { rankLocally, applyAiOrder } from "@/lib/search";
import { SearchField, type Lane } from "./search-field";
import { SkillCard, SkillRow } from "./skill-card";
import styles from "./roster.module.css";

/**
 * The roster.
 *
 * One rule governs the whole surface: rank is the only state. Every skill is on
 * the page in every mode — typing changes the order and how much room each one
 * takes, and the AI lane changes the same two things plus attaches a reason.
 * Nothing is ever filtered out, so there is no empty state and no dead end, and
 * a visitor who typed a bad query can still see the thing they were looking for.
 */

type Props = {
  skills: SkillSummary[];
  groups: Group[];
  suggestions: string[];
};

type AiResult = {
  order: string[];
  reasons: Map<string, string>;
  alsoConsider: { name: string; why: string }[];
  noMatch: string | null;
};

export function Roster({ skills, groups, suggestions }: Props) {
  const [query, setQuery] = useState("");
  const [lane, setLane] = useState<Lane>("browse");
  const [ai, setAi] = useState<AiResult | null>(null);
  const [note, setNote] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const trimmed = query.trim();

  const ranked = useMemo(() => {
    if (lane === "ai" && ai) return applyAiOrder(skills, ai.order, ai.reasons);
    return rankLocally(skills, trimmed);
  }, [skills, trimmed, lane, ai]);

  const promoted = ranked.filter((entry) => entry.matched);
  const rest = ranked.filter((entry) => !entry.matched);

  const reset = useCallback(() => {
    abortRef.current?.abort();
    setQuery("");
    setAi(null);
    setNote(null);
    setLane("browse");
  }, []);

  const onQueryChange = useCallback((value: string) => {
    setQuery(value);
    setAi(null);
    setNote(null);
    setLane(value.trim() ? "local" : "browse");
  }, []);

  const ask = useCallback(
    async (raw?: string) => {
      const q = (raw ?? query).trim();
      if (!q) return;

      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      setLane("asking");
      setNote(null);

      try {
        const response = await fetch("/api/search", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ query: q }),
          signal: controller.signal,
        });

        if (!response.ok) {
          const reason =
            response.status === 429
              ? "Too many questions from here in the last minute — this is the plain text match instead."
              : response.status === 503
                ? "The AI lane is not configured on this deployment."
                : "The AI lane did not answer, so this is the plain text match.";
          setNote(reason);
          setLane("degraded");
          return;
        }

        const payload = (await response.json()) as {
          matches?: { slug: string; reason: string }[];
          alsoConsider?: { slug: string; why: string }[];
          noMatch?: string;
        };

        // Only slugs that exist in the catalogue survive. The model cannot invent
        // a skill, and a hostile query cannot put arbitrary text on a card.
        const known = new Set(skills.map((skill) => skill.name));
        const matches = (payload.matches ?? []).filter((match) => known.has(match.slug));

        if (matches.length === 0) {
          setNote(payload.noMatch ?? "Nothing here fits that. The plain text match is below.");
          setLane("degraded");
          return;
        }

        setAi({
          order: matches.map((match) => match.slug),
          reasons: new Map(matches.map((match) => [match.slug, match.reason])),
          alsoConsider: (payload.alsoConsider ?? [])
            .filter((entry) => known.has(entry.slug))
            .map((entry) => ({ name: entry.slug, why: entry.why })),
          noMatch: payload.noMatch ?? null,
        });
        setLane("ai");
      } catch (error) {
        if ((error as Error).name === "AbortError") {
          setLane(q ? "local" : "browse");
          return;
        }
        setNote("Could not reach the AI lane. This is the plain text match.");
        setLane("degraded");
      }
    },
    [query, skills],
  );

  const onSuggestion = useCallback(
    (value: string) => {
      setQuery(value);
      setAi(null);
      void ask(value);
    },
    [ask],
  );

  return (
    <>
      <SearchField
        query={query}
        onQueryChange={onQueryChange}
        onAsk={() => void ask()}
        onSuggestion={onSuggestion}
        onStop={() => abortRef.current?.abort()}
        onReset={reset}
        lane={lane}
        matchCount={promoted.length}
        total={skills.length}
        note={note}
        suggestions={suggestions}
      />

      <div className={styles.roster} id="skills">
        {lane === "browse" ? (
          <BrowseMode skills={skills} groups={groups} />
        ) : (
          <QueryMode
            promoted={promoted}
            rest={rest}
            reasons={ai?.reasons}
            alsoConsider={ai?.alsoConsider ?? []}
            skills={skills}
            asking={lane === "asking"}
          />
        )}
      </div>
    </>
  );
}

/* ------------------------------------------------------------ browse mode -- */

function BrowseMode({ skills, groups }: { skills: SkillSummary[]; groups: Group[] }) {
  return (
    <>
      {groups.map((group) => {
        const members = skills.filter((skill) => skill.group === group.id);
        return (
          <section key={group.id} className={styles.group} aria-labelledby={`group-${group.id}`}>
            <header className={styles.groupHead} data-motion="group-head">
              <h2 className={styles.groupLabel} id={`group-${group.id}`}>
                {group.label}
              </h2>
              <span className={styles.groupCount}>
                {group.count} skill{group.count === 1 ? "" : "s"}
              </span>
              <p className={styles.groupBlurb}>{group.blurb}</p>
            </header>
            <div className={styles.grid}>{layOutWithPairs(members)}</div>
          </section>
        );
      })}
    </>
  );
}

/**
 * Group a section's skills so a confusable pair renders as one unit carrying the
 * rule that tells them apart. Both stay separate cards with their own links.
 */
function layOutWithPairs(members: SkillSummary[]) {
  const byName = new Map(members.map((skill) => [skill.name, skill]));
  const used = new Set<string>();
  const nodes: React.ReactNode[] = [];

  for (const skill of members) {
    if (used.has(skill.name)) continue;

    const partnerName = skill.neighbours.find(
      (name) => byName.has(name) && !used.has(name) && name !== skill.name,
    );

    if (partnerName) {
      const partner = byName.get(partnerName)!;
      used.add(skill.name);
      used.add(partnerName);
      nodes.push(
        <div className={styles.pair} key={`${skill.name}+${partnerName}`}>
          <p className={styles.pairRule}>
            <span className={styles.pairLabel}>Easily confused</span>
            <span>{decisionRule(skill, partner)}</span>
          </p>
          <SkillCard skill={skill} />
          <SkillCard skill={partner} />
        </div>,
      );
      continue;
    }

    used.add(skill.name);
    nodes.push(<SkillCard key={skill.name} skill={skill} />);
  }

  return nodes;
}

/**
 * The rule that tells a pair apart, built from each side's own boundary clause —
 * the skills' own words, not an editorial gloss added here.
 *
 * Boundary clauses nest parentheticals ("… (use ship-fleet for a repo's backlog,
 * ship-feature for one feature) and NOT for a single manifest entry update (use
 * armada-sync)"), so the inner asides are removed before the clause immediately
 * preceding the referral is taken. Anything that comes out implausible falls back
 * to pointing at the two boundary lines rather than printing a mangled sentence.
 */
function decisionRule(a: SkillSummary, b: SkillSummary): string {
  const sides = [sideOf(a, b.name), sideOf(b, a.name)].filter(Boolean);
  if (sides.length === 2) return `${sides[0]}; ${sides[1]}.`;
  if (sides.length === 1) return `${sides[0]}.`;
  return `${a.name} and ${b.name} each name the other as the wrong tool — the "not for" line on each card says which.`;
}

function sideOf(skill: SkillSummary, other: string): string | null {
  const clause = skill.boundary?.text ?? "";
  const at = clause.indexOf(`(use ${other}`);
  if (at === -1) return null;

  let before = clause.slice(0, at).replace(/\([^)]*\)/g, "");

  // Keep only the clause this referral belongs to. "or" is deliberately not a
  // cut point — it joins items inside one clause ("interval or polling work").
  const cut = Math.max(
    before.lastIndexOf(";"),
    before.lastIndexOf(" NOT for "),
    before.lastIndexOf(" Not for "),
    before.lastIndexOf(","),
  );
  if (cut !== -1) before = before.slice(cut);

  const scope = before
    .replace(/^[;,]/, "")
    .replace(/^\s*(and|or)\s+/i, "")
    .replace(/^\s*(NOT|Not)\s+for\s+/, "")
    .replace(/\s+/g, " ")
    .trim();

  return scope.length >= 8 && scope.length <= 90 ? `${other} for ${scope}` : null;
}

/* ------------------------------------------------------------- query mode -- */

function QueryMode({
  promoted,
  rest,
  reasons,
  alsoConsider,
  skills,
  asking,
}: {
  promoted: ReturnType<typeof rankLocally>;
  rest: ReturnType<typeof rankLocally>;
  reasons: Map<string, string> | undefined;
  alsoConsider: { name: string; why: string }[];
  skills: SkillSummary[];
  asking: boolean;
}) {
  const byName = new Map(skills.map((skill) => [skill.name, skill]));

  return (
    <div className={styles.ranked}>
      {/* While the AI lane is working the local ranking stays on screen and
          stays correct — dimmed, not replaced. Swapping real results for
          skeletons would take away an answer the visitor already has. */}
      <div className={asking ? `${styles.promoted} ${styles.working}` : styles.promoted}>
        {promoted.map(({ skill }) => (
          <SkillCard key={skill.name} skill={skill} reason={reasons?.get(skill.name)} />
        ))}
      </div>

      {alsoConsider.length > 0 ? (
        <div className={styles.also}>
          <p className={styles.alsoLabel}>You will probably also want</p>
          {alsoConsider.map((entry) => {
            const skill = byName.get(entry.name);
            if (!skill) return null;
            return (
              <p className={styles.alsoItem} key={entry.name}>
                <a className={styles.alsoName} href={`/skills/${skill.name}`}>
                  {skill.name}
                </a>
                <span>{entry.why}</span>
              </p>
            );
          })}
        </div>
      ) : null}

      {rest.length > 0 ? (
        <div className={styles.rest}>
          <p className={styles.restLabel}>Everything else, still here</p>
          {rest.map(({ skill }) => (
            <SkillRow key={skill.name} skill={skill} />
          ))}
        </div>
      ) : null}
    </div>
  );
}

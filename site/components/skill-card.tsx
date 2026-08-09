import Image from "next/image";
import Link from "next/link";
import type { SkillSummary } from "@/lib/skills";
import styles from "./skill-card.module.css";

/**
 * One skill, at one of two densities.
 *
 * The roster never removes a skill — a query changes how much room each one
 * takes, not whether it is there. `full` is the browse and match density;
 * `compact` is everything below the promotion line.
 */

type Props = {
  skill: SkillSummary;
  /** The AI lane's one-line answer for THIS query. Rendered as marked AI copy. */
  reason?: string | undefined;
};

function pluralise(count: number, singular: string) {
  return `${count} ${singular}${count === 1 ? "" : "s"}`;
}

export function SkillCard({ skill, reason }: Props) {
  const { signals } = skill;

  return (
    <article className={styles.card}>
      <header className={styles.head}>
        <Image
          className={styles.icon}
          src={skill.icon}
          alt=""
          width={52}
          height={52}
          sizes="52px"
        />
        <div className={styles.titles}>
          <h3 className={styles.name}>
            <Link href={`/skills/${skill.name}`}>{skill.name}</Link>
          </h3>
          <p className={styles.meta}>
            <span>v{skill.version}</span>
            <span className={styles.metaDot} aria-hidden="true" />
            <span>{skill.group.replace(/-/g, " ")}</span>
          </p>
        </div>
      </header>

      <div>
        {reason ? (
          <p className={styles.reason}>
            <span className={styles.reasonLabel}>Matched by AI</span>
            {/* The lane returns a clause, not a sentence, so the frame lives here
                — one shape for every reason, and the model spends its words on
                the part that differs. */}
            Use this because {stripTrailingStop(reason)}.
          </p>
        ) : null}
        <p className={styles.blurb}>{skill.blurb}</p>
      </div>

      <footer>
        {skill.boundary ? (
          <p className={styles.boundary}>
            <span className={styles.boundaryLabel}>Not for</span>
            <span className={styles.boundaryText}>
              {stripLeadingNot(skill.boundary.text)}
              {skill.boundary.referrals.some((referral) => !referral.here) ? (
                <>
                  {" "}
                  <span className={styles.elsewhere}>
                    (
                    {skill.boundary.referrals
                      .filter((referral) => !referral.here)
                      .map((referral) => referral.name)
                      .join(", ")}{" "}
                    is in another marketplace)
                  </span>
                </>
              ) : null}
            </span>
          </p>
        ) : (
          <div className={styles.signals}>
            {signals.evals ? <span className={styles.signal}>Evals</span> : null}
            {signals.scripts ? <span className={styles.signal}>Scripts</span> : null}
            {signals.references > 0 ? (
              <span className={styles.signal}>{pluralise(signals.references, "reference")}</span>
            ) : null}
          </div>
        )}
      </footer>
    </article>
  );
}

export function SkillRow({ skill }: { skill: SkillSummary }) {
  return (
    <article className={styles.compact}>
      <Image
        className={styles.compactIcon}
        src={skill.icon}
        alt=""
        width={26}
        height={26}
        sizes="26px"
      />
      <div className={styles.compactBody}>
        <h3 className={styles.compactName}>
          <Link href={`/skills/${skill.name}`}>{skill.name}</Link>
        </h3>
        <p className={styles.compactBlurb}>{firstSentence(skill.blurb)}</p>
      </div>
      <span className={styles.compactGroup}>{skill.group.replace(/-/g, " ")}</span>
    </article>
  );
}

/** The label already says "Not for", so the clause should not say it twice. */
function stripLeadingNot(text: string): string {
  const trimmed = text.replace(/^(NOT|Not)\s+(for|a|to)\s+/, "");
  return trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
}

/** The card supplies the "Use this because …" frame and the full stop with it. */
function stripTrailingStop(text: string): string {
  return text.trim().replace(/[.\s]+$/, "");
}

function firstSentence(text: string): string {
  const end = text.search(/\.\s/);
  return end === -1 ? text : text.slice(0, end + 1);
}

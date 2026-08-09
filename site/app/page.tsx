import { Roster } from "@/components/roster";
import { CopyCommand } from "@/components/copy-command";
import { MARKETPLACE, getGroups, getSkillCount, getSkillSummaries } from "@/lib/skills";
import styles from "./page.module.css";

/**
 * Four real problems, drawn from what these skills actually address. They are
 * the answer to the blank-box problem: a click runs the query immediately, and
 * each one teaches that this field takes a situation, not a keyword.
 */
const SUGGESTIONS = [
  "my agent burns tokens without doing more work",
  "the UI it built looks AI-generated",
  "my long run stopped overnight and said it was done",
  "I need to write up what I just worked out",
];

export default function HomePage() {
  const skills = getSkillSummaries();
  const groups = getGroups();

  return (
    <>
      <section className={styles.hero}>
        <div className="container">
          <p className={`eyebrow ${styles.eyebrow}`}>
            Fledgeling · {getSkillCount()} skills for Claude Code
          </p>
          <h1 className={`display ${styles.title}`}>
            Skills built because a real workflow <em>needed</em> them.
          </h1>
          <p className={`lede ${styles.lede}`}>
            Each one exists because something kept going wrong, and each carries its own README,
            evals or references where the work justified them. Describe what you are trying to do —
            you do not need to know any of their names.
          </p>

          <div className={styles.search}>
            <Roster skills={skills} groups={groups} suggestions={SUGGESTIONS} />
          </div>
        </div>
      </section>

      <section className={styles.install}>
        <div className={`container ${styles.installInner}`}>
          <div className={styles.installCopy}>
            <h2 className={styles.installTitle}>Installing</h2>
            <p className={styles.installBody}>
              Add the marketplace once, then install whichever skills you want. Third-party
              marketplaces have auto-update switched off by default, so refreshing is something you
              do rather than something that happens.
            </p>
            <a className={styles.installLink} href="/install">
              The full lifecycle — update, disable, uninstall →
            </a>
          </div>
          <div className={styles.installCommands}>
            <CopyCommand
              label="Once"
              command={`/plugin marketplace add fledgeling-co/${MARKETPLACE}`}
            />
            <CopyCommand label="Then, per skill" command={`/plugin install trawl@${MARKETPLACE}`} />
          </div>
        </div>
      </section>
    </>
  );
}

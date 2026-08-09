import type { Metadata } from "next";
import Link from "next/link";
import { CopyCommand } from "@/components/copy-command";
import { MARKETPLACE, REPO, getSkillCount } from "@/lib/skills";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "Install",
  description:
    `Add the ${MARKETPLACE} marketplace, install skills from it, and keep them current. ` +
    "Third-party marketplaces do not auto-update by default.",
};

export default function InstallPage() {
  return (
    <article className={styles.page}>
      <div className="container">
        <Link href="/" className={styles.back}>
          ← All skills
        </Link>

        <h1 className={`display ${styles.title}`}>
          Add it once. Then install what you <em>need</em>.
        </h1>
        <p className={`lede ${styles.lede}`}>
          Everything below runs inside Claude Code. Adding a marketplace registers the catalogue and
          installs nothing; installing a skill is a separate, per-skill decision.
        </p>

        <section className={styles.step}>
          <h2 className={styles.stepTitle}>
            <span className={styles.stepNumber}>01</span> Add the marketplace
          </h2>
          <p className={styles.stepBody}>
            Once per machine. This registers all {getSkillCount()} skills as available; nothing is
            installed yet and nothing is added to your context.
          </p>
          <CopyCommand command={`/plugin marketplace add ${REPO}`} />
        </section>

        <section className={styles.step}>
          <h2 className={styles.stepTitle}>
            <span className={styles.stepNumber}>02</span> Install a skill
          </h2>
          <p className={styles.stepBody}>
            Per skill, by name. Claude Code opens the details so you can pick a scope — user (you,
            everywhere), project (everyone on the repo), or local (you, this repo only).
          </p>
          <CopyCommand command={`/plugin install trawl@${MARKETPLACE}`} />
          <p className={styles.stepNote}>
            For scripting, or to skip the interactive step:{" "}
            <code className={styles.inlineCode}>
              claude plugin install trawl@{MARKETPLACE} --scope project
            </code>
          </p>
        </section>

        <section className={styles.step}>
          <h2 className={styles.stepTitle}>
            <span className={styles.stepNumber}>03</span> Keep it current
          </h2>
          <p className={styles.stepBody}>
            Claude Code turns auto-update <strong>off</strong> by default for third-party
            marketplaces like this one — only Anthropic&rsquo;s own are on. So updating is something
            you do. Refresh the catalogue first, then reinstall or reload.
          </p>
          <CopyCommand command={`/plugin marketplace update ${MARKETPLACE}`} />
          <p className={styles.stepNote}>
            You can switch auto-update on per marketplace: run{" "}
            <code className={styles.inlineCode}>/plugin</code>, open{" "}
            <strong>Marketplaces</strong>, select this one, then{" "}
            <strong>Enable auto-update</strong>. Updates land after your session starts and prompt
            you to reload.
          </p>
        </section>

        <section className={styles.step}>
          <h2 className={styles.stepTitle}>
            <span className={styles.stepNumber}>04</span> Apply changes without restarting
          </h2>
          <p className={styles.stepBody}>
            If an install summary says the skill is not active yet, reload. When the reload would
            invalidate the prompt cache it warns and skips until you rerun it with{" "}
            <code className={styles.inlineCode}>--force</code>.
          </p>
          <CopyCommand command="/reload-plugins" />
        </section>

        <section className={styles.step}>
          <h2 className={styles.stepTitle}>
            <span className={styles.stepNumber}>05</span> Audit, disable, remove
          </h2>
          <p className={styles.stepBody}>
            Every installed skill costs context on every turn. Claude Code lists what you have not
            used recently under a <strong>Not used recently</strong> header in{" "}
            <code className={styles.inlineCode}>/plugin</code> → <strong>Installed</strong>.
          </p>
          <div className={styles.commandStack}>
            <CopyCommand label="What do I have" command="/plugin list" />
            <CopyCommand
              label="Switch one off, keep it installed"
              command={`/plugin disable trawl@${MARKETPLACE}`}
            />
            <CopyCommand label="Remove it" command={`/plugin uninstall trawl@${MARKETPLACE}`} />
          </div>
          <p className={styles.stepNote}>
            Removing the marketplace itself uninstalls everything you installed from it.
          </p>
        </section>

        <section className={styles.trust}>
          <h2 className={styles.trustTitle}>Before you install anything</h2>
          <p className={styles.trustBody}>
            A plugin runs with your privileges and can execute arbitrary code — that is true of this
            marketplace and every other one. Everything here is MIT and readable:{" "}
            <a
              className={styles.inlineLink}
              href={`https://github.com/${REPO}`}
              rel="noreferrer noopener"
            >
              read the source
            </a>{" "}
            before you add it, the same as you would for anything else you install.
          </p>
        </section>
      </div>
    </article>
  );
}

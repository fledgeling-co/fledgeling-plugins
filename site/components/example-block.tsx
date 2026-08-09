import type { Example } from "@/content/examples";
import styles from "./example-block.module.css";

/**
 * Example prompts and an illustrative output.
 *
 * The prompts are extracted from the skill's own SKILL.md — they are the phrases
 * the author wrote to make it fire. The output is not: it is a written sketch of
 * what the skill documents itself as producing, and it says so, once, where it
 * cannot be missed. Presenting a written sketch as a captured run on a page that
 * reads as authoritative is the failure this marker exists to prevent.
 */
export function ExampleBlock({
  prompts,
  example,
}: {
  prompts: string[];
  example: Example | undefined;
}) {
  if (prompts.length === 0 && !example) return null;

  return (
    <section className={styles.section}>
      {prompts.length > 0 ? (
        <div className={styles.prompts}>
          <h2 className={styles.label}>Say any of this</h2>
          <ul className={styles.promptList}>
            {prompts.map((prompt) => (
              <li key={prompt} className={styles.prompt}>
                {prompt}
              </li>
            ))}
          </ul>
          <p className={styles.promptNote}>
            Taken from the skill&rsquo;s own trigger description — these are the phrases it listens
            for. You do not have to match them exactly.
          </p>
        </div>
      ) : null}

      {example ? (
        <figure className={styles.example}>
          <figcaption className={styles.exampleHead}>
            <span className={styles.label}>What comes back</span>
            <span className={styles.illustrative}>
              Illustrative — written from the skill&rsquo;s documentation, not captured from a run
            </span>
          </figcaption>
          <p className={styles.examplePrompt}>
            <span className={styles.exampleCaret} aria-hidden="true">
              ›
            </span>
            {example.prompt}
          </p>
          <pre className={styles.exampleOutput}>{example.output}</pre>
        </figure>
      ) : null}
    </section>
  );
}

import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { CopyCommand } from "@/components/copy-command";
import { ExampleBlock } from "@/components/example-block";
import { EXAMPLES } from "@/content/examples";
import { MARKETPLACE, getSkill, getSkills } from "@/lib/skills";
import styles from "./page.module.css";
import { DeferPill } from "@/components/skill-card";

export function generateStaticParams() {
  return getSkills().map((skill) => ({ slug: skill.name }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const skill = getSkill(slug);
  if (!skill) return {};

  return {
    title: skill.name,
    description: firstSentences(skill.blurb, 2),
    openGraph: {
      title: `${skill.name} — Fledgeling Skills`,
      description: firstSentences(skill.blurb, 2),
      images: [{ url: skill.icon, width: 256, height: 256 }],
    },
  };
}

export default async function SkillPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const skill = getSkill(slug);
  if (!skill) notFound();

  const neighbours = skill.neighbours
    .map((name) => getSkill(name))
    .filter((entry): entry is NonNullable<typeof entry> => Boolean(entry));

  const lead = triggerLead(skill.trigger);

  return (
    <article className={styles.page}>
      <div className="container">
        <Link href="/" className={styles.back}>
          ← All skills
        </Link>

        <header className={styles.head}>
          <Image
            className={styles.icon}
            src={skill.icon}
            alt=""
            width={84}
            height={84}
            sizes="84px"
            priority
          />
          <div>
            <h1 className={styles.name}>{skill.name}</h1>
            <p className={styles.meta}>
              <span>v{skill.version}</span>
              <span className={styles.dot} aria-hidden="true" />
              <span>{skill.license}</span>
              <span className={styles.dot} aria-hidden="true" />
              <span>{skill.groupLabel}</span>
            </p>
          </div>
        </header>

        <p className={styles.blurb}>{skill.blurb}</p>

        <div className={styles.install}>
          <CopyCommand label="Install" command={skill.install} />
          <p className={styles.installNote}>
            Needs the marketplace added first —{" "}
            <Link className={styles.inlineLink} href="/install">
              how to do that
            </Link>
            .
          </p>
        </div>

        <div className={styles.facts}>
          <section className={styles.fact}>
            <h2 className={styles.factLabel}>Reach for it when</h2>
            <p className={styles.factBody}>{lead}</p>
          </section>

          {skill.boundary ? (
            <section className={styles.fact}>
              <h2 className={styles.factLabel}>Not for</h2>
              <p className={styles.factBody}>{skill.boundary.text}</p>
              {skill.boundary.referrals.length > 0 ? (
                <ul className={styles.referrals}>
                  {skill.boundary.referrals.map((referral) =>
                    referral.here ? (
                      <li key={referral.name}>
                        <Link className={styles.referralHere} href={`/skills/${referral.name}`}>
                          {referral.name}
                        </Link>
                        <span className={styles.referralNote}>in this marketplace</span>
                      </li>
                    ) : (
                      <li key={referral.name}>
                        <span className={styles.referralAway}>{referral.name}</span>
                        <span className={styles.referralNote}>
                          not in this marketplace — you cannot install it from here
                        </span>
                      </li>
                    ),
                  )}
                </ul>
              ) : null}
            </section>
          ) : null}

          {skill.signals.defer ? (
            <section className={styles.fact}>
              <h2 className={styles.factLabel}>Uses multiple models</h2>
              <DeferPill />
            </section>
          ) : null}

          <section className={styles.fact}>
            <h2 className={styles.factLabel}>What ships with it</h2>
            <ul className={styles.shipList}>
              <li>{skill.signals.scripts ? "Scripts it runs itself" : "No scripts — prose only"}</li>
              <li>
                {skill.signals.references > 0
                  ? `${skill.signals.references} reference file${skill.signals.references === 1 ? "" : "s"}`
                  : "No reference files"}
              </li>
              <li>
                {skill.signals.evals && skill.signals.evalsUrl ? (
                  <a className={styles.inlineLink} href={skill.signals.evalsUrl} rel="noreferrer noopener">
                    Measured evals
                  </a>
                ) : (
                  "No published evals"
                )}
              </li>
            </ul>
          </section>
        </div>

        <ExampleBlock prompts={skill.examplePrompts} example={EXAMPLES[skill.name]} />

        {neighbours.length > 0 ? (
          <section className={styles.neighbours}>
            <h2 className={styles.neighboursLabel}>Easily confused with</h2>
            <div className={styles.neighboursList}>
              {neighbours.map((neighbour) => (
                <Link key={neighbour.name} href={`/skills/${neighbour.name}`} className={styles.neighbour}>
                  <Image src={neighbour.icon} alt="" width={32} height={32} sizes="32px" />
                  <span className={styles.neighbourName}>{neighbour.name}</span>
                  <span className={styles.neighbourBlurb}>{firstSentences(neighbour.blurb, 1)}</span>
                </Link>
              ))}
            </div>
          </section>
        ) : null}

        <div className={styles.prose}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{skill.readme}</ReactMarkdown>
        </div>

        <footer className={styles.foot}>
          <a className={styles.footLink} href={skill.repoUrl} rel="noreferrer noopener">
            Source on GitHub
          </a>
          <span className={styles.dot} aria-hidden="true" />
          <span className={styles.footMeta}>
            {skill.name}@{MARKETPLACE} · v{skill.version}
          </span>
        </footer>
      </div>
    </article>
  );
}

/**
 * The human-readable lead of a trigger description.
 *
 * Trigger text is written for the model, not for a reader: a sentence or two of
 * plain description followed by a long run of quoted invocations. Those quoted
 * phrases are rendered properly further down the page as example prompts, so the
 * lead stops at the first one and keeps only whole sentences — a raw cut leaves
 * a dangling "or whenever someone says".
 *
 * Sentence boundaries need a following capital, or `~/Dev/CLAUDE.md` and
 * `audit.html` split mid-filename.
 */
function triggerLead(trigger: string): string {
  const firstQuote = trigger.search(/["“‘]/);
  const head = firstQuote > 60 ? trigger.slice(0, firstQuote) : trigger;

  const sentences = head.split(/(?<=\.)\s+(?=[A-Z])/).filter((part) => part.trim().endsWith("."));

  let lead = "";
  for (const sentence of sentences) {
    if (lead && (lead + sentence).length > 300) break;
    lead += (lead ? " " : "") + sentence.trim();
  }

  if (lead.length >= 40) return lead;

  const whole = trigger.split(/(?<=\.)\s+(?=[A-Z])/);
  return (whole[0] ?? trigger).trim();
}

function firstSentences(text: string, count: number): string {
  const parts = text.split(/(?<=\.)\s+(?=[A-Z])/);
  return parts.slice(0, count).join(" ");
}

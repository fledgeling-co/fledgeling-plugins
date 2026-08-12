import Link from "next/link";
import { REPO_URL, getSkillCount } from "@/lib/skills";
import { FooterSubscribe } from "./subscribe";
import { SubscribeBar } from "./subscribe-bar";
import styles from "./chrome.module.css";

export function SiteNav() {
  return (
    <header className={styles.header}>
      <nav className={`container ${styles.nav}`} aria-label="Primary">
        <Link href="/" className={styles.brand}>
          <span className={styles.brandName}>Fledgeling</span>
          <span className={styles.brandSep} aria-hidden="true">
            /
          </span>
          <span className={styles.brandSection}>Skills</span>
        </Link>
        <div className={styles.links}>
          <Link href="/install" className={styles.link}>
            Install
          </Link>
          <a className={styles.link} href={REPO_URL} rel="noreferrer noopener">
            GitHub
          </a>
          <a className={styles.cta} href="https://www.fledgeling.app" rel="noreferrer noopener">
            fledgeling.app
          </a>
        </div>
      </nav>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className={styles.footer}>
      <FooterSubscribe className={`container ${styles.footerSubscribe}`} />
      <div className={`container ${styles.footerInner}`}>
        <p>
          {getSkillCount()} skills · MIT · built and used daily by{" "}
          <a className={styles.footerLink} href="https://github.com/lprhodes" rel="noreferrer noopener">
            Luke Rhodes
          </a>
        </p>
        <p className={styles.footerMeta}>
          This page is generated from{" "}
          <a className={styles.footerLink} href={`${REPO_URL}/blob/main/.claude-plugin/marketplace.json`} rel="noreferrer noopener">
            marketplace.json
          </a>{" "}
          at build time, so it cannot disagree with what you install.
        </p>
      </div>
      <SubscribeBar />
    </footer>
  );
}

import type { Metadata, Viewport } from "next";
import { fontVariables } from "@/lib/fonts";
import { SiteNav, SiteFooter } from "@/components/chrome";
import { getSkillCount } from "@/lib/skills";
import "./globals.css";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://skills.fledgeling.app";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `Fledgeling Skills — ${getSkillCount()} Claude Code skills, searchable`,
    template: "%s — Fledgeling Skills",
  },
  description:
    `Search ${getSkillCount()} Claude Code skills by the problem you have rather than the name you don't know. ` +
    "Install instructions, what each one refuses to do, and the evidence behind it.",
  openGraph: {
    type: "website",
    siteName: "Fledgeling Skills",
    url: SITE_URL,
  },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#F5F3EF" },
    { media: "(prefers-color-scheme: dark)", color: "#F5F3EF" },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={fontVariables}>
      <body>
        <a className="skipLink" href="#main">
          Skip to content
        </a>
        <SiteNav />
        <main id="main">{children}</main>
        <SiteFooter />
      </body>
    </html>
  );
}

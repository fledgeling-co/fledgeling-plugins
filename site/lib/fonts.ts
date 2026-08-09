import { Newsreader, Instrument_Sans, IBM_Plex_Mono } from "next/font/google";

/**
 * Self-hosted through next/font so no Google origin appears in the CSP. Matches
 * fledgeling-app/apps/website/lib/fonts.ts exactly — three families, no more.
 */

export const newsreader = Newsreader({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-newsreader",
  style: ["normal", "italic"],
});

export const instrumentSans = Instrument_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-instrument-sans",
});

export const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-ibm-plex-mono",
  weight: ["400", "500", "600"],
  style: ["normal", "italic"],
});

export const fontVariables = `${newsreader.variable} ${instrumentSans.variable} ${ibmPlexMono.variable}`;

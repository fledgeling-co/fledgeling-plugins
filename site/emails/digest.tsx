import {
  Body,
  Button,
  Column,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Img,
  Link,
  Preview,
  Row,
  Section,
  Text,
} from "@react-email/components";

/**
 * The new-skill digest.
 *
 * Same brand literals as emails/welcome.tsx, for the same reason: email clients
 * do not resolve CSS custom properties, so the tokens in styles/tokens.css are
 * copied here rather than referenced.
 *
 * Three constraints from the email surface shaped this more than taste did:
 *
 *   * It has to work with images off, which several clients still default to.
 *     So the skill icons carry `alt=""` and nothing load-bearing lives inside
 *     an image; every heading, every command and every link is real text.
 *   * `--color-accent` (#c4622d) is used nowhere. White on it measures 3.96:1
 *     and it measures 3.92:1 as text on the card, both under the 4.5 that AA
 *     asks for at these sizes. `accentDeep` is the same hue at 5.5:1 and is what
 *     the site's own buttons already use.
 *   * A digest is a list, so the serial-position rule applies: the newest skill
 *     leads, and when there is only one it supplies the h1 and the subject line
 *     rather than being announced by a generic one.
 *
 * The per-skill prose is written at publish time by the Claude CLI through
 * create-luke-content and stored on the item. Nothing here generates copy.
 */

const ink = "#24221e";
const muted = "#6b665d";
const paper = "#f5f3ef";
const surface = "#fbfaf8";
const accentDeep = "#a44e20";
const hairline = "#e0dbd2";
const codeBg = "#edeae3";

const serif = 'Newsreader, Georgia, "Times New Roman", serif';
const sans = '"Instrument Sans", -apple-system, "Segoe UI", Helvetica, Arial, sans-serif';
const mono = '"IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace';

export type DigestItemView = {
  skill: string;
  headline: string;
  body: string;
  install: string;
  url: string;
  iconUrl: string;
};

export type DigestEmailProps = {
  email: string;
  cadence: string;
  items: DigestItemView[];
  preferencesUrl: string;
  unsubscribeUrl: string;
  siteUrl: string;
};

const NUMBER_WORDS = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"];

/** Words up to nine, digits after. Editorial convention, and "Three new skills"
 *  sets better in a serif display than "3 new skills". */
function countWord(n: number): string {
  return NUMBER_WORDS[n] ?? String(n);
}

export function digestHeading(items: DigestItemView[]): string {
  if (items.length === 1) return items[0]?.headline || "A new skill landed";
  return `${countWord(items.length)} new skills`;
}

/**
 * Optical sizing, because the h1 is written copy rather than a fixed string.
 *
 * A one-skill digest promotes that skill's own headline to the h1, and a good
 * headline is sometimes long. Capping the writer to fit a font size is the
 * wrong way round, so the size gives instead: three lines at 24px reads as a
 * headline, three lines at 28px reads as a wall.
 */
function headingSize(text: string): number {
  if (text.length > 78) return 22;
  if (text.length > 52) return 25;
  return 28;
}

/** The icon and name for one skill. Above the h1 when there is only one, and
 *  inside each block when there are several. */
function SkillLine({ item }: { item: DigestItemView }) {
  return (
    <Row style={{ marginBottom: 10 }}>
      <Column style={{ width: 36, verticalAlign: "middle" }}>
        <Img
          src={item.iconUrl}
          width="28"
          height="28"
          /* Decorative: the skill's name is right beside it as text, so an
             images-off reader loses nothing. */
          alt=""
          style={{ borderRadius: 6, display: "block" }}
        />
      </Column>
      <Column style={{ verticalAlign: "middle" }}>
        <Text
          style={{
            margin: 0,
            fontFamily: mono,
            fontSize: 14,
            letterSpacing: "0.02em",
            color: ink,
            fontWeight: 600,
          }}
        >
          {item.skill}
        </Text>
      </Column>
    </Row>
  );
}

export function DigestEmail({
  email,
  cadence,
  items,
  preferencesUrl,
  unsubscribeUrl,
  siteUrl,
}: DigestEmailProps) {
  const single = items.length === 1;
  const lede = single
    ? "What it does, and the line to install it."
    : "What each one does, and the line to install it.";
  const heading = digestHeading(items);

  return (
    <Html lang="en">
      <Head>
        {/* Clients invert unpredictably; declaring both stops the worst of it. */}
        <meta name="color-scheme" content="light dark" />
        <meta name="supported-color-schemes" content="light dark" />
      </Head>
      {/* Continues the subject rather than repeating it. */}
      <Preview>{lede}</Preview>
      <Body style={{ backgroundColor: paper, margin: 0, padding: "32px 12px", fontFamily: sans }}>
        <Container
          style={{
            backgroundColor: surface,
            border: `1px solid ${hairline}`,
            borderRadius: 12,
            margin: "0 auto",
            maxWidth: 560,
            padding: "36px 32px 28px",
          }}
        >
          <Text
            style={{
              margin: "0 0 20px",
              fontFamily: mono,
              fontSize: 11,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
              color: muted,
            }}
          >
            Fledgeling · Skills
          </Text>

          {/* Named before it is pitched. With one skill the h1 is that skill's
              own headline, so without this the thing being announced would be
              the smallest text on the page and would arrive after the claim
              made about it. */}
          {single && items[0] ? <SkillLine item={items[0]} /> : null}

          <Heading
            as="h1"
            style={{
              margin: "0 0 10px",
              fontFamily: serif,
              fontSize: headingSize(heading),
              lineHeight: 1.22,
              color: ink,
              fontWeight: 600,
            }}
          >
            {heading}
          </Heading>

          <Text style={{ margin: "0 0 28px", fontSize: 15, lineHeight: 1.6, color: muted }}>
            {lede}
          </Text>

          {items.map((item, index) => (
            <Section key={item.skill}>
              {index > 0 ? (
                <Hr style={{ border: "none", borderTop: `1px solid ${hairline}`, margin: "0 0 26px" }} />
              ) : null}

              {/* Already stated above the h1 in the single case. */}
              {!single ? <SkillLine item={item} /> : null}

              {/* Skipped when there is one item, because the h1 above already
                  carries this exact line. Saying it twice is the multi-slot
                  filler pattern, not hierarchy. */}
              {!single ? (
                <Heading
                  as="h2"
                  style={{
                    margin: "0 0 10px",
                    fontFamily: serif,
                    fontSize: 20,
                    lineHeight: 1.3,
                    color: ink,
                    fontWeight: 600,
                  }}
                >
                  {item.headline}
                </Heading>
              ) : null}

              <Text style={{ margin: "0 0 18px", fontSize: 16, lineHeight: 1.6, color: ink }}>
                {item.body}
              </Text>

              <Text style={{ margin: "0 0 6px", fontSize: 14, lineHeight: 1.6, color: muted }}>
                One line, if you want it:
              </Text>
              <Text
                style={{
                  margin: "0 0 20px",
                  padding: "12px 14px",
                  backgroundColor: codeBg,
                  borderRadius: 8,
                  fontFamily: mono,
                  /* 13px keeps the longest install line (53 characters) inside
                     the 496px content column without wrapping. */
                  fontSize: 13,
                  lineHeight: 1.5,
                  color: ink,
                  wordBreak: "break-word",
                }}
              >
                {item.install}
              </Text>

              <Button
                href={item.url}
                style={{
                  display: "inline-block",
                  backgroundColor: accentDeep,
                  color: "#fdfbf8",
                  fontSize: 15,
                  fontWeight: 600,
                  lineHeight: "16px",
                  /* 14 + 16 + 14 = 44px tall, the touch-target floor. */
                  padding: "14px 20px",
                  borderRadius: 8,
                  textDecoration: "none",
                }}
              >
                See what {item.skill} does
              </Button>

              <Section style={{ height: 28 }} />
            </Section>
          ))}

          <Hr style={{ border: "none", borderTop: `1px solid ${hairline}`, margin: "0 0 20px" }} />

          <Text style={{ margin: 0, fontSize: 13, lineHeight: 1.7, color: muted }}>
            Sent to {email}. You&rsquo;re on {cadence}.
          </Text>
          <Text style={{ margin: "4px 0 0", fontSize: 13, lineHeight: 1.7, color: muted }}>
            <Link href={preferencesUrl} style={{ color: accentDeep, textDecoration: "underline" }}>
              Change how often you hear
            </Link>
            {"  ·  "}
            {/* Plain, findable, and its own link. A hidden unsubscribe buys a
                spam complaint, which costs more than the address does. */}
            <Link href={unsubscribeUrl} style={{ color: accentDeep, textDecoration: "underline" }}>
              Unsubscribe
            </Link>
          </Text>
          <Text style={{ margin: "12px 0 0", fontSize: 13, lineHeight: 1.7, color: muted }}>
            <Link href={siteUrl} style={{ color: muted, textDecoration: "underline" }}>
              skills.fledgeling.app
            </Link>
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

/**
 * The text/plain alternative.
 *
 * Written rather than stripped out of the HTML: some clients, some readers and
 * some spam filters want a real one, and an auto-generated part full of collapsed
 * markup reads worse than no part at all. Full URLs, because a text part has
 * nowhere to hide a link.
 */
export function digestText({
  email,
  cadence,
  items,
  preferencesUrl,
  unsubscribeUrl,
  siteUrl,
}: DigestEmailProps): string {
  const single = items.length === 1;
  const lede = single
    ? "What it does, and the line to install it."
    : "What each one does, and the line to install it.";

  const blocks = items.map((item) =>
    [
      // Named above the heading in the single case, exactly as the HTML does,
      // so the two parts of the same email do not disagree about what leads.
      single ? null : item.skill,
      single ? null : item.headline,
      single ? null : "",
      item.body,
      "",
      "One line, if you want it:",
      `  ${item.install}`,
      "",
      `See what ${item.skill} does: ${item.url}`,
    ]
      .filter((line) => line !== null)
      .join("\n"),
  );

  return [
    "FLEDGELING · SKILLS",
    "",
    ...(single && items[0] ? [items[0].skill, ""] : []),
    digestHeading(items),
    lede,
    "",
    "---",
    "",
    blocks.join("\n\n---\n\n"),
    "",
    "---",
    "",
    `Sent to ${email}. You're on ${cadence}.`,
    `Change how often you hear: ${preferencesUrl}`,
    `Unsubscribe: ${unsubscribeUrl}`,
    "",
    siteUrl,
    "",
  ].join("\n");
}

export default DigestEmail;

import {
  Body,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Link,
  Preview,
  Section,
  Text,
} from "@react-email/components";

/**
 * The welcome email.
 *
 * Fledgeling's brand values, inlined as literals. Email clients do not resolve
 * CSS custom properties, so the tokens in styles/tokens.css cannot be
 * referenced here; they are copied, and the comment is the link back.
 *
 * Newsreader and Instrument Sans are not web-safe, so each stack falls through
 * to a serif and a system sans that hold the same register. A webfont would
 * load in roughly two clients and be ignored by the rest.
 */

const ink = "#24221e";
const muted = "#6b665d";
const paper = "#f5f3ef";
const surface = "#fbfaf8";
const accent = "#c4622d";
const hairline = "#e0dbd2";

const serif = 'Newsreader, Georgia, "Times New Roman", serif';
const sans = '"Instrument Sans", -apple-system, "Segoe UI", Helvetica, Arial, sans-serif';
const mono = '"IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace';

export type WelcomeEmailProps = {
  email: string;
  cadence: string;
  preferencesUrl: string;
  siteUrl: string;
};

export function WelcomeEmail({ email, cadence, preferencesUrl, siteUrl }: WelcomeEmailProps) {
  return (
    <Html lang="en">
      <Head />
      <Preview>An email when a skill lands or changes. You&rsquo;re on {cadence}; daily is one click away.</Preview>
      <Body style={{ backgroundColor: paper, margin: 0, padding: "32px 12px", fontFamily: sans }}>
        <Container
          style={{
            backgroundColor: surface,
            border: `1px solid ${hairline}`,
            borderRadius: 12,
            margin: "0 auto",
            maxWidth: 520,
            padding: "36px 36px 28px",
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

          <Heading
            as="h1"
            style={{ margin: "0 0 16px", fontFamily: serif, fontSize: 28, lineHeight: 1.2, color: ink, fontWeight: 600 }}
          >
            That&rsquo;s you subscribed.
          </Heading>

          <Text style={{ margin: "0 0 16px", fontSize: 16, lineHeight: 1.6, color: ink }}>
            Thanks for signing up. You&rsquo;ll get an email when a skill is new or has changed, and
            nothing else; there&rsquo;s no newsletter attached to this.
          </Text>

          <Text style={{ margin: "0 0 24px", fontSize: 16, lineHeight: 1.6, color: ink }}>
            You&rsquo;re on <strong style={{ color: ink }}>{cadence}</strong> at the moment, so
            that&rsquo;s{" "}
            {cadence === "daily"
              ? "an email on any day something lands, and quiet days stay quiet"
              : "everything from the past seven days in one go"}
            .{" "}
            <Link href={preferencesUrl} style={{ color: accent, textDecoration: "underline" }}>
              {cadence === "daily" ? "Switch to weekly" : "Switch to daily"}
            </Link>{" "}
            if that suits you better.
          </Text>

          <Section>
            <Text style={{ margin: "0 0 8px", fontSize: 15, lineHeight: 1.6, color: ink }}>
              If you haven&rsquo;t added the marketplace yet, it&rsquo;s one line:
            </Text>
            <Text
              style={{
                margin: "0 0 24px",
                padding: "12px 14px",
                backgroundColor: "#edeae3",
                borderRadius: 8,
                fontFamily: mono,
                fontSize: 13,
                lineHeight: 1.5,
                color: ink,
                wordBreak: "break-all",
              }}
            >
              /plugin marketplace add fledgeling-co/fledgeling-plugins
            </Text>
          </Section>

          <Hr style={{ border: "none", borderTop: `1px solid ${hairline}`, margin: "4px 0 20px" }} />

          <Text style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: muted }}>
            Sent to {email}.{" "}
            <Link href={preferencesUrl} style={{ color: muted, textDecoration: "underline" }}>
              Change how often you hear, or leave the list entirely
            </Link>
            .
          </Text>
          <Text style={{ margin: "8px 0 0", fontSize: 13, lineHeight: 1.6, color: muted }}>
            <Link href={siteUrl} style={{ color: muted, textDecoration: "underline" }}>
              skills.fledgeling.app
            </Link>
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

export default WelcomeEmail;

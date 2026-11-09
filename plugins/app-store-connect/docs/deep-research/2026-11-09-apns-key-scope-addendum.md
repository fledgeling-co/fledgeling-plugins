# Addendum to 2026-11-09-apns-key-automation (read after it)

Written after `research_verify_citations` on the run above returned one dead citation, so the
claim that rested on it could be re-sourced from Apple rather than left thinner than it looks.

**Dead citation.** `https://github.com/pagis-co/pagis/pull/179` answered 404 on 2026-11-09. It
came from a search-result summary and was never opened, so treat it as unconfirmed. The report's
claim that "topic-specific keys come in pairs, one per environment" is re-sourced below.

**Primary source.** Apple's "Establishing a token-based connection to APNs", read on 2026-11-09
through its JSON rendering
(`https://developer.apple.com/tutorials/data/documentation/usernotifications/establishing-a-token-based-connection-to-apns.json`,
because the HTML page renders client-side). Verbatim:

- "Use team-scoped keys to generate authentication tokens for sending notifications to any topic in a team."
- "These keys restrict usage to either Sandbox or Production, enhancing security."
- "Each environment can have a maximum of two keys."
- "If you have existing team-scoped keys that work in both the Sandbox and Production environments it will continue to be supported."
- "However, it's recommended to use different, environment-specific keys to create distinct workflows and to safely manage your development process."
- "Use topic-specific keys to generate authentication tokens for sending notifications to specific team topics within a single environment."
- "You can create a maximum of 200 keys for Sandbox and 200 for Production, with up to 400 topics per topic-based key."

**What changes.** A topic-specific key covers one environment, so the "pairs" claim holds, now on
Apple's text. Team-scoped keys are capped at two per environment, which makes "check for an
existing key before creating one" a hard limit rather than tidiness.

**Held loosely.** Apple's page describes new team-scoped keys as restricted to one environment
and recommends environment-specific keys, while OneSignal's current setup guide (source 7 in the
run) tells users to pick "Sandbox & Production" with "Team Scoped (All Topics)" and rejects
single-environment keys. Both can be true if the portal still offers a both-environments
team-scoped key; this was not confirmed in the portal itself.

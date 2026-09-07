/** Extract referral owners for catalogue links; this does not prove skill availability. */
const token = "[a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)?";
// Keep a slash inside backticks, and reject partial matches of paths or invented
// three-part namespaces. A sentence-ending period is allowed; a file extension is not.
const identifier = "(?<quoted>`?)(?<slash>/?)(?<name>" + token + ")(?![a-z0-9_:/-]|\\.[a-z0-9])`?";
const referral = new RegExp("\\buse\\s+(?:(?:the|either|both)\\s+)?" + identifier, "gi");
const continuation = new RegExp("^(?:\\s*,\\s*(?:(?:and|or)\\s+)?|\\s+(?:and|or|\\+)\\s+)" + identifier, "i");
const inventedOwners = new Set(["plugin", "fledgeling-plugins", "diolog-plugins"]);

export function referralPlugins(text, knownPlugins = new Set()) {
  const owners = new Set();
  const add = (match) => {
    const { name, quoted, slash } = match.groups;
    const owner = name.split(":")[0];
    if (inventedOwners.has(owner)) return false;
    // Unformatted hyphenated English such as "state-of-the-art" is not a
    // dependency. Unknown external referrals need an explicit ID or code/slash form.
    if (knownPlugins.has(name) || name.includes(":") || ((quoted || slash) && name.includes("-"))) {
      owners.add(owner);
      return true;
    }
    return false;
  };
  for (const match of text.matchAll(referral)) {
    if (!add(match)) continue;
    let rest = text.slice(match.index + match[0].length);
    let next;
    while ((next = continuation.exec(rest)) && add(next)) {
      rest = rest.slice(next[0].length);
    }
  }
  return [...owners];
}

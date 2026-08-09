import type { SkillSummary } from "./skills";

/**
 * The local lane.
 *
 * Runs on every keystroke, in the browser, with no network. It never filters —
 * it scores, and the roster renders every skill in rank order regardless. A
 * query that matches nothing still shows all sixteen; that is the point of the
 * model, and it is why there is no empty state to design.
 */

export type Ranked = {
  skill: SkillSummary;
  score: number;
  /** Above the promotion line: rendered as a full card rather than a compact row. */
  matched: boolean;
};

const STOP_WORDS = new Set([
  "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "do", "for", "from", "get",
  "has", "have", "how", "i", "if", "in", "is", "it", "its", "me", "my", "of", "on", "or",
  "should", "so", "that", "the", "there", "this", "to", "up", "want", "was", "what", "when",
  "which", "with", "you", "your",
]);

/** Weights reflect how much a hit in each field says about intent. */
const FIELDS = [
  { key: "name", weight: 12 },
  { key: "keywords", weight: 6 },
  { key: "blurb", weight: 3 },
  { key: "trigger", weight: 2 },
  { key: "description", weight: 2 },
  { key: "group", weight: 2 },
] as const;

function tokenise(input: string): string[] {
  return input
    .toLowerCase()
    .split(/[^a-z0-9+#-]+/)
    .filter((token) => token.length > 1 && !STOP_WORDS.has(token));
}

function haystack(skill: SkillSummary, field: (typeof FIELDS)[number]["key"]): string {
  switch (field) {
    case "keywords":
      return skill.keywords.join(" ");
    default:
      return skill[field];
  }
}

/**
 * Score one skill against the query tokens. A term hit in a field scores that
 * field's weight, doubled when it lands on a word boundary — so "report" scores
 * higher on `report` than on `dossier-report`'s prose, and "icon" does not have
 * to compete with every mention of the word inside a README-length blurb.
 */
function scoreSkill(skill: SkillSummary, tokens: string[]): number {
  let score = 0;

  for (const field of FIELDS) {
    const text = haystack(skill, field.key).toLowerCase();
    if (!text) continue;

    for (const token of tokens) {
      const at = text.indexOf(token);
      if (at === -1) continue;

      const before = at === 0 ? " " : text[at - 1]!;
      const boundary = /[^a-z0-9]/.test(before);
      score += field.weight * (boundary ? 2 : 1);

      // An exact name match is decisive: someone told this visitor to install
      // `trawl` and they typed it. Nothing should outrank that.
      if (field.key === "name" && text === token) score += 100;
    }
  }

  return score;
}

export function rankLocally(skills: SkillSummary[], query: string): Ranked[] {
  const tokens = tokenise(query);

  if (tokens.length === 0) {
    return skills.map((skill) => ({ skill, score: 0, matched: true }));
  }

  const scored = skills.map((skill) => ({ skill, score: scoreSkill(skill, tokens) }));
  const best = Math.max(...scored.map((entry) => entry.score));

  return scored
    .map((entry) => ({
      ...entry,
      // Promote anything scoring at least a third of the leader. A hard "score > 0"
      // line lets one incidental word in an 800-character blurb promote a skill
      // that has nothing to do with the query.
      matched: entry.score > 0 && entry.score >= best / 3,
    }))
    .sort((a, b) => b.score - a.score || a.skill.name.localeCompare(b.skill.name));
}

/** Reorder a ranked list to match slugs the AI lane returned, in its order. */
export function applyAiOrder(
  skills: SkillSummary[],
  order: string[],
  reasons: Map<string, string>,
): Ranked[] {
  const position = new Map(order.map((name, index) => [name, index]));

  return [...skills]
    .sort((a, b) => {
      const aAt = position.get(a.name) ?? Number.MAX_SAFE_INTEGER;
      const bAt = position.get(b.name) ?? Number.MAX_SAFE_INTEGER;
      return aAt - bAt || a.name.localeCompare(b.name);
    })
    .map((skill) => ({
      skill,
      score: position.has(skill.name) ? order.length - position.get(skill.name)! : 0,
      matched: reasons.has(skill.name),
    }));
}

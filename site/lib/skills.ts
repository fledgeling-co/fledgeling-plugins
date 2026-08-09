import catalogue from "./catalogue.json";

/**
 * Typed access to the catalogue that `scripts/build-catalogue.mjs` generates from
 * the repository at build time. Nothing here touches the filesystem, so the same
 * data is available to static pages and to the search route without either of
 * them depending on `../plugins` existing at runtime.
 */

export type SkillSignals = {
  evals: boolean;
  evalsUrl: string | null;
  scripts: boolean;
  references: number;
};

/** A referral named inside a boundary clause. `here` is false when the named
 * skill lives in a different marketplace and cannot be installed from this site. */
export type Referral = {
  name: string;
  here: boolean;
};

export type Boundary = {
  text: string;
  referrals: Referral[];
};


export type Skill = {
  name: string;
  version: string;
  group: string;
  /** Capability prose from marketplace.json — what the skill does. */
  description: string;
  /** Trigger prose from SKILL.md — when to reach for it, and when not to. */
  trigger: string;
  /** The root README's paragraph. The best short copy in the repo. */
  blurb: string;
  /** The plugin README with its banner, title and badge chrome removed. */
  readme: string;
  license: string;
  keywords: string[];
  allowedTools: string | null;
  /** The trigger's own "NOT for X (use Y)" clause, on 10 of the 16. */
  boundary: Boundary | null;
  /** Skills named in a boundary clause on either side — the confusable pairs. */
  neighbours: string[];
  /** The author's own quoted trigger phrases, extracted from SKILL.md. */
  examplePrompts: string[];
  icon: string;
  install: string;
  repoUrl: string;
  signals: SkillSignals;
};

export type Group = {
  id: string;
  label: string;
  blurb: string;
  count: number;
};

export type Catalogue = {
  marketplace: string;
  repo: string;
  generatedFrom: string;
  groups: Group[];
  skills: Skill[];
};

const data = catalogue as Catalogue;

export const MARKETPLACE = data.marketplace;
export const REPO = data.repo;
export const REPO_URL = `https://github.com/${data.repo}`;

export function getSkills(): Skill[] {
  return data.skills;
}

export function getGroups(): Group[] {
  return data.groups;
}

export function getSkill(name: string): Skill | undefined {
  return data.skills.find((skill) => skill.name === name);
}

export function getSkillCount(): number {
  return data.skills.length;
}

/**
 * The shape the client bundle gets: everything the cards and local search need,
 * without the full README bodies. Sixteen READMEs is roughly 120 KB of prose that
 * only the detail pages ever render.
 */
export type SkillSummary = Omit<Skill, "readme">;

export function getSkillSummaries(): SkillSummary[] {
  return data.skills.map(({ readme: _readme, ...rest }) => rest);
}

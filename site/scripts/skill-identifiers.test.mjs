import assert from "node:assert/strict";
import test from "node:test";
import { referralPlugins } from "./skill-identifiers.mjs";

test("qualified multi-skill referrals link to the owning plugin page", () => {
  assert.deepEqual(referralPlugins("Not for delivery (use `shipyard:work` or use /shipyard:triage)."), ["shipyard"]);
});

test("ordinary prose is not advertised as an external dependency", () => {
  assert.deepEqual(referralPlugins("Not for authored copy (use that person's voice; use the content skill)."), []);
});

test("preserves known single-word plugins and external hyphenated referrals", () => {
  assert.deepEqual(referralPlugins("Not for browsing (use proctor); use email-mockups:email-mockups.", new Set(["proctor"])), ["proctor", "email-mockups"]);
});

test("slash commands inside backticks retain the owning plugin", () => {
  assert.deepEqual(referralPlugins("Use `/shipyard:work` or `/shipyard:triage`."), ["shipyard"]);
});

test("paths, partial namespaces and hyphenated English are not referrals", () => {
  assert.deepEqual(referralPlugins("use /shipyard/skills/work/SKILL.md; use state-of-the-art tooling; use `shipyard.md`", new Set(["shipyard"])), []);
  assert.deepEqual(referralPlugins("use plugin:agent-voice:agent-voice; use fledgeling-plugins:ship-feature"), []);
});

test("coordinated alternative skills all contribute their owners", () => {
  assert.deepEqual(referralPlugins("Use `shipyard:work`, `test-campaign:test-campaign`, or `email-mockups:email-mockups`."), ["shipyard", "test-campaign", "email-mockups"]);
  assert.deepEqual(referralPlugins("Use proctor and defer.", new Set(["proctor", "defer"])), ["proctor", "defer"]);
});

test("repeated calls have no regex state leakage and never alter executable text", () => {
  const text = "use `shipyard:triage`";
  assert.deepEqual(referralPlugins(text), ["shipyard"]);
  assert.deepEqual(referralPlugins(text), ["shipyard"]);
  assert.equal(text, "use `shipyard:triage`");
});

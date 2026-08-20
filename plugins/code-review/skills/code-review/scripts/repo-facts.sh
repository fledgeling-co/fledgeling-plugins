#!/usr/bin/env bash
# repo-facts.sh — derive the repo profile the review needs, from the repo itself.
#
# Prints a draft profile: instruction files, workspace layout, package manager, gate commands,
# frameworks present at their installed versions, test layout and CI config. Read the output,
# then fill the judgement half (global controls, cross-package boundaries) yourself — those need
# greps that depend on what the diff touched. See references/repo-discovery.md.
#
#   ./repo-facts.sh              # profile the repository root
#   ./repo-facts.sh <dir>        # profile a subdirectory as the root
#
# Uses jq where available and falls back to grep, so it runs on a machine without jq.

set -uo pipefail
ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$ROOT" || { echo "repo-facts.sh: cannot enter $ROOT" >&2; exit 2; }
HAVE_JQ=0; command -v jq >/dev/null 2>&1 && HAVE_JQ=1
# Directories whose package.json describes a copy of the repo, not the repo.
PRUNE="-not -path */node_modules/* -not -path */.next/* -not -path */dist/* -not -path */build/* -not -path */.worktrees/* -not -path */vendor/* -not -path */.venv/*"

sec() { printf '\n## %s\n' "$1"; }
have() { [ -e "$1" ] && echo "  $1"; }

echo "# Repo profile — $(basename "$ROOT") — derived $(date +%Y-%m-%d)"
echo "# Source of truth is the repo. Where a doc disagrees with this output, the repo wins."

sec "Instruction files (angle N reads these; a convention finding quotes them)"
found=0
for f in CLAUDE.md AGENTS.md .cursorrules .cursor/rules CONTRIBUTING.md CODING_PRACTICES.md .github/copilot-instructions.md; do
  [ -e "$f" ] && { echo "  $f"; found=1; }
done
# Per-package instruction files govern files at or below their directory.
git ls-files '*/CLAUDE.md' '*/AGENTS.md' 2>/dev/null | head -20 | sed 's/^/  /' && found=1
[ "$found" -eq 0 ] && echo "  none — angle N is not-applicable, and the ledger says so"

sec "Workspace layout"
for f in pnpm-workspace.yaml turbo.json nx.json lerna.json rush.json go.work Cargo.toml pyproject.toml deno.json; do have "$f"; done
if [ -f package.json ]; then
  if [ "$HAVE_JQ" -eq 1 ]; then
    jq -r 'if .workspaces then "  package.json#workspaces: \(.workspaces | tostring)" else empty end' package.json
  else
    grep -A4 '"workspaces"' package.json 2>/dev/null | sed 's/^/  /'
  fi
fi
[ -f pnpm-workspace.yaml ] && grep -vE '^\s*(#|$)' pnpm-workspace.yaml | head -12 | sed 's/^/  /'

sec "Package manager (the lockfile decides — every command you print must be the one that works here)"
for f in pnpm-lock.yaml package-lock.json yarn.lock bun.lockb uv.lock poetry.lock Cargo.lock go.sum Gemfile.lock composer.lock; do have "$f"; done
[ -f package.json ] && [ "$HAVE_JQ" -eq 1 ] && jq -r 'if .packageManager then "  packageManager field: \(.packageManager)" else empty end' package.json

sec "Packages and their gate commands (invoke the script, never the tool you assume is behind it)"
# Depth 4 covers apps/*/package.json, packages/*/x/package.json and the usual monorepo shapes.
find . -maxdepth 4 -name package.json $PRUNE 2>/dev/null \
  | sort | head -40 | while read -r pkg; do
  echo "  $pkg"
  if [ "$HAVE_JQ" -eq 1 ]; then
    jq -r '.scripts // {} | to_entries
           | map(select(.key | test("^(lint|typecheck|type-check|tsc|test|test:.*|build|check|verify|e2e)$")))
           | .[] | "      \(.key): \(.value)"' "$pkg" 2>/dev/null
  else
    sed -n '/"scripts"/,/}/p' "$pkg" | grep -E '"(lint|typecheck|test|build|check)' | sed 's/^/      /'
  fi
done

sec "Frameworks present, at installed versions (checklist routing and Gate 2 turn on these)"
if [ "$HAVE_JQ" -eq 1 ]; then
  find . -maxdepth 4 -name package.json $PRUNE 2>/dev/null | while read -r pkg; do
    out=$(jq -r '((.dependencies // {}) + (.devDependencies // {})) | to_entries
      | map(select(.key | test("^(next|react|react-native|expo|@nestjs/core|@angular/core|vue|nuxt|svelte|@sveltejs/kit|remix|@remix-run/react|astro|solid-js|express|fastify|koa|hono|@prisma/client|prisma|mongoose|typeorm|drizzle-orm|sequelize|knex|@supabase/supabase-js|zod|valibot|yup|class-validator|@tanstack/react-query|swr|redux|zustand|jest|vitest|mocha|@playwright/test|cypress|typescript|@typescript/native-preview|eslint|oxlint|biome|@biomejs/biome|prettier|tailwindcss)$")))
      | .[] | "      \(.key)@\(.value)"' "$pkg" 2>/dev/null)
    [ -n "$out" ] && { echo "  $pkg"; echo "$out"; }
  done
else
  echo "  jq not installed — read each touched package.json directly"
fi
for f in requirements.txt pyproject.toml go.mod Cargo.toml Gemfile pom.xml build.gradle; do have "$f"; done

sec "Absences worth stating (a finding naming an absent framework is refuted at Gate 1)"
for probe in "@nestjs/core:NestJS" "prisma:Prisma" "mongoose:Mongoose" "typeorm:TypeORM" "drizzle-orm:Drizzle" "graphql:GraphQL" "next:Next.js" "react-native:React Native"; do
  key="${probe%%:*}"; label="${probe##*:}"
  if grep -rqs --include=package.json --exclude-dir=node_modules "\"$key\"" . 2>/dev/null; then
    echo "  present: $label"
  else
    echo "  ABSENT: $label"
  fi
done

sec "Test layout (a coverage claim rests on this file list, not an impression)"
for d in test tests __tests__ spec e2e cypress playwright; do [ -d "$d" ] && echo "  $d/"; done
git ls-files '*test*' '*spec*' 2>/dev/null | grep -vE 'node_modules|\.snap$' | head -12 | sed 's/^/  /'
echo "  (total test-named files: $(git ls-files '*test*' '*spec*' 2>/dev/null | grep -cvE 'node_modules|\.snap$' || echo 0))"

sec "CI (a gate can live here and nowhere else)"
ls -1 .github/workflows/*.y*ml 2>/dev/null | sed 's/^/  /'
for f in .gitlab-ci.yml Jenkinsfile .circleci/config.yml azure-pipelines.yml .husky/pre-push .husky/pre-commit vercel.json netlify.toml; do have "$f"; done

sec "Contract and architecture docs (angles X and M fire on what these name)"
git ls-files 'docs/*' 2>/dev/null | grep -iE 'contract|architecture|adr|api|schema|openapi' | head -12 | sed 's/^/  /'
git ls-files '*.proto' '*openapi*' '*swagger*' 'schema.graphql' 2>/dev/null | head -8 | sed 's/^/  /'

sec "Next"
cat <<'EOF'
  Fill these by grep, against the files the diff actually touched:
    - global controls: validation at the boundary, auth/session, the mutating-request preamble,
      data-layer constraints, locks and counters, response headers and CSP
    - cross-package boundaries: hand-mirrored types, wire DTOs, generated clients, a constant
      restated in several places, and whether a guard test pins each side
  Then write the 15-to-30-line profile and inline it into every shard and verifier prompt.
EOF

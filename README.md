# fledgeling-plugins

Claude Code plugins from [Fledgeling](https://github.com/fledgeling-co).

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
```

Then install what you want:

```
/plugin install design-review@fledgeling-plugins
```

## Plugins

### design-review

The last pass before a human looks at AI-built UI. Renders the surface at a viewport matrix, runs deterministic accessibility, contrast, target-size, performance and motion gates, then judges hierarchy, states, flows and design-system coherence — returning severity-ranked findings with pasteable fixes, the evidence behind each, and an explicit list of what was never checked.

Works with Playwright, Puppeteer, chrome-devtools-mcp, agent-browser or claude-in-chrome. With none of them it runs source-only and says so rather than implying a page was seen.

[Details](./plugins/design-review/README.md)

## Licence

MIT

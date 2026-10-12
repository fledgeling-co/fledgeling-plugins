# Follow through

<img src="assets/banner.png" alt="Follow through: evidence, next action, verified outcome" />

Open items tend to spread across mail, tracking pages, research tabs and conversations.
This plugin brings the selected set back to its sources, works out what still needs
doing, and keeps the next action attached to the evidence. Old screen activity can
point to the source; it cannot prove today's balance, delivery or completed promise.

Install from this repository's marketplace:

```text
/plugin install follow-through@fledgeling-plugins
```

| Invocation | Use it for |
|---|---|
| `/follow-through:follow-through Review these loose ends` | A bounded mixed review |
| `/follow-through:ops-triage Review selected project alerts and credits` | Operational errors, cost and credit deadlines |
| `/follow-through:household-follow-up Check these two shipments` | Deliveries, returns and household administration |
| `/follow-through:decision-brief Decide a storage approach from this research` | Product/tool research with a decision to make |
| `/follow-through:commitments Reconcile promises in these conversations` | Colleague commitments and handoffs |

For repeatable UI checks use `test-campaign:ui-regression`; for already authorised
agent continuation use `flagship:fleet-console`. Referrals are checked against the
receiving runtime. Missing connectors or skills remain visible as gaps.

Creating these skills grants no authority to start monitors, send messages, buy,
book, redeem credits, change accounts or release software. A review produces
evidence and next actions. When the user authorises execution, the skill carries
that bounded work through and verifies the requested outcome.

An optional read-only helper validates a private JSON ledger and prints a summary:

```bash
python3 plugins/follow-through/scripts/ledger.py check /path/to/private-ledger.json
python3 plugins/follow-through/scripts/ledger.py summary /path/to/private-ledger.json
python3 -m unittest discover -s plugins/follow-through/tests -v
```

Its format is bundled in the router skill. No daemon, connector credentials,
settings changes or personal data ship with this plugin. See [EVALS.md](EVALS.md)
for what was tested and what remains unproved.

No. Each recursive call runs `paymentIntents.create` again with no idempotency key, so a single `submitPayment(order)` can create up to four distinct PaymentIntents for the same order and insert four rows into `payments`. Retrying is creating new payment attempts, not re-driving one.

Three things make it worse:

`requires_action` is not a transient failure. It means the customer must complete authentication (3DS, redirect, etc.). Nothing about re-calling `create` server-side can change that, so the branch is guaranteed to run to `attempt === 3` every time it's entered — the retry ceiling is the normal path, not the exceptional one. You then fall through and call `toReceipt(res)` on the *last* unauthenticated intent, minting a receipt for a payment that hasn't been captured.

The DB insert happens before the retry decision and isn't in a transaction with anything, so the `payments` rows are the durable record of the mess: N rows per order, all with different `intentId`s, no marker of which one (if any) is authoritative. There's no unique constraint on `orderId` implied here to catch it either.

`attempt` is part of the public signature with a default, so any caller — including a retry wrapper one layer up — can pass `attempt: 3` and silently disable the bound, or pass `0` and restart the whole cycle.

To be idempotent it needs a stable idempotency key derived from the order (Stripe's `idempotencyKey` request option, keyed on something like `order.id` plus an attempt counter you actually persist), a lookup-or-create against an existing intent for the order before creating a new one, and `requires_action` returned to the caller as a state to surface to the customer rather than something to retry.

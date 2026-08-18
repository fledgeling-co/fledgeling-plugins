**No, this retry logic is not idempotent.**

### Why:
1. **Creates duplicate PaymentIntents:** `stripe.paymentIntents.create()` is invoked on every attempt without an `idempotencyKey` or an existing intent ID, generating a brand-new Stripe `PaymentIntent` on each retry.
2. **Creates duplicate database records:** `db.insert(payments)` inserts a new payment row for every attempt, linking multiple distinct intent IDs to the same `order.id`.
3. **Misinterprets `requires_action`:** A `requires_action` status indicates that customer interaction is needed (e.g., 3D Secure authentication). Creating new payment intents in a recursive loop will not resolve the required customer action and may lead to multiple pending or accidental duplicate charges.

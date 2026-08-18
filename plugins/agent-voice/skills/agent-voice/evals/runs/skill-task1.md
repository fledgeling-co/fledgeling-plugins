No. Each retry calls `stripe.paymentIntents.create` without an idempotency key, creating a new `PaymentIntent` and inserting a new payment record on every attempt. 

Retrying immediately on `requires_action` will also orphan the prior intent without giving the customer a way to complete authentication (such as 3D Secure).

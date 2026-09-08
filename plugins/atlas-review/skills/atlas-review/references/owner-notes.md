# Stage 7: the backend work, and the notes

## Why this is a stage

The product owner writes the interface and says plainly what they did not do:

> "A lot of changes so I imagine there might be a few issues again, but this time I tried
> not to touch anything backend/API wise and will leave that to you."

So a stack of UI PRs arrives with its backend deliberately absent. The screens render, and
the numbers behind them are invented. Nobody files a ticket for this, because from the
owner's side it is already done.

Their notes arrive as prose alongside the PRs. Read them as a work list. A real example, all
three of which turned out to be separate pieces of work:

> "the rating/chart 'lists' functionality + ranking movements. The logic should be there,
> but it's all mock data at the moment. Group 'membership' being able to actually join
> groups (it's just a UI button for now). the two 'just reviewed' pills on the product home
> page (should accurately show the two most recent reviews made on the app)."

## The standard

**Nothing counts as partly done.** Content a reader takes as fact is served by the API and
managed by an operator, never hardcoded in the client, even where the hardcoded value
happens to be right today.

That rule has teeth. Applying it to one stack turned up five more invented values nobody had
named: movement arrows, a hero product, curated lists, group counts, and a collage.

## Sweep for the rest

The three named items are rarely all of it. Grep the touched screens for values that look
like data and are not: literal arrays, hardcoded counts, a `TODO` next to a number, a
placeholder date. Anything a reader would take as a fact about the product is in scope.

Where wiring something needs a decision only the owner can take, say so with the options
rather than picking. Where it needs an endpoint that does not exist, build it: the contract
guards on both sides will tell you if you got the shape wrong.

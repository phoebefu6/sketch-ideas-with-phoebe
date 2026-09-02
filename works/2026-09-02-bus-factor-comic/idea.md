# You have a Sam

## Key Concept

"Bus factor" is software engineering's bluntest risk metric: how many people can be hit by
a bus - or, more politely, hand in a resignation - before a system stops working. Data and
AI estates are full of systems with a bus factor of one: the nightly ETL, the churn model's
retraining loop, the pricing engine's years of exception logic. The system looks like
infrastructure. Operationally, it is one person's memory.

The tension this piece exposes: the danger is invisible on the day it is created and
obvious only on the day it detonates. Panel 2 - Sam cheerfully boarding the bus - is the
moment every org waves through with a farewell card.

## Explanation

This is a deliberate register experiment. The companion piece on the wall
(2026-08-29, "One driver per route") plays the same concept as a deadpan municipal
timetable - strongest for readers who already know the term. A cold first read proved the
cost of that register: if you don't know "bus factor," the artifact stays locked.

So this version teaches instead of winks. Four panels, one story:

1. **Meet Sam** - one person, one humming machine labeled PRICING SYSTEM, coworkers
   not looking. The dependency forms in plain sight.
2. **Sam gets on a bus** - the metaphor made literal. The term's origin IS the picture,
   so the vocabulary teaches itself.
3. **Nobody can run it** - the machine survives; the knowledge doesn't. The sticky note
   reading "password??" is every handover that never happened.
4. **The definition card** - delivered only after the reader has lived the problem, plus
   the three unglamorous fixes: document, pair, rotate.

The single red accent is spent once, on the ERROR light - the same one-meaning-accent
discipline as the timetable, in a friendlier register.

## Recipe

- **Pipeline**: baoyu-infographic skill - comic-strip layout x craft-handmade style,
  4:3, rendered via codex-imagegen. Full prompt preserved in `prompts/infographic.md`.
- **Text discipline**: every label scripted verbatim in the prompt (10 labels, all
  rendered clean); short captions to minimize raster-text garble risk.
- **Crop contract**: all text inside the centre safe area so the LinkedIn 1.35:1
  centre-crop (`linkedin-1.35.png`) never clips a word.
- **Taste distinction banked**: register is a targeting decision, not a quality
  decision - the same concept can need an insider artifact AND a teaching artifact,
  and one work cannot be both.

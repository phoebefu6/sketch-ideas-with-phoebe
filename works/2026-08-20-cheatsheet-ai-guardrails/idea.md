# Where Guardrails Go in an AI Application

## Key Concept

Most guardrail diagrams show two placements - screen the user's input, screen the model's
output - and stop. That covers the chat surface and leaves the parts of a modern application
that actually reach the outside world completely unwatched.

NVIDIA's NeMo taxonomy is the most complete public one and it names five: input, dialog,
retrieval, execution and output. Add streaming and you have the real surface area. The two
that teams skip are retrieval, where indirect prompt injection arrives inside the documents
you fetched, and execution, where tool arguments go out and tool results come back. Execution
is the only station that can cause irreversible harm, and on Amazon Bedrock the managed
guardrail does not inspect it at all.

## Explanation

The sheet is a reference card, not an argument - one page holding the taxonomy, the costs and
the numbers so a practitioner can decide where to spend.

The schematic redraws the familiar two-band diagram and then extends it: a greyed unguarded
lane across the top as the before-state, then the input guard, the application with dashed
guard capsules sitting at retrieval and at the tool call, the output guard, and a stream guard
on the wire back to the user. Fail branches are labelled with real enforcement actions rather
than a generic X.

Below that, the things that change decisions. Guards ordered by cost, because a word filter is
free and near-instant while an LLM judge is a full generation - and Anthropic's two-stage
cascade cut overhead from 23.7% to about 1% by putting the cheap classifier first. What guards
actually cost, from Bedrock's own price list, where stacking four policies reaches $0.50 per
1,000 text units before a single model token. The real on-fail action set from Guardrails AI,
with the advice to ship every new guard on NOOP. And the numbers vendors do not lead with:
Llama Guard 4 at 69% recall and 11% false positives on English, Prompt Guard 1 scoring .987
AUC while catching only 21.2% of attacks at a 1% false-positive rate.

That last pair is the sheet's sharpest lesson: **AUC alone is nearly useless for a guardrail.
Always ask for TPR at your operating FPR.**

## Design-Built Recipe

Register V - every element is studied from, so nothing is raster. Hand-authored HTML with an
inline SVG hero, rendered with Chrome headless at A4 portrait, 794x1123 CSS px at
`--force-device-scale-factor=2`.

The hero is SVG rather than a generated image on purpose: the schematic is all labels and
precise geometry, so a model would garble the words and cost sharpness. Text renders perfectly
because it *is* text.

Sources are vendor documentation, model cards and standards bodies. The one figure taken from
model knowledge rather than a source is marked with a small circle, and the footer legend says
so.

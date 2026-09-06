# The journey of a question

## Key Concept

Ask most people what happens when they press Enter on a prompt and the honest answer is "it
looks something up." It doesn't. There is no lookup anywhere in the pipeline. A question is
tokenized, embedded, weighed by attention, and then the answer is *generated* - sampled one
token at a time, each choice conditioned on everything before it. The single most useful
correction to anyone's mental model of an LLM is: **the answer was never looked up, it was
grown.** Retrieval exists only when you bolt it on from outside.

## Explanation

The pipeline is drawn as a pilgrimage - four stations on one winding path up a mountain
through a sea of cloud, read bottom to top like the climb itself.

**Station I, the Gate (tokenizer).** A cinnabar paifang at the mountain's foot. Travelers
pass through carrying nothing; their baskets sit abandoned in a row outside. Your words are
never admitted - they are exchanged for tokens at the gate, and everything the model does
from here on happens to the tokens, not to your words.

**Station II, the Cloud-Sea (embeddings).** A lantern-strung rope bridge across a strait of
cloud. Each token crosses as coordinates in a vast space where meaning is a neighborhood,
not a definition - things that mean similar things live near each other.

**Station III, the Hall (attention).** The vast lantern-lit great hall built into the cliff.
Inside, every token weighs every other; the hall decides what matters to what. This is where
context becomes meaning.

**Station IV, the Summit (sampling).** A small pavilion alone above the cloud, one figure at
a stone table in dawn light. One word is chosen at a time - dice weighted by everything
below - and then the entire climb repeats for the next word.

The composition carries the argument: there is no library on this mountain, no archive, no
shelf to consult. Only a path, a crossing, a weighing, and a choice - repeated for every
word you read.

The shape deliberately continues the wall's illustrated-journey lineage (The Minds of Modern
AI) with the craft upgraded: that piece let the image model paint its own lettering; here the
hero was generated with all lettering refused and every character is hand-set, so the
painting stays cinematic and the type stays exact.

## Recipe

HYBRID. Hero: codex image_gen, portrait 3:4, first attempt - full prompt in
`prompts/01-hero-journey.md`. The two load-bearing parts are the four-station scene list
(each station described as architecture, not as a concept) and the reserved zones - big calm
cloud banks left and right, soft bands top and bottom, all named explicitly. Every script,
character and numeral form refused individually.

Type layer: Cormorant Garamond (editorial serif, italic deck) + IBM Plex Mono station
labels, cinnabar `#A93A26` accents, gold hairline leaders, soft cloud-toned text halos for
readability on the painting. Hand-authored HTML (`poster.html`), rendered headless Chrome at
1086x1448 @2x. Four registration rounds: the summit annotation originally collided with the
masthead (moved to the top-right sun cloud), and the terminal line drowned in the dark
baskets twice before landing in the light cloud column, hard-broken into three short lines.

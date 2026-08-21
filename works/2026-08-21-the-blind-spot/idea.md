# The Blind Spot

## Key Concept

Guardrail diagrams almost always answer "where can a guard sit?" - a list of five
stations, all treated as equally solved. That framing is comfortable and wrong. On an
agent, four of those stations are routinely covered by a managed service and one is not,
and the uncovered one is the only station that can reach outside the conversation and do
something irreversible.

Amazon Bedrock Guardrails do not inspect `toolUse.input` (the arguments the model
generates), `toolResult` (whatever your tool hands back), or `toolSpec` (your own tool
definitions). Content filters skip them and sensitive-information filters skip them, so
PII in a tool call is neither blocked nor masked. AWS shipped `InvokeGuardrailChecks` in
June 2026 precisely because of that gap: a resource-less, score-only check that you have
to call yourself, before the tool runs. The OpenAI Agents SDK has the mirror trap - input
guardrails fire only for the first agent in a chain and output guardrails only for the
last, leaving every intermediate handoff bare.

So the tension is not "add guardrails." It is: the thing you bought is watching the text,
and the damage happens at the tool.

## Explanation

The poster refuses the list. Instead of five labelled stations it shows five machined
modules exploded on one axis, and it makes the viewer's eye land on an absence.

Four discs are sealed, each ringed by a continuous cold-cyan seam - the visual grammar of
a closed instrument. The third is punched clean through: a chamfered circular bore with
nothing in it, no seam light, rimmed in hot amber, the glow spilling onto its neighbours.
You can see straight through the assembly at exactly the point that is supposed to be
protected. The hole is the hero, and every label reinforces it - four read SEALED in cyan,
one reads UNGUARDED in amber.

The right-hand column carries the evidence rather than decoration: the three Bedrock
fields that get skipped, why the June 2026 API had to exist, the first-agent/last-agent
trap, and the assay of the best open guard - Llama Guard 4 at 69% recall and 11% false
positives on English, meaning three in ten unsafe items pass unseen and one in nine safe
ones is refused. Multilingual recall falls to 43%. Guards cap the tail; they do not close
it. The lower-left block prescribes the fix so the piece argues rather than only accuses.

The reusable taste distinction: **when the story is a gap, draw the gap.** Rendering the
missing thing as a void is stronger than labelling the present things as fine.

## Hybrid Recipe

The hero is raster; every character is hand-set. Diffusion cannot set type, so it was
never asked to - the prompt forbids all lettering and reserves large empty black margins,
then the spec layer is composited in HTML and rendered with Chrome headless. That keeps
the illustration cinematic and the typography exact.

Registration matters more than it looks. With `object-fit: cover` on a background hero,
the label positions are percentages of the plate, and the five disc centres sit at 20.4%,
34.5%, 49.0%, 63.5% and 77.3% of height with the assembly spanning x 33.1% to 65.6%.
Everything else is margin, deliberately reserved at generation time.

### Hero prompt (codex image_gen, 3:4)

See `prompt.md` for the exact text. The two load-bearing parts are the breach description
and the negative list - every script and numeral form has to be refused individually, or
the model letters the machined faces.

### Type layer

Near-black `#07090C` ground, `#F2F4F7` body, `#8A929C` muted, cold cyan `#4FC3E8` for
sealed, hot amber `#E8912F` for the breach. All five clear WCAG AA on the ground. Tight
Helvetica-grotesque display with monospace spec labels - the Modern Metro vocabulary.
Source in `poster.html`.

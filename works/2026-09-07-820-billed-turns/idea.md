# You sent 40 turns. The API billed 820.

## Key concept

A chat with a model looks like a conversation. The invoice is a triangle.

The Claude Messages API is **stateless**: it remembers nothing between calls, so the caller
re-sends the entire prior conversation with every request. Request 1 carries 1 turn. Request 40
carries 40. Draw that honestly and you get a lower-triangular matrix - and the count in it is not
40, it is **820**.

```
T(N) = N(N+1)/2        T(40) = 40 x 41 / 2 = 820
820 / 40 = 20.5x       820 - 40 = 780 blocks of pure replay
```

Three things the picture says that the sentence cannot:

- **The left column is solid.** That is your first message. You wrote it once. It was billed forty
  times, because it was on the wire in every single request.
- **The diagonal is the only new text in the whole image** - 40 blocks out of 820. Everything to
  the left of it is text the model has already been sent.
- **The multiplier grows with the chat.** It is `(N+1)/2`, so the cost per turn is worst exactly
  when the conversation is going well and you keep going.

A bonus for anyone who has trained a transformer, deliberately left off the poster: this is the
same lower-triangular shape as a causal attention mask. The billing shape and the attention shape
are the same triangle.

## Explanation

**Why it compounds.** Statelessness is a design choice, not a bug - it is what makes the API
horizontally scalable and reproducible. The cost consequence is arithmetic: N requests, each
carrying one more turn than the last, bill the triangular number of turn-blocks rather than N of
them. Nobody chose 820. Every turn only added one.

**What it costs.** The prices are sourced; the conversation shape is not, so it is stamped
ILLUSTRATIVE on the sheet. At 1,000 tokens a turn, those 820 blocks are 820,000 input tokens -
USD 4.10 on Claude Opus 5 at USD 5.00 per MTok. Per-turn math predicts 40,000 tokens and 20 cents.
Same conversation, 20.5x the bill, and output tokens are billed on top. Re-run it with your own
tokens-per-turn; the shape does not change.

**What this piece refuses to claim.** That prompt caching fixes it. Caching **re-prices** the
replay - a cache hit bills 0.1x base input (50 cents per MTok on Opus 5) - but the replay still
happens, each new block still costs a 1.25x write, and the default cache lives five minutes, which
is shorter than most human pauses in a real chat. "Just turn on caching" is the comfortable half
of the answer. The other half is capping the history you send and summarising old turns instead of
re-sending them.

## Recipe

**DESIGN-BUILT**, not generated. Hand-authored HTML/CSS with a generated inline SVG, rendered with
headless Chrome at 1000x1250 CSS px and `--force-device-scale-factor=2` (2000x2500, 4:5).

- **Style:** SV-034 Two-Color Acid - acid lime `#D2FF00` on near-black `#111112`, exactly two
  colours, no white, no grey, no gradients, no mid-tones. Lime is never decoration: it is the
  token you were billed for.
- **Geometry:** the 40x40 matrix is computed in the generator, not eyeballed, and the script
  asserts the cell count equals 820 (40 solid + 780 hairline) before it writes the file. When the
  concept *is* a count, the count has to be auditable.
- **Hierarchy without a third colour:** weight inside the one accent - a hairline square is one
  more billing, a solid square is the same message billed again.
- **Type:** Archivo 800 for the title and the hero count; IBM Plex Mono for every spec label,
  annotation and source line.
- **Sources are printed on the work**, in mono, at the foot: published reasoning is part of the
  wall, not a footnote to it.

Sources: platform.claude.com/docs - Messages API ("stateless multi-turn conversations", prior
turns supplied by the caller) and Pricing (Claude Opus 5 base input USD 5.00 per MTok, cache hit
USD 0.50 per MTok = 0.1x, 5-minute cache write 1.25x), fetched 2026-09-07.

# Retries don't add. They multiply.

## Key Concept

Every engineer reads "3 retries" as *three more calls*. In a layered stack it is not
addition, it is a product. A request that passes through three layers, each configured to
retry three times - four attempts apiece - can arrive at the bottom **64 times** from a
single user action.

This is documented, not clever. Google's SRE book states it plainly in *Addressing Cascading
Failures*: "a single request at the highest layer may produce a number of attempts as large
as the *product* of the number of attempts at each layer to the lowest layer. If the database
can't service requests because it's overloaded, and the backend, frontend, and JavaScript
layers all issue 3 retries (4 attempts), then a single user action may create 64 attempts
(4^3) on the database."

Swap the database for a model endpoint and the arithmetic is unchanged. What changes is who
is holding the amplifier: an agent loop that retries, behind a gateway that retries, on top
of an SDK that retries. That is exactly three layers.

The tension: the thing being hit 64 times is almost always the thing that was already
failing. The 429 you were being polite about is the reason all 64 calls exist. Retries
designed to survive an overload are a mechanism for extending it.

## Explanation

The sheet is an honest count, and the count is the whole argument - which is why it was
design-built rather than generated. Diffusion cannot draw 64 of anything reliably, and
"roughly a lot of lines" would have destroyed the piece.

Every mark carries one meaning. One hairline is one real request on the wire; all 64 are
drawn, never symbolised. Each horizontal band is a layer that owns a retry decision, with
its `ATTEMPTS x4` stamp on the right. The ladder down the left margin is the running tally -
x1, 4, 16, 64 - so the eye can watch the multiplication happen without reading a word.

The two-second read is geometry: a wide dense fan pinching into a port that is visibly too
small for it. That inversion is deliberate. A funnel narrows because you *want* it to; this
narrows because the endpoint has no choice. The single accent - alarm red - is spent only on
the 64-fan, its comb, the port, and the x64 tally: one meaning, amplification and its victim.
Everything structural stays indigo.

The 64 lines get a short parallel segment before they converge. Without it they merged into
a solid triangle and the count became a vibe. The comb is what keeps the claim checkable.

Two annotations do the argumentative work, one on each side of the port. Left: **"Nobody
wrote 64. Every layer wrote 3."** - the number is emergent, and no individual code review
would catch it, because each local decision was textbook. Right: **"Already returning 429.
That is what started this."**

The AI-native sting sits in the footer. You probably wired two retry layers on purpose. The
third came free: the Anthropic Python SDK auto-retries connection errors, 408, 409, 429 and
5xx with exponential backoff at a default `max_retries = 2` - up to three attempts per call -
and it is on until you set it to `0`. Most LLM stacks are running a retry layer their author
never chose.

The fix was published before the problem reached AI. The Amazon Builders' Library: "for
low-cost control-plane and data-plane operations, the best practice is to retry at a single
point in the stack." Google's SRE handbook adds the numbers - a per-request cap of three
attempts, plus a per-client budget that retries only while the retry ratio stays under 10%,
which holds load growth to 1.1x rather than the ~3x it reaches unbudgeted.

The reusable taste distinction: **when the concept is a count, draw the count.** A schematic
with "N retries" written on an arrow explains nothing that the sentence didn't. Sixty-four
individually drawn hairlines pinching into one port is an argument the reader can audit with
their own eyes.

One claim was deliberately left off the sheet: that all 64 calls are billed. Retried 429s and
5xx are not billed for output, while a retry after a client-side timeout can bill for work
already done. Too fine a distinction for a poster and easy to get wrong - so the piece argues
load, not spend.

## Recipe

Design-built, no diffusion. Hand-authored HTML/CSS with an inline SVG hero (`poster.html`),
rendered with headless Chrome at 1000x1250 CSS px and `--force-device-scale-factor=2`
(2000x2500 final, 4:5).

The fan geometry is computed rather than eyeballed: each layer's children are generated from
its parent positions, so 4, 16 and 64 are literally countable and the tree is structurally
correct - every parent emits exactly four children.

Style skin: **SV-033 Blueprint Ledger**, third outing and first non-cheatsheet. Warm paper
`#FDFDFB`, blueprint indigo `#1F3A5F` at single stroke weight, pale wash `#EAF0F7` for
components you own and configured, hairline grid `#D5DDE8`, and one meaning accent - alarm
red `#C2372B`. Type: Georgia serif title, system sans body, IBM Plex Mono for every spec
label, stamp and source line.

Sources, all published and named on the sheet itself: Google SRE Book (*Addressing Cascading
Failures*, *Handling Overload*), Amazon Builders' Library (*Timeouts, retries, and backoff
with jitter*), and the `anthropic-sdk-python` README for the retry default.

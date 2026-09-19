Your chat had 40 turns. The API billed 820.

Not a typo, and not a bug either. The Messages API is stateless - it remembers nothing between
calls, so every turn re-sends the whole conversation as input tokens. Request 1 carries one turn.
Request 40 carries forty. Draw that honestly and the invoice is a triangle: T(40) = 820 blocks on
the wire, 20.5x what per-turn math predicts.

I drew all 820 of them, because when the point IS a count, you should be able to count it.

Three things I only saw once it was on the page:

The left column is solid. That is my first message. I wrote it once. It was billed forty times,
because it rode along in every single request.

The diagonal is the only new text in the picture - 40 blocks out of 820. Everything left of it is
text the model has already been sent.

And the multiplier is (N+1)/2, so it grows with the chat. The cost per turn is worst exactly when
the conversation is going well and you keep going.

One thing I deliberately did not say on the poster: that caching fixes this. A cache hit bills
0.1x base input, which re-prices the replay - it does not stop it. Each new block still costs a
1.25x write, and the default cache lives five minutes, which is shorter than most of my pauses.
The rest of the answer is unglamorous: cap the history you send, and summarise old turns instead
of re-sending them.

Prices are from the Claude docs and printed on the work. The tokens-per-turn is mine and labelled
illustrative - swap in your own, the shape does not change.

For the transformer people: yes, it is the causal attention mask. The billing shape and the
attention shape are the same triangle.

#AI #DataEngineering

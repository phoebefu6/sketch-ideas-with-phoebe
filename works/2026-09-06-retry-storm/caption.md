# LinkedIn caption - Retries don't add. They multiply.

I have never met an engineer who wrote 64 retries. I have met plenty of systems that made 64 calls.

Here is how that happens.

Your agent loop retries three times. Sensible. The gateway in front of the model retries three times. Also sensible. The provider SDK retries three times - and that one you probably did not configure at all, because it ships on by default. The Anthropic Python SDK auto-retries connection errors, 408, 409, 429 and 5xx with exponential backoff at max_retries = 2, until you set it to 0.

Three layers, four attempts each. Not 3 + 3 + 3. It is 4 x 4 x 4.

One user action, 64 calls on the endpoint.

Google's SRE book has been saying this for years, with a database instead of a model: a single request at the highest layer produces attempts equal to the product of the attempts at each layer. Their example is literally 4 cubed. Swap the database for a model endpoint and nothing about the arithmetic changes.

The part that still gets me is which endpoint takes the hit. It is the one that was already returning 429. That rate limit is the reason all 64 calls exist. Retries meant to survive an overload become a very efficient way to extend it.

Nobody wrote 64. Every layer wrote 3.

The fix was published long before any of us put an LLM behind a proxy:

- Retry at a single point in the stack, not at every layer that could (Amazon Builders' Library).
- Cap attempts per request. Three is the number Google uses.
- Add a retry budget on top of the cap. Their per-client rule only retries while the retry ratio stays under 10%, which holds load growth to 1.1x instead of roughly 3x.

If you run agents in production, the useful question is not "do we retry?" - it is "how many layers of ours retry, and did we choose all of them?" Count the layers. Then multiply.

I drew all 64 lines rather than writing "64" on an arrow, because the count is the entire argument and I wanted it countable.

#AppliedAI #LLMOps #Reliability

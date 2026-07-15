# Source configuration

## YouTube subscriptions

- Feed: `https://www.youtube.com/feed/subscriptions`
- Authentication: signed-in Codex in-app browser session
- Frequency: daily
- Window: since previous successful run; fall back to the most recent 48 hours
- Limit: inspect at most 30 feed items and create at most 10 new Notion candidates per run

For each video capture:

- video ID and canonical watch URL
- title and channel
- publication timestamp
- duration when visible
- transcript or captions when available
- chapter structure when available
- 3–7 key topics
- source-backed evidence with timestamps

Do not use the public subscriptions page while signed out as a substitute for the personalized feed. If sign-in is missing, report the block and do not guess subscriptions.

## Future sources

Add RSS, websites, newsletters, Slack channels, podcasts, and papers only after the user supplies or authorizes each source. Keep credentials and private source lists outside public repository files.

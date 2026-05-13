# Decisions Log

A record of every technical choice I made and why.
This is my thinking, not just my code.

---

## Week 1 — Foundations

### Why I switched from google.generativeai to google-genai
The old library was deprecated and throwing FutureWarnings.
The new google-genai SDK is the officially supported package
and works cleanly with gemini-2.0-flash.

### Why I use gemini-2.0-flash instead of gemini-2.5-flash
The 2.5-flash free tier has a limit of 20 requests/day —
too low for active learning and experimentation.
2.0-flash has a much more generous free tier (1500 RPD)
so I can run experiments without hitting limits.

### Why conversation history is a plain Python list
The model only needs the text of the conversation.
A list is the simplest structure that holds exactly that.
In production I would persist this to Redis between sessions,
but the core data structure stays the same.

### Why summarise history instead of truncate
Truncation deletes old messages and loses context — the agent
forgets important facts. Summarisation compresses the information
instead of removing it. Tradeoff: one extra API call per compression.
For most agents that cost is worth preserving the context.

### Why estimate tokens with len(text) // 4
This is a rough heuristic, not exact. The real approach is
using the model's native tokeniser. I used the estimate here
to keep focus on the concept — in production I'd use the
actual token count from the API response.
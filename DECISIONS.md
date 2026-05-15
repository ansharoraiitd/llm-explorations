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

## Why Pydantic over plain json.loads()
json.loads() just gives you a dict — no validation, no types,
no guarantee the fields you need are actually there.
Pydantic validates the shape, enforces types, and raises a 
clear error with the exact field that's wrong. In a multi-step
agent where one step's output feeds the next, silent bad data
is catastrophic. Pydantic makes bad data loud and obvious.

## Why wrap JSON parsing in try/except always
LLMs are probabilistic — even with a perfect system prompt,
the model occasionally returns malformed JSON (extra text,
wrong field names, wrong types). In production you cannot
let a parsing failure crash the entire agent. try/except lets
you retry with a stronger prompt or return a safe fallback.

## Why self-consistency works
A model that's uncertain tends to vary its answer across runs.
A model that's confident tends to give the same answer.
By running the same question 3 times and taking majority vote,
you statistically filter out the uncertain, wrong answers.
Tradeoff: 3x the API cost. Worth it for high-stakes factual queries.

## Why use a class for the chatbot instead of functions
The chatbot has state — history, session ID, turn count, system prompt.
Functions would require passing all this state around as parameters.
A class bundles state and behaviour together cleanly. When you read
ChatBot.chat() you immediately know it uses self.history and
self.system_prompt — no hunting through parameters.

## Why handle KeyboardInterrupt separately from Exception
Ctrl+C is not a bug — it's intentional user behaviour.
Catching it separately lets me run save_session() cleanly before
exiting. If I only had a broad except, Ctrl+C might get swallowed
or handled identically to a real error. Separate handling = 
correct behaviour for each case.

## Why auto-compress at 20 messages not sooner
Too aggressive compression loses context too early — the chatbot
starts forgetting things the user just said. 20 messages is roughly
10 conversation turns, which is enough for meaningful sessions while
still being well within token limits for the models I'm using.
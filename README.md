# LLM Explorations

Hands-on experiments building with LLM APIs — from first API calls
to a fully-featured CLI chatbot. Week 1 of a 14-week agentic AI roadmap.

## What this repo covers
- LLM API calls, streaming, and token management
- System prompt engineering — personas, output formats, JSON enforcement
- Conversation memory and context window management  
- Structured outputs with Pydantic
- Prompt patterns: chain-of-thought, few-shot, self-consistency
- A complete CLI chatbot bringing all concepts together

## Project: CLI Chatbot
A fully-featured command-line chatbot with:
- Streaming token-by-token output
- Persistent conversation history
- Automatic history compression when context gets long
- Session save/load to JSON
- Commands: /save /stats /history /clear /quit

**Run it:**
pip install -r requirements.txt
Add GEMINI_API_KEY to .env
python chatbot.py

## Files
| File | What it does |
|------|-------------|
| llm.py | Reusable Gemini helper — chat() and chat_stream() |
| 01_first_call.py | First API calls, max_tokens, streaming experiments |
| 02_system_prompts.py | 5 system prompt experiments — personas, formats, JSON |
| 03_conversation.py | Multi-turn memory, stateless proof, history growth |
| 04_context_limits.py | Token counting, context limits, summarisation |
| 05_structured_output.py | Pydantic structured outputs, safe JSON parsing |
| 06_prompt_patterns.py | CoT, few-shot, self-consistency patterns |
| chatbot.py | Complete CLI chatbot — the week's main deliverable |

## Key learnings
- LLMs are stateless — memory is a list you manage, not the model
- System prompts control behaviour more than the question does
- Structured outputs with Pydantic make agents reliable
- Chain-of-thought prompting improves accuracy on complex tasks
- Context windows are finite — summarisation beats truncation

## Tech stack
Python · Google Gemini API · Pydantic · google-genai SDK
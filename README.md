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

## Project structure
llm-explorations/
├── llm.py                  # Reusable Gemini API helper
├── chatbot.py              # Main CLI chatbot application
├── 01_first_call.py        # Basic API calls and streaming
├── 02_system_prompts.py    # System prompt experiments
├── 03_conversation.py      # Conversation memory
├── 04_context_limits.py    # Token counting and summarisation
├── 05_structured_output.py # Pydantic structured outputs
├── 06_prompt_patterns.py   # CoT, few-shot, self-consistency
├── requirements.txt        # Python dependencies
└── .env.example            # Template for API keys

## Key learnings
- LLMs are stateless — memory is a list you manage, not the model
- System prompts control behaviour more than the question does
- Structured outputs with Pydantic make agents reliable
- Chain-of-thought prompting improves accuracy on complex tasks
- Context windows are finite — summarisation beats truncation

## Tech stack
Python · Google Gemini API · Pydantic · google-genai SDK
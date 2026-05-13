from llm import chat

#Part1 : understanding token counting

#simplest way to estimate tokens: len(text) / 4

def estimate_tokens(text):
    return len(text) // 4

test_texts = [
    "Hello",
    "What is a large language model?",
    "Explain the entire history of artificial intelligence from its origins in the 1950s to modern transformer models."
]    

for text in test_texts:
    est = estimate_tokens(text)
    print(f"Text: '{text[:50]}...'" if len(text)>50 else f"Text: '{text}'" )
    print(f"Estimated tokens: ~ {est}\n")

#Part2: watching content grow in a conversation

print('='*50)
print("Part 2: How content grows per turn:")
print('='*50)

history=[]

def talk_with_tokens(user_message, system):
    history.append({
        "role": "user",
        "content": user_message
    })

    #estimating the total tokens being sent this turn

    total_text = system + " " + " ".join([m["content"] for m in history])

    estimated_tokens = estimate_tokens(total_text)

    response = chat(
        system=system,
        messages=history
    )
    history.append({
        "role": "assistant",
        "content": response
    })

    return response, estimated_tokens

system_prompt = "You are an AI tutor. Give detailed, thorough answers to every question. Never give short answers."

turns = [
    "Explain what RAG is in detail.",
    "Now explain how vector databases work in detail.",
    "How do embeddings relate to what you just explained?",
    "What are the tradeoffs between different chunking strategies?"
]

for turn in turns:
    reply, tokens = talk_with_tokens(turn, system_prompt)
    print(f"Turn: {turn[:50]}")
    print(f"Estimated tokens sent this call: ~{tokens}")
    print(f"History messages: {len(history)}")
    print(f"Reply preview: {reply[:100]}...\n")

# ── Part 3: the solution — conversation summarisation ────────
print("=" * 55)
print("PART 3: Handling long conversations — summarise")
print("=" * 55)

def summarise_history(history):
    """
    When history gets too long, summarise it into one message.
    This is a real technique used in production agents.
    """
    if len(history) <= 4:
        return history # short enough, keep as is
    
    #build a history of everything except the last two turns
    old_messages=history[:-2]
    recent_messages=history[-2:]

    conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in old_messages])

    summary = chat(
        system="You are a conversation summariser. Be concise.",
        messages=[{
            "role": "user",
            "content": f"Summarise this conversation in 3 bullet points preserving all the important facts and context: {conversation_text}"
        }]
    )
    #replace old messages with one summary message

    compressed_history = [
        {"role": "user", "content": f"[Conversation summary: {summary}]"},
        {"role": "assistant", "content": "Understood, I have the context."}
    ] + recent_messages

    return compressed_history

# Test the summariser
long_history = [
    {"role": "user", "content": "My name is Ansh. I am learning agentic AI."},
    {"role": "assistant", "content": "Great to meet you Ansh! Agentic AI is a fascinating field."},
    {"role": "user", "content": "I want to build a research agent using LangGraph."},
    {"role": "assistant", "content": "LangGraph is perfect for that. It handles stateful workflows well."},
    {"role": "user", "content": "I also want to add RAG to it."},
    {"role": "assistant", "content": "Adding RAG to a LangGraph agent is a great combination."},
]

print(f"History before summarisation: {len(long_history)} messages")
compressed = summarise_history(long_history)
print(f"History after summarisation: {len(compressed)} messages")
print("\nCompressed history:")
for m in compressed:
    print(f"  {m['role'].upper()}: {m['content'][:100]}")




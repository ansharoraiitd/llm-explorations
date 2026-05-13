from llm import chat

#we define:

conversation_history = []

#this list is the memory.
#it grows with every turn of the conversation

def talk(user_message):
    """
    Send a message and get a reply.
    Automatically maintains conversation history.
    """
    #step1 - add user's message to the history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

#step2 - send the FULL history to the model
#not just the latest message - the whole list
    response = chat(
    system="You are a helpful AI tutor teaching agentic AI systems.",
    messages=conversation_history #send the whole history every time
    )

#step3 - add the model's reply to the history too
    conversation_history.append({
    "role": "assistant",
    "content": response
    })

    return response

#Test 1 - see if it remembers across turns
print("="*50)
print("TEST 1 - BASIC MEMORY ACROSS TURNS")
print("="*50)

reply1 = talk("My name is Ansh and I am learning agentic AI.")
print(f"Turn 1: {reply1}\n")

reply2 = talk("What is my name?")
print(f"Turn 2: {reply2}\n")

reply3 = talk("What am I learning?")
print(f"Turn 3: {reply3}\n")

# ── Show the raw history ─────────────────────────────────────
print("=" * 55)
print("RAW HISTORY LIST (what gets sent to the model):")
print("=" * 55)
for i, msg in enumerate(conversation_history):
    print(f"[{i}] {msg['role'].upper()}: {msg['content'][:80]}..."
          if len(msg['content']) > 80
          else f"[{i}] {msg['role'].upper()}: {msg['content']}")

print(f"\nTotal messages in history: {len(conversation_history)}")

#Experiment 1 - proving the model has no memory without history

sep = '\n' + "="*50
print(sep)
print("Experiment 1 - No history = no memory")
print(sep)

#Call1 - tell the model our name (no history maintained)

response1 = chat(
    messages=[{
        "role": "user",
        "content": "My name is Ansh."
    }]
)

#Call2 - ask for the same name (completely fresh call - no history)

response2 = chat(
    messages=[{
        "role": "user",
        "content": "What is my name?"
    }]
)

print(f"Without history: {response2}\n")
# It will say it doesn't know — proving the model is stateless

#Experiment 2 - watching the history grow with every turn

print(sep)
print("Experiment 2 - watching the history grow with every turn")
print(sep)

#we should follow this practise of rsetting conversation history
conversation_history.clear()

questions = [
    "What is LangChain?",
    "How does it differ from calling the API directly?",
    "What is LangGraph?",
    "How does LangGraph relate to what you just told me about LangChain?",
    "Which one should I learn first?"
]

for q in questions:
    reply = talk(q)
    print(f"Q: {q}")
    print(f"A: {reply[:120]}...")
    print(f"History size: {len(conversation_history)} messages.\n" )



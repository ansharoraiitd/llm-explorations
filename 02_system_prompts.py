from llm import chat

QUESTION = "What is RAG and when should I use it?"

#Experiment 1 - no system prompt

a1 = chat(
    messages=[{
        "role": "user",
        "content": QUESTION
    }]
)

#Experiment 2 - strict bullet points

a2 = chat(
    system="""You are a concise technical tutor teaching agentic AI.
Rules you must follow:
- Answer in exactly 3 bullet points
- Each bullet is one sentence maximum  
- No extra explanation outside the bullets
- End with one concrete real-world example""",
    messages=[{
        "role": "user",
        "content": QUESTION
    }]
)

#Experiment 3 - senior engineer persona

a3 = chat(
    system="""You are a senior AI engineer with 8 years of production
experience building LLM systems at scale. You give direct, opinionated
answers based on real experience. You always mention concrete tradeoffs.
You never say 'it depends' without immediately saying what it depends on.
You speak like you are mentoring a smart junior engineer.""",
    messages=[{
        "role": "user",
        "content": QUESTION
    }]
)

#experiment 4 - force JSON output

a4 = chat(
    system="""You are a technical documentation API.
CRITICAL RULE: Respond with valid JSON only.
No markdown. No backticks. No explanation. Just raw JSON.
Use exactly this structure:
{
  "concept": "name of the concept",
  "definition": "one sentence definition",
  "when_to_use": ["reason 1", "reason 2", "reason 3"],
  "when_not_to_use": ["reason 1", "reason 2"],
  "example": "one concrete example sentence"
}""",
    messages=[{
        "role": "user",
        "content": QUESTION
    }]

)

#experiment 5 - my own personal system prompt

a5 = chat(
    system="""respond in a very informal way as if you are talking to a very old friend, say things in a casual way, use slangs to talk and give your message""",
    messages=[{
        "role": "user",
        "content": QUESTION
    }]
)

#so now we print all the answers clearly, since the output will be large , we should use a good separation

sep = "\n" + "="*55+ "\n"

print(sep)
print("Experiment 1 - no system prompt:")
print(sep)
print(a1)

print(sep)
print("EXPERIMENT 2: Strict bullet-point tutor")
print(sep)
print(a2)

print(sep)
print("EXPERIMENT 3: Senior engineer persona")
print(sep)
print(a3)

print(sep)
print("EXPERIMENT 4: Forced JSON output")
print(sep)
print(a4)

print(sep)
print("EXPERIMENT 5: My personal prompt - casual and friendly output")
print(sep)
print(a5)

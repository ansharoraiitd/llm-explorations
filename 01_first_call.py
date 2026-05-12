from llm import chat, chat_stream
"""
# this is my very first API call

response = chat(
    messages=[{
        "role": "user",
        "content": "What is a large language model? Explain in 3 sentences."

    }]
)

print("RESPONSE:")
print(response)
print(f"\nType : {type(response)}")
print(f"Length : {len(response)} characters")
"""

"""
#Experiment A : studying the effect of max tokens

short = chat(
    messages=[{
        "role": "user",
        "content": "Explain neural networks in detail."
    }],
    max_tokens=100
)

print("\nExperiment A - max_tokens=100:")
print(short)
"""

# Experiment B: Try these one at a time — change the content string each run
# 1. "Write a Python function that reverses a string"
# 2. "What is the difference between RAG and fine-tuning?"
# 3. "Give me 5 project ideas for an agentic AI portfolio"
"""
question1 = chat(
    messages=[{
        "role": "user",
        "content": "Write a Python function that reverses a string"

    }]

)
print("\nExperiment B:")
print(question1)
"""
"""
question2 = chat(
    messages=[{
        "role": "user",
        "content": "What is the difference between RAG and fine-tuning?"

    }]

)
print("\nExperiment B:")
print(question2)
"""
"""
question3 = chat(
    messages=[{
        "role": "user",
        "content": "Give me 5 project ideas for an agentic AI portfolio"

    }]

)
print("\nExperiment B:")
print(question3)
"""

#experiment C - streaming: tokens appear live as generated
print("\nExperiment C - streaming:")
print("Response: ", end="", flush=True)
chat_stream(
    messages=[{
        "role": "user",
        "content": "Explain how AI agents work step by step."

    }]

)



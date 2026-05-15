from llm import chat

#Pattern1 - Chain of Thought(CoT)
# We force the model to give step by step reasoning before answering.
# Works dramatically better for complex reasoning tasks.

print("="*70)
print("PATTERN 1: Chain of Thought")
print("="*70)

HARD_QUESTION = """An AI agent pipeline has 4 steps. Each step calls
an LLM. Each call costs 0.5 seconds on average. The pipeline runs
100 times per hour. How many seconds per hour are spent on LLM calls?
And what would happen to this if you added a 5th step?"""

#Without CoT

without_cot= chat(
    messages=[{
        "role": "user",
        "content": HARD_QUESTION
    }]
)

#With Cot

with_cot = chat(
    system="""You are a precise technical analyst.
Before giving your final answer, always:
1. Break the problem into clear steps
2. Work through each step explicitly
3. State your final answer clearly at the end
Label your reasoning as THINKING: and your answer as ANSWER:""",
    messages=[{
        "role": "user",
        "content": HARD_QUESTION
    }]
)

print("Without Chain of Thought:")
print(without_cot)
print("\nWith Chain of Thought:")
print(with_cot)


#Pattern 2 - few shot prompting
# We give the model examples of input-output pairs.
#The model learns the pattern from the examples and applies it to the new question.

print("\n" + "=" * 55)
print("PATTERN 2: Few-shot prompting")
print("=" * 55)

few_shot_system = """Classify the user's intent into one of these categories:
SEARCH, WRITE, RECALL, ANALYSE, or UNCLEAR.

Here are examples of correct classifications:
Input: "find recent papers on RAG" → SEARCH
Input: "search for LangGraph tutorials" → SEARCH
Input: "write a summary of this document" → WRITE  
Input: "draft an email about the project" → WRITE
Input: "what did we discuss earlier?" → RECALL
Input: "remind me what I said about memory" → RECALL
Input: "compare these two approaches" → ANALYSE
Input: "which is better, A or B?" → ANALYSE

Respond with ONLY the category word. Nothing else."""

test_inputs = [
    "look up the latest news on LLMs",
    "create a report on our agent performance",
    "what was the context we established earlier?",
    "evaluate the tradeoffs between these options",
    "hmmm I dunno maybe something"
]

print("Classifying user inputs:")

for user_input in test_inputs:
    result = chat(
        system=few_shot_system,
        messages=[{
            "role": "user",
            "content": user_input
        }]
    )
    print(f"Input: {user_input}")
    print(f"Intent: {result.strip()}\n")


#Pattern 3 - Self-consistency
#Asking the same questions multiple times and take the majority answer.
#Dramatically reduces hallucination on factual questions.

print("\n" + "=" * 55)
print("PATTERN 3: Self-consistency(reduce hallucination)")
print("=" * 55)

FACTUAL_QUESTION = "What year was the transformer architecture introduced in the paper 'Attention is All You Need'?"

answers=[]
for i in range(5):
    answer = chat(
        system="Answer with the year only. Single number, nothing else.",
        messages=[{
            "role": "user",
            "content": FACTUAL_QUESTION
        }]
    )
    answers.append(answer.strip())
    print(f"Run {i+1}: {answer.strip()}")

#Now we have to find the majority year in answers

from collections import Counter
answer_counts = Counter(answers)
majority_answer, count = answer_counts.most_common(1)[0]
print(f"\nMajority answer: {majority_answer} (appeared {count} out of 5 times)")


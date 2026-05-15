import json
from llm import chat
from pydantic import BaseModel
from typing import List, Optional

#Step 1 is to define what we want back from the model
#This is our "contract" with the model
#We are saying - I want exactly this back, nothing else

class TechAnalysis(BaseModel):
    technology: str
    one_line_summary: str
    pros: List[str]
    cons: List[str]
    best_for: str
    avoid_when: str
    verdict: str

#Step 2 is to define a function that enforces the contract

def analyse_tech(tech_name: str) -> TechAnalysis:
    """
    Ask the model to analyse a technology.
    Forces the output into a clean TechAnalysis object.
    """
    response = chat(
        system="""You are a technical analyst. 
    You MUST respond with valid JSON only.
    No markdown. No backticks. No explanation before or after.
    Just the raw JSON object and nothing else.""",
        messages=[{
            "role": "user",
            "content": f"""Analyse the technology: {tech_name}
            Return a JSON object with EXACTLY these keys:
    - technology: string (the name)
    - one_line_summary: string (one sentence)
    - pros: list of 3 strings
    - cons: list of 3 strings  
    - best_for: string (one sentence on ideal use case)
    - avoid_when: string (one sentence on when not to use it)
    - verdict: string (your recommendation in one sentence)"""
        }]
    )

    #Parse the JSON string into a python dict
    #Remove any accidental markdown the model adds (e.g. if it adds ```json at the start or ``` at the end, we remove that)    

    raw = response.strip()
    if raw.startswith("```"):
    # model wrapped it in backticks despite instructions - strip them
        raw = raw.split("```")[1]
    if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)

    # Validate against our Pydantic model
    # This raises a clear error if any field is missing or wrong type
    return TechAnalysis(**data)

#Step 3: use it 
print("=" * 50)
print("TEST 1: Analyse LangChain")
print("=" * 50)

result = analyse_tech("LangChain")

#Now we access fields like a python object - no parsing needed, no guessing about keys, no messy dicts

print(f"Technology: {result.technology}")
print(f"Summary: {result.one_line_summary}")
print(f"Best for: {result.best_for}")
print(f"Avoid when: {result.avoid_when}")
print(f"Verdict: {result.verdict}")
print(f"\nPros:")
for pro in result.pros:
    print(f" + {pro}")
print(f"\nCons:")
for con in result.cons:
    print(f" - {con}")

#Step 4: we try and run it on multiple technologies

technologies = ["ChromaDB", "FastAPI", "Docker"]

for t in technologies:
    output = analyse_tech(t)
    print(f"\n{output.technology}: {output.one_line_summary}")
    print(f"Verdict: {output.verdict}")


# Experiment: what happens with bad JSON?
print("\n" + "=" * 55)
print("EXPERIMENT: Handling bad model output")
print("=" * 55)

def analyse_tech_safe(tech_name: str) -> Optional[TechAnalysis]:
    """
    Same as analyse_tech but handles failures gracefully.
    In production agents, we ALWAYS wrap parsing in try/except.
    """
    try:
        return analyse_tech(tech_name)
    except json.JSONDecodeError as e:
        print(f"Model returned invalid JSON: {e}")
        return None
    except Exception as e:
        print(f"Validation failed: {e}")
        return None

# Try with a vague input that might confuse the model
result = analyse_tech_safe("quantum computing is tough")
if result:
    print(f"Got result: {result.technology}")
else:
    print("Handled failure gracefully - no crash")    




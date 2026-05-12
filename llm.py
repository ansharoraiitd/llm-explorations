import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Creating one client, reused across all calls
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.1-flash-lite"


def chat(messages, system=None, max_tokens=1024):
    """
    Single reusable function for all LLM calls.

    Args:
        messages  : list of {"role": "user"/"assistant", "content": "..."}
        system    : optional system prompt string
        max_tokens: max length of response

    Returns:
        string — the model's response text
    """
    # Convert our simple format to what google-genai expects
    genai_messages = []
    for m in messages:
        # new library uses "user" and "model" as roles
        role = "user" if m["role"] == "user" else "model"
        genai_messages.append(
            types.Content(
                role=role,
                parts=[types.Part(text=m["content"])]
            )
        )

    # Build config — system prompt goes in here
    config = types.GenerateContentConfig(
        max_output_tokens=max_tokens,
        temperature=0.7,
        system_instruction=system if system else None
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=genai_messages,
        config=config
    )

    return response.text


def chat_stream(messages, system=None):
    """
    Streaming version — prints tokens as they arrive.
    Use this when you want ChatGPT-style live output.
    """
    genai_messages = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        genai_messages.append(
            types.Content(
                role=role,
                parts=[types.Part(text=m["content"])]
            )
        )

    config = types.GenerateContentConfig(
        temperature=0.7,
        system_instruction=system if system else None
    )

    full_text = ""
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=genai_messages,
        config=config
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_text += chunk.text
    print()  # newline at end

    return full_text


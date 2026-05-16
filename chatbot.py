import os
import json
from datetime import datetime
from llm import chat, chat_stream
from dotenv import load_dotenv

load_dotenv()


class ChatBot:
    """
    A complete CLI chatbot that remembers conversation history,
    saves sessions to disk, and supports streaming output.

    Everything in this class uses concepts from this week:
    - conversation history 
    - system prompts 
    - streaming 
    - session persistence (new)
    """

    def __init__(self, system_prompt: str, use_streaming: bool = True):
        self.system_prompt = system_prompt
        self.use_streaming = use_streaming
        self.history = []
        # timestamp used for unique session filenames
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.turn_count = 0

    def chat(self, user_message: str) -> str:
        """
        Send a message, get a reply, update history.
        Returns the assistant's response as a string.
        """
        # Add user message to history
        self.history.append({
            "role": "user",
            "content": user_message
        })

        # Auto-compress history if it gets too long
        # (using the summarisation concept from earlier)
        if len(self.history) > 20:
            self._compress_history()

        # Get response - streaming or regular
        if self.use_streaming:
            print("Bot: ", end="", flush=True)
            response = chat_stream(
                system=self.system_prompt,
                messages=self.history
            )
        else:
            response = chat(
                system=self.system_prompt,
                messages=self.history
            )
            print(f"Bot: {response}")

        # Add assistant reply to history
        self.history.append({
            "role": "assistant",
            "content": response
        })

        self.turn_count += 1
        return response

    def _compress_history(self):
        """
        When history gets long, summarise old turns.
        Keeps the last 4 messages fresh, summarises the rest.
        (summarisation concept, now as a class method)
        """
        if len(self.history) <= 4:
            return

        old = self.history[:-4]
        recent = self.history[-4:]

        conversation_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in old
        )

        summary = chat(
            system="Summarise this conversation in 3 bullet points. Be concise.",
            messages=[{
                "role": "user",
                "content": f"Summarise: {conversation_text}"
            }]
        )

        self.history = [
            {"role": "user", "content": f"[Earlier summary: {summary}]"},
            {"role": "assistant", "content": "Understood, I have context."}
        ] + recent

        print("\n[History compressed to save context]\n")

    def save_session(self):
        """
        Save the full conversation to a JSON file.
        Creates a sessions/ folder if it doesn't exist.
        """
        os.makedirs("sessions", exist_ok=True)
        filename = f"sessions/session_{self.session_id}.json"

        session_data = {
            "session_id": self.session_id,
            "system_prompt": self.system_prompt,
            "turn_count": self.turn_count,
            "history": self.history,
            "saved_at": datetime.now().isoformat()
        }

        with open(filename, "w") as f:
            json.dump(session_data, f, indent=2)

        print(f"\n[Session saved → {filename}]")
        return filename

    def show_stats(self):
        """Show current session statistics."""
        total_chars = sum(len(m["content"]) for m in self.history)
        estimated_tokens = total_chars // 4
        print(f"\n--- Session Stats ---")
        print(f"Turns          : {self.turn_count}")
        print(f"Messages stored: {len(self.history)}")
        print(f"Approx tokens  : ~{estimated_tokens}")
        print(f"Session ID     : {self.session_id}")
        print("---------------------\n")

    def show_history(self):
        """Print the raw conversation history."""
        print("\n--- Conversation History ---")
        for i, msg in enumerate(self.history):
            role = msg["role"].upper()
            content = msg["content"][:100]
            print(f"[{i}] {role}: {content}{'...' if len(msg['content']) > 100 else ''}")
        print("----------------------------\n")


def print_help():
    """Print available commands."""
    print("\nCommands:")
    print("  /save    - save session to disk")
    print("  /stats   - show token usage and turn count")
    print("  /history - show raw conversation history")
    print("  /clear   - start a fresh conversation")
    print("  /help    - show this menu")
    print("  /quit    - save and exit\n")
    print("  /model   - show which AI model is being used")



def main():
    """Main entry point — runs the chatbot loop."""

    print("=" * 50)
    print("   AI Tutor — Agentic AI Learning Assistant")
    print("=" * 50)
    print("Type /help to see commands\n")

    # The system prompt defines the chatbot's entire personality.
    # This is the senior engineer persona from Tuesday's experiments.
    SYSTEM_PROMPT = """You are an expert AI engineering tutor 
specialising in agentic AI systems. You are direct, technical, 
and give actionable answers. You teach by example — whenever 
possible you use concrete code snippets or real tools like 
LangChain, LangGraph, FastAPI, and ChromaDB. You don't hedge 
unnecessarily. You treat the student as a smart person who 
wants depth, not simplifications."""

    bot = ChatBot(system_prompt=SYSTEM_PROMPT, use_streaming=True)

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()

            # Skip empty input
            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "/quit":
                bot.save_session()
                print("Goodbye!")
                break
            elif user_input.lower() == "/save":
                bot.save_session()
            elif user_input.lower() == "/stats":
                bot.show_stats()
            elif user_input.lower() == "/history":
                bot.show_history()
            elif user_input.lower() == "/clear":
                bot.history = []
                bot.turn_count = 0
                print("[Conversation cleared — fresh start]\n")
            elif user_input.lower() == "/help":
                print_help()
            elif user_input.lower() == "/model":
                print(f"\n[Model: gemini-3.1-flash-lite | Session: {bot.session_id}]\n")    
            else:
                # Normal message — send to bot
                bot.chat(user_input)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nInterrupted — saving session...")
            bot.save_session()
            break
        except Exception as e:
            # Never let an error crash the whole chatbot
            print(f"\n[Error: {e}]")
            print("[Continuing — your history is safe]\n")


if __name__ == "__main__":
    main()



            


    

#!/usr/bin/env python3
"""
Manager Agent CLI — interactive REPL for the multi-agent system.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("Error: ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
    sys.exit(1)

from manager_agent import run_manager  # noqa: E402 — import after env check

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║              Manager Agent System                            ║
║  Orchestrates: FileAgent · CodeAgent · SearchAgent · DataAgent ║
╚══════════════════════════════════════════════════════════════╝
Type your instructions. The manager will coordinate sub-agents.
Commands: 'clear' — reset history | 'quit' / 'exit' — stop
"""

DIVIDER = "─" * 64


def main() -> None:
    print(BANNER)
    conversation_history: list = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            conversation_history.clear()
            print("[Conversation history cleared]\n")
            continue

        print()
        try:
            response = run_manager(user_input, conversation_history)
        except Exception as exc:
            print(f"[Error] {exc}")
            print("The manager encountered an error. You can continue or type 'clear' to reset.\n")
            continue

        print(f"\nManager:\n{response}\n")
        print(DIVIDER)


if __name__ == "__main__":
    main()

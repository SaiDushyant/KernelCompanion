from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
import os

from kernelsense.llm.gemini import GeminiClient
from kernelsense.parser.command_parser import parse_gemini_response, CommandParseError

HISTORY_FILE = os.path.expanduser("~/.kernelsense_history")


class KernelSenseShell:
    def __init__(self):
        self.session = PromptSession(history=FileHistory(HISTORY_FILE))
        self.gemini = GeminiClient()

    def run(self):
        print("KernelSense Shell started.")
        print("Type 'exit' or 'quit' to leave.\n")

        while True:
            try:
                user_input = self.session.prompt(
                    HTML("<ansigreen>KernelSense</ansigreen> > ")
                ).strip()

                if not user_input:
                    continue

                if user_input.lower() in ("exit", "quit"):
                    print("Exiting KernelSense.")
                    break

                self.handle_intent(user_input)

            except KeyboardInterrupt:
                print("\n(Interrupted — Ctrl+D or 'exit' to quit)")
            except EOFError:
                print("\nExiting KernelSense.")
                break

    def handle_intent(self, user_input: str):
        try:
            raw = self.gemini.generate_command(user_input)
            parsed = parse_gemini_response(raw)
            self.show_suggestions(parsed)
        except CommandParseError as e:
            print(f"⚠ Gemini error: {e}")
        except Exception as e:
            print(f"⚠ Unexpected error: {e}")

    def show_suggestions(self, data: dict):
        print("\nSuggested Commands:")
        print(f"1) {data['primary_command']}")

        for i, alt in enumerate(data["alternatives"], start=2):
            print(f"{i}) {alt}")

        print(f"\nRisk Level: {data['risk_level']}")
        print(f"Explanation: {data['explanation']}\n")


def start_shell():
    KernelSenseShell().run()

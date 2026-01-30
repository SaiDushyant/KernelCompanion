from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
import os

from kernelsense.llm.gemini import GeminiClient
from kernelsense.parser.command_parser import parse_gemini_response, CommandParseError

from kernelsense.safety.validator import validate_command
from kernelsense.explain.explainer import explain_command

from kernelsense.executor import execute_command
from kernelsense.config import load_config
from kernelsense.history import log_command

HISTORY_FILE = os.path.expanduser("~/.kernelsense_history")


class KernelSenseShell:
    def __init__(self):
        self.session = PromptSession(history=FileHistory(HISTORY_FILE))
        self.gemini = GeminiClient()
        self.config = load_config()

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
            self.choose_and_validate(parsed)

        except TimeoutError:
            print("⚠ Model is taking too long to respond. Please try again.")

        except CommandParseError as e:
            print(f"⚠ Unable to understand Model response: {e}")

        except Exception:
            print("⚠ Something went wrong while processing your request.")

    def choose_and_validate(self, data: dict):
        command = data["primary_command"]

        print(f"\nCommand : {command}")

        # 🔒 Safety validation
        result = validate_command(command)

        if result.status == "block":
            print("\n🚫 This command is blocked and cannot be executed.")
            print(f"Reason: {result.reason}")
            return

        # 📖 Explain?
        if self.config["auto_explain"]:
            print("\nCommand Explanation:")
            print(explain_command(command))
        else:
            explain = input("Explain this command? (y/n): ").strip().lower()
            if explain == "y":
                print("\nCommand Explanation:")
                print(explain_command(command))

        # ▶ Confirm execution
        confirm = input("\nRun this command? (y/n): ").strip().lower()
        if confirm != "y":
            print("Command execution cancelled.")
            return

        # ▶ Execute
        print("Output :")
        execute_command(command)
        log_command(data["intent"], command)


def start_shell():
    KernelSenseShell().run()

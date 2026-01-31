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

from kernelsense.input_classifier import is_shell_command


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
            # Power-user flags
            auto_explain = "--explain" in user_input
            auto_run = "--run" in user_input

            # Remove flags before sending to model
            clean_input = (
                user_input.replace("--explain", "").replace("--run", "").strip()
            )

            # 🔀 DECISION POINT
            if is_shell_command(clean_input):
                # Direct shell command → skip LLM
                self.run_direct_command(
                    clean_input, auto_explain=auto_explain, auto_run=auto_run
                )
            else:
                # Natural language → use LLM
                raw = self.gemini.generate_command(clean_input)
                parsed = parse_gemini_response(raw)
                self.choose_and_validate(
                    parsed, auto_explain=auto_explain, auto_run=auto_run
                )

        except TimeoutError:
            print("⚠ Gemini is taking too long to respond. Please try again.")
        except CommandParseError as e:
            print(f"⚠ Unable to understand response: {e}")
        except Exception:
            print("⚠ Something went wrong while processing your request.")

    def run_direct_command(self, command: str, auto_explain=False, auto_run=False):

        print(f"Command : {command}")

        result = validate_command(command)

        if result.status == "block":
            print("🚫 This command is blocked and cannot be executed.")
            print(f"Reason : {result.reason}")

            return

        # Explanation
        if auto_explain:

            print("Explanation :")
            print(explain_command(command))

        else:
            explain = input("Explain this command? (y/n): ").strip().lower()
            if explain == "y":

                print("Explanation :")
                print(explain_command(command))

            elif explain != "n":
                print("Operation cancelled by user.")

                return

        # Execution
        if auto_run:
            confirm = "y"
        else:
            confirm = input("Run this command? (y/n): ").strip().lower()

        if confirm != "y":
            print("Operation cancelled by user.")

            return

        print("Output :")
        execute_command(command)

    def choose_and_validate(self, data: dict, auto_explain=False, auto_run=False):
        command = data["primary_command"]

        print(f"Command : {command}")

        # 🔒 Safety validation
        result = validate_command(command)

        if result.status == "block":
            print("🚫 This command is blocked and cannot be executed.")
            print(f"Reason : {result.reason}")

            return

        # 📖 Explain
        if auto_explain:

            print("Explanation :")
            print(explain_command(command))

        else:
            explain = input("Explain this command? (y/n): ").strip().lower()
            if explain == "y":

                print("Explanation :")
                print(explain_command(command))

            elif explain != "n":
                print("Operation cancelled by user.")

                return

        # ▶ Run
        if auto_run:
            confirm = "y"
        else:
            confirm = input("Run this command? (y/n): ").strip().lower()

        if confirm != "y":
            print("Operation cancelled by user.")

            return

        print("Output :")
        execute_command(command)
        log_command(data["intent"], command)


def start_shell():
    KernelSenseShell().run()

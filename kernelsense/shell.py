from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
import os

HISTORY_FILE = os.path.expanduser("~/.kernelsense_history")


class KernelSenseShell:
    def __init__(self):
        self.session = PromptSession(history=FileHistory(HISTORY_FILE))

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

                # Phase 1 behavior: echo input
                print(f"You typed: {user_input}")

            except KeyboardInterrupt:
                # Ctrl+C → don’t exit shell
                print("\n(Interrupted — press Ctrl+D or type 'exit' to quit)")
            except EOFError:
                # Ctrl+D → exit shell
                print("\nExiting KernelSense.")
                break


def start_shell():
    shell = KernelSenseShell()
    shell.run()

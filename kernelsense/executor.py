import subprocess
import sys


class CommandExecutionError(Exception):
    pass


# Commands that require live terminal interaction
INTERACTIVE_COMMANDS = {"top", "htop", "watch", "tail", "ping", "less", "more"}


def is_interactive_command(command: str) -> bool:
    """
    Detects whether a command needs live terminal output.
    """
    base = command.strip().split()[0]
    return base in INTERACTIVE_COMMANDS


def execute_static(command: str):
    """
    Executes a command and prints output after completion.
    """
    completed = subprocess.run(command, shell=True, text=True, capture_output=True)

    if completed.stdout:
        print(completed.stdout)

    if completed.stderr:
        print(completed.stderr)


def execute_interactive(command: str):
    """
    Executes a command with live terminal I/O.
    """
    print("⚠ Interactive command running. Press Ctrl+C or 'q' to exit.\n")

    try:
        subprocess.run(
            command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
    except KeyboardInterrupt:
        print("\nInteractive command stopped.")


def execute_command(command: str):
    """
    Automatically chooses static or interactive execution.
    """
    try:
        if is_interactive_command(command):
            execute_interactive(command)
        else:
            execute_static(command)
    except Exception as e:
        raise CommandExecutionError(str(e))

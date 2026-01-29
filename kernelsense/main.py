# kernelsense/main.py

import sys
from kernelsense.shell import start_shell


def main():
    if len(sys.argv) < 2:
        print("Usage: kernelsense start")
        return

    command = sys.argv[1]

    if command == "start":
        start_shell()
    else:
        print(f"Unknown command: {command}")

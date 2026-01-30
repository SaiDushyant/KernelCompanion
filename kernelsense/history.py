import json
import os
from datetime import datetime

HISTORY_PATH = os.path.expanduser("~/.kernelsense_usage.json")


def log_command(intent: str, command: str):
    entry = {
        "time": datetime.utcnow().isoformat(),
        "intent": intent,
        "command": command,
    }

    history = []

    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f)

    history.append(entry)

    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)

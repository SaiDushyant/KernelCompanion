import json
import os

CONFIG_PATH = os.path.expanduser("~/.kernelsense_config.json")

DEFAULT_CONFIG = {
    "auto_explain": False,
    "auto_confirm": False,
    "show_alternatives": False,
}


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

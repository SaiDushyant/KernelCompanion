# kernelsense/parser/command_parser.py

import json

REQUIRED_KEYS = {
    "intent",
    "primary_command",
    "alternatives",
    "risk_level",
    "explanation",
}


class CommandParseError(Exception):
    pass


def parse_gemini_response(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise CommandParseError("Gemini response is not valid JSON")

    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise CommandParseError(f"Missing keys: {missing}")

    if not isinstance(data["alternatives"], list):
        raise CommandParseError("alternatives must be a list")

    return data

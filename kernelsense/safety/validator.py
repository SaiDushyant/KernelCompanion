import shlex
from dataclasses import dataclass

# 🔴 NEVER ALLOWED (HARD BLOCK)
HARD_BLOCK_PATTERNS = [
    "rm -rf /",
    "mkfs",
    "dd if=",
    ":(){ :|:& };:",
]

# 🟡 REQUIRES CONFIRMATION
SOFT_CONFIRM_COMMANDS = ["rm", "chmod", "chown", "kill", "sudo"]


@dataclass
class SafetyResult:
    status: str  # block | confirm | allow
    reason: str
    danger_level: str


def tokenize(command: str) -> list[str]:
    return shlex.split(command)


def is_hard_block(command: str) -> bool:
    for pattern in HARD_BLOCK_PATTERNS:
        if pattern in command:
            return True
    return False


def is_soft_confirm(tokens: list[str]) -> bool:
    return tokens and tokens[0] in SOFT_CONFIRM_COMMANDS


def validate_command(command: str) -> SafetyResult:
    tokens = tokenize(command)

    if is_hard_block(command):
        return SafetyResult(
            status="block",
            reason="Command matches a hard-blocked dangerous pattern",
            danger_level="high",
        )

    if is_soft_confirm(tokens):
        return SafetyResult(
            status="confirm",
            reason="Command may modify or delete system resources",
            danger_level="medium",
        )

    return SafetyResult(
        status="allow", reason="Command considered safe", danger_level="low"
    )

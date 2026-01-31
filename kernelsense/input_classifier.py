import shlex

KNOWN_COMMANDS = {
    "ls",
    "cd",
    "rm",
    "cp",
    "mv",
    "ps",
    "top",
    "cat",
    "grep",
    "find",
    "du",
    "df",
    "chmod",
    "chown",
    "kill",
    "ping",
    "curl",
    "wget",
    "docker",
    "git",
    "npm",
}

SHELL_OPERATORS = {"|", "&&", "||", ">", ">>", "<", ";"}


def is_shell_command(user_input: str) -> bool:
    user_input = user_input.strip()
    if not user_input:
        return False

    # Tokenize safely
    try:
        tokens = shlex.split(user_input)
    except ValueError:
        return False

    if not tokens:
        return False

    first = tokens[0]

    # Rule 1: starts with known command
    if first in KNOWN_COMMANDS:
        return True

    # Rule 2: shell operators
    for op in SHELL_OPERATORS:
        if op in user_input:
            return True

    # Rule 3: path execution
    if first.startswith(("./", "/", "~")):
        return True

    return False

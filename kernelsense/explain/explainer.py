import shlex

COMMAND_EXPLANATIONS = {
    "ps": "Report a snapshot of current processes",
    "top": "Display real-time process information",
    "head": "Output the first part of files",
    "ls": "List directory contents",
    "rm": "Remove files or directories",
    "du": "Estimate file space usage",
    "find": "Search for files in a directory hierarchy",
}

FLAG_EXPLANATIONS = {
    "-l": "Long listing format",
    "-h": "Human-readable output",
    "-a": "Include all entries",
    "-r": "Recursive operation",
    "-f": "Force operation",
    "-n": "Limit number of output lines",
}

SPECIAL_TOKENS = {
    "|": "Pipe output of one command to another",
}


def explain_command(command: str) -> str:
    # Split pipeline first
    pipeline_parts = [part.strip() for part in command.split("|")]
    explanation_lines = []

    for idx, part in enumerate(pipeline_parts, start=1):
        tokens = shlex.split(part)

        if not tokens:
            continue

        base_cmd = tokens[0]
        explanation_lines.append(f"\nCommand {idx}: {base_cmd}")
        explanation_lines.append(
            f"  {base_cmd} : {COMMAND_EXPLANATIONS.get(base_cmd, 'Unknown command')}"
        )

        for token in tokens[1:]:
            if token in SPECIAL_TOKENS:
                explanation_lines.append(f"  {token} : {SPECIAL_TOKENS[token]}")

            elif token.startswith("--"):
                explanation_lines.append(
                    f"  {token} : Long option modifying command behavior"
                )

            elif token.startswith("-"):
                explanation_lines.append(f"  {token} : Option flag")

            else:
                explanation_lines.append(f"  {token} : Argument")

    return "\n".join(explanation_lines)

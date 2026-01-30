import subprocess


class CommandExecutionError(Exception):
    pass


def execute_command(command: str):
    """
    Executes a shell command safely and streams output.
    """
    try:
        completed = subprocess.run(
            command,
            shell=True,  # needed for pipes like |
            text=True,
            capture_output=True,
        )

        if completed.stdout:
            print(completed.stdout)

        if completed.stderr:
            print(completed.stderr)

    except Exception as e:
        raise CommandExecutionError(str(e))

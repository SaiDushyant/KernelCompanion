import platform


def detect_os() -> str:
    system = platform.system().lower()

    if "linux" in system:
        return "Linux"
    if "darwin" in system:
        return "macOS"
    if "windows" in system:
        return "Windows"

    return "Unknown"

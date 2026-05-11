import re


# Minimal ANSI color codes (no external deps)
class _Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


C = _Color


def highlight_symbol(text: str) -> str:
    """
    Color the intercepted function name.
    Incoming (event handler) in blue, outgoing in green.
    """
    if "call_event_handler" in text or "incoming" in text.lower():
        return f"{C.BOLD}{C.BLUE}{text}{C.RESET}"
    return f"{C.BOLD}{C.GREEN}{text}{C.RESET}"


def highlight_timestamp(text: str) -> str:
    return f"{C.DIM}{text}{C.RESET}"


def highlight_connection(text: str) -> str:
    """
    Highlight connection description. Focus on the service name and pid.
    """
    # Highlight service name (single-quoted or unquoted)
    text = re.sub(
        r"(name\s*=\s*')([^']+)(')",
        rf"\1{C.CYAN}{C.BOLD}\2{C.RESET}\3",
        text,
    )
    text = re.sub(
        r"(name\s*=\s*)([^'\s,}]+)",
        rf"\1{C.CYAN}{C.BOLD}\2{C.RESET}",
        text,
    )
    # Highlight hex addresses
    text = re.sub(
        r"(\b0x[0-9a-fA-F]+\b)",
        rf"{C.YELLOW}\1{C.RESET}",
        text,
    )
    return text


def highlight_message(text: str) -> str:
    """
    Minimal highlighting for the XPC message description string.
    """
    # Object type tags: <OS_xpc_dictionary>, <OS_xpc_string>, etc.
    text = re.sub(
        r"(<(OS_xpc_)[a-z_]+>)",
        rf"{C.YELLOW}\1{C.RESET}",
        text,
    )

    # Quoted strings
    text = re.sub(
        r'("[^"]*")',
        rf"{C.GREEN}\1{C.RESET}",
        text,
    )

    # Dictionary keys:  key = value  (key before =)
    text = re.sub(
        r"^(\s+)([a-zA-Z0-9_\-:/\.]+)(\s*=)",
        rf"\1{C.CYAN}\2{C.RESET}\3",
        text,
        flags=re.MULTILINE,
    )

    # Hex byte dumps (e.g. from <data> contents)
    text = re.sub(
        r"(\b[0-9a-fA-F]{2}\b)",
        rf"{C.MAGENTA}\1{C.RESET}",
        text,
    )

    # Numbers (integers / floats, simple)
    text = re.sub(
        r"(\b\d+\.?\d*\b)",
        rf"{C.MAGENTA}\1{C.RESET}",
        text,
    )

    # Parsed bplist annotations
    text = re.sub(
        r"(Parsed\s+bplist\d+\s+data\s+for\s+key)",
        rf"{C.BOLD}{C.CYAN}\1{C.RESET}",
        text,
    )

    return text


def highlight_divider(text: str) -> str:
    return f"{C.DIM}{text}{C.RESET}"

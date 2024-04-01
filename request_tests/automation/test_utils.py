import re


def colorize(text: str, color_code: str):
    return f"\033[{color_code}m{text}\033[0m"


def normalize_string(s: str) -> str:
    """Convert sequences of whitespace to a single space and trim the string."""
    return re.sub(r'\s+', ' ', s).strip()


def less_strict_comparison(str1: str, str2: str) -> bool:
    normalized_str1 = normalize_string(str1)
    normalized_str2 = normalize_string(str2)
    return normalized_str1 == normalized_str2

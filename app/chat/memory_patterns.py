# memory_patterns.py
import re

REMEMBER_PATTERNS = [
    r"(?i)remember that (.+)",
    r"(?i)don't forget that (.+)",
    r"(?i)don't forget (.+)",
    r"(?i)ayudame a recordar (.+)",
    r"(?i)ayudame a recordar que (.+)",
    r"(?i)no olvides que (.+)",
    r"(?i)!recuerda  (.+)"
]

def check_remember_patterns(message):
    for pattern in REMEMBER_PATTERNS:
        match = re.search(pattern, message)
        if match:
            memory_content = match.group(1)
            return memory_content
    return None

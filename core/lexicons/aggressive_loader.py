import re

def load_aggressive_words(path: str) -> set:
    words = set()

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if not line:
                continue

            tokens = re.findall(r"\b\w+\b", line)

            words.update(tokens)
    return words
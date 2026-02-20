import re
import os
from core.lexicons.aggressive_loader import load_aggressive_words

# def load_word_list(path):
#     if not os.path.exists(path):
#         return set()
    
#     with open(path, "r", encoding="utf-8") as f:
#         return set(
#             line.strip().lower()
#             for line in f
#             if line.strip()
#         )

# AGGRESSIVE_WORDS = load_aggressive_words(
#       "core/lexicons/aggressive_words.txt"
#   )
# #     "corrupt", "shameful", "disgrace", "failed", "exposed", "liar", "fraud", "scandal", "murder", "rape", "killed", "hijacked", "hacked"
# # ]


LEXICON_PATH = os.path.join(
    os.path.dirname(__file__),
    "lexicons",
    "aggressive_words.txt"
)

AGGRESSIVE_WORDS = load_aggressive_words(LEXICON_PATH)

print("Aggressive vocab size:", len(AGGRESSIVE_WORDS))
print("guilty in lexicon:", "guilty" in AGGRESSIVE_WORDS)
print("LEXICON PATH:", LEXICON_PATH)


ABSOLUTE_WORDS = [
    "always", "never", "completely", "entirely", "totally"
]

ATTRIBUTION_WORDS = [
    "according to", "reported by", "stated by", "said", "claimed", "alleged"
]

WORD_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)

def check_aggression(text : str):
    if not isinstance(text, str):
        return 0, []
    
    text_lower = text.lower()
    tokens = WORD_PATTERN.findall(text_lower)

    found_unique = sorted(set(w for w in tokens if w in AGGRESSIVE_WORDS))

    return len(found_unique), found_unique
print("guilty in lexicon:", "guilty" in AGGRESSIVE_WORDS)
print("Aggressive vocab size:", len(AGGRESSIVE_WORDS))




    # score = 0


    # found = []

    # text_lower = text.lower()


    # for word in AGGRESSIVE_WORDS:
    #     if word in text_lower:
    #         score += 1
    #         found.append(word)
    # return score, found

def check_absolutes(text : str):
    score = 0

    found = []

    text_lower = text.lower()

    for word in ABSOLUTE_WORDS:
        if word in text_lower:
            score += 1
            found.append(word)

    return score, found

def check_attribution(text : str, source_provided: bool):
    """
    This checks attributions and if not found, it must increase the risk score.

    """

    text_lower = text.lower()

    if source_provided:
        return 0, []
    
    for phrase in ATTRIBUTION_WORDS:
        if phrase in text_lower:
            return 0, []
        
    return 1, ["Missing Attribution"]

def check_length(text : str, max_length : int):
    if not isinstance(text, str):
        return 0, []
    if len(text) > max_length:
        return 1, ["Text Length has been exceeded"]
    return 0, []


def evaluate_risk(text : str, max_length : int, source_provided : bool):
    total_score = 0

    flags = []

    aggression_score, aggression_words = check_aggression(text)
    total_score += aggression_score

    flags.extend(aggression_words)

    absolute_score, absolute_words = check_absolutes(text)
    total_score += absolute_score

    flags.extend(absolute_words)

    attribution_score, attribution_flags = check_attribution(text, source_provided)
    total_score += attribution_score

    flags.extend(attribution_flags)

    length_score, length_flags = check_length(text, max_length)
    total_score += length_score
    flags.extend(length_flags)

    ## The following parameters can be adjusted according to business needs/Risk Mapping

    if total_score == 0:
        risk_level = "low"

    elif total_score <= 2:
        risk_level = "medium"
    elif total_score <= 5:
        risk_level = "High"
    else:
        risk_level = "Very High"

    return {
        "risk_score" : total_score,
        "risk_level" : risk_level,
        "flags" : flags
    }
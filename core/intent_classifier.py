"""

This is a length controller function, call it wherever required.
Last modified : 02/10/2026

"""
from core.platform_rules import PLATFORM_RULES

def length_control(max_length : int, length_pref : str) -> int:
    if length_pref == "short":
        return int(max_length * 0.5)
    elif length_pref == "medium":
        return int(max_length * 0.7)
    elif length_pref == "long":
        return int(max_length * 0.9)
    else:
        return int(max_length * 0.7)


"""

This is a intent_classifier function, call it wherever required.
Last modified : 02/10/2026

"""
def intent_classify(headline: str, content_type: str) -> str:
    headline_lower = headline.lower()

    if content_type == "announcement":
        return "annuncement"
    elif content_type == "opinion":
        return "political_opinion"
    elif content_type == "news":
        political_keywords = [
            "government", "minister", "chief minister", "parliament", "assembly", "political party",
            "opposition party", "bjp", "congress", "BRS", "party leaders", "elections"
        ]

        for word in political_keywords:
            if word in headline_lower:
                return "political_news"
        return "news"
    else:
        return "general"
    
def custom_platform_content(platforms: list, length_pref: str):
        """
       This function is responsible for custom platform generation.
        """
        plan = {}

        for platform in platforms:
            rules = PLATFORM_RULES.get(platform)

            if not rules:
                continue

            target_length = length_control(
                rules["max_length"], length_pref
            )


            plan[platform] = {
                "max_length" : rules["max_length"],
                "target_length" : target_length,
                "tone_bias": rules["tone_bias"],
                "hashtags_range" : rules["hashtags"]
            }

        return plan
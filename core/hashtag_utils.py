import re


def extract_hashtags(text:str):
    return re.findall(r"#\w+", text)

## Function to ensure Ensure hashtags are getting generated.

def ensure_hashtag_compliance(text: str, platform_plan: dict, language: str, geo_location=None):
    hashtags = extract_hashtags(text)
    min_tags, max_tags = platform_plan["hashtags_range"]

    required_min = max(2, min_tags)


    if geo_location:
        location_tag = f"#{geo_location.replace(' ', '')}"
        if location_tag not in hashtags:
            hashtags.append(location_tag)
            text = text.strip() + " " + location_tag

    if len(hashtags) >= required_min:
        return text
    

    fallback_map = {
        "en": ["#BreakingNews", "#LatestUpdate", "#OnsiteNews"],
        "hi": ["#ताज़ाखबर", "#समाचार", "#ऑनसाइटन्यूज़"],
        "te": ["#తాజావార్త", "#బ్రేకింగ్‌న్యూస్", "#ఆన్సైట్‌న్యూస్"],
    }
    needed = required_min - len(hashtags)
    candidates = fallback_map.get(language, fallback_map["en"]).copy()
    candidates = [c for c in candidates if c not in hashtags]


    to_add = candidates[:needed]


    if to_add:
        text = text.strip() + "\n" + " ".join(to_add)
    return text

    # return text.strip() + "\n" + " ". join(to_add)
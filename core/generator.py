import requests

from core.platform_rules import PLATFORM_RULES
from core.language import get_language_name


def build_prompt(headline, intent, platform, platform_plan,language = "en", context= None, source = None, geo_location=None):
    ## Buiding a structured prompt
    target_length = platform_plan["target_length"]
    tone_bias = platform_plan["tone_bias"]
    hashtag_min, hashtag_max = platform_plan["hashtags_range"]

    prompt = f"""
    You are a professional media content writer.
    
    Generate a social media post with the following constraints:

    Headline : {headline}
    Intent : {intent}
    Platform : {platform}
    Tone : {tone_bias}
    Target length : approx {target_length} characters
    Target Language : {get_language_name(language)}
    Hashtags: between {hashtag_min} and {hashtag_max}
    Additional context : {context if context else "None"}
    source (if any) : {source if source else "None"}
    Location: {geo_location if geo_location else "Not specified"}

    Rules: 1. Never Fabricate the facts,
        2. If source is provided, include attribution.
        3. Strictly follow {PLATFORM_RULES}
        4.Maintain as instructed
        5.Maintain only final output text.
        6. Do not lie
        7. The entire output MUST be written in {get_language_name(language)}.
        8. If the output is not in {language}, regenerate internally before returning.
        9. Do not use English sentences.
        10. Use proper {language} script.

    Generate now:
    
    """
    return prompt
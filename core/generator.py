import requests

from core.platform_rules import PLATFORM_RULES

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

def build_prompt(headline, intent, platform, platform_plan, context= None, source = None):
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
    Hashtags: between {hashtag_min} and {hashtag_max}
    Additional context : {context if context else "None"}
    source (if any) : {source if source else "None"}

    Rules: 1. Never Fabricate the facts,
        2. If source is provided, include attribution.
        3. Strictly follow {PLATFORM_RULES}
        4.Maintain as instructed
        5.Maintain only final output text.
        6. Do not lie

    Generate now:
    
    """
    return prompt


def generate_post(headline, intent, platform, platform_plan, context = None, source = None):
    prompt = build_prompt(

        headline, intent, platform, platform_plan, context, source

    )
    response = requests.post (

        OLLAMA_URL,

        json={
            "model" : MODEL_NAME,
            "prompt" : prompt,
            "stream" : False
        }
    )

    if response.status_code != 200:
        return "LLM Generation Failed."



    return response.json()["response"].strip()        
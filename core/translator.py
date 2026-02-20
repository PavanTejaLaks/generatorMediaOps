import requests
from core.language import get_language_name
import os
from dotenv import load_dotenv
##OLLAMA_URL = "http://localhost:11434/api/generate"
##MODEL_NAME = "Mistral"

# def translate_to_english(text : str, source_lang : str):
#     """
#    Translating the supported language to English for judging.
#     """
#     if source_lang == "en":
#         return text
    
#     source_language_name = get_language_name(source_lang)

#     prompt = f"""
# Translate the following {source_language_name} text to English, preserve meaning accurately and DO NOT ADD NEW INFORMATION. 

# Text: {text}

# Translation:
# """
#     response = requests.post(
#         OLLAMA_URL,
#         json={
#             "model" : MODEL_NAME,
#             "prompt" : prompt,
#             "stream" : False
#         }
#     )

#     if response.status_code != 200:
#         return text
    
#     return response.json()["response"].strip()

load_dotenv()

SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"
SARVAM_KEY = os.getenv("SARVAM_API_KEY")


def translate_to_english(text:str, source_lang:str) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    if source_lang == "en":
        return text
    
    source_language_name = get_language_name(source_lang)

    prompt = f"""

Translate the following {source_language_name} text to English.

Rules:
1. Preserve Exact meaning
2. Do not add information
3. Keep tone according to the content.
4.Return ONLY the English Translation.

Text: 

{text}
"""
    try:
        response = requests.post(
            SARVAM_URL,
            headers={
                "Authorization" : f"Bearer {SARVAM_KEY}",
                "Content-Type" : "application/json",
            },
            json = {
                "model" : "sarvam-m",
                "messages" : [{"role": "user", "content": prompt}],
                "temperature" : 0.0,
            },

            timeout=15,
        )

        if response.status_code != 200:
            print("Sarvam translation error: ", response.status_code, response.text[:200])
            return text
        
        data = response.json()

        return data["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        print("Sarvam translation failed:", e)
        return text

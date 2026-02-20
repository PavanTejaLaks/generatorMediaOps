import os
import requests
from dotenv import load_dotenv
from core.generator import build_prompt

## Load dotenv()

load_dotenv()

SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"
SARVAM_KEY = os.getenv("SARVAM_API_KEY")

##Function to generate content in Telugu/Hindi using Sarvam AI

def generate_with_sarvam(**kwargs):
    prompt = build_prompt(**kwargs)

    headers = {

        "Authorization" : f"Bearer {SARVAM_KEY}",
        "Content-Type" : "application/json",
    }

    payload = {
        "model" : "sarvam-m",
        "messages" : [
            {"role": "user", "content" : prompt}
        ],
        "temperature" : 0.6,
    }

    response = requests.post(SARVAM_URL, headers=headers, json=payload, timeout=14)

    if response.status_code != 200:
        return "Sarvam generation failed."
    
    data = response.json()

    return data["choices"][0]["message"]["content"].strip()
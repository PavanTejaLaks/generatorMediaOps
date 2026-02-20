## Modified on 17/02/2026 by Pavan Tejavath


import os
from openai import OpenAI
from core.generator import build_prompt
from dotenv import load_dotenv

## Loading the environment varaibles
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

## Function to generate using LLM- In this case via GPT-4o-mini

def generate_with_openai(**kwargs):
    try:

        prompt = build_prompt(**kwargs)

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {"role" : "system", "content": "You are a professional media content writer."},
                {"role" : "user", "content" : prompt},
            ],
            temperature=0.6, ## Never go beyond 0.8 for this use case.
            timeout=12,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI generation failed: {str(e)[:120]}"
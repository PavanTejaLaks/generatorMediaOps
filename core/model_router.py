from core.language import validate_language
from core.providers.openai_provider import generate_with_openai
from core.providers.sarvam_provider import generate_with_sarvam

## Function to use Sarvam to generate content in Telugu and Hndi or any other langauges in future.

def select_generation_provider(language: str) -> str:
    lang = validate_language(language)

    if lang == "en":
        return "openai"
    
    if lang in ("hi", "te"):
        return "sarvam"
    

    return "openai"


def generate_via_router(**kwargs):
    language = kwargs.get("language", "en")
    provider = select_generation_provider(language)


    if provider == "sarvam":
        return generate_with_sarvam(**kwargs)
    
    return generate_with_openai(**kwargs)
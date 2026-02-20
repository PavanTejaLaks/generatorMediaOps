SUPPORTED_LANGUAGES = {
    "en" : "English",
    "te" : "Telugu",
    "hi" : "Hindi"
}

def validate_language(lang_code: str) -> str:
    """
   Language must be supported else English will be default.
    """
    if lang_code in SUPPORTED_LANGUAGES:
        return lang_code
    return "en"



def get_language_name(lang_code : str) -> str:
    return SUPPORTED_LANGUAGES.get(lang_code, "English")
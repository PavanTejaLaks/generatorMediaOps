from core.intent_classifier import intent_classify, custom_platform_content
##from core.generator import generate_post
from core.model_router import generate_via_router
from core.judge import evaluate_risk
from core.translator import translate_to_english
from core.language import validate_language
from core.hashtag_utils import ensure_hashtag_compliance
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_platform(platform, headline, intent, plan, language):
    post = generate_via_router(
        headline = headline,
        intent = intent,
        platform = platform,
        platform_plan = plan[platform],
        context = "None",
        source = "Onsite News",
        language = language
    )
    post = ensure_hashtag_compliance(post, plan[platform], language)
    if language == "en":
            english_version = post
    else:
            english_version = translate_to_english(post, language)

    risk = evaluate_risk(
            text = english_version,
            max_length = plan[platform]["max_length"],
            source_provided = True

    )

    return platform, post, risk

if  __name__ == "__main__":
    headline = "A local MLA found guilt for corruption in Hyderabad"
    content_type = "news"
    platforms = ["X", "Instagram", "Facebook"]
    length = "medium"

    intent = intent_classify(headline, content_type)
    plan = custom_platform_content(platforms, length)
    language = validate_language("en")
    start = time.time()

    with ThreadPoolExecutor(max_workers=len(platforms)) as executor:
          futures = [
                executor.submit(
                      process_platform,
                      platform,
                      headline,
                      intent,
                      plan,
                      language,
                )
                for platform in platforms
          ]

          for future in as_completed(futures):
                platform, post, risk = future.result()

                print("Risk Evaluation", risk)
                print("\n Here is the generated post for", platform)
                print(post)
    print("\nTotal latency: ", time.time() - start)

    

    

        # print("\n--- DEBUG TRANSLATION ---")
        # print("Original:", post[:120])
        # print("English :", english_version[:120])
        # print("--------------------------\n")

    # print("Risk Evaluation", risk)

    # print("\n Here is the generated post for", platform)
    # print(post)

    
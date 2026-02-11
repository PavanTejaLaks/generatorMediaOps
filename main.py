from core.intent_classifier import intent_classify, custom_platform_content
from core.generator import generate_post


if  __name__ == "__main__":
    headline = "Major flight accident occured in Mumbai"
    content_type = "news"
    platforms = ["X", "Instagram", "Facebook"]
    length = "short"

    intent = intent_classify(headline, content_type)
    plan = custom_platform_content(platforms, length)

    for platform in platforms:
        post = generate_post(
            headline = headline,
            intent = intent,
            platform = platform,
            platform_plan=plan[platform],
            context = "None",
            source = "Onsite news"

        )

        print("\n Here is the generated post for", platform)


        print(post)
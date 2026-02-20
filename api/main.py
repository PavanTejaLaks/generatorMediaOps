from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import time
import os
from core.intent_classifier import intent_classify, custom_platform_content
from core.model_router import generate_via_router
from core.judge import evaluate_risk
from core.translator import translate_to_english
from core.language import validate_language
from core.hashtag_utils import ensure_hashtag_compliance
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import logging
import uuid
from core.security.rate_limiter import check_rate_limit


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("mediaops")

load_dotenv()

API_KEY = os.getenv("MEDIAOPS_API_KEY", "dev-key")
app = FastAPI(title="MediaOps AI Service")

# logger.info(
#     f"Request started | id={request_id} | platforms={req.platforms} | lang={req.language}"
# )

ALLOWED_PLATFORMS = {"X", "Instagram", "Facebook", "Linkedin"}
ALLOWED_LENGTHS = {"short", "medium", "long"}
ALLOWED_LANGUAGES = {"en", "hi", "te"}

class GenerateRequest(BaseModel):
    headline : str = Field(..., min_length = 5, max_length= 500)
    content_type: str
    platforms : List[str]
    length: str = "medium"
    language: str = "te"
    context: Optional[str] = None
    source: Optional[str] = None
    geo_location: Optional[str] = Field(default=None, max_length=100)

    @field_validator("platforms")
    @classmethod
    def validate_platforms(cls, v):
        invalid = [p for p in v if p not in ALLOWED_PLATFORMS]
        if invalid:
            raise ValueError(f"Unsupported platforms: {invalid}")
        return v
    @field_validator("length")
    @classmethod
    def validate_length(cls, v):
        if v not in ALLOWED_LENGTHS:
            raise ValueError(f"Unsupported language: {v}")
        return v
    @field_validator("language")
    @classmethod
    def validate_language_field(cls, v):
        if v not in ALLOWED_LANGUAGES:
            raise ValueError(f"Unsupported Language: {v}")
        return v
    
class PlatformResult(BaseModel):
    platform: str
    post: Optional[str]
    risk: Optional[dict]
    status: str = "success"
    error: Optional[str] = None

class GenerateResponse(BaseModel):
    request_id = str
    results: List[PlatformResult]
    latency: float

# class GenerateRequest(BaseModel):
#     headline: str
#     content_type: str
#     platforms: List[str]                           //Old version and maybe useful in future.
#     length: str = "medium"
#     language: str = "en"
#     context: Optional[str] = None
#     source: Optional[str] = None

def process_platform(platform, headline, intent, plan, language, context, source, geo_location = None, request_id = None ):
    logger.info(f"[{request_id}] Generating for platform={platform}")
    try:
        post = generate_via_router(
            headline = headline,
            intent= intent,
            platform=platform,
            platform_plan = plan[platform],
            context = context,
            source = source,
            language = language,
            geo_location=geo_location,
        )


        post = ensure_hashtag_compliance(post, plan[platform], language)

        if language == "en":
            english_version = post
        else:
            english_version = translate_to_english(post, language)

        risk = evaluate_risk(
            text = english_version,
            max_length=plan[platform]["max_length"],
            source_provided=bool(source),
        )

        return {
            "platform": platform,
            "post": post,
            "risk": risk,
            "status": "success",
            "error": None,
        }
    
    except Exception as e:
        logger.error(f"[{request_id}]  Generation failed for platform={platform} | error={e}")
        return {
            "platform": platform,
            "post": None,
            "risk": None,
            "status": "failed",
            "error": str(e)[:200],

    }
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mediaops-ai",
        "timestamp": time.time(),
    }

@app.post("/generate", response_model=GenerateResponse)

def generate_content(
    req: GenerateRequest,
    x_api_key: str = Header(default=None)
):
    
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
# def generate_content(req: GenerateRequest):
    
    check_rate_limit(x_api_key)

    request_id = str(uuid.uuid4())

    start = time.time()

    logger.info(
        f"Generate request id ={request_id}| platforms={req.platforms} | lang = {req.language}"
    )

    language = validate_language(req.language)

    intent = intent_classify(req.headline, req.content_type)
    plan = custom_platform_content(req.platforms, req.length)

    results = []

    with ThreadPoolExecutor(max_workers=len(req.platforms)) as executor:
        futures = [
            executor.submit(
                process_platform,
                platform,
                req.headline,
                intent,
                plan,
                language,
                req.context,
                req.source,
                req.geo_location,
                request_id,
            )

            for platform in req.platforms
        ]

        for future in as_completed(futures, timeout = 25):
            try:
                results.append(future.result(timeout=15))
            except Exception as e:
                results.append ({
                    "platform": "unknown",
                    "post": None,
                    "risk" : None,
                    "status": "timeout",
                    "error": str(e)[:200],
                })
    
            # results.append(future.result())

    # for platform in req.platforms:
    #     result = process_platform(
    #         platform = platform,
    #         headline = req.headline,
    #         intent=intent,
    #         plan = plan,
    #         language = language,
    #         context=req.context,
    #         source=req.source,
    #     )

    #     results.append(result)

    latency = time.time() - start

    logger.info(f"Request completed | {request_id} | latency={latency:.2f}s")

    return {
        "request_id": request_id,
        "results": results,
        "latency": round(latency, 3),
    }


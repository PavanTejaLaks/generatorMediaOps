import time
from collections import defaultdict, deque
from fastapi import HTTPException

RATE_LIMIT_REQUESTS = 30 #max requests
RATE_LIMIT_WINDOW = 60 #seconds (time limit)

_request_log = defaultdict(deque)

def check_rate_limit(api_key: str):
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    user_queue = _request_log[api_key]


    while user_queue and user_queue[0] < window_start:
        user_queue.popleft()

    if len(user_queue) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please Slow Down.",
        )
    
    user_queue.append(now)
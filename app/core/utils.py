import string
import random
from typing import Optional
import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Redis connection
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

def generate_short_url(length: int = 6) -> str:
    """Generates random short URL"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def cache_url(short_url: str, original_url: str) -> None:
    """Caches URL in Redis"""
    redis_client.setex(f"url:{short_url}", 3600, original_url)  # 1 hour cache

def get_cached_url(short_url: str) -> Optional[str]:
    """Gets URL from cache"""
    cached = redis_client.get(f"url:{short_url}")
    return cached.decode('utf-8') if cached else None 
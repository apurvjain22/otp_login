import redis
import os

# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
REDIS_URL = os.getenv("REDIS_URL", "localhost")
r = redis.from_url(REDIS_URL, decode_responses=True)

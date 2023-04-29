import os
import redis

class RedisMemoryController:
    def __init__(self):
        self.redis = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), db=os.getenv("REDIS_DB", 0))

    def store_memory(self, key, value):
        self.redis.setex(key, int(os.getenv("SHORT_TERM_EXPIRY", 3600)), value)

    def retrieve_memory(self, key):
        value = self.redis.get(key)
        return value.decode("utf-8") if value else None

    def delete_memory(self, key):
        self.redis.delete(key)

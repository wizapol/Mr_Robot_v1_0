import os
import redis

class RedisMemoryController:
    def __init__(self):
        self.redis = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), db=os.getenv("REDIS_DB", 0))
        #print("Connected to Redis at {}:{}".format(os.getenv("REDIS_HOST", "localhost"), os.getenv("REDIS_PORT", 6379)))


    def store_memory(self, key, value):
        self.redis.setex(key, int(os.getenv("SHORT_TERM_EXPIRY", 3600)), value)
        #print("Stored memory with key: {} and value: {}".format(key, value))

    def retrieve_memory(self, key):
        value = self.redis.get(key)        
        #print("Retrieved memory with key: {} and value: {}".format(key, value))
        return value.decode("utf-8") if value else None

    def delete_memory(self, key):
        self.redis.delete(key)
        #print("Deleted memory with key: {}".format(key))

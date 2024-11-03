import hashlib


class CacheManager:
    def __init__(self):
        self.cache = {}

    def get_cache_key(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, question):
        cache_key = self.get_cache_key(question)
        return self.cache.get(cache_key)

    def set(self, question, answer):
        cache_key = self.get_cache_key(question)
        self.cache[cache_key] = answer

import redis


class RedisStore:
    def __init__(self, host: str, port: int) -> None:
        self.redis: redis.Redis = redis.Redis(host=host, port=port)

    def get(self, key: str) -> str:
        value: bytes = self.redis.get(key)
        if not value:
            return None
        return value.decode("utf-8")

    def set(self, key: str, value: str) -> None:
        self.redis.set(key, value)

    def cache_get(self, key: str) -> str:
        value: bytes = self.redis.get(key)
        if not value:
            return None
        return value.decode("utf-8")

    def cache_set(self, key: str, value: str, expired: int) -> None:
        self.redis.set(key, value, ex=expired)

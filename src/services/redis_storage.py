import json
import redis.asyncio as redis
from src.core.config import get_redis_url

class RedisStorage:
    def __init__(self):
        self.client = redis.from_url(get_redis_url(), decode_responses=True)

    async def get_history(self, user_id: int) -> list:
        data = await self.client.get(f"chat:{user_id}")
        return json.loads(data) if data else []

    async def save_history(self, user_id: int, history: list):
        # Храним историю, например, 24 часа (TTL)
        await self.client.set(f"chat:{user_id}", json.dumps(history), ex=86400)

    async def clear_history(self, user_id: int):
        await self.client.delete(f"chat:{user_id}")
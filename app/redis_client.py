import redis.asyncio as redis
import json
from app.config import settings

client = redis.Redis.from_url(settings.redis_url)

async def cache_queue_entry(entry_id: str, data: dict, expire_seconds: int = 30):
    await client.set(f"queue:status:{entry_id}",
                     json.dumps(data), 
                     ex=expire_seconds)


async def get_cached_queue_entry(entry_id: str):
    cached = await client.get(f"queue:status:{entry_id}")
    if cached:
        return json.loads(cached) 
    
    return None

async def invalidate_cached_queue_entry(entry_id: str):
    await client.delete(f"queue:status:{entry_id}")
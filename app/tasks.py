from app.celery_app import app
import asyncio
from app.database import AsyncSessionLocal
from app.redis_client import cache_queue_entry
from app.models import Queue_entries, QueueStatus


@app.task
def process_check_in(entry_id: str):
    async def process():
        async with AsyncSessionLocal() as db:
            entry = await db.get(Queue_entries, entry_id)
            if not entry:
                return
            
            
            entry.status = QueueStatus.QUEUED
            await db.commit()
            await db.refresh(entry)
            
            await cache_queue_entry(entry_id, {
                "id": str(entry.id),
                "status": entry.status.value,
                "queue_entry_no": entry.queue_entry_no,
                "service_type": entry.service_type.value,
                "priority": entry.priority.value
                })
        
    asyncio.run(process())
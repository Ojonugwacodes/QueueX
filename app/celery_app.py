from celery import Celery
from app.config import settings

app = Celery('queuex', broker = settings.rabbitmq_url, result_backend = settings.redis_url)

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
)
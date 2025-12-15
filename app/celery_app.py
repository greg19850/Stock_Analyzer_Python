from celery import Celery
from app.config import settings

celery_app = Celery(
    "investment analyser",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"]
)

# Configuration
celery_app.conf.update(
    task_serialzer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
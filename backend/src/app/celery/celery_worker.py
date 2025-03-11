from celery import Celery

from src.config import settings

# from src.app.utils.celery_tasks import MessageTasks

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

celery_app = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    broker_connection_retry_on_startup=True,
)

celery_app.conf.update(
    result_expire=3600,  # 3600 seconds -> 1 hrs.
)

# Register tasks
celery_app.autodiscover_tasks(["src.app.utils.celery_tasks"])
# celery_app.register_task(MessageTasks.store_messages)

from celery import Celery
from config import settings

app = Celery("trails", broker=settings.redis_url, backend=settings.redis_url)
app.conf.timezone = "UTC"

app.autodiscover_tasks(["workers.tasks"])

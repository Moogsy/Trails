from celery import Celery
from config import settings
from logging_setup import configure_logging

configure_logging(json_logs=True)

app = Celery("trails", broker=settings.redis_url, backend=settings.redis_url)
app.conf.timezone = "UTC"
app.conf.result_expires = 3600

app.autodiscover_tasks(["workers.tasks"])

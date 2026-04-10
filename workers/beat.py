from celery.schedules import crontab
from workers import app

app.conf.beat_schedule = {
    "match-batch": {
        "task": "workers.tasks.run_match_batch",
        "schedule": crontab(hour=21, minute=0),  # 21:00 UTC — adjust per market
    },
}

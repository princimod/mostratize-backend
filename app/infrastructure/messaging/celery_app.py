from celery import Celery

celery_app = Celery(
    "mostratize_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=20,        # hard limit
    task_soft_time_limit=15,   # RNF-001
)

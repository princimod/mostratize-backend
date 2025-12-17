from kombu import Queue

CELERY_QUEUES = (
    Queue("ai_high_priority", routing_key="ai.#"),
)

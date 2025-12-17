from app.infrastructure.messaging.celery_app import celery_app
from app.application.services.ai_service import AIService

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
    retry_backoff=True,
    retry_jitter=True,
)
def process_voice_task(self, audio_base64: str):
    """
    Task Celery para processamento de voz (US-110)
    """
    service = AIService()
    return service.process_voice(audio_base64)

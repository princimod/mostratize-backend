from fastapi import APIRouter
from app.infrastructure.messaging.tasks_ai import process_voice_task
from celery.result import AsyncResult
from app.infrastructure.messaging.celery_app import celery_app

router = APIRouter()


@router.post("/bj/voice")
def register_by_voice(payload: dict):
    task = process_voice_task.delay(payload["audio"])
    return {
        "task_id": task.id,
        "status": "PROCESSING"
    }

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }
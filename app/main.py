# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.routers import api_router

def create_app() -> FastAPI:
    """
    Factory da aplicação FastAPI.
    Permite fácil extensão, testes e múltiplos ambientes.
    """

    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
    )

    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app

app = create_app()

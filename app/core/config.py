# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """
    Configurações globais da aplicação.
    Carregadas automaticamente do arquivo .env
    """

    # Aplicação
    APP_NAME: str = "MOSTRATIZE API"
    ENVIRONMENT: str = "development"

    # API
    API_PREFIX: str = "/api/v1"

    # Banco de Dados
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

settings = Settings()

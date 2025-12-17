# app/infrastructure/database/models/base_model.py
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

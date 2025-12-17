from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.infrastructure.database.base import Base

# Configuração Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata das models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL.replace("+asyncpg", ""),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        {
            "sqlalchemy.url": settings.DATABASE_URL,
            "sqlalchemy.poolclass": pool.NullPool,
        },
        prefix="sqlalchemy.",
    )

    def do_run_migrations(connection: Connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    async def run():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    import asyncio
    asyncio.run(run())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

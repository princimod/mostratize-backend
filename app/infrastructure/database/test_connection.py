# app/infrastructure/database/test_connection.py
import asyncio
from app.infrastructure.database.session import engine


async def test():
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    print("✅ Conexão com banco OK")


if __name__ == "__main__":
    asyncio.run(test())

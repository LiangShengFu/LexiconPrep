"""Initialize the database — create all tables and seed data."""
import asyncio
from app.core.database import engine, Base
import app.models  # noqa: ensure all models are registered


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

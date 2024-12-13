import asyncio

import httpx
import pytest

from database.connection import Settings
from models.event import Event
from models.user import User


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"
    await test_settings.initialize_database()


@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    client = httpx.AsyncClient(base_url="http://0.0.0.0:8000")
    try:
        yield client
    finally:
        await client.aclose()
        await Event.find_all().delete()
        await User.find_all().delete()

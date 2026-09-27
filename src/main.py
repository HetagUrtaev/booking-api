from contextlib import asynccontextmanager
import sys
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from init import redis_manager
import uvicorn


sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO) # устанавливает уровень логирования


# ruff: noqa: I001
from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.database import *


@asynccontextmanager
async def lifespan(app: FastAPI):  # подключение/отключение Redis
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")

    yield
    await redis_manager.disconnect()


app = FastAPI(
    lifespan=lifespan, title="Booking API", description="Сервер для бронирования отелей"
)


app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

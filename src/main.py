from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

from init import redis_manager

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache



from src.database import *


#print(f'settings = {settings.DB_URL}')

@asynccontextmanager
async def lifespan(app: FastAPI): # подключение/отключение Redis
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    print('подключение к Redis')

    yield
    await redis_manager.disconnect()
    print('отключение от Redis')


app = FastAPI(
    lifespan=lifespan, title="Booking API",
    description="Сервер для бронирования отелей"
)


app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)




if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
"""
Конфигурационный файл pytest (conftest.py).

Содержит глобальные фикстуры для управления жизненным циклом тестовой базы данных,
инициализации моков (кэш, Redis) и предоставления HTTPX-клиентов для интеграционного
тестирования эндпоинтов FastAPI.
"""

import json
from unittest import mock

import pytest
from httpx import ASGITransport, AsyncClient

mock.patch(
    "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f
).start()  # мокаем работу с кэшом
mock.patch(
    "src.api.facilities.task_task.delay", lambda *args, **kwargs: None
).start()  # мокаем подключение в redis

from src.config import settings
from src.database import Base, async_session_maker_null_pool, engine
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBMamager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    """Предохранитель, который проверяет, что тесты
    запущены строго в изолированном тестовом режиме."""
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db():
    """Предоставляет чистую сессию базы данных на время выполнения
    теста для прямой проверки работы репозиториев."""
    async with DBMamager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    """Автоматически зачищает старую структуру базы данных
    и накатывает чистые таблицы на время сессии тестов."""

    # Сначала полностью подготавливаем чистые таблицы в БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # Заполняем БД тестовыми данными:
    # 1. Читаем файлы, преобразуя JSON-данные в Python-объекты
    with open("tests/mock_hotels.json", "r", encoding="utf8") as file_hotels:  # noqa: ASYNC230
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", "r", encoding="utf8") as rooms_hotels:  # noqa: ASYNC230
        rooms = json.load(rooms_hotels)

    # 2. Преобразовываем сырые данные в Pydantic-схемы для валидации
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    # 3. Соединяемся с тестовой БД через менеджер контекста
    async with DBMamager(session_factory=async_session_maker_null_pool) as db_:
        # 4. Передаем все наши данные в репозитории
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        # 5. Сохраняем (коммитим) изменения в базе данных
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    """Создает виртуальный HTTP-клиент для отправки запросов
    в эндпоинты приложения без запуска реального сервера."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    """Автоматически регистрирует тестового юзера через HTTPX-клиент
    сразу после того, как setup_database создаст таблицы."""
    await ac.post("/auth/register", json={"email": "test@user.com", "password": "123"})


@pytest.fixture(scope="session")
async def authenticated_as(register_user, ac):
    """
    Выполняет аутентификацию тестового пользователя и возвращает
    клиент HTTPX с сохраненными в куках JWT-токенами.
    """
    await ac.post(url="/auth/login", json={"email": "test@user.com", "password": "123"})
    assert ac.cookies["access_token"]
    yield ac

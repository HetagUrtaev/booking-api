# НАЗНАЧЕНИЕ ФАЙЛА: Главный узел настройки БД.
# Связывает Python-код проекта с PostgreSQL.
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


# Движок с постоянным пулом соединений
engine = create_async_engine(settings.DB_URL)
# Движок без пула соединений
# (для редких фоновых задач Celery, чтобы не забивать память БД)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

# Фабрика сессий
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
# Фабрика сессий без пула
# (используется в Celery для разовых тяжелых фоновых запросов)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

# Базовый класс-фундамент, от которого наследуются все ORM-таблицы в коде
class Base(DeclarativeBase):
    pass
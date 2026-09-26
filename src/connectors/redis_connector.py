import logging

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.host = host
        self.port = port
        self.redis: Redis | None = None

    async def connect(self) -> None:
        """Устанавливает асинхронное соединение с сервером Redis."""
        try:
            self.redis = Redis(host=self.host, port=self.port, decode_responses=True)
            await self.redis.ping()
            logger.info(f"Successfully connected to Redis at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def set(self, key: str, value: str, expire: int | None = None) -> bool:
        """Сохраняет значение по ключу.

        Аргумент expire задает время жизни ключа в секундах (TTL).
        """
        if expire:
            return await self.redis.set(key, value, ex=expire)
        else:
            return await self.redis.set(key, value)

    async def get(self, key: str) -> str | None:
        """Получает значение по ключу. Если ключа нет — возвращает None."""
        return await self.redis.get(key)

    async def delete(self, key: str) -> int:
        """Удаляет ключ из базы данных. Возвращает количество удаленных ключей."""
        return await self.redis.delete(key)

    async def disconnect(self) -> None:
        """Безопасно закрывает пул соединений с Redis."""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed.")

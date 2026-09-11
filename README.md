# Booking API

Асинхронное бэкенд-приложение на FastAPI для бронирования отелей. Проект реализует полноценную работу с базой данных, миграции и автоматизацию фоновых задач по расписанию.

## 🛠️ Технологический стек
* **Фреймворк:** FastAPI (Python)
* **База данных:** PostgreSQL + SQLAlchemy 2.0 (Драйвер `asyncpg`)
* **Миграции:** Alembic
* **Фоновые задачи:** Celery + Celery Beat
* **Брокер очередей:** Redis (Docker)

## 🏗️ Архитектура и особенности
* **Разделение процессов:** FastAPI и Celery запущены как независимые процессы в системе.
* **Управление базой данных:** Для FastAPI настроен быстрый пул соединений (`QueuePool`), а для редких фоновых задач Celery используется одноразовый движок (`NullPool`), чтобы беречь память PostgreSQL.
* **Асинхронные мосты:** Синхронные задачи Celery безопасно общаются с асинправной базой данных через мост `asyncio.run()`.

## 🚀 Инструкция по локальному запуску

1. **Запуск Docker-контейнера с Redis:**
   ```bash
   docker run --name booking-redis -p 6379:6379 -d redis
   ```

2. **Запуск веб-сервера FastAPI:**
   ```bash
   uvicorn src.main:app --reload
   ```

3. **Запуск Celery (в двух разных терминалах):**
   ```bash
   # Исполнитель задач (Worker)
   celery -A src.tasks.celery_app:celery_instance worker -P solo --loglevel=info

   # Автоматический будильник (Beat)
   celery -A src.tasks.celery_app:celery_instance beat --loglevel=info
   ```

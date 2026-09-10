from celery import Celery

from src.config import settings

# ─── ИНИЦИАЛИЗАЦИЯ ДИРИЖЕРА CELERY ───
celery_instance = Celery(
    'tasks',                    # Имя нашего Celery-приложения
    broker=settings.REDIS_URL,  # Адрес Docker-Redis очереди задач
    include=[
        'src.tasks.tasks',      # Файл, где лежат наши фоновые функции
    ]
)

# ─── НАСТРОЙКА АВТОМАТИЧЕСКОГО БУДИЛЬНИКА (BEAT) ───
celery_instance.conf.beat_schedule = {
    'любое_название': {
        'task': 'booking_today_checkin',  # Какую задачу запускать по имени из декоратора
        'schedule': 5                     # Периодичность запуска в секундах
    }
}

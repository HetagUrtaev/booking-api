from time import sleep
import os
from PIL import Image
import asyncio

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBMamager


@celery_instance.task
def task_task():
    print('Я начал')
    sleep(5)
    print('Я закончил')

@celery_instance.task
def resize_and_save_image(file_path: str):
    """
    Берет оригинальную картинку, делает 3 сжатые копии
    и железно всегда сохраняет ВСЕ ТРИ файла в ту же папку
    с суффиксами _1000, _500, _200 на конце.
    """
    if not os.path.exists(file_path):
        print(f"❌ Файл {file_path} не найден!")
        return

    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name_without_ext, ext = os.path.splitext(base_name)

    target_widths = [1000, 500, 200]

    with Image.open(file_path) as img:
        orig_width, orig_height = img.size

        for width in target_widths:
            # 🛠️ ИСПРАВЛЕНИЕ: Если оригинал меньше нужной ширины (например, 800px < 1000px),
            # мы НЕ пропускаем её, а просто берем максимальную ширину оригинала, чтобы файл создался!
            current_width = width
            if orig_width < width:
                current_width = orig_width

            # Считаем высоту пропорционально
            ratio = current_width / float(orig_width)
            height = int(float(orig_height) * float(ratio))

            # Сжимаем картинку
            resized_img = img.resize((current_width, height), Image.Resampling.LANCZOS)

            # Формируем имя: все три файла ложатся рядом (например, hotel_1000.jpg, hotel_500.jpg)
            new_filename = f"{name_without_ext}_{width}{ext}"
            new_file_path = os.path.join(dir_name, new_filename)

            # Сохраняем
            resized_img.save(new_file_path, optimize=True, quality=85)
            print(f"✅ Создана копия: {new_file_path} (Размер: {current_width}x{height})")

    # Удаляем временный исходник, так как у нас теперь есть все 3 нужных файла!
    os.remove(file_path)
    print(f"🗑️ Исходный файл {base_name} удален.")

async def get_bookings_with_today_checkin_helper():
    """
    Асинхронный помощник. Celery работает отдельно от FastAPI, поэтому эта функция
    руками открывает сессию к Postgres, забирает сегодняшние бронирования и печатает их.
    """
    print('Я запускаюсь')
    async with DBMamager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f'{bookings}')


@celery_instance.task(name='booking_today_checkin')
def sent_emails_to_users_with_today_checkin():
    """
    Синхронная задача Celery. Воркер не умеет напрямую делать await.
    Поэтому мы используем asyncio.run(), чтобы запустить асинправного помощника выше.
    """
    asyncio.run(get_bookings_with_today_checkin_helper())


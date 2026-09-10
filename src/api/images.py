from fastapi import APIRouter, UploadFile
import shutil

from src.tasks.tasks import resize_and_save_image

router = APIRouter(prefix='/images', tags=['Картинки'])


@router.post('', summary = 'Изображения отелей')
def upload_images( fail: UploadFile):
    file_path = f"src/static/images/{fail.filename}"
    with open(file_path, 'wb+') as new_fail:
        shutil.copyfileobj(fail.file, new_fail)

    resize_and_save_image.delay(file_path)


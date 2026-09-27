from datetime import date

from fastapi import HTTPException


class BookingException(Exception):
    """Базовое исключение для всего нашего проекта."""
    detail = "Произошла внутренняя ошибка приложения"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingException):
    detail = "Объект не найден"

class ObjectAlreadyExistsException(BookingException):
    detail = "Похожий объект уже существует"

class AllRoomsBookedException(BookingException):
    detail = 'На данные даты мест нет'


def check_date_to_after_date_from(date_to: date, date_from: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=400, detail='Дата заезда не может быть меньше даты выезда'
        )

class BookingHTTPException(HTTPException):
    '''Базовый шаблон для всех HTTP-ошибок проекта.'''
    status_code = 500
    detail = None
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = 'Такого отеля нет'

class RoomNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = 'Такого номера нет'
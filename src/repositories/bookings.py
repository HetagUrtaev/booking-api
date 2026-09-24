from sqlalchemy import select
from datetime import date
from fastapi import HTTPException

from src.schemas.bookings import BookingAdd
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepositories
from src.repositories.utils import rooms_ids_for_booking




class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        """
        Выбираем из базы все бронирования, у которых дата заезда (заселения)
        совпадает с сегодняшним днем - для Celery.
        """
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]


    """Проверяет доступность и создаёт бронь."""
    async def add_booking(self, data: BookingAdd, hotel_id: int):

        booking_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id
        )
        booking_ids_to_book_res = await self.session.execute(booking_ids_to_get)
        booking_ids_to_book: list[int] = booking_ids_to_book_res.scalars().all()

        if data.room_id in booking_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(status_code=400, detail="На данные даты мест нет")
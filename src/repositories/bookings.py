from sqlalchemy import select
from datetime import date

from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepositories




class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        """
        Выбираем из базы все бронирования, у которых дата заезда (заселения)
        совпадает с сегодняшним днем.
        """
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

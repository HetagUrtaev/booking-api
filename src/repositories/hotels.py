from datetime import date

from src.repositories.mappers.mappers import HotelDataMapper
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepositories
from sqlalchemy import select, func
from src.schemas.hotels import Hotel


class HotelsRepositories(BaseRepositories):
    model = HotelsOrm
    mapper = HotelDataMapper


    async def get_filtered_by_time(
            self,
            location,
            title,
            limit,
            offset,
            date_from: date,
            date_to: date
    ) -> list[Hotel]:

        room_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(room_ids_to_get))
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
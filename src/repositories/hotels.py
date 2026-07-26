from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepositories
from sqlalchemy import insert, select, func
from src.schemas.hotels import Hotel


class HotelRepositories(BaseRepositories):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset):

        query = select(HotelsOrm)
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
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]





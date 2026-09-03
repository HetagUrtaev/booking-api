from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepositories
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepositories(BaseRepositories):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ):


        room_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        #print(room_ids_to_get.compile(bind=engine, compile_kwargs={'literal_binds': True}))

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(room_ids_to_get))
        )
        result = await self.session.execute(query)
        # Получаем данные из БД и сразу превращаем каждую строчку в красивый Pydantic-объект
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]


    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None # Если в базе ничего не нашлось, возвращаем None
        # Если нашли — превращаем в Pydantic-объект и отдаем наружу
        return RoomWithRels.model_validate(res, from_attributes=True)


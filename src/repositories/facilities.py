from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepositories

from sqlalchemy import insert, select, delete, update


class FacilitiesRepositories(BaseRepositories):
    model = FacilitiesOrm
    mapper = FacilityDataMapper

class RoomsFacilitiesRepositories(BaseRepositories):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilityDataMapper

    async def set_rooms_facilities(self, room_id: int, facilities_ids: list[int]):
        get_corrent_facilities_ids_query= select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(get_corrent_facilities_ids_query)
        corrent_facilities_ids = res.scalars().all()

        ids_to_insert = list(set(facilities_ids) - set(corrent_facilities_ids)) # список услуг которые нужно добавить в бд
        ids_to_delete = list(set(corrent_facilities_ids) - set(facilities_ids))  # список услуг которые нужно удалить из бд

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{'room_id': room_id, 'facility_id': f_id} for f_id in ids_to_insert]
                )
            )
            await self.session.execute(insert_m2m_facilities_stmt)
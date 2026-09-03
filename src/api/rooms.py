from fastapi import APIRouter, Body, Query
from datetime import date

from api.dependencies import DBDep
from schemas.rooms import RoomAdd, RoomAddReqest, RoomPatch, RoomPatchReqest
from schemas.facilities import RoomFacilityAdd


router = APIRouter(prefix='/hotels/{hotel_id}/rooms', tags=['Номера'])


@router.get('', summary = 'Вывести все номера')
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example= '2026-08-01'),
        date_to: date = Query(example= '2026-08-07')
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from= date_from,
        date_to=date_to
    )

@router.get('/{room_id}', summary = 'Вывести один номер')
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    print(type(await db.rooms.get_one_or_none(id=room_id)))
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post('', summary = 'Добавить номер')
async def create_room(
        hotel_id: int,
        db: DBDep,
        rooms_data: RoomAddReqest = Body(),
):

    _room_data = RoomAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id,
                        facility_id=f_id) for f_id in rooms_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {'status': 'OK', 'data': room}


@router.put('/{room_id}', summary = 'Полное обновление номера')
async def put_room(
    hotel_id: int,
    room_id: int,
    rooms_data: RoomAddReqest,
    db: DBDep
):
    _room_data = RoomAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_rooms_facilities(room_id, facilities_ids=rooms_data.facilities_ids)
    await db.commit()
    return {'status': 'OK'}


@router.patch('/{room_id}', summary = 'Частичное обновление номера')
async def patch_room(
    hotel_id: int,
    room_id: int,
    rooms_data: RoomPatchReqest,
    db: DBDep
):
    _rooms_data_dict = rooms_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_rooms_data_dict)
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id
    )

    if 'facilities_ids' in _rooms_data_dict:
        await db.rooms_facilities.set_rooms_facilities(
            room_id,
            facilities_ids=_rooms_data_dict['facilities_ids']
        )
    await db.commit()
    return {'status': 'OK'}


@router.delete('/{room_id}', summary = 'Удаление номера')
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return  {'status': 'OK'}






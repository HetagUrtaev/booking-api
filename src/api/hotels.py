from datetime import date

from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get('', summary = 'Вывести все отели')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(default=None, description='Локация'),
        title: str | None = Query(default=None, description='Название отеля'),
        date_from: date = Query(example= '2026-08-01'),
        date_to: date = Query(example= '2026-08-07')
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
        date_from = date_from,
        date_to = date_to
    )

@router.get('/{hotel_id}', summary = 'Вывести один отель')
async def get_hotel(hotel_id: int, db: DBDep ):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post('', summary = 'Добавить отель')
async def post_hotel( db: DBDep,
                      hotel_data: HotelAdd = Body(openapi_examples= {
    '1': {'summary': 'Сочи', "value": {  # это пример для Swagger
        "title": "Сочи",
        "location": "ул. Сочинская, д. 1"
    }},
    '2': {'summary': 'Воронеж', "value": {
        "title": "Воронеж",
        "location": "ул. Воронежская, д. 1"
    }}
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {'status': 'OK', 'data': hotel}


@router.put('/{id}', summary = 'Полное обновление отеля')
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.patch('/{id}', summary = 'Частичное обновление отеля')
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):

    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {'status': 'OK'}


@router.delete('/{id_hotel}', summary = 'Удаление отеля')
async def delete_hotels(id_hotel: int, db: DBDep):

    await db.hotels.delete(id=id_hotel)
    await db.commit()
    return  {'status': 'OK'}
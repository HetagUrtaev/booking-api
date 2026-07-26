from fastapi import Query, APIRouter, Body, Depends
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelRepositories
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get('', summary = 'Вывести все отели')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(default=None, description='Локация'),
        title: str | None = Query(default=None, description='Название отеля'),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepositories(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)

        )

@router.get('/{hotel_id}', summary = 'Вывести один отель')
async def get_hotel(hotel_id: int):
    async  with async_session_maker() as session:
        print(type(await HotelRepositories(session).get_one_or_none(id=hotel_id)))
        return await HotelRepositories(session).get_one_or_none(id=hotel_id)



@router.post('', summary = 'Добавить отель')
async def post_hotel( hotel_data: HotelAdd = Body(openapi_examples= {
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
    async with async_session_maker() as session:
        hotel = await HotelRepositories(session).add(hotel_data)
        await session.commit()

    return {'status': 'OK', 'data': hotel}

@router.put('/{id}', summary = 'Полное обновление отеля')
async def put_hotel(
    hotel_id: int,
    hotel_data: HotelAdd
):
    async with async_session_maker() as session:
        await HotelRepositories(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {'status': 'OK'}


@router.patch('/{id}', summary = 'Частичное обновление отеля')
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):

    async with async_session_maker() as session:
        await HotelRepositories(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {'status': 'OK'}


@router.delete('/{id_hotel}', summary = 'Удаление отеля')
async def delete_hotels(
        id_hotel: int
):
    async with async_session_maker() as session:
        await HotelRepositories(session).delete(id=id_hotel)
        await session.commit()
    return  {'status': 'OK'}
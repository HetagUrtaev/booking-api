from fastapi import Query, APIRouter, Body, Depends
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, Hotel_PATCH

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'lol4'},
    {'id': 2, 'title': 'Дубай', 'name': 'lol4'},
    {'id': 3, 'title': 'Vladikavz', 'name': 'lol4'},
    {'id': 4, 'title': 'Samara', 'name': 'lol4'},
    {'id': 5, 'title': 'Samara', 'name': 'lol4'},
    {'id': 6, 'title': 'Samara', 'name': 'lol4'},
    {'id': 7, 'title': 'Samara', 'name': 'lol4'},
    {'id': 8, 'title': 'Samara', 'name': 'lol4'},
    {'id': 9, 'title': 'Samara', 'name': 'lol4'},
    {'id': 10, 'title': 'Samara', 'name': 'lol4'},
    {'id': 11, 'title': 'Samara', 'name': 'lol4'},
    {'id': 12, 'title': 'Samara', 'name': 'lol4'},
    {'id': 13, 'title': 'Samara', 'name': 'lol4'},
]



router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('', summary = 'мое название ручки')
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(default=None, description='тут я тестирую описание параметра'),
        title: str | None = Query(default=None, description='Название отеля'),
        name: str | None =  Query(default=None, description='имя отеля'),
):
    global hotels
    if id != None:
        return [hotel for hotel in hotels if hotel['id'] == id]
    if title != None:
        return [hotel for hotel in hotels if hotel['title'] == title]
    if name != None:
        hotel = [hotel for hotel in hotels if hotel['name'] == name]

        if pagination.page and pagination.per_page:
            return hotel[pagination.per_page * (pagination.page-1):][:pagination.per_page]
        return hotel


@router.delete('/{id_hotel}')
def delete_hotels(
        id_hotel: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id_hotel]
    return hotels


@router.post('')
def post_hotel( hotel_data: Hotel = Body(openapi_examples= {
    '1': {'summary': 'Сочи', "value": {  # это пример для Swagger
        "title": "Hostel 24",
        "name": "Hostel Central"
    }},
    '2': {'summary': 'Воронеж', "value": {
        "title": "Воронеж",
        "name": "Hostel Central"
    }}
})
):
    global hotels
    id = hotels[-1]['id'] + 1
    hotels.append({'id': id, 'title': hotel_data.title, 'name': hotel_data.name})
    return hotels

@router.put('/{id}')
def put_hotel(
    id: int,
    hotel_data: Hotel
):
    global hotels
    hotels[id] = {'id': id, 'title': hotel_data.title, 'name': hotel_data.name}
    return hotels


@router.patch('/{id}')
def patch_hotel(id: int, hotel_data: Hotel_PATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id']==id][0]
    print(hotel)
    if hotel_data.title:
        hotel['title'] = hotel_data.title
    if hotel_data.name:
        hotel['name'] = hotel_data.name
    return hotels
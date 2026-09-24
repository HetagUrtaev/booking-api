from datetime import date
from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm

"""
Возвращает подзапрос со списком ID комнат, доступных для бронирования на указанные даты.
"""
def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None
):
    # 1) Запрос для создания таблицы rooms_count в которой будет:
    # - столбец room_id
    # - столбец rooms_booked (количество броней этого номера за данный период)
    rooms_count = (
        select(BookingsOrm.room_id, func.count('*').label('rooms_booked'))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from
        )
        .group_by(BookingsOrm.room_id)
        .cte(name='rooms_count')
    )

    # 2) Запрос для создания таблицы rooms_left_table в которой будет:
    # - столбец room_id
    # - столбец rooms_left (количество номеров минус количество броней)
    rooms_left_table = (
        select(
            RoomsOrm.id.label('room_id'),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0))
            .label('rooms_left')
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name='rooms_left_table')
    )

    # 3) Запрос для создания таблицы rooms_ids_for_hotel в которой будет:
    # - столбец id (комнаты)
    rooms_ids_for_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )

    # 4) Если таблица передан аргумент hotel_id
    # тогда столбец с id (комнаты) будет отображать комнаты конкретного отеля
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name='rooms_ids_for_hotel')

    # 5) Запрос для создания таблицы room_ids_to_get в которой будет:
    # - столбец room_id (id комнаты) если количество свободных номеров больше 0
    # и эта комната есть в списке номеров конкретного отеля
    room_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(select(rooms_ids_for_hotel))
                )
    )
    return room_ids_to_get # список id свободных комнат

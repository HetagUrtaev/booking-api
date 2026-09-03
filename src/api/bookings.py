from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddReqest

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('', summary='Получение все бронирований')
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get('/me', summary='Получение всех бронирований пользователя')
async def get_my_booking(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)



@router.post('', summary = 'Добавить бронирование номера')
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddReqest = Body(),
    ):
    room = await db.rooms.get_one_or_none(id = booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {'status': 'OK', 'data': booking}




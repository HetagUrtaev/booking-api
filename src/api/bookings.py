from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsBookedException, ObjectNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddReqest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение все бронирований")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение всех бронирований пользователя")
async def get_my_booking(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Добавить бронирование номера")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddReqest = Body(),  # noqa: B008
):
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=401, detail="Номер не найден"
        )

    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsBookedException as e:
        raise HTTPException(
            status_code=409, detail=e.detail
        )
    await db.commit()
    return {"status": "OK", "data": booking}

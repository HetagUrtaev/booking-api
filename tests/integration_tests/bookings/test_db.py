from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    """Полное тестирование роутера bookings"""

    # добавление
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=10, day=1),
        date_to=date(year=2026, month=10, day=10),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    # получение
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking

    # сверка данных
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id
    assert booking.price == new_booking.price
    assert booking.date_from == new_booking.date_from
    assert booking.date_to == new_booking.date_to

    # изменение
    date_to = date(year=2026, month=10, day=15)
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=10, day=1),
        date_to=date_to,
        price=100,
    )

    await db.bookings.edit(update_booking_data, id=new_booking.id)
    update_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert update_booking
    assert update_booking.date_to == date_to

    # удаление
    await db.bookings.delete(id=booking.id)
    await db.commit()
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking

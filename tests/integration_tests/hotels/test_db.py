from src.schemas.hotels import HotelAdd


async def test_post_hotel(db):
    """Тестирует успешное добавление нового отеля в базу данных."""
    hotel_data = HotelAdd(title="Отель_1", location="г. Энск")
    await db.hotels.add(hotel_data)
    await db.commit()

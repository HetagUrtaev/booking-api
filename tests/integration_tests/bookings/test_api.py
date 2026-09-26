import pytest

from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBMamager


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-10-10", "2026-10-15", 200),
        (1, "2026-10-10", "2026-10-15", 200),  # noqa: PT014
        (1, "2026-10-10", "2026-10-15", 200),  # noqa: PT014
        (1, "2026-10-10", "2026-10-15", 200),  # noqa: PT014
        (1, "2026-10-10", "2026-10-15", 200),  # noqa: PT014
        (1, "2026-10-10", "2026-10-15", 400),
        (1, "2026-10-20", "2026-10-25", 200),
    ],
)  # параметризация теста
async def test_add_booking(
    room_id, date_from, date_to, status_code, authenticated_as, db
):
    """Проверяет создание бронирований, лимиты комнат
    и успешные запросы на разные даты."""

    response = await authenticated_as.post(
        url="/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code
    res = response.json()
    if status_code == 200:
        assert isinstance(res, dict)
        assert res["data"]["room_id"] == room_id
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="session")
async def delete_all_bookings():
    """Очищает все бронирования пользователя перед началом тестирования."""
    async with DBMamager(session_factory=async_session_maker_null_pool) as _db:
        await _db.bookings.delete(user_id=1)
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booking_len",
    [
        (1, "2026-10-10", "2026-10-15", 1),
        (1, "2026-10-10", "2026-10-15", 2),
        (1, "2026-10-10", "2026-10-15", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id, date_from, date_to, booking_len, delete_all_bookings, authenticated_as
):
    """Проверяет последовательное добавление броней
    и корректность подсчета их количества в списке пользователя."""
    response = await authenticated_as.post(
        url="/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == 200
    response_my_bookings = await authenticated_as.get(url="/bookings/me")
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booking_len

async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels", params={"date_from": "2026-01-10", "date_to": "2026-01-20"}
    )
    """
    Проверяет получение списка отелей, доступных для бронирования 
    в указанный диапазон дат через Query-параметры.
    """
    assert response.status_code == 200
    assert isinstance(response.json(), list)

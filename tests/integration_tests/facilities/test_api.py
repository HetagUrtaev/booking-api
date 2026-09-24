async def test_get_facilities(ac):
    """
    Проверяет успешное получение полного списка всех удобств (facilities) отеля.
    """
    response = await ac.get('/facilities')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_facilities(ac):
    """
    Проверяет успешное создание нового удобства (facility).
    """
    response = await ac.post(url='/facilities', json={'title':'тест-удобство'})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res['data']['title'] == 'тест-удобство'
    assert res['status'] == 'OK'
    assert 'data' in res

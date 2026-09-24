import pytest



@pytest.mark.parametrize('email, password, status_code', [
    ('test@user.com', '123', 400),
    ('test2@user.com', '123', 200),
    ('test2@user.com', '123', 400),
    ('ахахахаха', '123', 422),
])
async def test_auth_flow(
        email,
        password,
        status_code,
        ac
):
    """Проверяет сквозной сценарий авторизации: регистрацию, вход,
    получение профиля и выход из системы."""


    # /register
    resp_register = await ac.post(
        url='/auth/register',
        json={'email': email, 'password': password}
    )
    assert resp_register.status_code == status_code
    if status_code != 200:
        return
    res = resp_register.json()
    assert isinstance(res, dict)
    assert res['status'] == 'OK'


    # /login
    resp_login = await ac.post(
        url='/auth/login',
        json={'email': email, 'password': password}
    )
    assert resp_login.status_code == status_code
    res = resp_login.json()
    assert isinstance(res, dict)
    assert ac.cookies['access_token']
    assert 'access_token' in resp_login.json()


    # /me
    resp_me = await ac.get(
        url='/auth/me',
    )

    assert resp_me.status_code == 200
    user = resp_me.json()
    assert isinstance(user, dict)
    assert user['email'] == email
    assert 'password' not in user
    assert 'hashed_password' not in user

    # /logout
    assert 'access_token' in ac.cookies
    resp_logout = await ac.get(url='/auth/logout')
    assert 'access_token' not in ac.cookies
    assert resp_logout.status_code == 200
    assert resp_logout.json()['status'] == 'OK'

from src.service.auth import AuthService


def test_create_access_token():
    """Проверяет успешную генерацию JWT-токена доступа и
    валидирует строковый тип возвращаемых данных."""

    data = {'user_id': 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

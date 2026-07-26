from fastapi import APIRouter, HTTPException, Response, Request
from api.dependencies import UserIdDep

from src.database import async_session_maker
from src.repositories.auth import UsersRepositories
from src.schemas.auth import UserRequestAdd, UserAdd
from src.service.auth import AuthServise



router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

@router.post('/login', summary = 'Вход в систему')
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail= 'Пользователь с таким email не зарегистрирован')
        if not AuthServise().verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail='Пароль неверный')
        access_token = AuthServise().create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}


@router.post('/register', summary = 'Регистрация')
async def register_user(
        data: UserRequestAdd,
):
    hash_password = AuthServise().hash_password(data.password)
    now_user_data = UserAdd(email=data.email,  password=hash_password)
    async with async_session_maker() as session:
        await UsersRepositories(session).add(now_user_data)
        await session.commit()
    return {'status': 'OK'}


@router.get('/me', summary='Информация о пользователе')
async def get_me(
    user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_one_or_none(id=user_id)
        return user

@router.get('/logout', summary='Выйти из аккаунта')
async def logout(
    response: Response
):
    response.delete_cookie('access_token')
    return {'status': 'OK'}

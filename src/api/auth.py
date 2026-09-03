from fastapi import APIRouter, HTTPException, Response
from api.dependencies import UserIdDep, DBDep

from src.schemas.auth import UserRequestAdd, UserAdd
from src.service.auth import AuthServise


router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

@router.post('/login', summary = 'Вход в систему')
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail='Пользователь с таким email не зарегистрирован')
    if not AuthServise().verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail='Пароль неверный')
    access_token = AuthServise().create_access_token({'user_id': user.id})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.post('/register', summary = 'Регистрация')
async def register_user(data: UserRequestAdd, db: DBDep):
    hash_password = AuthServise().hash_password(data.password)
    now_user_data = UserAdd(email=data.email,  password=hash_password)
    await db.users.add(now_user_data)
    await db.commit()
    return {'status': 'OK'}


@router.get('/me', summary='Информация о пользователе')
async def get_me(user_id: UserIdDep, db: DBDep):
    return await db.users.get_one_or_none(id=user_id)

@router.get('/logout', summary='Выйти из аккаунта')
async def logout(
    response: Response
):
    response.delete_cookie('access_token')
    return {'status': 'OK'}

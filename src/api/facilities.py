from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from api.dependencies import DBDep
from schemas.facilities import FacilityAddReqest


router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('', summary='Получение всех видов удобств')
@cache(expire=10)
async def get_facilities(db: DBDep):
    print('Иду в БД')
    return await db.facilities.get_all()


@router.post('', summary = 'Добавление нового вида удобства')
async def add_facilities(
        db: DBDep,
        facilities_data: FacilityAddReqest = Body(),
    ):
    facility = await db.facilities.add(facilities_data)
    await db.commit()
    return {'status': 'OK', 'data': facility}

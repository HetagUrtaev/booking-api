from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import FacilityAddReqest

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('', summary='Получение всех видов удобств')
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post('', summary = 'Добавление нового вида удобства')
async def add_facilities(
        db: DBDep,
        facilities_data: FacilityAddReqest = Body(),
    ):
    facility = await db.facilities.add(facilities_data)
    await db.commit()
    return {'status': 'OK', 'data': facility}

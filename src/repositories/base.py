from sqlalchemy import insert, select, func, delete, update
from pydantic import BaseModel

from src.schemas.hotels import Hotel


class BaseRepositories:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs): #
        # ─── ПОЛУЧИТЬ ВСЕ ЗАПИСИ ИЗ ТАБЛИЦЫ ───
        query = select(self.model)
        result = await self.session.execute(query)
        # Получаем данные из БД и сразу превращаем каждую строчку в красивый Pydantic-объект
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_one_or_none(self, **filter_by):
        # ─── НАЙТИ ОДНУ ЗАПИСЬ ПО ФИЛЬТРУ ИЛИ ВЕРНУТЬ NONE ───
        query = select(self.model).filter_by(**filter_by) # Например: filter_by(id=1)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None # Если в базе ничего не нашлось, возвращаем None
        # Если нашли — превращаем в Pydantic-объект и отдаем наружу
        return self.schema.model_validate(res, from_attributes=True)

    async def add(self, data):
        # ─── ДОБАВИТЬ НОВУЮ ЗАПИСЬ В ТАБЛИЦУ ───
        # Берем данные из Pydantic-схемы (data.model_dump()) и формируем SQL-запрос на вставку
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        resul = await self.session.execute(add_data_stmt)
        # Возвращаем созданную запись, которую нам вернула база данных
        return resul.scalars().one()

    async def edit(self, data, exclude_unset: bool = False, **filter_by):
        # ─── ОБНОВИТЬ (РЕДАКТИРОВАТЬ) СУЩЕСТВУЮЩУЮ ЗАПИСЬ ───
        # Находим запись по фильтру и обновляем поля данными из Pydantic-модели.
        # exclude_unset=True позволяет обновлять ТОЛЬКО те поля, которые пользователь реально прислал
        update_stmt = (
            update(self.model).
            filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        # ─── УДАЛИТЬ ЗАПИСЬ ИЗ БАЗЫ ПО ФИЛЬТРУ ───
        # Формируем и выполняем SQL-запрос на удаление (например: удалить отель где id=5)
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)



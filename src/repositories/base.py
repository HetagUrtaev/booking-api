from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepositories:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        # ─── ПОЛУЧИТЬ ВСЕ ЗАПИСИ ИЗ ТАБЛИЦЫ ПО ФИЛЬТРУ ───
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        # Получаем данные из БД и сразу превращаем каждую строчку в красивый Pydantic-объект
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        # ─── ПОЛУЧИТЬ ВСЕ ЗАПИСИ ИЗ ТАБЛИЦЫ ───
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        # ─── НАЙТИ ОДНУ ЗАПИСЬ ПО ФИЛЬТРУ ИЛИ ВЕРНУТЬ NONE ───
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        # ─── НАЙТИ ОДНУ ЗАПИСЬ ПО ФИЛЬТРУ ───
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        # ─── ДОБАВИТЬ НОВУЮ ЗАПИСЬ В ТАБЛИЦУ ───
        # Берем данные из Pydantic-схемы (data.model_dump()) и формируем SQL-запрос на вставку
        try:
            add_data_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            resul = await self.session.execute(add_data_stmt)
            model = resul.scalars().one()
            # Возвращаем созданную запись, которую нам вернула база данных
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e
            else:
                raise


    async def add_bulk(self, data: list[BaseModel]):
        # Данный метод добавлен для добавления объекта со связью многие-ко-многим
        # Также он подходит для добавления неопределенного количества данных (используем в тестах)
        if not data:
            return
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data, exclude_unset: bool = False, **filter_by):
        # ─── ОБНОВИТЬ (РЕДАКТИРОВАТЬ) СУЩЕСТВУЮЩУЮ ЗАПИСЬ ───
        # Находим запись по фильтру и обновляем поля данными из Pydantic-модели.
        # exclude_unset=True позволяет обновлять ТОЛЬКО те поля, которые пользователь реально прислал
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        # ─── УДАЛИТЬ ЗАПИСЬ ИЗ БАЗЫ ПО ФИЛЬТРУ ───
        # Формируем и выполняем SQL-запрос на удаление (например: удалить отель где id=5)
        delete_stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        if result.rowcount == 0:
            raise ObjectAlreadyExistsException

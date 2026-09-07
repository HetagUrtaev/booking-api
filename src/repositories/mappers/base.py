from typing import TypeVar
from pydantic import BaseModel

from database import Base

SchemaType = TypeVar('SchemaType', bound=BaseModel)
DBModelType = TypeVar('DBModelType', bound=Base)

class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(src, data):
        # Из ORM в Pydantic
        return src.schema.model_validate(data, from_attributes=True)


    @classmethod
    def map_to_persistence_entity(src, data):
        # Из Pydantic в ORM
        return src.db_model(**data.model_dump())
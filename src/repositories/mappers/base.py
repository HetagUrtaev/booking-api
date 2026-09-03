class DataMapper:
    db_model = None
    schema = None

    @classmethod
    def map_to_domain_entity(src, data):
        # Из ORM в Pydantic
        return src.schema.model_validate(data, from_attributes=True)


    @classmethod
    def map_to_persistence_entity(src, data):
        # Из Pydantic в ORM
        return src.db_model(**data.model_dump())
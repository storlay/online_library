from typing import ClassVar
from typing import Type

from pydantic import BaseModel

from src.db import Base


class BaseDataMapper:
    model: ClassVar[Type[Base]] = None  # type: ignore
    schema: ClassVar[Type[BaseModel]] = None  # type: ignore
    schema_with_rels: ClassVar[Type[BaseModel] | None] = None

    @classmethod
    def map_to_domain_entity(
        cls,
        model_instance: Base,
        with_rels: bool = False,
    ) -> BaseModel:
        schema_to_use = (
            cls.schema_with_rels if with_rels and cls.schema_with_rels else cls.schema
        )
        return schema_to_use.model_validate(
            model_instance,
            from_attributes=True,
        )

    @classmethod
    def map_to_persistence_entity(
        cls,
        schema_instance: BaseModel,
    ) -> Base:
        return cls.model(**schema_instance.model_dump())

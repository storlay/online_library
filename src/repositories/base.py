from typing import Any
from typing import Iterable

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.db.database import Base
from src.exceptions.repository.base import CannotAddObjectRepoException
from src.exceptions.repository.base import ObjectNotFoundRepoException
from src.repositories.mappers.base import BaseDataMapper


class BaseRepository:
    model: type[Base] = None  # type: ignore
    mapper: type[BaseDataMapper] = None  # type: ignore

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all(
        self,
        limit: int,
        offset: int,
    ) -> list[BaseModel | Any]:
        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)
        # fmt: off
        return [
            self.mapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]
        # fmt: on

    async def get_one_or_none(
        self,
        **filter_by,
    ) -> BaseModel | None | Any:
        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return model
        return self.mapper.map_to_domain_entity(model)

    async def get_one(
        self,
        query_options: Iterable[ExecutableOption] | None = None,
        with_rels: bool = False,
        **filter_by,
    ) -> BaseModel | Any:
        # fmt: off
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        if query_options is not None:
            query = query.options(*query_options)
        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound as ex:
            raise ObjectNotFoundRepoException from ex

        return self.mapper.map_to_domain_entity(model, with_rels=with_rels)

    async def add(
        self,
        data: BaseModel,
    ) -> BaseModel | Any:
        # fmt: off
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        # fmt: on
        try:
            result = await self.session.execute(stmt)
            model = result.scalar_one()
        except IntegrityError as ex:
            raise CannotAddObjectRepoException from ex
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(
        self,
        data: list[BaseModel],
    ) -> None:
        # fmt: off
        stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        # fmt: on
        try:
            await self.session.execute(stmt)
        except IntegrityError as ex:
            raise CannotAddObjectRepoException from ex

    async def update_one(
        self,
        data: BaseModel,
        partially: bool = False,
        **filter_by,
    ) -> int:
        # fmt: off
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=partially))
            .filter_by(**filter_by)
            .returning(self.model.id) # type: ignore
        )
        # fmt: on
        result = await self.session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound as ex:
            raise ObjectNotFoundRepoException from ex

    async def delete_one(
        self,
        **filter_by,
    ) -> int:
        # fmt: off
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
            .returning(self.model.id) # type: ignore
        )
        # fmt: on
        result = await self.session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound as ex:
            raise ObjectNotFoundRepoException from ex

    async def delete_bulk(
        self,
        **filter_by,
    ) -> None:
        # fmt: off
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        # fmt: on
        await self.session.execute(stmt)

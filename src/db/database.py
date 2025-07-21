import re

import inflect
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from src.config import settings


async_engine = create_async_engine(
    url=settings.db.URL,
)
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)

inflect_engine = inflect.engine()


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
        Converts `CamelCase` class name
        to plural `snake_case` table name.

        :return: Pluralized snake_case table name.
        """
        name = re.sub(
            r"(?<!^)(?=[A-Z])",
            "_",
            cls.__name__,
        ).lower()
        return inflect_engine.plural(name)  # type: ignore

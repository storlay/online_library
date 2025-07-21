import re

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


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
        Converting a class name (CamelCase)
        to a table name (snake_case).
        :return: Table name.
        """
        name = re.sub(
            r"(?<!^)(?=[A-Z])",
            "_",
            cls.__name__,
        ).lower()
        return name

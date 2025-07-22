from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db import Base
from src.db.mixins.pk import IntPkModelMixin
from src.schemas.enums.user import UserRoleEnum


class User(Base, IntPkModelMixin):
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )
    first_name: Mapped[str | None] = mapped_column(
        String(255),
    )
    last_name: Mapped[str | None] = mapped_column(
        String(255),
    )
    role: Mapped[UserRoleEnum] = mapped_column(
        server_default=UserRoleEnum.reader.value,
    )

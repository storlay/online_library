from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.config import RolesIDEnum
from src.db import Base
from src.db.mixins.pk import IntPkModelMixin


if TYPE_CHECKING:
    from src.models.permission import Role


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
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        server_default=str(RolesIDEnum.READER.value),
    )

    role: Mapped["Role"] = relationship(
        back_populates="users",
    )

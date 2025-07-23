from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.db import Base
from src.db.mixins.pk import IntPkModelMixin


if TYPE_CHECKING:
    from src.models.user import User


class Permission(Base, IntPkModelMixin):
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )
    description: Mapped[str] = mapped_column(
        String(1020),
        server_default="",
    )

    role_associations: Mapped[list["RolePermission"]] = relationship(
        back_populates="permission",
    )
    roles: Mapped[list["Role"]] = association_proxy(
        "role_associations",
        "role",
    )  # type: ignore


class Role(Base, IntPkModelMixin):
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    permission_associations: Mapped[list["RolePermission"]] = relationship(
        back_populates="role",
    )
    permissions: Mapped[list["Permission"]] = association_proxy(
        "permission_associations",
        "permission",
    )  # type: ignore
    users: Mapped[list["User"]] = relationship(
        back_populates="role",
    )


class RolePermission(Base):
    __tablename__ = "role_permission"  # type: ignore
    # The name has been overridden
    # for reliability and to comply
    # with the M2M table naming convention.

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"),
        primary_key=True,
    )

    role: Mapped["Role"] = relationship(
        back_populates="permission_associations",
    )
    permission: Mapped["Permission"] = relationship(
        back_populates="role_associations",
    )

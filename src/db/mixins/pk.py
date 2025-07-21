from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IntPkModelMixin:
    """
    Mixin is a primary key of type ``int``.
    """

    id: Mapped[int] = mapped_column(primary_key=True)

from typing import Annotated

from annotated_types import Ge


PositiveInteger = Annotated[
    int,
    Ge(0),
]
IntegerId = Annotated[
    int,
    Ge(1),
]

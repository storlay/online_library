from typing import Annotated

from fastapi import Depends

from src.schemas.pagination import PaginationRequestSchema
from src.schemas.pagination import PaginationSchema


def get_pagination_params(
    params: Annotated[
        PaginationRequestSchema,
        Depends(),
    ],
) -> PaginationSchema:
    return PaginationSchema(
        limit=params.per_page,
        offset=params.per_page * (params.page - 1),
    )


PaginationDep = Annotated[
    PaginationSchema,
    Depends(get_pagination_params),
]

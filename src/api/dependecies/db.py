from typing import Annotated
from typing import AsyncGenerator

from fastapi import Depends

from src.db.database import async_session
from src.utils.transaction import BaseManager
from src.utils.transaction import TransactionManager


async def get_db_transaction() -> AsyncGenerator[TransactionManager]:
    async with TransactionManager(
        session_factory=async_session,
    ) as transaction:
        yield transaction


DbTransactionDep = Annotated[
    BaseManager,
    Depends(get_db_transaction),
]

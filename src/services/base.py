from src.utils.transaction import TransactionManager


class BaseService:
    def __init__(
        self,
        db: TransactionManager | None = None,
    ) -> None:
        self.db = db

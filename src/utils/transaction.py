from abc import ABC
from abc import abstractmethod
from typing import Callable

from src.repositories.permission import PermissionRepository
from src.repositories.permission import RoleRepository
from src.repositories.user import UserRepository


class BaseManager(ABC):
    user: UserRepository
    permission: PermissionRepository
    role: RoleRepository

    @abstractmethod
    def __init__(self):
        """Initializing the manager"""
        pass

    @abstractmethod
    async def __aenter__(self):
        """Enter the asynchronous context"""
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the asynchronous context"""
        pass

    @abstractmethod
    async def commit(self):
        """Commit the transaction"""
        pass


class TransactionManager(BaseManager):
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.role = RoleRepository(self.session)
        self.permission = PermissionRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from src.app.database.models import User
from src.app.api.schemas.user import UserCreate

class AbstractUserRepository(ABC):
    @abstractmethod
    async def add_user(self, data: dict):
        raise NotImplementedError
    

class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, data) -> User:
        result = await self.session.execute(
            select(User).where(User.username == data.username)
        )
        user = result.scalar_one_or_none()

        return user
    
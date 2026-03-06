from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from src.app.database.models import User
from src.app.api.schemas.user import UserCreate, UserOut

class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_user_by_username(self, data: str): 
        raise NotImplementedError
    

class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        existing_user = result.scalar_one_or_none()

        return existing_user
    
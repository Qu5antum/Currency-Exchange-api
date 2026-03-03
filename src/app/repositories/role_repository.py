from abc import ABC, abstractmethod
from sqlalchemy import select

from src.app.database.db import AsyncSession
from src.app.database.models import Role

class AbstractRoleRepository(ABC):
    @abstractmethod
    async def get_role(self):
        raise NotImplementedError
    

class RoleRepository(AbstractRoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_role(self):
        result = await self.session.execute(
            select(Role).where(Role.name == "USER")
        )
        role = result.scalar_one_or_none()

        return role
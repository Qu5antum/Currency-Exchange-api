from abc import ABC, abstractmethod

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, model_id: int):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_custom_id(self, custom_id: int):
        raise NotImplementedError
    
    @abstractmethod
    async def update_data(self, obj_id: int, data: dict):
        raise NotImplementedError
    


class Repository(AbstractRepository):
    model = None 

    def __init__(self, session: AsyncSession):
        self.session = session 

    async def create(self, data: dict):
        model_name = self.model(**data)
        self.session.add(model_name)
        return model_name

    async def find_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
    
    async def get_by_id(self, model_id: int):
        result = await self.session.get(self.model, model_id)
        return result 
    
    async def get_by_custom_id(self, custom_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.cmc_id == custom_id)
        )
        existing_object = result.scalar_one_or_none()
        return existing_object
    
    async def update_data(self, obj_id: int, data: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**data)
            .returning(self.model)
        )

        result = await self.session.execute(stmt)

        await self.session.commit()

        return result.scalar_one_or_none()
    


        
        
    
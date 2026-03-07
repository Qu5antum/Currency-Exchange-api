from abc import ABC, abstractmethod

from sqlalchemy import select
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
    
    @abstractmethod
    async def find_all_with_custom_ids(self, obj_ids: list[int]):
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
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        obj = result.scalar_one_or_none()

        if obj is None:
            return None

        for field, value in data.items():
            setattr(obj, field, value)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj
    
    async def find_all_with_custom_ids(self, obj_ids: list[int]):
        result = await self.session.execute(
            select(self.model).where(self.model.id.in_(obj_ids))
        )
        objects = result.scalars().all()
        return objects


        
        
    
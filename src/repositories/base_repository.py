from typing import Generic, TypeVar, Type, Optional, Any
from fastapi import Depends
from sqlmodel import SQLModel, Session, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import get_session
from src.models import UserModel

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: Any) -> Optional[UserModel]:
        async with self.session.begin():
            statement = select(self.model).where(self.model.id == id)
            result = await self.session.exec(statement).first()
            return result

    async def create(self, data: dict) -> ModelType:
        async with self.session.begin():
            obj = self.model(**data)
            self.session.add(obj)
            return obj
    
    async def update(self, id: Any, data: dict) -> bool:
        async with self.session.begin():
            statement = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
            )   
            result = await self.session.exec(statement)
            return result.rowcount > 0 
    
    async def delete(self, id: Any) -> bool:
        async with self.session.begin():
            statement = delete(self.model).where(self.model.id == id)
            result = await self.session.exec(statement)
            return result.rowcount > 0
        
    
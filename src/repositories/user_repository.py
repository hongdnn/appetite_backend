from typing import Optional
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_session
from src.models import UserModel
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)
    
    async def get_by_email(self, email: str) -> Optional[UserModel]:
        async with self.session.begin():
            statement = select(UserModel).where(UserModel.email == email)
            result = await self.session.execute(statement)
            return result.scalars().first()
        
def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
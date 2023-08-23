from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.base import CRUDBase
from models import User as UserModel
from schemas.users import UserCreate, UserUpdate, UserActivate
from core.security import encrypt_password

class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    
    async def create(self, db: AsyncSession, *, data: UserCreate) -> UserModel:
        
        inner = UserModel(
            email=data.email,
            hashed_password=encrypt_password(data.password)
        )
        
        return await super().create(db, data=inner)
    

    async def activate(
        self,
        db: AsyncSession,
        *,
        data: UserActivate
    ) -> UserModel:
        user = await self.find_one(db=db, uid=data.uid, token=data.token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
            )
        
        # update and save
        user.is_active = True
        return await self.save(db=db, obj=user)


users = CRUDUser(UserModel)
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordRequestForm

from src.app.database.db import AsyncSession
from src.app.database.models import User, Role
from src.app.api.schemas.user import UserCreate
from src.app.security.security_context import hash_password, check_hashes
from src.app.security.security import create_jwt_token


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_new_user(self, user: UserCreate):
        result = await self.session.execute(
            select(User).where(User.username == user.username)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User already exists."
            )
        
        result = await self.session.execute(
            select(Role).where(Role.name == "USER")
        )
        role = result.scalar_one_or_none()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found."
            )
        
        new_user = User(
            **user.model_dump(exclude={"password"}),
            password = hash_password(user.password)
        )

        await self.session.add(new_user)

        new_user.roles.append(role)

        await self.session.commit()

        return {"detail": "Succesfully registered."}
    

    async def auth_user(
            self,
            credents: OAuth2PasswordRequestForm
    ):
        result = await self.session.execute(
            select(User).where(User.username == credents.username)
        )

        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        if not check_hashes(credents.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password."
            )
        
        token = await create_jwt_token({"sub": str(user.id)})

        return {"access_token": token, "token_type": "bearer"}
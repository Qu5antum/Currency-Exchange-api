from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.database.db import AsyncSession
from src.app.database.models import User
from src.app.api.schemas.user import UserCreate
from src.app.repositories.user_repository import UserRepository
from src.app.repositories.role_repository import RoleRepository
from src.app.security.security_context import hash_password, check_hashes
from src.app.security.security import create_jwt_token


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_new_user(self, user: UserCreate):
        existing_user = UserRepository(session=self.session).add_user(data=user)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User already exists."
            )
        
        role = RoleRepository(session=self.session).get_role()

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
        user = UserRepository(session=self.session).add_user(data=credents)
        
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
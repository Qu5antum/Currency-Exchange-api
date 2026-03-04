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
        user_repo = UserRepository(session=self.session)
        existing_user = await user_repo.add_user(data=user)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists."
            )
        
        role_repo = RoleRepository(session=self.session)
        role = await role_repo.get_role()


        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found."
            )
        
        new_user = User(
            **user.model_dump(exclude={"password"}),
            password = hash_password(user.password)
        )

        new_user.roles.append(role)

        self.session.add(new_user)
        await self.session.commit()

        return {"detail": "Succesfully registered."}
    

    async def auth_user(
            self,
            credents: OAuth2PasswordRequestForm
    ):
        user_repo = UserRepository(session=self.session)
        user = await user_repo.get_user_by_username(username=credents.username)
        
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
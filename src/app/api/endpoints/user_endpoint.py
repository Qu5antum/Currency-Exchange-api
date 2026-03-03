from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.database.db import AsyncSession, get_session
from src.app.database.models import User
from src.app.api.schemas.user import UserCreate, UserOut
from src.app.api.dependencies.dependency import get_current_user
from src.app.service.user_service import UserService


user_router = APIRouter(
    prefix="/api/user",
    tags=["users"]
)

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    user_service = UserService(session=session)
    return user_service.add_new_user(user=user)


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user_service = UserService(session=session)
    return user_service.auth_user(credents=user)
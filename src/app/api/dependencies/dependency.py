from fastapi import Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.app.database.models import User
from src.app.database.db import AsyncSession, get_session
from src.app.security.security import get_user_from_token

async def get_current_user(
        session: AsyncSession = Depends(get_session), 
        user_id: int = Depends(get_user_from_token)
) -> User:
    result = await session.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user



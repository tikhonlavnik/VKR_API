from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.utils.auth_config import settings
from src.apps.authorization.service import AuthService
from src.database import get_session


class AuthViews:
    def __init__(self, service: AuthService):
        self.service = service
        self.router = APIRouter(prefix="/api", tags=["Auth"])
        self.router.add_api_route("/login/", self.login, methods=["POST"])

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_session),
    ):
        user = await self.service.authenticate_user(
            db, form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = self.service.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


auth_service = AuthService()
auth_views = AuthViews(auth_service)

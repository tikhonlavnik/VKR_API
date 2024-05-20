from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.apps.users.schemas import CreateRequestUserSchema, ResponseUserSchema
from src.apps.users.service import UsersService
from src.database import get_session


class UsersViews:
    def __init__(self, service: UsersService):
        self.service = service
        self.router = APIRouter(prefix="/api", tags=["Users"])
        self.router.add_api_route("/users/", self.create_user, methods=["POST"])

    async def create_user(
        self, user: CreateRequestUserSchema, db: AsyncSession = Depends(get_session)
    ) -> ResponseUserSchema:
        new_user = await self.service.create_user_entity(user, db)
        return new_user


users_service = UsersService()
users_views = UsersViews(users_service)

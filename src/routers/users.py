from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.authorization.service import get_current_user
from src.apps.users.models import Users
from src.apps.users.schemas import (
    CreateRequestUserSchema,
    ResponseUserSchema,
    UpdateUserSchema,
    ResponseDeleteUserSchema,
)
from src.apps.users.service import UsersService
from src.database import get_session


class UsersViews:
    def __init__(self, service: UsersService):
        self.service = service
        self.router = APIRouter(prefix="/api", tags=["Users"])
        self.router.add_api_route("/users/", self.create_user, methods=["POST"])
        self.router.add_api_route("/users/{user_id}/", self.get_user, methods=["GET"])
        self.router.add_api_route("/users/", self.update_user, methods=["PUT"])
        self.router.add_api_route("/users/", self.delete_user, methods=["DELETE"])

    async def create_user(
        self, body: CreateRequestUserSchema, db: AsyncSession = Depends(get_session)
    ) -> ResponseUserSchema:
        new_user = await self.service.create_user_entity(body, db)
        return new_user

    async def get_user(
        self,
        user_id: UUID,
        db: AsyncSession = Depends(get_session),
    ) -> ResponseUserSchema:
        user = await self.service.get_user_entity(user_id, db)
        return user

    async def update_user(
        self,
        body: UpdateUserSchema,
        db: AsyncSession = Depends(get_session),
        current_user: Users = Depends(get_current_user),
    ) -> ResponseUserSchema:
        user = await self.service.update_user_entity(current_user.id, body, db)
        return user

    async def delete_user(
        self,
        db: AsyncSession = Depends(get_session),
        current_user: Users = Depends(get_current_user),
    ) -> ResponseDeleteUserSchema:
        user = await self.service.delete_user_entity(current_user.id, db)
        return user


users_service = UsersService()
users_views = UsersViews(users_service)

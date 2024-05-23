from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.authorization.service import get_current_user
from src.apps.users.models import Users
from src.apps.users.schemas import (
    ResponseUserSchema,
    UpdateUserSchema,
    ResponseDeleteUserSchema,
)
from src.apps.users.service import UsersService
from src.database import get_session


class AdminUsersViews:
    def __init__(self, service: UsersService):
        self.service = service
        self.router = APIRouter(prefix="/api/admin", tags=["Administration users"])
        self.router.add_api_route(
            "/users/{user_id}/", self.admin_update_user, methods=["PUT"]
        )
        self.router.add_api_route(
            "/users/{user_id}/", self.admin_delete_user, methods=["DELETE"]
        )

    async def admin_update_user(
        self,
        user_id: UUID,
        body: UpdateUserSchema,
        db: AsyncSession = Depends(get_session),
        current_user: Users = Depends(
            get_current_user
        ),  # TODO: add method to check is_admin
    ) -> ResponseUserSchema:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin"
            )
        user = await self.service.update_user_entity(user_id, body, db)
        return user

    async def admin_delete_user(
        self,
        user_id: UUID,
        db: AsyncSession = Depends(get_session),
        current_user: Users = Depends(get_current_user),
    ) -> ResponseDeleteUserSchema:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin"
            )
        user = await self.service.delete_user_entity(user_id, db)
        return user


users_service = UsersService()
admin_users_views = AdminUsersViews(users_service)

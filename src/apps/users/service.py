from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.users.models import Users
from src.apps.users.schemas import (
    CreateRequestUserSchema,
    UpdateUserSchema,
    SystemUserSchema,
)
from src.utils.logger import setup_logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersService:
    def __init__(self):
        self.model = Users
        self.logger = setup_logger("apps.users.UsersService")

    async def create_user_entity(
        self, body: CreateRequestUserSchema, db: AsyncSession
    ) -> "Users":
        async with db.begin():
            result = await db.execute(
                select(Users).filter(
                    (Users.email == body.email) | (Users.username == body.username)
                )
            )
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email or username already registered",
                )

            hashed_password = pwd_context.hash(body.password)
            body.password = hashed_password
            new_user = Users(**body.dict())
            db.add(new_user)
            try:
                await db.commit()
                self.logger.info(f"User created successfully: {new_user.email}")
                return new_user
            except IntegrityError as e:
                await db.rollback()
                self.logger.error(f"Error creating user: {e.detail}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not create user",
                )
            finally:
                await db.close()

    async def get_user_entity(self, user_id: UUID, db: AsyncSession) -> "Users":
        # async with db.begin():
        user_query = await db.execute(select(Users).filter(Users.id == user_id))
        user = user_query.scalars().first()
        if not user:
            self.logger.error(f"User not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or username already registered",
            )
        return user

    async def update_user_entity(
        self, user_id: UUID, body: UpdateUserSchema, db: AsyncSession
    ) -> "Users":
        # async with db.begin():
        user_query = await db.execute(select(Users).filter(Users.id == user_id))
        user = user_query.scalars().first()
        if not user:
            self.logger.error(f"User is not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.sex = body.sex
        user.birthday = body.birthday
        user.updated_at = datetime.now()
        try:
            await db.commit()
            self.logger.info(f"User updated successfully: {user.email}")
            return user
        except IntegrityError as e:
            await db.rollback()
            self.logger.error(f"Error updating user: {e.detail}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not update user",
            )

    async def delete_user_entity(self, user_id: UUID, db: AsyncSession) -> "Users":
        # async with db.begin():
        user_query = await db.execute(
            select(Users).filter(and_(Users.id == user_id, Users.is_active == True))
        )
        user = user_query.scalars().first()
        if not user:
            self.logger.error(f"User is not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user.is_active = False
        try:
            await db.commit()
            self.logger.info(f"User deleted successfully: {user.email}")
            return user
        except IntegrityError as e:
            await db.rollback()
            self.logger.error(f"Error deleting user: {e.detail}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not delete user",
            )

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str):
        query = select(Users).filter(Users.username == username)
        result = await db.execute(query)
        user = result.scalars().first()
        if user:
            return SystemUserSchema(**user.__dict__)
        return None

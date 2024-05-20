import logging
from logging.handlers import RotatingFileHandler

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.users.models import Users
from src.apps.users.schemas import CreateRequestUserSchema
from src.utils.logger import setup_logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersService:
    def __init__(self):
        self.model = Users
        self.logger = setup_logger("apps.users.UsersService")

    async def create_user_entity(self, user: CreateRequestUserSchema, db: AsyncSession):
        async with db.begin():
            result = await db.execute(
                select(Users).filter(
                    (Users.email == user.email) | (Users.username == user.username)
                )
            )
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email or username already registered",
                )

            hashed_password = pwd_context.hash(user.password)
            user.password = hashed_password
            new_user = Users(**user.dict())
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

import pytest
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from src.apps.users.service import UsersService
from src.apps.users.models import Users
from src.apps.users.schemas import CreateRequestUserSchema, UpdateUserSchema
from src.utils.logger import setup_logger
from datetime import datetime

DATABASE_URL = Config.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# @pytest.fixture(scope="module", autouse=True)
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Users.metadata.create_all)
#         yield
#         await conn.run_sync(Users.metadata.drop_all)


# Создание всех таблиц в базе данных
# models.Base.metadata.create_all(engine)


# @pytest.fixture
# def db_session():
#     session = Session()
#     yield session
#     # session.close()


@pytest.fixture
def mock_logger():
    return setup_logger("mock_logger")


@pytest.fixture
def users_service(mock_logger):
    return UsersService()


@pytest.mark.asyncio
async def test_create_user_entity(users_service):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "sex": "Male",
        "birthday": datetime(1990, 1, 1),
    }
    user_schema = CreateRequestUserSchema(**user_data)
    db_session = Session()
    user = await users_service.create_user_entity(user_schema, db_session)
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    delete_stmt = delete(Users).where(Users.id == user.id)
    await db_session.execute(delete_stmt)
    await db_session.commit()


@pytest.mark.asyncio
async def test_get_user_entity(users_service):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "sex": "Male",
        "birthday": datetime(1990, 1, 1),
    }
    user_schema = CreateRequestUserSchema(**user_data)
    db_session = Session()
    user = await users_service.create_user_entity(user_schema, db_session)

    retrieved_user = await users_service.get_user_entity(user.id, db_session)
    assert retrieved_user.username == user_data["username"]
    assert retrieved_user.email == user_data["email"]
    delete_stmt = delete(Users).where(Users.id == user.id)
    await db_session.execute(delete_stmt)
    await db_session.commit()


@pytest.mark.asyncio
async def test_update_user_entity(users_service):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "sex": "Male",
        "birthday": datetime(1990, 1, 1),
    }
    user_schema = CreateRequestUserSchema(**user_data)
    db_session = Session()
    user = await users_service.create_user_entity(user_schema, db_session)

    updated_data = {
        "first_name": "Updated",
        "last_name": "User",
        "sex": "Male",
        "birthday": datetime(1990, 1, 1),
    }
    update_schema = UpdateUserSchema(**updated_data)
    updated_user = await users_service.update_user_entity(
        user.id, update_schema, db_session
    )

    assert updated_user.first_name == updated_data["first_name"]
    assert updated_user.last_name == updated_data["last_name"]
    assert updated_user.sex == updated_data["sex"]
    delete_stmt = delete(Users).where(Users.id == updated_user.id)
    await db_session.execute(delete_stmt)
    await db_session.commit()


@pytest.mark.asyncio
async def test_delete_user_entity(users_service):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "sex": "Male",
        "birthday": datetime(1990, 1, 1),
    }
    user_schema = CreateRequestUserSchema(**user_data)
    db_session = Session()
    user = await users_service.create_user_entity(user_schema, db_session)

    deleted_user = await users_service.delete_user_entity(user.id, db_session)
    assert not deleted_user.is_active
    delete_stmt = delete(Users).where(Users.id == deleted_user.id)
    await db_session.execute(delete_stmt)
    await db_session.commit()

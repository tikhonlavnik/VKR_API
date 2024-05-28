from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    sex: str
    birthday: datetime
    is_admin: bool = False


class CreateRequestUserSchema(UserBaseSchema):
    password: str


class ResponseUserSchema(UserBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool


class UpdateUserSchema(BaseModel):
    first_name: str
    last_name: str
    sex: str
    birthday: date


class ResponseDeleteUserSchema(BaseModel):
    id: UUID


class SystemUserSchema(ResponseDeleteUserSchema):
    username: str
    password: str
    is_admin: bool
    is_active: bool

from typing import Optional

from pydantic import Field, BaseModel


class UserLoginSchema(BaseModel):
    username: str = Field(alias="username")
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    pass


class UserRead(BaseModel):
    id: str
    avatar: str
    username: str
    email: str
    password: str
    deleted: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6)


class UserUpdate(UserBase):
    avatar: str | None = None
    username: str | None = Field(default=None, min_length=4, max_length=16)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6)


class UserUpdateAdmin(UserUpdate):
    deleted: bool | None = None
    roles: list[str] | list[None] | None = None

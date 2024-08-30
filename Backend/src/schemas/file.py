from datetime import datetime
from typing import Any
from pydantic import BaseModel

from src.schemas.user_schemas.user import UserRead
from src.schemas.custom_response import CustomResponse


class FileBase(BaseModel):
    filename: str = 'example.json'
    description: str | None = None


class FileCreate(FileBase):
    content: Any


class FileRead(FileBase):
    id: str
    url: str
    created_at: datetime
    updated_at: datetime
    deleted: bool
    user: UserRead


class FileResponseModel(CustomResponse):
    data: FileRead | None = None

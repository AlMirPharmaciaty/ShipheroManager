from datetime import datetime
from typing import Any
from pydantic import BaseModel

from src.schemas.user_schemas.user import UserRead
from src.schemas.custom_response import CustomResponse


class FileBase(BaseModel):
    filename: str = 'example.json'
    description: str | None = ''


class FileCreate(FileBase):
    content: Any


class FileRead(FileBase):
    id: int
    url: str
    created_at: datetime
    updated_at: datetime
    deleted: bool


class FileReadWithRelation(FileBase):
    user: UserRead


class FileResponseModel(CustomResponse):
    data: FileReadWithRelation | list[FileReadWithRelation] | None = None

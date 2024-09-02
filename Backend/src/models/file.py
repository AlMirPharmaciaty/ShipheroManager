from typing import Optional
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.models.user_models.user import User


class File(BaseModel):
    "Files table model"

    __tablename__ = "files"

    file_id: Mapped[Optional[str]] = mapped_column(unique=True)
    filename: Mapped[Optional[str]]
    url: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    deleted: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    user = relationship('User')

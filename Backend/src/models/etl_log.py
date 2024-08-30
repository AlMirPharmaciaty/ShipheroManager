from typing import Optional
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.models.user_models.user import User
from src.models.file import File


class ETLLog(BaseModel):
    "table to log etl output"

    __tablename__ = "etl_logs"

    process: Mapped[str]
    success: Mapped[bool]
    description: Mapped[str] = mapped_column(Text)
    file_id: Mapped[Optional[str]] = mapped_column(ForeignKey(File.id))
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    user = relationship('User')

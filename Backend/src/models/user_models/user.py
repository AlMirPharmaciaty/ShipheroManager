from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.utils.avatar_picker import get_random_avatar


class User(BaseModel):
    "Users table model"

    __tablename__ = "users"

    avatar: Mapped[str] = mapped_column(default=get_random_avatar)
    username: Mapped[str] = mapped_column(String(16))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    deleted: Mapped[bool] = mapped_column(default=False)
    roles = relationship("Role",
                         secondary="user_roles",
                         back_populates='users')

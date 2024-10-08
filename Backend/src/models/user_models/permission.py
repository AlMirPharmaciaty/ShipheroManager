from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Permission(BaseModel):
    "Permissions table model"

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(unique=True)
    roles = relationship("Role",
                         secondary="role_permissions",
                         back_populates='permissions')

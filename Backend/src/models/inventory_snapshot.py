from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.models.user_models.user import User


class InventorySnapshot(BaseModel):
    "Shiphero Inventory Snapshot table model"

    __tablename__ = "inventory_snapshots"

    snapshot_id: Mapped[str] = mapped_column(unique=True)
    status: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    user = relationship('User')

from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.models.user_models.user import User
from src.models.file import File


class InventorySnapshot(BaseModel):
    "Shiphero Inventory Snapshot table model"

    __tablename__ = "inventory_snapshots"

    snapshot_id: Mapped[str] = mapped_column(unique=True)
    status: Mapped[str]
    snapshot_url: Mapped[Optional[str]] = mapped_column(Text)
    snapshot_expiration: Mapped[Optional[datetime]]
    job_user_id: Mapped[Optional[str]]
    job_account_id: Mapped[Optional[str]]
    warehouse_id: Mapped[Optional[str]]
    customer_account_id: Mapped[Optional[str]]
    notification_email: Mapped[Optional[str]]
    email_error: Mapped[Optional[str]]
    post_url: Mapped[Optional[str]]
    post_error: Mapped[Optional[str]]
    post_url_pre_check: Mapped[Optional[bool]]
    error: Mapped[Optional[bool]]
    enqueued_at: Mapped[Optional[datetime]]
    created_at_shiphero: Mapped[Optional[datetime]]
    updated_at_shiphero: Mapped[Optional[datetime]]
    downloaded: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id))
    file_id: Mapped[Optional[str]] = mapped_column(ForeignKey(File.id))
    user = relationship('User')
    file = relationship('File')

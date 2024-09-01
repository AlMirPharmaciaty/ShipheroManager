from datetime import datetime
from pydantic import BaseModel, Field

from src.schemas.user_schemas.user import UserRead
from src.schemas.file import FileRead
from src.schemas.custom_response import CustomResponse


class InventorySnapshotCreate(BaseModel):
    """Inventory Snapshot filters"""
    warehouse_id: str | None = None
    customer_account_id: str | None = None
    has_inventory: bool | None = None
    updated_from: str | None = Field(default=None,
                                     pattern=r'^\d{4}-\d{2}-\d{2}$')


class InventorySnapshotRead(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    snapshot_id: str
    status: str
    snapshot_url: str | None
    snapshot_expiration: datetime | None
    job_user_id: str | None
    job_account_id: str | None
    warehouse_id: str | None
    customer_account_id: str | None
    notification_email: str | None
    email_error: str | None
    post_url: str | None
    post_error: str | None
    post_url_pre_check: bool | None
    error: bool | None
    enqueued_at: datetime | None
    created_at_shiphero: datetime | None
    updated_at_shiphero: datetime | None
    downloaded: bool


class InventorySnapshotReadWithRelation(InventorySnapshotRead):
    user: UserRead
    file: FileRead | None


class InventorySnapshotResponseModel(CustomResponse):
    data: InventorySnapshotReadWithRelation | list[InventorySnapshotReadWithRelation] | None = None

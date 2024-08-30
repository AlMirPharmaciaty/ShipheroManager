from datetime import datetime
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    permissions: list[str] | list[None] | None = None


class RoleRead(BaseModel):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass

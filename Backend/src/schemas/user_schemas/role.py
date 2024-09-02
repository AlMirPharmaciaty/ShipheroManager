from datetime import datetime
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    permissions: list[int] | list[None] | None = None


class RoleRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass

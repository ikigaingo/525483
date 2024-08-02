from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr


class GroupAdminBase(BaseModel):
    group_id: UUID
    code: Optional[str]
    email: EmailStr
    device: Optional[str]
    group_admin_data: Optional[Dict[str, Any]]
    token: Optional[str]
    name: Optional[str]
    mobile: Optional[str]


class GroupAdminCreate(GroupAdminBase):
    pass


class GroupAdminUpdate(GroupAdminBase):
    pass


class GroupAdmin(GroupAdminBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class GroupAdminAuthRequest(BaseModel):
    mobile: str


class GroupAdminAuthResponse(BaseModel):
    token: str

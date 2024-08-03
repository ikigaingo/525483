from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class GroupData(BaseModel):
    address: Optional[str] = None
    city_state_country: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    contact_person: Optional[str] = None
    phone_number: Optional[str] = None
    notes: Optional[str] = None
    donorbox: Optional[bool] = None
    facebook: Optional[str] = None
    tiktok: Optional[str] = None
    instagram: Optional[str] = None


class GroupBase(BaseModel):
    name: Optional[str] = None
    group_data: Optional[GroupData] = None
    organisation_id: Optional[UUID] = None
    country_id: Optional[UUID] = None
    language_id: Optional[int] = None
    audit_items_id: Optional[int] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: UUID
    organisation_name: Optional[str] = None
    country_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PaginatedGroups(BaseModel):
    data: List[Group]
    total_count: int
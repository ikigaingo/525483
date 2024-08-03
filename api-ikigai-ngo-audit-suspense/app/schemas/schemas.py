from datetime import date
from typing import Optional, Dict
from uuid import UUID

from pydantic import BaseModel


class AuditSuspenseBase(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    geo_data: Dict
    address: Optional[str] = None
    devicetype: Optional[str] = None


class AuditSuspenseCreate(AuditSuspenseBase):
    pass


class AuditSuspenseUpdate(AuditSuspenseBase):
    pass


class AuditSuspenseInDB(AuditSuspenseBase):
    id: int

    class Config:
        from_attributes = True

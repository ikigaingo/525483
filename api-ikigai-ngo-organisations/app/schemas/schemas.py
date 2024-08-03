from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel, UUID4, Field


class AppIdentifierBase(BaseModel):
    app_name: str
    language: str


class AppIdentifierCreate(AppIdentifierBase):
    pass


class AppIdentifier(AppIdentifierBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrganisationBase(BaseModel):
    name: str
    organisation_data: dict
    app_id: int


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Name of the organisation")
    organisation_data: Optional[Dict[str, str]] = Field(None, title="Organisation data in JSON format")
    app_id: Optional[int] = Field(None, title="ID of the associated app")
    updated_at: Optional[str] = Field(None, title="Timestamp of last update")


class OrganisationResponse(BaseModel):
    id: UUID4
    name: str
    organisation_data: Dict[str, str]
    app_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Organisation(OrganisationBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

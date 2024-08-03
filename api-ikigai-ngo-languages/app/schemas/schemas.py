from pydantic import BaseModel
from datetime import datetime


class LanguageBase(BaseModel):
    language: str


class LanguageCreate(LanguageBase):
    pass


class Language(LanguageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

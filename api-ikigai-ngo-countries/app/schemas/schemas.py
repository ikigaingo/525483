from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional, Dict, Any
from datetime import datetime


class CountryBase(BaseModel):
    name: str
    flag: Optional[HttpUrl] = None

    @property
    def country_data(self) -> Dict[str, Any]:
        return {"flag": str(self.flag) if self.flag else None}


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryInDB(CountryBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Country(CountryInDB):
    pass

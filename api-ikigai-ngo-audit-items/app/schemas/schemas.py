from typing import Optional

from pydantic import BaseModel
from pydantic.types import conint, constr, conbytes


class AuditItemSchemaBase(BaseModel):
    image: str
    category: Optional[constr(min_length=1)]


class AuditItemCreate(AuditItemSchemaBase):
    pass


class AuditItemInDB(BaseModel):
    id: int
    image: str  # Considera cómo quieres manejar el campo de imagen, ¿como URL, base64?
    category: str


class Config:
    from_attributes = True

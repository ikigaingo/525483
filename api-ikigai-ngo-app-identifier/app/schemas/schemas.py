from pydantic import BaseModel, Field


class AppIdentifierBase(BaseModel):
    app_name: str
    language: str


class AppIdentifierCreate(AppIdentifierBase):
    pass


class AppIdentifierUpdate(BaseModel):
    app_name: str
    language: str


class AppIdentifierInDB(AppIdentifierBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
        from_attributes = True


class AppIdentifierResponse(BaseModel):
    id: int
    appName: str = Field(..., alias='app_name')
    language: str

    class Config:
        orm_mode = True
        from_attributes = True

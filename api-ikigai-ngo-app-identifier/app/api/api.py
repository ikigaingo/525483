from typing import List

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..crud import crud_app_identifiers
from ..schemas import schemas
from ..schemas.schemas import AppIdentifierUpdate

app = FastAPI()
router = APIRouter()


@router.post("/app-identifiers/", response_model=schemas.AppIdentifierResponse)
def create_app_identifier(app_identifier: schemas.AppIdentifierCreate, db: Session = Depends(get_db)):
    return crud_app_identifiers.create_app_identifier(db=db, app_identifier=app_identifier)


@router.get("/app-identifiers/", response_model=List[schemas.AppIdentifierResponse])
def read_app_identifiers(db: Session = Depends(get_db)):
    db_app_identifiers = crud_app_identifiers.get_app_identifiers(db)
    return [schemas.AppIdentifierResponse.from_orm(app_identifier) for app_identifier in db_app_identifiers]


@router.get("/app-identifiers/{id}", response_model=schemas.AppIdentifierResponse)
def read_app_identifier(id: int, db: Session = Depends(get_db)):
    db_app_identifier = crud_app_identifiers.get_app_identifier(db, id)
    if db_app_identifier is None:
        raise HTTPException(status_code=404, detail="App Identifier not found")
    return db_app_identifier


@router.put("/app-identifiers/{id}", response_model=schemas.AppIdentifierResponse)
def update_app_identifier(id: int, app_identifier: AppIdentifierUpdate, db: Session = Depends(get_db)):
    db_app_identifier = crud_app_identifiers.get_app_identifier(db, id)
    if not db_app_identifier:
        raise HTTPException(status_code=404, detail="App Identifier not found")
    return crud_app_identifiers.update_app_identifier(db=db, app_identifier_id=id, app_identifier=app_identifier)


@router.delete("/app-identifiers/{id}", response_model=schemas.AppIdentifierResponse)
def delete_app_identifier(id: int, db: Session = Depends(get_db)):
    db_app_identifier = crud_app_identifiers.get_app_identifier(db, id)
    if not db_app_identifier:
        raise HTTPException(status_code=404, detail="App Identifier not found")
    return crud_app_identifiers.delete_app_identifier(db=db, app_identifier_id=id)

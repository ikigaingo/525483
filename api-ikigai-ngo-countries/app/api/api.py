from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..crud import crud_country
from ..schemas import schemas
from typing import List

app = FastAPI()
router = APIRouter()


@router.post("/countries/", response_model=schemas.CountryInDB)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    return crud_country.create_country(db=db, country=country)


@router.get("/countries/", response_model=List[schemas.CountryInDB])
def read_countries(db: Session = Depends(get_db)):
    countries = crud_country.get_countries(db)
    return countries


@router.get("/countries/{country_id}", response_model=schemas.CountryInDB)
def read_country(country_id: UUID, db: Session = Depends(get_db)):
    db_country = crud_country.get_country(db, country_id=country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country


@router.put("/countries/{country_id}", response_model=schemas.CountryInDB)
def update_country(country_id: UUID, country: schemas.CountryUpdate, db: Session = Depends(get_db)):
    return crud_country.update_country(db=db, country_id=country_id, country_update=country)


@router.delete("/countries/{country_id}", response_model=schemas.CountryInDB)
def delete_country(country_id: UUID, db: Session = Depends(get_db)):
    db_country = crud_country.get_country(db, country_id=country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return crud_country.delete_country(db=db, country_id=country_id)

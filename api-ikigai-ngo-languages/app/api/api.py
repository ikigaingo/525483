from typing import List

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from ..crud import crud_languages
from ..dependencies import get_db
from ..schemas.schemas import Language, LanguageCreate

app = FastAPI()
router = APIRouter()


@router.post("/languages/", response_model=Language)
def create_language(language: LanguageCreate, db: Session = Depends(get_db)):
    return crud_languages.create_language(db=db, language=language)


@router.get("/languages/", response_model=List[Language])
def read_languages(db: Session = Depends(get_db)):
    languages = crud_languages.get_languages(db)
    return languages


@router.get("/languages/{language_id}", response_model=Language)
def read_language(language_id: int, db: Session = Depends(get_db)):
    db_language = crud_languages.get_language(db, language_id=language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_language


@router.put("/languages/{language_id}", response_model=Language)
def update_language(language_id: int, language: LanguageCreate, db: Session = Depends(get_db)):
    db_language = crud_languages.update_language(db=db, language_id=language_id, language=language)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_language


@router.delete("/languages/{language_id}", response_model=Language)
def delete_language(language_id: int, db: Session = Depends(get_db)):
    db_language = crud_languages.delete_language(db=db, language_id=language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_language

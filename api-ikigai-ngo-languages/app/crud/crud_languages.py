# app/crud/crud_languages.py
from sqlalchemy.orm import Session
from ..models.models import Language
from ..schemas.schemas import LanguageCreate


def get_language(db: Session, language_id: int):
    return db.query(Language).filter(Language.id == language_id).first()


def get_languages(db: Session):
    return db.query(Language).all()


def create_language(db: Session, language: LanguageCreate):
    db_language = Language(language=language.language)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def update_language(db: Session, language_id: int, language: LanguageCreate):
    db_language = db.query(Language).filter(Language.id == language_id).first()
    if db_language:
        db_language.language = language.language
        db.commit()
        db.refresh(db_language)
    return db_language


def delete_language(db: Session, language_id: int):
    db_language = db.query(Language).filter(Language.id == language_id).first()
    if db_language:
        db.delete(db_language)
        db.commit()
    return db_language

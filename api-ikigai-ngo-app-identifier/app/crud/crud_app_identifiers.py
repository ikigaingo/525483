from sqlalchemy.orm import Session

from ..models import models
from ..schemas import schemas


def get_app_identifier(db: Session, app_identifier_id: int):
    return db.query(models.AppIdentifier).filter(models.AppIdentifier.id == app_identifier_id).first()


def get_app_identifiers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AppIdentifier).offset(skip).limit(limit).all()


def create_app_identifier(db: Session, app_identifier: schemas.AppIdentifierCreate):
    db_app_identifier = models.AppIdentifier(
        app_name=app_identifier.app_name,
        language=app_identifier.language
    )
    db.add(db_app_identifier)
    db.commit()
    db.refresh(db_app_identifier)
    return db_app_identifier


def update_app_identifier(db: Session, app_identifier_id: int, app_identifier: schemas.AppIdentifierUpdate):
    db_app_identifier = db.query(models.AppIdentifier).filter(models.AppIdentifier.id == app_identifier_id).first()
    if not db_app_identifier:
        return None
    db_app_identifier.app_name = app_identifier.app_name
    db_app_identifier.language = app_identifier.language
    db.commit()
    db.refresh(db_app_identifier)
    return db_app_identifier


def delete_app_identifier(db: Session, app_identifier_id: int):
    db_app_identifier = db.query(models.AppIdentifier).filter(models.AppIdentifier.id == app_identifier_id).first()
    if not db_app_identifier:
        return None
    db.delete(db_app_identifier)
    db.commit()
    return db_app_identifier

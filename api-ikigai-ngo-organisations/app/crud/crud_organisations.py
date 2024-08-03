from uuid import UUID

from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas


def get_organisation(db: Session, organisation_id: UUID):
    return db.query(models.Organisation).filter(models.Organisation.id == organisation_id).first()


def get_organisations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Organisation).offset(skip).limit(limit).all()


def create_organisation(db: Session, organisation: schemas.OrganisationCreate):
    # Convert OrganisationCreate to a dict and handle default values
    organisation_data = organisation.dict()
    if "organisation_data" in organisation_data and organisation_data["organisation_data"] is None:
        organisation_data["organisation_data"] = {}
    db_organisation = models.Organisation(**organisation_data)
    db.add(db_organisation)
    db.commit()
    db.refresh(db_organisation)
    return db_organisation


def update_organisation(db: Session, organisation_id: UUID, organisation: schemas.OrganisationUpdate):
    db_organisation = db.query(models.Organisation).filter(models.Organisation.id == organisation_id).first()
    if db_organisation:
        organisation_data = organisation.dict()
        if "organisation_data" in organisation_data and organisation_data["organisation_data"] is None:
            organisation_data["organisation_data"] = {}
        for key, value in organisation_data.items():
            setattr(db_organisation, key, value)
        db.commit()
        db.refresh(db_organisation)
    return db_organisation


def delete_organisation(db: Session, organisation_id: UUID):
    db_organisation = db.query(models.Organisation).filter(models.Organisation.id == organisation_id).first()
    if db_organisation:
        db.delete(db_organisation)
        db.commit()
    return db_organisation

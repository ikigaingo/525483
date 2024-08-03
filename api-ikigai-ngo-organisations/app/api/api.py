import json
from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import models
from ..schemas import schemas

app = FastAPI()
router = APIRouter()


@router.post("/app-identifiers/", response_model=schemas.AppIdentifier)
def create_app_identifier(app_identifier: schemas.AppIdentifierCreate, db: Session = Depends(get_db)):
    db_app_identifier = models.AppIdentifier(**app_identifier.dict())
    db.add(db_app_identifier)
    db.commit()
    db.refresh(db_app_identifier)
    return db_app_identifier


@router.get("/app-identifiers/", response_model=List[schemas.AppIdentifier])
def read_app_identifiers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    app_identifiers = db.query(models.AppIdentifier).offset(skip).limit(limit).all()
    return app_identifiers


@router.post("/organisations/", response_model=schemas.Organisation)
def create_organisation(organisation: schemas.OrganisationCreate, db: Session = Depends(get_db)):
    db_organisation = models.Organisation(**organisation.dict())
    db.add(db_organisation)
    db.commit()
    db.refresh(db_organisation)
    return db_organisation


@router.get("/organisations/", response_model=List[schemas.Organisation])
def get_all_organisations(db: Session = Depends(get_db)):
    organisations = db.query(models.Organisation).all()
    if not organisations:
        raise HTTPException(status_code=404, detail="No organisations found")

    validated_organisations = []
    for org in organisations:
        validated_org = {
            "id": org.id,
            "name": org.name,
            "organisation_data": org.organisation_data if org.organisation_data else {},
            "app_id": org.app_id if org.app_id is not None else -1,
            "created_at": org.created_at,
            "updated_at": org.updated_at
        }
        validated_organisations.append(validated_org)

    return validated_organisations


@router.put("/organisations/{organisation_id}", response_model=schemas.OrganisationResponse)
def update_organisation(
        organisation_id: UUID,
        organisation: schemas.OrganisationUpdate,
        db: Session = Depends(get_db)
):
    db_organisation = db.query(models.Organisation).filter(models.Organisation.id == organisation_id).first()

    if db_organisation is None:
        raise HTTPException(status_code=404, detail="Organisation not found")

    update_data = organisation.dict(exclude_unset=True)

    for key, value in update_data.items():
        if value is not None:
            setattr(db_organisation, key, value)

    db_organisation.updated_at = datetime.utcnow()

    db.add(db_organisation)
    db.commit()
    db.refresh(db_organisation)

    return db_organisation


@router.get("/organisations/{organisation_id}", response_model=schemas.OrganisationResponse)
def read_organisation(organisation_id: UUID, db: Session = Depends(get_db)):
    db_organisation = db.query(models.Organisation).filter(models.Organisation.id == organisation_id).first()

    if not db_organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")

    response_data = {
        "id": str(db_organisation.id),
        "name": db_organisation.name,
        "organisation_data": db_organisation.organisation_data if db_organisation.organisation_data else {},
        "app_id": db_organisation.app_id,
        "created_at": db_organisation.created_at.isoformat(),
        "updated_at": db_organisation.updated_at.isoformat(),
    }

    return response_data


@router.delete("/organisations/{organisation_id}", response_model=schemas.OrganisationResponse)
def delete_organisation(organisation_id: UUID, db: Session = Depends(get_db)):
    db_organisation = db.query(models.Organisation).filter(models.Organisation.id == organisation_id).first()

    if not db_organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")

    db.delete(db_organisation)
    db.commit()

    return {
        "id": str(db_organisation.id),
        "name": db_organisation.name,
        "organisation_data": db_organisation.organisation_data,
        "app_id": db_organisation.app_id,
        "created_at": db_organisation.created_at.isoformat(),
        "updated_at": db_organisation.updated_at.isoformat(),
    }

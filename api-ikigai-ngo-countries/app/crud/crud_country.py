from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from ..models import models
from ..schemas import schemas


def get_countries(db: Session):
    countries = db.query(models.Country).all()
    return [schemas.Country(
        id=country.id,
        name=country.name,
        flag=country.country_data.get('flag') if country.country_data else None,
        created_at=country.created_at,
        updated_at=country.updated_at
    ) for country in countries]


def get_country(db: Session, country_id: UUID):
    return db.query(models.Country).filter(models.Country.id == country_id).first()


def create_country(db: Session, country: schemas.CountryCreate):
    db_country = models.Country(
        name=country.name,
        country_data=country.country_data,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def update_country(
        country_id: UUID,
        country_update: schemas.CountryUpdate,
        db: Session
):
    db_country = db.query(models.Country).filter(models.Country.id == country_id).first()

    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    update_data = country_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key == 'flag':
            if db_country.country_data:
                db_country.country_data['flag'] = str(value)
            else:
                db_country.country_data = {'flag': str(value)}

            flag_modified(db_country, "country_data")
        else:
            setattr(db_country, key, value)

    db_country.updated_at = datetime.utcnow()

    db.add(db_country)
    db.commit()
    db.refresh(db_country)

    return db_country


def delete_country(db: Session, country_id: UUID):
    db_country = db.query(models.Country).filter(models.Country.id == country_id).first()
    db.delete(db_country)
    db.commit()
    return db_country

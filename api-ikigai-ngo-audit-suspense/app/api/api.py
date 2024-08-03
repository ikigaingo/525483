from typing import List

from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.models import AuditSuspense
from app.schemas.schemas import AuditSuspenseInDB, AuditSuspenseCreate, AuditSuspenseUpdate

app = FastAPI()
router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/audits/", response_model=AuditSuspenseInDB)
def create_audit(audit: AuditSuspenseCreate, db: Session = Depends(get_db)):
    db_audit = AuditSuspense(**audit.dict())
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit

@router.get("/audits/", response_model=List[AuditSuspenseInDB])
def read_all_audits(db: Session = Depends(get_db)):
    audits = db.query(AuditSuspense).all()
    return audits

@router.get("/audits/{audit_id}", response_model=AuditSuspenseInDB)
def read_audit(audit_id: int, db: Session = Depends(get_db)):
    db_audit = db.query(AuditSuspense).filter(AuditSuspense.id == audit_id).first()
    if db_audit is None:
        raise HTTPException(status_code=404, detail="Audit not found")
    return db_audit


@router.put("/audits/{audit_id}", response_model=AuditSuspenseInDB)
def update_audit(audit_id: int, audit: AuditSuspenseUpdate, db: Session = Depends(get_db)):
    db_audit = db.query(AuditSuspense).filter(AuditSuspense.id == audit_id).first()
    if db_audit is None:
        raise HTTPException(status_code=404, detail="Audit not found")

    try:
        update_data = audit.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_audit, key, value)

        db.commit()
        db.refresh(db_audit)
        return db_audit
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/audits/{audit_id}", response_model=AuditSuspenseInDB)
def delete_audit(audit_id: int, db: Session = Depends(get_db)):
    db_audit = db.query(AuditSuspense).filter(AuditSuspense.id == audit_id).first()
    if db_audit is None:
        raise HTTPException(status_code=404, detail="Audit not found")
    db.delete(db_audit)
    db.commit()
    return db_audit


@router.post("/audits/bulk/", response_model=List[AuditSuspenseInDB])
def create_audits(audits: List[AuditSuspenseCreate], db: Session = Depends(get_db)):
    db_audits = [AuditSuspense(**audit.dict()) for audit in audits]
    db.add_all(db_audits)
    db.commit()
    for audit in db_audits:
        db.refresh(audit)
    return db_audits

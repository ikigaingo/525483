from sqlalchemy.orm import Session
from app.models import AuditItem


def get_all_audit_items(db: Session):
    return db.query(AuditItem).all()

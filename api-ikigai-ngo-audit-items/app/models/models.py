from sqlalchemy import Column, Integer, String, LargeBinary

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuditItem(Base):
    __tablename__ = 'audit_items'
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    image = Column(String)
    category = Column(String)

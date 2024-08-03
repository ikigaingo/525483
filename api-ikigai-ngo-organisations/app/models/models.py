import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class AppIdentifier(Base):
    __tablename__ = 'app_identifiers'

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String(255), nullable=False)
    language = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    organisations = relationship("Organisation", back_populates="app_identifier")


class Organisation(Base):
    __tablename__ = 'organisation'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    organisation_data = Column(JSON, nullable=False)
    app_id = Column(Integer, ForeignKey('app_identifiers.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    app_identifier = relationship("AppIdentifier", back_populates="organisations")

from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Country(Base):
    __tablename__ = 'country'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False)
    country_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

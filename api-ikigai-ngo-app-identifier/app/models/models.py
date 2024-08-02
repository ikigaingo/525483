from sqlalchemy import Column, String, Integer, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AppIdentifier(Base):
    __tablename__ = "app_identifiers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_name = Column(String, nullable=False)
    language = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

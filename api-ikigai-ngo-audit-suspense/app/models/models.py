from enum import Enum

from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DeviceTypeEnum(Enum):
    android = "android"
    ios = "ios"


class AuditSuspense(Base):
    __tablename__ = 'audit_suspense'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    quantity = Column(Integer)
    geo_data = Column(JSONB)
    address = Column(Text)
    devicetype = Column(ENUM('android', 'ios', name='device_type', create_type=False), nullable=False)

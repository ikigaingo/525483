import uuid

from sqlalchemy import Column, String, ForeignKey, JSON, TIMESTAMP, UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class GroupAdmin(Base):
    __tablename__ = 'group_admin'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey('group.id', ondelete='CASCADE'))
    code = Column(String(50))
    email = Column(String(256), nullable=False)
    device = Column(String(256))
    group_admin_data = Column(JSON)
    created_at = Column(TIMESTAMP, nullable=False, default='now()')
    updated_at = Column(TIMESTAMP, nullable=False, default='now()')
    token = Column(String)
    name = Column(String)
    mobile = Column(String)

    group = relationship("Group", back_populates="group_admins")


class Group(Base):
    __tablename__ = 'group'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # other fields...

    group_admins = relationship("GroupAdmin", back_populates="group")

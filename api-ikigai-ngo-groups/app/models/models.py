from sqlalchemy import Column, String, JSON, ForeignKey, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()


class Organisation(Base):
    __tablename__ = 'organisation'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(256), nullable=True)
    organisation_data = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default='now()')
    updated_at = Column(TIMESTAMP, nullable=False, default='now()')
    app_id = Column(Integer, ForeignKey('app_identifiers.id'))

    groups = relationship('Group', back_populates='organisation')


class Country(Base):
    __tablename__ = 'country'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    country_data = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default='now()')
    updated_at = Column(TIMESTAMP, nullable=False, default='now()')

    groups = relationship('Group', back_populates='country')


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class AuditItem(Base):
    __tablename__ = 'audit_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(50), nullable=False)


class Group(Base):
    __tablename__ = 'group'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    group_data = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default='now()')
    updated_at = Column(TIMESTAMP, nullable=False, default='now()')
    organisation_id = Column(UUID(as_uuid=True), ForeignKey('organisation.id', ondelete='CASCADE'))
    country_id = Column(UUID(as_uuid=True), ForeignKey('country.id', ondelete='CASCADE'))
    language_id = Column(Integer, ForeignKey('languages.id', ondelete='CASCADE'))
    audit_items_id = Column(Integer, ForeignKey('audit_items.id', ondelete='CASCADE'))

    organisation = relationship('Organisation', back_populates='groups')
    country = relationship('Country', back_populates='groups')
    language = relationship('Language')
    audit_items = relationship('AuditItem')

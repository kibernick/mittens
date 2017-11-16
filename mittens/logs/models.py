from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Text, String

from mittens.db import Base


class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True, nullable=False)
    api_key = Column(String(100), unique=True)

    error_logs = relationship('ErrorLog', back_populates='tenant')

    @property
    def is_authenticated(self):
        """Used by Flask-Login."""
        return True


class ErrorLog(Base):
    __tablename__ = 'error_logs'

    id = Column(Integer, primary_key=True, nullable=False)
    meta = Column(JSON)
    content = Column(Text, nullable=False)

    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    tenant = relationship('Tenant', back_populates='error_logs')

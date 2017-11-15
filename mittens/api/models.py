from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text

from mittens.db import Base


class ErrorLog(Base):
    __tablename__ = 'error_logs'

    id = Column(Integer, primary_key=True, nullable=False)
    meta = Column(JSON)
    content = Column(Text, nullable=False)

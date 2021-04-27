import pytz
from dateutil.parser import parse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime

db = SQLAlchemy()


class Base(db.Model):
    """Abstract base class for our models."""

    __abstract__ = True

    created_on = Column(DateTime, default=db.func.utc_timestamp())
    updated_on = Column(DateTime, default=db.func.utc_timestamp(), onupdate=db.func.utc_timestamp())


def coerce_to_utc(datetime_str):
    try:
        dt = parse(datetime_str)
    except (TypeError, ValueError):
        return None
    if dt is not None and dt.tzinfo is not None:
        # Convert any existing timezone information to UTC.
        dt = dt.astimezone(pytz.UTC)
    return dt

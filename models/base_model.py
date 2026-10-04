#!/usr/bin/python3

import uuid
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String


Base = declarative_base()


class BaseModel(Base):
    """Base class for all models."""

    __abstract__ = True

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, *args, **kwargs):
        """Initialize a BaseModel instance."""
        super().__init__()

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue

                if key in ("created_at", "updated_at"):
                    if isinstance(value, str):
                        value = datetime.strptime(
                            value,
                            "%Y-%m-%dT%H:%M:%S.%f"
                        )

                setattr(self, key, value)

        if "id" not in kwargs:
            self.id = str(uuid.uuid4())

        if "created_at" not in kwargs:
            self.created_at = datetime.now()

        if "updated_at" not in kwargs:
            self.updated_at = datetime.now()

    def __str__(self):
        """Return string representation."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )

    def save(self):
        """Update updated_at and save to storage."""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return dictionary representation."""
        result = {}

        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                result[key] = value

        result["__class__"] = self.__class__.__name__
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()

        return result

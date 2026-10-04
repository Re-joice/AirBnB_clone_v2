#!/usr/bin/python3

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models."""

    def __init__(self, *args, **kwargs):
        """Initialize a BaseModel instance."""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

            if "created_at" in kwargs:
                self.created_at = datetime.strptime(
                    kwargs["created_at"],
                    "%Y-%m-%dT%H:%M:%S.%f"
                )

            if "updated_at" in kwargs:
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"],
                    "%Y-%m-%dT%H:%M:%S.%f"
                )

            if "id" not in kwargs:
                self.id = str(uuid.uuid4())

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
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
        result = self.__dict__.copy()
        result["__class__"] = self.__class__.__name__
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result

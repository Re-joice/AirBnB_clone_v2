#!/usr/bin/python3
"""Amenity model."""

from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Representation of an amenity."""

    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize an Amenity instance."""
        super().__init__(*args, **kwargs)

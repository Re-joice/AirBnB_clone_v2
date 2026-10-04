#!/usr/bin/python3

from sqlalchemy import Column, String

from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model."""

    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize an Amenity."""
        super().__init__(*args, **kwargs)

#!/usr/bin/python3

from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel


class City(BaseModel):
    """City model."""

    __tablename__ = "cities"

    state_id = Column(
        String(60),
        ForeignKey("states.id"),
        nullable=False
    )
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a City."""
        super().__init__(*args, **kwargs)

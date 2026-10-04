#!/usr/bin/python3

from sqlalchemy import Column, String

from models.base_model import BaseModel


class State(BaseModel):
    """State model."""

    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a State."""
        super().__init__(*args, **kwargs)

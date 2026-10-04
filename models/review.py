#!/usr/bin/python3

from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel


class Review(BaseModel):
    """Review model."""

    __tablename__ = "reviews"

    place_id = Column(
        String(60),
        ForeignKey("places.id"),
        nullable=False
    )
    user_id = Column(
        String(60),
        ForeignKey("users.id"),
        nullable=False
    )
    text = Column(String(1024), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a Review."""
        super().__init__(*args, **kwargs)

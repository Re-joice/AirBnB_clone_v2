
#!/usr/bin/python3
"""Place model."""

import models
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class Place(BaseModel):
    """Representation of a place."""

    __tablename__ = "places"

    city_id = Column(
        String(60),
        ForeignKey("cities.id"),
        nullable=False
    )
    user_id = Column(
        String(60),
        ForeignKey("users.id"),
        nullable=False
    )
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if models.storage_type == "db":
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete, delete-orphan"
        )
    else:
        @property
        def reviews(self):
            """Return reviews associated with this place."""
            from models import storage
            from models.review import Review

            all_reviews = storage.all(Review)
            return [
                review for review in all_reviews.values()
                if review.place_id == self.id
            ]

    def __init__(self, *args, **kwargs):
        """Initialize a Place."""
        super().__init__(*args, **kwargs)

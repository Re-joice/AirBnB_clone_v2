#!/usr/bin/python3
"""Place model."""

import models
from sqlalchemy import (
    Column, String, Integer, Float, ForeignKey, Table
)
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False
    )
)


class Place(BaseModel, Base):
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

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False
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

        @property
        def amenities(self):
            """Return amenities associated with this place."""
            from models import storage
            from models.amenity import Amenity

            all_amenities = storage.all(Amenity)
            amenity_list = []

            for amenity_id in getattr(self, "amenity_ids", []):
                key = "Amenity.{}".format(amenity_id)
                amenity = all_amenities.get(key)
                if amenity is not None:
                    amenity_list.append(amenity)

            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Append an Amenity ID when given an Amenity object."""
            from models.amenity import Amenity

            if isinstance(obj, Amenity):
                if not hasattr(self, "amenity_ids"):
                    self.amenity_ids = []
                self.amenity_ids.append(obj.id)

    def __init__(self, *args, **kwargs):
        """Initialize a Place."""
        super().__init__(*args, **kwargs)

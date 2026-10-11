
#!/usr/bin/python3
"""User model."""

import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class User(BaseModel):
    """Representation of a user."""

    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if models.storage_type == "db":
        reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete, delete-orphan"
        )

    def __init__(self, *args, **kwargs):
        """Initialize a User."""
        super().__init__(*args, **kwargs)

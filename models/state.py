#!/usr/bin/python3

from models.base_model import BaseModel


class State(BaseModel):
    """State model."""

    def __init__(self, *args, **kwargs):
        """Initialize a State."""
        super().__init__(*args, **kwargs)
        self.name = kwargs.get("name", "")

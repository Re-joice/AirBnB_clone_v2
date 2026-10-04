#!/usr/bin/python3

import unittest
from datetime import datetime

from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test BaseModel."""

    def test_create(self):
        """Test instance creation."""
        obj = BaseModel()
        self.assertIsNotNone(obj.id)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_id_is_string(self):
        """Test ID is a string."""
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)

    def test_different_ids(self):
        """Test IDs are unique."""
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotEqual(obj1.id, obj2.id)

    def test_to_dict(self):
        """Test to_dict."""
        obj = BaseModel()
        data = obj.to_dict()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["__class__"], "BaseModel")
        self.assertIsInstance(data["created_at"], str)
        self.assertIsInstance(data["updated_at"], str)

    def test_to_dict_no_sqlalchemy_state(self):
        """Test SQLAlchemy state is excluded."""
        obj = BaseModel()
        data = obj.to_dict()

        self.assertNotIn("_sa_instance_state", data)

    def test_kwargs(self):
        """Test initialization with kwargs."""
        obj = BaseModel(
            id="test-id",
            name="Test",
            created_at="2026-01-01T12:00:00.000000",
            updated_at="2026-01-01T12:00:00.000000"
        )

        self.assertEqual(obj.id, "test-id")
        self.assertEqual(obj.name, "Test")
        self.assertEqual(
            obj.created_at,
            datetime(2026, 1, 1, 12, 0, 0)
        )

    def test_str(self):
        """Test string representation."""
        obj = BaseModel()
        text = str(obj)

        self.assertIn("[BaseModel]", text)
        self.assertIn(obj.id, text)


if __name__ == "__main__":
    unittest.main()

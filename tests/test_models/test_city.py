#!/usr/bin/python3

import unittest

from models.city import City


class TestCity(unittest.TestCase):
    """Test City."""

    def test_create(self):
        """Test City creation."""
        city = City()
        self.assertIsNotNone(city.id)

    def test_name(self):
        """Test name."""
        city = City(name="Los Angeles")
        self.assertEqual(city.name, "Los Angeles")

    def test_state_id(self):
        """Test state ID."""
        city = City(state_id="state-123")
        self.assertEqual(city.state_id, "state-123")

    def test_table_name(self):
        """Test table name."""
        self.assertEqual(City.__tablename__, "cities")

    def test_to_dict(self):
        """Test to_dict."""
        city = City(name="Accra", state_id="state-1")
        data = city.to_dict()

        self.assertEqual(data["__class__"], "City")
        self.assertEqual(data["name"], "Accra")
        self.assertEqual(data["state_id"], "state-1")


if __name__ == "__main__":
    unittest.main()

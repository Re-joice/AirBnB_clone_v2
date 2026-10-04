#!/usr/bin/python3

import unittest

from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test Amenity."""

    def test_create(self):
        """Test Amenity creation."""
        amenity = Amenity()
        self.assertIsNotNone(amenity.id)

    def test_name(self):
        """Test name."""
        amenity = Amenity(name="WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_table_name(self):
        """Test table name."""
        self.assertEqual(Amenity.__tablename__, "amenities")

    def test_to_dict(self):
        """Test to_dict."""
        amenity = Amenity(name="Pool")
        data = amenity.to_dict()

        self.assertEqual(data["__class__"], "Amenity")
        self.assertEqual(data["name"], "Pool")

    def test_id(self):
        """Test ID."""
        amenity = Amenity()
        self.assertIsInstance(amenity.id, str)


if __name__ == "__main__":
    unittest.main()
